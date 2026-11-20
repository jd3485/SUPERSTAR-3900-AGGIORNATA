#include "audio_decim.h"

/* FIR simmetrico a 48 kHz, finestra Kaiser beta 8, taglio a 6 kHz.
   Metà sinistra in Q15, coefficiente centrale 8192. */
static const int16_t taps[32] = {
    0,-1,-3,-4,0,9,19,19,0,-34,-63,-57,0,91,160,139,
    0,-206,-352,-298,0,425,718,606,0,-879,-1523,-1346,0,2379,5140,7349
};

void audio_decim_reset(struct audio_decim *s)
{
    s->next = 0;
    s->remaining = 65;
}

bool audio_decim_sample(struct audio_decim *s, int32_t input, int32_t *output)
{
    unsigned newest = s->next;
    s->history[newest] = input;
    s->next = (newest + 1u) & 127u;
    if (--s->remaining)
        return false;
    s->remaining = 3;
    int64_t sum = (int64_t)8192 * s->history[(newest - 32u) & 127u];
    for (unsigned k = 0; k < 32; ++k) {
        int64_t pair = (int64_t)s->history[(newest - k) & 127u]
                     + s->history[(newest - 64u + k) & 127u];
        sum += pair * taps[k];
    }
    int64_t rounded = (sum + (sum < 0 ? -16384 : 16384)) / 32768;
    *output = rounded > INT32_MAX ? INT32_MAX :
              rounded < INT32_MIN ? INT32_MIN : (int32_t)rounded;
    return true;
}
