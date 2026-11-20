/* Verifica end-to-end dal quantizzatore signed 13 bit al demodulatore C. */
#include "../../Firmware/RX/am_sync.h"
#include <assert.h>
#include <math.h>
#include <stdio.h>

static const double tau = 6.2831853071795864769;
static uint32_t seed;
static double noise(void)
{
    seed = seed * 1664525u + 1013904223u;
    return ((double)(seed >> 8) / 16777216.0 - .5) * sqrt(12.);
}

static void trial(double carrier, double detune, double tone, double depth, double rms)
{
    struct am_sync s;
    struct iq_pair offset = {37, -62};
    am_sync_reset(&s, offset);
    seed = 151;
    double x2 = 0, xy = 0, y2 = 0;
    int32_t audio = 0;
    unsigned measured = 0;
    for (int n = 0; n < 19200; ++n) {
        /* Un salto di campioni con fase sconosciuta dopo il buco. */
        if (n == 9600 && detune <= 0)
            am_sync_reset(&s, offset);
        double t = (n + (n >= 9600 ? 13 : 0)) / 48000.;
        double phase = 2.7 + tau * detune * t;
        double modulation = depth * carrier * sin(tau * tone * t);
        double amplitude = carrier + modulation;
        struct iq_pair pair = {
            (int16_t)lround(offset.i + amplitude * cos(phase) + rms * noise()),
            (int16_t)lround(offset.q + amplitude * sin(phase) + rms * noise())
        };
        int32_t before = audio;
        uint32_t stamp = UINT32_MAX - 800u + 384u * (unsigned)(n + (n >= 9600 ? 13 : 0));
        bool valid = am_sync_sample(&s, pair, stamp, &audio);
        int age = n % 9600;
        assert(valid == (age >= 32));
        if (!valid) {
            assert(audio == before);
            continue;
        }
        if (age == 32)
            assert(audio == 0);
        if (age < 4800)
            continue;
        double y = audio / 128.;
        x2 += modulation * modulation;
        xy += modulation * y;
        y2 += y * y;
        ++measured;
    }
    assert(measured == 9600);
    double gain = xy / x2, corr = xy / sqrt(x2 * y2);
    printf("portante %.1f, offset %+.0f Hz, tono %.0f Hz, m %.2f, rumore %.1f LSB: guadagno %.4f, correlazione %.4f\n",
           carrier, detune, tone, depth, rms, gain, corr);
    assert(fabs(gain - 1) < .08);
    assert(corr > (carrier >= 100 ? .99 : .80));
}

int main(void)
{
    for (int sign = -1; sign <= 1; ++sign)
        for (unsigned j = 0; j < 3; ++j)
            trial(850., sign * 450., (double[]){300, 1000, 3000}[j], .8, 2.);
    trial(850., -700., 1000., .98, 4.);
    trial(4., 180., 1000., .8, 1.);
    /* Assenza di portante all'avvio, poi vertici del convertitore e offset. */
    struct am_sync s;
    struct iq_pair offset = {-4096, 4095};
    am_sync_reset(&s, offset);
    int32_t audio = 7;
    for (unsigned n = 0; n < 96; ++n)
        assert(!am_sync_sample(&s, offset, 384u * n, &audio) && audio == 7);
    for (unsigned n = 0; n < 1000; ++n)
        (void)am_sync_sample(&s, (struct iq_pair){4095, -4096}, 384u * (96 + n), &audio);
}
