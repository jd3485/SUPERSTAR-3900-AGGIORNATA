/* gcc -std=c11 -O2 -Wall -Wextra -Werror Firmware/RX/iq_frame.c
   Verifiche/Firmware/iq_frame_test.c -o /tmp/iq-test && /tmp/iq-test */
#include "../../Firmware/RX/iq_frame.h"
#include <assert.h>
#include <stdio.h>

enum fault { NORMAL, NO_I, NO_Q, OVERFLOW, CLOCK_LOST, LATE_ENTRY,
             TIMER_STUCK, WRAPPED, STALE, BAD_NULL, EXTRA_WORD, STUCK_BUSY };
static enum fault fault;
static unsigned tick, launch_tick, selected_tick;
static bool selected, launched, consumed;
static uint16_t wi, wq;
static unsigned resets;

static struct iq_snapshot status(void)
{
    if (fault != TIMER_STUCK)
        tick += 4;
    bool complete = launched && tick >= launch_tick + 512;
    return (struct iq_snapshot){
        .tick = (uint16_t)(tick % 768),
        .invalid_slot = tick >= 768 || (launched && fault == CLOCK_LOST) ||
                        (complete && fault == WRAPPED),
        .ready_i = (complete && !consumed && fault != NO_I) || fault == STALE ||
                   (consumed && fault == EXTRA_WORD),
        .ready_q = complete && !consumed && fault != NO_Q,
        .overrun = complete && fault == OVERFLOW,
        .busy = launched && (!complete || fault == STUCK_BUSY)
    };
}

static void select_frame(bool active)
{
    selected = active;
    if (active)
        selected_tick = tick;
}
static void launch(void)
{
    assert(selected && !launched && tick - selected_tick >= 16);
    launch_tick = tick;
    launched = true;
}
static void read_pair(uint16_t *i, uint16_t *q)
{
    assert(selected && launched && !consumed);
    *i = wi;
    *q = fault == BAD_NULL ? (uint16_t)(wq | 0x2000) : wq;
    consumed = true;
}
static void reset(void)
{
    selected = false;
    launched = false;
    consumed = false;
    ++resets;
}
static const struct iq_port port = {status, select_frame, launch, read_pair, reset};

static enum iq_status run(enum fault f, struct iq_pair *out)
{
    fault = f;
    tick = f == LATE_ENTRY ? 100 : 0;
    /* Il modello riceve lo slot successivo a ricevitori vuoti. */
    launched = false;
    consumed = false;
    return iq_capture(&port, out);
}

int main(void)
{
    struct iq_pair out = {0, 0};
    for (int i = -4096; i <= 4095; ++i) {
        int q = 4095 - (i + 4096);
        wi = (uint16_t)((i & 8191) | 0x8000);
        wq = (uint16_t)((q & 8191) | 0xc000);
        assert(run(NORMAL, &out) == IQ_OK && out.i == i && out.q == q && !selected);
    }
    for (enum fault f = NO_I; f <= STUCK_BUSY; ++f) {
        struct iq_pair before = out;
        wi = 0x1087;
        wq = 0x1243;
        unsigned previous = resets;
        assert(run(f, &out) != IQ_OK);
        assert(out.i == before.i && out.q == before.q && resets == previous + 1 && !selected);
        wi = (uint16_t)f;
        wq = (uint16_t)(3 * f);
        assert(run(NORMAL, &out) == IQ_OK && out.i == (int)f && out.q == 3 * (int)f);
    }
    puts("8192 coppie valide, 11 guasti con scarto e successiva ripresa.");
}
