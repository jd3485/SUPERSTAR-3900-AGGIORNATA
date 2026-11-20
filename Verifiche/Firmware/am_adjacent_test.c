/* Due stazioni AM sintetiche al convertitore I/Q. Livelli riferiti alle portanti. */
#include "../../Firmware/RX/am_sync.h"
#include "../../Firmware/RX/audio_decim.h"
#include "../../Firmware/RX/iq_iir.h"
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

static double noise(uint32_t *seed)
{
    *seed = 1664525u * *seed + 1013904223u;
    return ((double)(*seed >> 8)/16777216. - .5) * sqrt(12.);
}

static void trial(int spacing, double ratio, double phase, unsigned mode,
                  double carrier, double tone, double rms)
{
    struct channel_filter channel = {0};
    struct iq_iir elliptic = {0};
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
        if (mode == 1) {
            pair = channel_sample(&channel, pair);
            if (n < 30)
                continue;
        }
        bool valid = mode == 2 ? iq_iir_am_sample(&elliptic, &am, pair, n*384u, &audio)
                               : am_sync_sample(&am, pair, n*384u, &audio);
        if (!valid) {
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
    struct iq_iir s = {0};
    uint32_t seed = 1;
    for (unsigned run = 0; run < 32; ++run) {
        for (unsigned n = 0; n < 1024; ++n) {
            seed = 1664525u * seed + 1013904223u;
            (void)iq_iir_filter(&s, (struct iq_pair){seed >> 31 ? 4095 : -4096, 0});
        }
        for (unsigned n = 0; n < 1024; ++n) {
            int16_t y = iq_iir_filter(&s, (struct iq_pair){0, 0}).i;
            if (n >= 512)
                assert(y >= -1 && y <= 1);
        }
    }
}

struct chain {
    struct iq_iir channel;
    struct am_sync am;
    struct audio_decim decim;
};

static void restart(struct chain *s)
{
    iq_iir_reset(&s->channel);
    am_sync_reset(&s->am, (struct iq_pair){12, -17});
    audio_decim_reset(&s->decim);
}

static bool sample_chain(struct chain *s, struct iq_pair pair, uint32_t stamp, int32_t *y)
{
    int32_t audio;
    if (!iq_iir_am_sample(&s->channel, &s->am, pair, stamp, &audio)) {
        audio_decim_reset(&s->decim);
        return false;
    }
    return audio_decim_sample(&s->decim, audio, y);
}

static void check_restart(unsigned before, uint32_t elapsed, bool rejected)
{
    struct chain used, fresh;
    restart(&used);
    restart(&fresh);
    uint32_t stamp = UINT32_MAX - 1500u;
    int32_t old = 0;
    for (unsigned n = 0; n < before; ++n) {
        (void)sample_chain(&used, (struct iq_pair){-815,321}, stamp, &old);
        stamp += 384u;
    }
    stamp += elapsed - 384u;
    if (rejected)
        restart(&used);
    for (unsigned n = 0; n < 420; ++n, stamp += 384u) {
        struct iq_pair pair = {(int16_t)(750 + (int)(n%49)), -200};
        int32_t a = 12345, b = 12345;
        bool ready = sample_chain(&used, pair, stamp, &a);
        assert(sample_chain(&fresh, pair, stamp, &b) == ready);
        assert(ready == (n >= 126 && (n-126)%3 == 0));
        assert(a == b && (ready || a == 12345));
    }
}

int main(void)
{
    check_decay();
    for (unsigned j = 0; j < 4; ++j) {
        unsigned before = ((const unsigned[]){4, 45, 100, 240})[j];
        check_restart(before, 384, true);
        check_restart(before, 191, false);
        check_restart(before, 576, false);
        check_restart(before, 14*384, false);
    }
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
