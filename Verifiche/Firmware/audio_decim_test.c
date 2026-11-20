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

int main(void)
{
    struct audio_decim s;
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
