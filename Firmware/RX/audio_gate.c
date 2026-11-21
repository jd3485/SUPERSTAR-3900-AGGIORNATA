#include "audio_gate.h"

void audio_gate_step(struct audio_gate *s, bool valid, int32_t carrier_q7,
                     uint32_t open_q7, uint32_t close_q7, int32_t audio_q7,
                     uint16_t duty[3])
{
    bool was_open = s->open;
    uint32_t carrier = carrier_q7 > 0 ? (uint32_t)carrier_q7 : 0;
    if (!valid || close_q7 >= open_q7) {
        s->open = false;
        s->dwell = 0;
    } else {
        bool change = s->open ? carrier <= close_q7 : carrier >= open_q7;
        s->dwell = change ? s->dwell + 1 : 0;
        if (s->dwell == (s->open ? 128u : 32u)) {
            s->open = !s->open;
            s->dwell = 0;
        }
    }
    if (was_open && !s->open) {
        s->level = (struct audio_level){0};
        s->pwm = (struct audio_pwm){0};
        s->fade = 0;
    }
    int16_t input = 0;
    if (s->open) {
        if (s->fade < 64)
            ++s->fade;
        input = (int16_t)((int32_t)audio_level_sample(&s->level, audio_q7)
                          * (int32_t)s->fade / 64);
    }
    for (unsigned p = 0; p < 3; ++p) {
        if (s->open)
            s->last_offset = (int)audio_pwm_phase(&s->pwm, p, input) - 128;
        else
            s->last_offset += (s->last_offset < 0) - (s->last_offset > 0);
        duty[p] = (uint16_t)(128 + s->last_offset);
    }
}
