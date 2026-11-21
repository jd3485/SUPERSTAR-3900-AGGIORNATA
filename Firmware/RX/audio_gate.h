#ifndef RX_AUDIO_GATE_H
#define RX_AUDIO_GATE_H
#include "audio_level.h"
#include "audio_pwm.h"
#include <stdbool.h>

/* Inizializzare a zero. Un passo per intervallo audio (16 kHz), anche
   durante i buchi. Le tre uscite vanno distribuite sui tre slot a 48 kHz. */
struct audio_gate {
    struct audio_level level;
    struct audio_pwm pwm;
    unsigned dwell, fade;
    int last_offset;
    bool open;
};

void audio_gate_step(struct audio_gate *s, bool valid, int32_t carrier_q7,
                     uint32_t open_q7, uint32_t close_q7, int32_t audio_q7,
                     uint16_t duty[3]);
#endif
