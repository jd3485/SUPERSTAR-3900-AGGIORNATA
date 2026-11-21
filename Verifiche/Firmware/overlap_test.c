/* Esegue il ciclo firmware sostituendo solo polling e lettura CP0. */
#define main rx_firmware_main
#include "../../Firmware/RX/main.c"
#undef main
#include <assert.h>
#include <setjmp.h>

static jmp_buf finished;
#ifdef RX_AUDIO_OC1
static unsigned changing_slots;
#endif
static unsigned step, accepted, errors, count;
static bool reference_valid;
static int32_t reference_audio;
static struct iq_iir reference_channel;
static struct am_sync reference_am;
static struct audio_decim reference_filter;
static uint32_t clock_tick;

uint32_t mock_cp0_count(void) { return clock_tick++; }
bool pic32_iq_init(void) { return true; }

static void check_audio(void)
{
    assert(rx_am_audio_samples == count && rx_am_audio_valid == reference_valid);
    assert(rx_am_audio_q7 == reference_audio);
}

enum iq_status pic32_iq_poll(struct iq_pair *out)
{
    static bool queued;
    static struct iq_pair saved;
    static uint32_t saved_stamp;
    check_audio();
    assert(rx_valid_pairs == accepted && rx_rejected_frames == errors);
    unsigned n = step++;
    if (n == 1024)
        longjmp(finished, 1);
#ifdef RX_AUDIO_OC1
    uint16_t duty = rx_audio_slot(UINT32_MAX - 4096u + n*384u);
    assert(duty <= 256);
    changing_slots += duty != 128;
#endif
    if (n == 410 || n == 411)
        return IQ_IDLE;
    clock_tick = UINT32_MAX - 4096u + n * 384u;
    bool before = n == 300, after = n == 700 || n == 1023;
    bool had_pair = queued;
    if (queued) {
        int32_t audio;
        if (iq_iir_am_sample(&reference_channel, &reference_am, saved, saved_stamp, &audio)) {
            if (audio_decim_sample(&reference_filter, audio, &reference_audio)) {
                reference_valid = true;
                ++count;
            }
        } else {
            audio_decim_reset(&reference_filter);
            reference_valid = false;
        }
        queued = false;
    }
    if (!before) {
        rx_process_pending();
        if (had_pair)
            assert(channel.previous == saved_stamp);
        check_audio();
    }
    if (before || after) {
        ++errors;
        iq_iir_reset(&reference_channel);
        am_sync_reset(&reference_am, offset);
        audio_decim_reset(&reference_filter);
        reference_valid = false;
        return before ? IQ_NOT_READY : IQ_BAD_NULL;
    }
    /* Il timestamp di cattura è distinto dal momento del callback. */
    clock_tick = UINT32_MAX - 4096u + n * 384u + 280u;
    saved_stamp = clock_tick;
    saved = (struct iq_pair){(int16_t)(800 + n%79), (int16_t)(170 - (int)(n%33))};
    *out = saved;
    queued = true;
    ++accepted;
    return IQ_OK;
}

int main(void)
{
    am_sync_reset(&reference_am, offset);
    audio_decim_reset(&reference_filter);
    if (!setjmp(finished))
        (void)rx_firmware_main();
#ifdef RX_AUDIO_OC1
    assert(changing_slots > 10);
#endif
    assert(count > 100 && errors == 3 && accepted == 1019);
    assert(rx_profile_data.previous_stamp == UINT32_MAX - 4096u + 1022u*384u + 280u);
    assert(rx_profile_data.interval_max == 3*384u && rx_profile_data.long_intervals == 3);
#ifdef RX_AUDIO_MONITOR
    assert(rx_profile_data.work_max[RX_FIR] == 2);
    assert(!monitor.streaming && !monitor.gate.open);
    assert(rx_audio_duties == (monitor.duty[0] | ((uint32_t)monitor.duty[1] << 9)
                               | ((uint32_t)monitor.duty[2] << 18)));
#else
    assert(rx_profile_data.work_max[RX_FIR] == 1);
#endif
}
