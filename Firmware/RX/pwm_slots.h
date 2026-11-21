#ifndef RX_PWM_SLOTS_H
#define RX_PWM_SLOTS_H
#include "am_sync.h"

struct pwm_slots {
    uint16_t duty[3], last;
    unsigned remaining;
    uint32_t previous;
    bool started;
};

static inline void pwm_slots_submit(struct pwm_slots *s, const uint16_t duty[3])
{
    for (unsigned n = 0; n < 3; ++n)
        s->duty[n] = duty[n];
    s->remaining = 3;
}

static inline uint16_t pwm_slots_next(struct pwm_slots *s, uint32_t now)
{
    if (s->started && !am_interval_valid(now - s->previous))
        s->remaining = 0;
    s->started = true;
    s->previous = now;
    if (s->remaining) {
        s->last = s->duty[3u - s->remaining];
        --s->remaining;
    } else {
        s->last += (s->last < 128u) - (s->last > 128u);
    }
    return s->last;
}
#endif
