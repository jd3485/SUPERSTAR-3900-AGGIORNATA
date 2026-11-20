/* Due stazioni AM sintetiche al convertitore I/Q. Livelli riferiti alle portanti. */
#include "../../Firmware/RX/am_sync.h"
#include "../../Firmware/RX/audio_decim.h"
#include <assert.h>
#include <math.h>
#include <stdio.h>

static const double tau = 6.2831853071795864769;

static void trial(int spacing, double ratio, double phase)
{
    struct am_sync am;
    struct audio_decim filter;
    am_sync_reset(&am, (struct iq_pair){0, 0});
    audio_decim_reset(&filter);
    double energy = 0, in_phase = 0, quadrature = 0, sum = 0;
    unsigned measured = 0;
    for (unsigned n = 0; n < 72000; ++n) {
        double t = n / 48000.;
        double wanted = 180 * (1 + .6 * sin(tau * 1000 * t));
        double adjacent = ratio * 180 * (1 + .7 * sin(tau * 1700 * t));
        double a = tau * 230 * t + .31, b = a + tau * spacing * t + phase;
        long i = lround(wanted*cos(a) + adjacent*cos(b));
        long q = lround(wanted*sin(a) + adjacent*sin(b));
        assert(i >= -4096 && i <= 4095 && q >= -4096 && q <= 4095);
        int32_t audio, y;
        if (!am_sync_sample(&am, (struct iq_pair){(int16_t)i, (int16_t)q}, n*384u, &audio)) {
            audio_decim_reset(&filter);
            continue;
        }
        if (!audio_decim_sample(&filter, audio, &y) || n < 24000)
            continue;
        double sample = y / 128.;
        in_phase += sample * cos(tau * 1000 * t);
        quadrature += sample * sin(tau * 1000 * t);
        sum += sample;
        energy += sample * sample;
        ++measured;
    }
    assert(measured == 16000);
    double tone_power = 2*(in_phase*in_phase + quadrature*quadrature)/(measured*(double)measured);
    double residual = energy/measured - pow(sum/measured, 2) - tone_power;
    assert(residual > 0 && tone_power > 0);
    double gain = 10*log10(tone_power / (108.*108./2));
    double quality = 10*log10(tone_power/residual);
    printf("%+6d Hz  %4.1fx  fase %.1f  tono %+.2f dB  tono/residuo %.2f dB\n",
           spacing, ratio, phase, gain, quality);
    if (ratio == 0) {
        assert(fabs(gain) < .1);
        assert(quality > 40);
    } else if (ratio <= 3.2) {
        /* Soglie di regressione per questi stimoli sintetici. */
        assert(fabs(gain) < .2);
        assert(quality > (ratio <= 1 ? 29 : 19));
    }
}

int main(void)
{
    trial(10000, 0, 0);
    const double ratios[] = {.1, 1, 3.16227766016838, 10};
    for (int sign = -1; sign <= 1; sign += 2)
        for (unsigned level = 0; level < sizeof ratios / sizeof ratios[0]; ++level)
            for (unsigned phase = 0; phase < 2; ++phase)
                trial(sign * 10000, ratios[level], phase * 1.5);
}
