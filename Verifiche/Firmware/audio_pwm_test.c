#include "../../Firmware/RX/audio_pwm.h"
#include <assert.h>

int main(void)
{
    static const int16_t h[19] = {30,86,78,-113,-427,-481,197,1643,3197,3868,
                                  3197,1643,197,-481,-427,-113,78,86,30};
    struct audio_pwm s = {0};
    int16_t x[2048];
    unsigned clipped_low = 0, clipped_high = 0;
    uint32_t seed = 321;
    for (unsigned n = 0; n < 2048; ++n) {
        seed = seed*1664525u + 1013904223u;
        x[n] = (int16_t)((int32_t)(seed >> 16)-32768);
        for (unsigned phase = 0; phase < 3; ++phase) {
            int64_t sum = 0;
            for (unsigned j = 0; j < 19 && j <= 3*n+phase; ++j) {
                unsigned index = 3*n+phase-j;
                if (index%3 == 0)
                    sum += (int64_t)x[index/3]*h[j];
            }
            int64_t duty = (sum + 128LL*1048576 + 524288)/1048576;
            if (duty <= 0) { duty = 0; ++clipped_low; }
            if (duty >= 256) { duty = 256; ++clipped_high; }
            assert(audio_pwm_phase(&s, phase, phase ? 123 : x[n]) == duty);
        }
    }
    assert(clipped_low && clipped_high);
}
