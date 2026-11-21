#ifndef RX_AUDIO_PWM_H
#define RX_AUDIO_PWM_H
#include <stdint.h>

/* Stato iniziale a zero: silenzio centrato a 128 tick su 256. */
struct audio_pwm {
    int16_t history[8];
    unsigned next;
};

/* Chiamare le fasi 0,1,2 in ordine. Solo la fase 0 acquisisce input_q8,
   espresso in tick duty con otto bit frazionari. Serve un'uscita a 48 kHz. */
uint16_t audio_pwm_phase(struct audio_pwm *s, unsigned phase, int16_t input_q8);
#endif
