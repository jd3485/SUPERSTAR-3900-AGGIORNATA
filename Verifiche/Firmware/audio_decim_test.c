#include "../../Firmware/RX/audio_decim.h"
#include <assert.h>
#include <math.h>
#include <stdio.h>

static void constant(struct audio_decim *s, int32_t x)
{
    audio_decim_reset(s);
    for (unsigned n = 0; n < 500; ++n) {
        int32_t y = 123;
        bool ready = audio_decim_sample(s, x, &y);
        assert(ready == (n >= 64 && (n-64)%3 == 0));
        assert(y == (ready ? x : 123));
    }
}

/* Convoluzione diretta indipendente, nello stesso formato Q15. */
static int32_t direct(const int32_t *window)
{
    static const int16_t half[33] = {
        0,-1,-3,-4,0,9,19,19,0,-34,-63,-57,0,91,160,139,
        0,-206,-352,-298,0,425,718,606,0,-879,-1523,-1346,0,2379,5140,7349,8192
    };
    int64_t acc = 0;
    for (unsigned k = 0; k < 65; ++k)
        acc += (int64_t)window[k] * half[k <= 32 ? k : 64-k];
    acc = (acc + (acc < 0 ? -16384 : 16384)) / 32768;
    return acc > INT32_MAX ? INT32_MAX : acc < INT32_MIN ? INT32_MIN : (int32_t)acc;
}

static void compare_streams(struct audio_decim *s)
{
    uint32_t seed = 1;
    int32_t inputs[1026];
    for (unsigned run = 0; run < 3; ++run) {
        audio_decim_reset(s);
        for (unsigned n = 0; n < 1024 + run; ++n) {
            seed = 1664525u * seed + 1013904223u;
            inputs[n] = (int32_t)((int64_t)seed - 2147483648LL);
            int32_t y = 123;
            bool ready = audio_decim_sample(s, inputs[n], &y);
            assert(ready == (n >= 64 && (n-64)%3 == 0));
            assert(y == (ready ? direct(inputs + n - 64) : 123));
        }
    }
}

int main(void)
{
    struct audio_decim s;
    compare_streams(&s);
    constant(&s, INT32_MAX);
    constant(&s, INT32_MIN);
    constant(&s, 0);
    /* Sweep in fase con il ritardo di gruppo, inclusi continua e Nyquist. */
    for (unsigned hz = 0; hz <= 24000; hz += 25) {
        if (hz > 4000 && hz < 8000)
            continue;
        audio_decim_reset(&s);
        double omega = 2 * acos(-1.0) * hz / 48000;
        for (unsigned n = 0; n < 320; ++n) {
            int32_t y;
            int32_t x = (int32_t)lround(1000000 * cos(omega * ((int)n-32)));
            if (audio_decim_sample(&s, x, &y)) {
                double reference = hz <= 4000 ? 1000000 * cos(omega * ((int)n-64)) : 0;
                assert(fabs(y-reference) < 200);
            }
        }
    }
    puts("Audio FIR /3: banda, reiezione, cadenza e reset verificati.");
}
