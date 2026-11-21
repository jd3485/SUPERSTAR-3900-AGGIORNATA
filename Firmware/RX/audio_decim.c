#include "audio_decim.h"

/* FIR simmetrico a 48 kHz, finestra Kaiser beta 8, taglio a 6 kHz.
   Metà sinistra in Q15, coefficiente centrale 8192. */
struct tap { unsigned char delay; int16_t weight; };

/* Otto coppie per ingresso. Ogni ritardo della prima e seconda fase
   permette di anticipare il prodotto rispettivamente di due e un campione. */
static const struct tap phases[3][8] = {
    {{22,718},{23,606},{25,-879},{26,-1523},{27,-1346},{29,2379},{30,5140},{31,7349}},
    {{11,-57},{13,91},{14,160},{15,139},{17,-206},{18,-352},{19,-298},{21,425}},
    {{1,-1},{2,-3},{3,-4},{5,9},{6,19},{7,19},{9,-34},{10,-63}}
};

void audio_decim_reset(struct audio_decim *s)
{
    s->next = 0;
    s->remaining = 65;
    s->partial = 0;
}

bool audio_decim_sample(struct audio_decim *s, int32_t input, int32_t *output)
{
    unsigned newest = s->next;
    s->history[newest] = input;
    s->next = (newest + 1u) & 63u;
    if (--s->remaining > 2)
        return false;

    unsigned ahead = s->remaining;
    unsigned target = newest + ahead;
    const struct tap *phase = phases[2u - ahead];
    int64_t sum = ahead == 2 ? (int64_t)8192 * s->history[(target - 32u) & 63u]
                             : s->partial;
    for (unsigned k = 0; k < 8; ++k) {
        unsigned delay = phase[k].delay;
        int64_t pair = (int64_t)s->history[(target - delay) & 63u]
                     + s->history[(target - 64u + delay) & 63u];
        sum += pair * phase[k].weight;
    }
    if (ahead) {
        s->partial = sum;
        return false;
    }
    s->remaining = 3;
    int64_t rounded = (sum + (sum < 0 ? -16384 : 16384)) / 32768;
    *output = rounded > INT32_MAX ? INT32_MAX :
              rounded < INT32_MIN ? INT32_MIN : (int32_t)rounded;
    return true;
}
