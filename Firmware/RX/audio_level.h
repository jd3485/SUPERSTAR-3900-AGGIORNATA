#ifndef RX_AUDIO_LEVEL_H
#define RX_AUDIO_LEVEL_H
#include <stdint.h>

/* Livellatore audio a 16 kHz dopo il decimatore. Azzerare a ogni
   discontinuità. L'uscita è in tick PWM Q8 per audio_pwm_phase. */
struct audio_level {
    uint32_t envelope, block_peak;
    unsigned count;
};
int16_t audio_level_sample(struct audio_level *s, int32_t audio_q7);
#endif
