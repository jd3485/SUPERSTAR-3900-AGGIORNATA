#include "audio_level.h"

int16_t audio_level_sample(struct audio_level *s, int32_t audio_q7)
{
    /* Attacco sul campione corrente, rilascio del 12,5% ogni 64 campioni.
       Il picco del blocco evita il rilascio fra due creste del tono. */
    uint32_t peak = audio_q7 < 0 ? 0u - (uint32_t)audio_q7 : (uint32_t)audio_q7;
    if (peak > s->block_peak)
        s->block_peak = peak;
    if (peak > s->envelope)
        s->envelope = peak;
    if (s->envelope < 307u)
        s->envelope = 307u;
    int16_t output = (int16_t)((int64_t)audio_q7 * 16384 / (int64_t)s->envelope);
    if (++s->count == 64) {
        uint32_t release = (s->envelope + 7u) / 8u;
        s->envelope -= release;
        if (s->envelope < s->block_peak)
            s->envelope = s->block_peak;
        s->block_peak = 0;
        s->count = 0;
    }
    return output;
}
