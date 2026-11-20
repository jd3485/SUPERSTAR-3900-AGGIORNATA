/* Due stazioni AM sintetiche al convertitore I/Q. Livelli riferiti alle portanti. */
#include "../../Firmware/RX/am_sync.h"
#include "../../Firmware/RX/audio_decim.h"
#include <assert.h>
#include <math.h>
#include <stdio.h>

static const double tau = 6.2831853071795864769;

/* Candidato per la sola caratterizzazione host, coeff. Q12 a 48 kHz. */
struct channel_filter {
    struct iq_pair history[32];
    unsigned next;
};

static int16_t quantize(int32_t sum)
{
    int32_t v = (sum + (sum >= 0 ? 2048 : -2048)) / 4096;
    return v > 4095 ? 4095 : v < -4096 ? -4096 : (int16_t)v;
}

static struct iq_pair channel_sample(struct channel_filter *s, struct iq_pair input)
{
    static const int16_t taps[15] = {
        -15,-21,-18,6,44,74,67,6,-92,-170,-157,-3,285,629,908
    };
    unsigned n = s->next;
    s->history[n] = input;
    s->next = (n+1u) & 31u;
    struct iq_pair center = s->history[(n-15u) & 31u];
    int32_t i = 1010 * center.i, q = 1010 * center.q;
    for (unsigned k = 0; k < 15; ++k) {
        struct iq_pair left = s->history[(n-k) & 31u];
        struct iq_pair right = s->history[(n-30u+k) & 31u];
        i += taps[k] * (left.i + right.i);
        q += taps[k] * (left.q + right.q);
    }
    return (struct iq_pair){quantize(i), quantize(q)};
}

/* Due biquad ellittici a guadagno unitario in continua. Stato Q3 e
   coefficienti Q12. b2=b0 riduce a quattro i prodotti per sezione. */
struct biquad_state { int32_t x1, x2, y1, y2; };
static const int16_t sos[2][4] = {
    {231,135,5641,-2142}, {1364,-1299,6055,-3388}
};

static int16_t elliptic_sample(struct biquad_state state[2], int16_t input)
{
    int32_t x = 8 * input;
    for (unsigned j = 0; j < 2; ++j) {
        struct biquad_state *s = &state[j];
        const int16_t *k = sos[j];
        int32_t acc = k[0]*(x+s->x2) + k[1]*s->x1 + k[2]*s->y1 + k[3]*s->y2;
        int32_t y = (acc + (acc < 0 ? -2048 : 2048))/4096;
        y = y > 65535 ? 65535 : y < -65535 ? -65535 : y;
        s->x2 = s->x1;
        s->x1 = x;
        s->y2 = s->y1;
        s->y1 = y;
        x = y;
    }
    x = (x + (x < 0 ? -4 : 4))/8;
    return x > 4095 ? 4095 : x < -4096 ? -4096 : (int16_t)x;
}

static double noise(uint32_t *seed)
{
    *seed = 1664525u * *seed + 1013904223u;
    return ((double)(*seed >> 8)/16777216. - .5) * sqrt(12.);
}

static void trial(int spacing, double ratio, double phase, unsigned mode,
                  double carrier, double tone, double rms)
{
    struct channel_filter channel = {0};
    struct biquad_state elliptic[2][2] = {0};
    uint32_t seed = 151;
    struct am_sync am;
    struct audio_decim filter;
    am_sync_reset(&am, (struct iq_pair){0, 0});
    audio_decim_reset(&filter);
    double energy = 0, in_phase = 0, quadrature = 0, sum = 0;
    unsigned measured = 0;
    for (unsigned n = 0; n < 72000; ++n) {
        double t = n / 48000.;
        double wanted = carrier * (1 + .6 * sin(tau * tone * t));
        double adjacent = ratio * carrier * (1 + .7 * sin(tau * 1700 * t));
        double a = tau * 230 * t + .31, b = a + tau * spacing * t + phase;
        long i = lround(wanted*cos(a) + adjacent*cos(b) + rms*noise(&seed));
        long q = lround(wanted*sin(a) + adjacent*sin(b) + rms*noise(&seed));
        assert(i >= -4096 && i <= 4095 && q >= -4096 && q <= 4095);
        int32_t audio, y;
        struct iq_pair pair = {(int16_t)i, (int16_t)q};
        if (mode) {
            if (mode == 1) {
                pair = channel_sample(&channel, pair);
            } else {
                pair.i = elliptic_sample(elliptic[0], pair.i);
                pair.q = elliptic_sample(elliptic[1], pair.q);
            }
            if (n < 30)
                continue;
        }
        if (!am_sync_sample(&am, pair, n*384u, &audio)) {
            audio_decim_reset(&filter);
            continue;
        }
        if (!audio_decim_sample(&filter, audio, &y) || n < 24000)
            continue;
        double sample = y / 128.;
        in_phase += sample * cos(tau * tone * t);
        quadrature += sample * sin(tau * tone * t);
        sum += sample;
        energy += sample * sample;
        ++measured;
    }
    assert(measured == 16000);
    double tone_power = 2*(in_phase*in_phase + quadrature*quadrature)/(measured*(double)measured);
    double residual = energy/measured - pow(sum/measured, 2) - tone_power;
    assert(residual > 0 && tone_power > 0);
    double gain = 10*log10(tone_power / (pow(carrier*.6, 2)/2));
    double quality = 10*log10(tone_power/residual);
    printf("%s A=%.0f tono %.0f Hz %+6d Hz  %4.1fx  fase %.1f  tono %+.2f dB  tono/residuo %.2f dB\n",
           ((const char *[]){"base","FIR","IIR"})[mode], carrier, tone, spacing, ratio, phase, gain, quality);
    if (rms > 0) {
        assert(fabs(gain) < .2 && quality > 10);
        return;
    }
    if (mode == 2) {
        assert(fabs(gain) < .35 && quality > 48);
        return;
    }
    if (mode == 1) {
        assert(fabs(gain) < .35 && quality > 49);
        return;
    }
    if (ratio == 0) {
        assert(fabs(gain) < .1);
        assert(quality > 40);
    } else if (ratio <= 3.2) {
        /* Soglie di regressione per questi stimoli sintetici. */
        assert(fabs(gain) < .2);
        assert(quality > (ratio <= 1 ? 29 : 19));
    }
}

static void check_decay(void)
{
    struct biquad_state s[2] = {0};
    uint32_t seed = 1;
    for (unsigned run = 0; run < 32; ++run) {
        for (unsigned n = 0; n < 1024; ++n) {
            seed = 1664525u * seed + 1013904223u;
            (void)elliptic_sample(s, seed >> 31 ? 4095 : -4096);
        }
        for (unsigned n = 0; n < 1024; ++n) {
            int16_t y = elliptic_sample(s, 0);
            if (n >= 512)
                assert(y >= -1 && y <= 1);
        }
    }
}

int main(void)
{
    check_decay();
    const double ratios[] = {.1, 1, 3.16227766016838, 10};
    for (unsigned mode = 0; mode < 3; ++mode) {
        trial(10000, 0, 0, mode, 180, 1000, 0);
        for (int sign = -1; sign <= 1; sign += 2)
            for (unsigned level = 0; level < sizeof ratios / sizeof ratios[0]; ++level)
                for (unsigned phase = 0; phase < 2; ++phase)
                    trial(sign * 10000, ratios[level], phase * 1.5, mode, 180, 1000, 0);
        trial(10000, 0, 0, mode, 4, 1000, 1);
        trial(10000, 0, 0, mode, 180, 300, 0);
        trial(10000, 0, 0, mode, 180, 3000, 0);
        trial(10000, 0, 0, mode, 180, 4000, 0);
    }
}
