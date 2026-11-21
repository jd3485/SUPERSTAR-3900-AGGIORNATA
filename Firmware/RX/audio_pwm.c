#include "audio_pwm.h"

/* FIR simmetrico a 19 coefficienti Q12, diviso in tre fasi a somma 4096. */
static const int16_t taps[3][7] = {
    {30, -113, 197, 3868, 197, -113, 30},
    {86, -427, 1643, 3197, -481, 78, 0},
    {78, -481, 3197, 1643, -427, 86, 0}
};

uint16_t audio_pwm_phase(struct audio_pwm *s, unsigned phase, int16_t input_q8)
{
    if (phase == 0) {
        s->history[s->next] = input_q8;
        s->next = (s->next + 1u) & 7u;
    }
    int32_t acc = 0;
    unsigned count = phase == 0 ? 7 : 6;
    for (unsigned k = 0; k < count; ++k)
        acc += (int32_t)taps[phase][k] * s->history[(s->next-1u-k) & 7u];
    /* Limitare prima della divisione rende il numeratore positivo. */
    acc += (128 * 1048576 + 524288);
    if (acc <= 0)
        return 0;
    if (acc >= 256 * 1048576)
        return 256;
    return (uint16_t)(acc / 1048576);
}
