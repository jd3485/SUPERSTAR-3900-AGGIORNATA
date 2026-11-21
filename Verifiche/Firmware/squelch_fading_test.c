/* Sequenza continua: adiacente sola, desiderata, buco breve, fading, ritorno. */
#include "../../Firmware/RX/iq_iir.h"
#include "../../Firmware/RX/audio_gate.h"
#include "../../Firmware/RX/audio_decim.h"
#include <assert.h>
#include <math.h>
#include <stdio.h>

static double wanted(unsigned n)
{
    if (n < 24000 || (n >= 48000 && n < 48192))
        return 0;
    if (n < 72000)
        return 4;
    if (n < 76800)
        return 4.*(76800-n)/4800;
    if (n < 86400)
        return 0;
    if (n < 91200)
        return 4.*(n-86400)/4800;
    return 4;
}

static double noise(uint32_t *seed)
{
    *seed = *seed*1664525u + 1013904223u;
    return sqrt(12.)*((*seed >> 8)/16777216.-.5);
}

static void run(int spacing, double offset, uint32_t seed)
{
    struct am_sync am;
    struct iq_iir iq = {0};
    struct audio_gate gate = {0};
    struct audio_decim d;
    am_sync_reset(&am, (struct iq_pair){0,0});
    audio_decim_reset(&d);
    unsigned events[4] = {0}, count = 0, false_open = 0, short_drop = 0;
    const double tau = 6.283185307179586;
    for (unsigned n = 0; n < 120000; ++n) {
        double t = n/48000.;
        double w = wanted(n)*(1+.6*sin(tau*1000*t));
        double b = 40*(1+.7*sin(tau*1700*t));
        double a = tau*180*t, p = a+tau*spacing*t+offset;
        double ni = noise(&seed);
        double nq = noise(&seed);
        struct iq_pair pair = {(int16_t)lround(w*cos(a)+b*cos(p)+ni),
                               (int16_t)lround(w*sin(a)+b*sin(p)+nq)};
        int32_t audio, filtered;
        if (!iq_iir_am_sample(&iq, &am, pair, 384u*n, &audio)) {
            audio_decim_reset(&d);
            continue;
        }
        if (!audio_decim_sample(&d, audio, &filtered))
            continue;
        bool before = gate.open;
        uint16_t duty[3];
        audio_gate_step(&gate, true, am.dc_q10/1024, 384, 256, filtered, duty);
        if (gate.open != before) {
            if (count < 4)
                events[count] = n;
            ++count;
        }
        if (n < 24000 || (n >= 79200 && n < 86400)) {
            if (gate.open || duty[0] != 128 || duty[1] != 128 || duty[2] != 128)
                ++false_open;
        }
        if (n >= 47997 && n < 56000 && !gate.open)
            ++short_drop;
    }
    printf("%+d Hz fase %.1f: eventi %u, spurie %u, cadute brevi %u, tempi %.1f %.1f %.1f ms\n",
           spacing, offset, count, false_open, short_drop, (events[0]/48.-500),
           (events[1]/48.-1500), (events[2]/48.-1800));
    assert(false_open == 0 && short_drop == 0 && count == 3);
    assert(events[0] >= 24000 && events[0] < 48000);
    assert(events[1] >= 72000 && events[1] < 79200);
    assert(events[2] >= 86400 && events[2] < 120000);
}

int main(void)
{
    for (int sign = -1; sign <= 1; sign += 2)
        for (unsigned k = 0; k < 4; ++k)
            run(sign*10000, k*.8, 851+37*k);
}
