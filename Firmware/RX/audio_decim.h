#ifndef RX_AUDIO_DECIM_H
#define RX_AUDIO_DECIM_H
#include <stdint.h>
#include <stdbool.h>

struct audio_decim {
    int32_t history[64];
    int64_t partial;
    unsigned next, remaining;
};

void audio_decim_reset(struct audio_decim *s);
/* Prima uscita al 65° campione contiguo, poi una ogni tre. */
bool audio_decim_sample(struct audio_decim *s, int32_t input, int32_t *output);
#endif
