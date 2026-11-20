/* Confronto host di due collocazioni dello stesso costo DSP sintetico.
   Tutti i tempi sono tick PBCLK. Il sequenziatore è quello del firmware. */
#include "../../Firmware/RX/iq_frame.h"
#include <assert.h>
#include <stdio.h>

struct scenario {
    unsigned poll, launch_delay, close, housekeeping;
};
static struct scenario timing;
static unsigned now, slot, completion, cost;
static bool overlap, active, read_done, pending;
static unsigned processed, pending_id;

static void process_previous(void)
{
    if (pending) {
        assert(pending_id == processed);
        ++processed;
        now += cost;
        pending = false;
    }
}

static struct iq_snapshot status(void)
{
    now += timing.poll;
    unsigned age = now - slot;
    bool ready = active && now >= completion && !read_done;
    return (struct iq_snapshot){.tick = age % 768, .invalid_slot = age >= 768,
        .ready_i = ready, .ready_q = ready, .busy = active && now < completion};
}

static void select_frame(bool enabled)
{
    if (!enabled) {
        active = false;
        now += timing.close;
    }
}

static void launch(void)
{
    now += timing.launch_delay;
    active = true;
    read_done = false;
    completion = now + 512;
    if (overlap)
        process_previous();
}

static void read_pair(uint16_t *i, uint16_t *q)
{
    assert(active && !read_done && now >= completion);
    *i = (uint16_t)(slot/768);
    *q = 0;
    read_done = true;
}
static void reset(void) { active = false; }
static const struct iq_port port = {status, select_frame, launch, read_pair, reset};

static bool sustained(unsigned ticks, bool during_spi)
{
    now = processed = 0;
    pending = active = read_done = false;
    cost = ticks;
    overlap = during_spi;
    bool seen_entry[65] = {false};
    for (unsigned n = 0; n < 68; ++n) {
        slot = n*768;
        if (now < slot)
            now = slot;
        unsigned entry = now - slot;
        /* Dopo lo slot iniziale, a pari fase di ingresso si ripete lo
           stesso stato temporale, inclusa la presenza della coppia pendente. */
        if (n && entry < 65) {
            if (seen_entry[entry]) {
                process_previous();
                assert(processed == n);
                return true;
            }
            seen_entry[entry] = true;
        }
        struct iq_pair out;
        if (iq_capture(&port, &out) != IQ_OK)
            return false;
        assert(out.i == (int)n && !pending);
        pending_id = (unsigned)out.i;
        pending = true;
        if (!overlap)
            process_previous();
        now += timing.housekeeping;
    }
    assert(0); /* Fasi utili finite: deve emergere un ciclo o uno scarto. */
    return false;
}

static unsigned budget(bool during_spi)
{
    /* Primo costo che perde almeno una trama, a partire da zero. */
    for (unsigned i = 0; i <= 768; ++i)
        if (!sustained(i, during_spi)) {
            assert(i > 0);
            return i-1;
        }
    assert(0);
    return 0;
}

/* Uno slot con DSP pesante ogni tre, negli altri costo fisso di 96
   tick. La fase è riferita alla coppia, anche quando il DSP è differito. */
struct state { unsigned entry, phase; };

static bool all_jitter_paths(unsigned peak, unsigned jitter, bool during_spi)
{
    struct state queue[65*3];
    bool seen[65][3] = {{false}};
    unsigned head = 0, tail = 0;
    /* A regime: tutte le tre fasi iniziali, ingresso puntuale. Con gli
       overhead scelti lo slot di avvio senza DSP pendente termina in tempo. */
    for (unsigned phase = 0; phase < 3; ++phase) {
        queue[tail++] = (struct state){0, phase};
        seen[0][phase] = true;
    }
    overlap = during_spi;
    while (head < tail) {
        struct state state = queue[head++];
        for (unsigned delay = 0; delay <= jitter; ++delay) {
            timing = (struct scenario){16, delay, 16, 32};
            slot = 768;
            now = slot + state.entry;
            processed = during_spi ? 0 : 1;
            pending_id = 0;
            pending = during_spi;
            active = read_done = false;
            unsigned phase = during_spi ? (state.phase+2)%3 : state.phase;
            cost = phase == 0 ? peak : 96;
            struct iq_pair out;
            if (iq_capture(&port, &out) != IQ_OK)
                return false;
            assert(out.i == 1 && !pending);
            if (!during_spi) {
                pending_id = 1;
                pending = true;
                process_previous();
            }
            now += timing.housekeeping;
            unsigned entry = now > 2*768 ? now-2*768 : 0;
            if (entry > 64)
                return false;
            unsigned next = (state.phase+1)%3;
            if (!seen[entry][next]) {
                seen[entry][next] = true;
                queue[tail++] = (struct state){entry, next};
            }
        }
    }
    return true;
}

static unsigned peak_budget(unsigned jitter, bool during_spi)
{
    for (unsigned peak = 96; peak <= 768; ++peak)
        if (!all_jitter_paths(peak, jitter, during_spi)) {
            assert(peak > 96);
            return peak-1;
        }
    assert(0);
    return 0;
}

int main(void)
{
    const struct scenario cases[] = {
        {4,0,0,0}, {8,8,8,16}, {12,16,12,24}, {16,16,16,32}
    };
    for (unsigned i = 0; i < sizeof cases / sizeof cases[0]; ++i) {
        timing = cases[i];
        unsigned after = budget(false), during = budget(true);
        printf("poll=%u lancio=%u chiusura=%u gestione=%u: dopo=%u durante=%u tick PBCLK\n",
            timing.poll, timing.launch_delay, timing.close, timing.housekeeping, after, during);
        assert(during > after && during >= 512);
        assert(!sustained(704, true));
    }
    for (unsigned jitter = 0; jitter <= 32; jitter += 16) {
        unsigned after = peak_budget(jitter, false);
        unsigned during = peak_budget(jitter, true);
        printf("Lancio 0..%u tick, picco DSP dopo=%u durante=%u tick PBCLK\n",
               jitter, after, during);
        assert(during >= 512 && during > after);
    }
}
