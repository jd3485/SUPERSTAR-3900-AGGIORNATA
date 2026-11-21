#include "../../Firmware/RX/audio_level.h"
#include "../../Firmware/RX/audio_pwm.h"
#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static void weak_with_noise(void)
{
    struct audio_level s = {0};
    uint32_t seed = 151;
    double in_sine = 0, in_cos = 0, energy = 0, dc = 0;
    for (unsigned n = 0; n < 32000; ++n) {
        double phase = 6.283185307179586*n/16;
        seed = seed*1664525u + 1013904223u;
        double noise = sqrt(12.)*((seed >> 8)/16777216.-.5);
        int32_t sample = (int32_t)lround(128*(2.4*sin(phase) + noise));
        double y = audio_level_sample(&s, sample)/256.;
        if (n >= 16000) {
            in_sine += y*sin(phase);
            in_cos += y*cos(phase);
            energy += y*y;
            dc += y;
        }
    }
    double tone = 2*(in_sine*in_sine + in_cos*in_cos)/(16000.*16000.);
    double residual = energy/16000 - tone - pow(dc/16000, 2);
    double ratio = 10*log10(tone/residual);
    assert(ratio > 4 && ratio < 5.5);
    printf("Debole con rumore: tono %.2f tick picco, tono/residuo %.2f dB\n",
           sqrt(2*tone), ratio);
}

int main(void)
{
    weak_with_noise();
    struct audio_level level = {0};
    struct audio_pwm pwm = {0};
    double noise_power = 0;
    unsigned recovered = 0, low = 256, high = 0;
    uint32_t seed = 1;
    for (unsigned n = 0; n < 24000; ++n) {
        double peak = n < 4000 || n >= 8000 ? 2.4 : 108;
        int32_t x = (int32_t)lround(128*peak*sin(6.283185307179586*n/16));
        if (n >= 16000) {
            seed = 1664525u*seed + 1013904223u;
            x = (int32_t)lround(128*sqrt(12.)*((seed >> 8)/16777216.-.5));
        }
        int16_t y = audio_level_sample(&level, x);
        assert(abs(y) <= 64*256);
        if (n == 3996 || n == 4004)
            assert(abs(y) == 64*256);
        if (n >= 8000 && n < 16000 && abs(y) >= .9*64*256 && !recovered)
            recovered = n - 8000;
        if (n >= 16000)
            noise_power += (y/256.)*(y/256.);
        for (unsigned phase = 0; phase < 3; ++phase) {
            unsigned duty = audio_pwm_phase(&pwm, phase, y);
            if (duty < low) low = duty;
            if (duty > high) high = duty;
        }
    }
    double noise_rms = sqrt(noise_power/8000);
    assert(recovered && recovered < 3200 && low > 0 && high < 256);
    assert(noise_rms > 25 && noise_rms < 28);
    printf("Recupero al 90%% %.2f ms, duty %u..%u, rumore %.2f tick RMS\n",
           recovered/16., low, high, noise_rms);
    level = (struct audio_level){0};
    assert(audio_level_sample(&level, INT32_MIN) == -16384);
    assert(audio_level_sample(&level, INT32_MAX) == 16383);
    level = (struct audio_level){0};
    assert(audio_level_sample(&level, 0) == 0);
}
