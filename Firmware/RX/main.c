/* Immagine RX candidata. Runtime C e vettore di reset forniti da XC32. */
#include <xc.h>
#include "pic32_iq.h"
#include "am_sync.h"
#include "audio_decim.h"

#ifdef RX_IQ_IIR
#include "iq_iir.h"
#endif

#ifdef RX_PROFILE
#include "rx_profile.h"
volatile struct rx_profile rx_profile_data;
#endif

#pragma config FNOSC = PRIPLL, POSCMOD = XT, FPLLIDIV = DIV_2
#pragma config FPLLMUL = MUL_16, FPLLODIV = DIV_2, FPBDIV = DIV_1
#pragma config FSOSCEN = OFF, IESO = OFF, FCKSM = CSECME
#pragma config UPLLEN = OFF, FUSBIDIO = OFF, FVBUSONIO = OFF
#pragma config JTAGEN = OFF, ICESEL = ICS_PGx1, IOL1WAY = ON
#pragma config FWDTEN = OFF

/* Diagnostica al debugger. Una sola scrittura allineata pubblica entrambi
   i campioni; il consumatore DSP dovrà acquisire ogni coppia in tempo. */
volatile uint32_t rx_last_pair;
volatile uint32_t rx_valid_pairs;
volatile uint32_t rx_rejected_frames;
volatile bool rx_initialized;
volatile int32_t rx_am_audio_q7;
volatile bool rx_am_audio_valid;
volatile uint32_t rx_am_audio_samples;

#ifdef RX_AUDIO_MONITOR
#include "audio_monitor.h"
static struct audio_monitor monitor = {.duty = {128,128,128}};
/* Parola diagnostica: tre confronti a 9 bit, dal primo nei bit meno significativi. */
volatile uint32_t rx_audio_duties = 128u | (128u << 9) | (128u << 18);
#endif

#ifdef RX_AUDIO_OC1
#include "pwm_slots.h"
static struct pwm_slots speaker = {.last = 128};
uint16_t rx_audio_slot(uint32_t now)
{
    return pwm_slots_next(&speaker, now);
}
#endif

static const struct iq_pair offset = {0, 0};
static struct am_sync am;
#ifdef RX_IQ_IIR
static struct iq_iir channel;
#endif
static struct audio_decim filter;

static void process_pair(struct iq_pair pair, uint32_t stamp)
{
#ifdef RX_PROFILE
    uint32_t start = _CP0_GET_COUNT();
    enum rx_work stage = RX_ACQUIRE;
#endif
    int32_t audio;
#ifdef RX_IQ_IIR
    bool valid = iq_iir_am_sample(&channel, &am, pair, stamp, &audio);
#else
    bool valid = am_sync_sample(&am, pair, stamp, &audio);
#endif
    if (valid) {
#ifdef RX_PROFILE
        stage = RX_DEMOD;
#endif
        int32_t filtered;
        if (audio_decim_sample(&filter, audio, &filtered)) {
#ifdef RX_PROFILE
            stage = RX_FIR;
#endif
#ifdef RX_AUDIO_MONITOR
            audio_monitor_sample(&monitor, _CP0_GET_COUNT(), am.dc_q10/1024, filtered);
#ifdef RX_AUDIO_OC1
            pwm_slots_submit(&speaker, monitor.duty);
#endif
#endif
            rx_am_audio_q7 = filtered;
            ++rx_am_audio_samples;
            rx_am_audio_valid = true;
        }
    } else {
#ifdef RX_AUDIO_MONITOR
        audio_monitor_poll(&monitor, _CP0_GET_COUNT(), true);
#ifdef RX_AUDIO_OC1
            speaker.remaining = 0;
#endif
#endif
        audio_decim_reset(&filter);
        rx_am_audio_valid = false;
    }
#ifdef RX_PROFILE
    rx_profile_record(&rx_profile_data, stage, stamp, _CP0_GET_COUNT() - start);
#endif
}

#ifdef RX_SPI_OVERLAP
static bool pending;
static struct iq_pair pending_pair;
static uint32_t pending_stamp;

void rx_process_pending(void)
{
    if (pending) {
        pending = false;
        process_pair(pending_pair, pending_stamp);
    }
}
#endif

int main(void)
{
    audio_decim_reset(&filter);
    am_sync_reset(&am, offset);
    rx_initialized = pic32_iq_init();
    if (!rx_initialized)
        for (;;) { }

    for (;;) {
        struct iq_pair pair;
        enum iq_status result = pic32_iq_poll(&pair);
        if (result == IQ_OK) {
            uint32_t stamp = _CP0_GET_COUNT();
            rx_last_pair = ((uint32_t)(uint16_t)pair.i << 16) | (uint16_t)pair.q;
            ++rx_valid_pairs;
#ifdef RX_SPI_OVERLAP
            pending_pair = pair;
            pending_stamp = stamp;
            pending = true;
#else
            process_pair(pair, stamp);
#endif
        } else if (result != IQ_IDLE) {
#ifdef RX_SPI_OVERLAP
            /* Uno scarto prima del lancio lascia valida la coppia precedente. */
            rx_process_pending();
#endif
#ifdef RX_AUDIO_MONITOR
            audio_monitor_poll(&monitor, _CP0_GET_COUNT(), true);
#ifdef RX_AUDIO_OC1
            speaker.remaining = 0;
#endif
#endif
            ++rx_rejected_frames;
#ifdef RX_IQ_IIR
            iq_iir_reset(&channel);
#endif
            am_sync_reset(&am, offset);
            audio_decim_reset(&filter);
            rx_am_audio_valid = false;
        }
#ifdef RX_AUDIO_MONITOR
        audio_monitor_poll(&monitor, _CP0_GET_COUNT(), false);
        rx_audio_duties = monitor.duty[0] | ((uint32_t)monitor.duty[1] << 9)
                         | ((uint32_t)monitor.duty[2] << 18);
#endif
    }
}
