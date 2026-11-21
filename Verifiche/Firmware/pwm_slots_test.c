#include "../../Firmware/RX/pwm_slots.h"
#include <assert.h>

int main(void)
{
    struct pwm_slots s = {.last = 128};
    uint32_t stamp = UINT32_MAX - 100;
    assert(pwm_slots_next(&s, stamp) == 128);
    uint16_t frame[3] = {0, 256, 193};
    pwm_slots_submit(&s, frame);
    for (unsigned n = 0; n < 3; ++n) {
        stamp += 384;
        assert(pwm_slots_next(&s, stamp) == frame[n]);
    }
    for (unsigned n = 0; n < 100; ++n) {
        stamp += 384;
        assert(pwm_slots_next(&s, stamp) == (n < 65 ? 192-n : 128));
    }
    pwm_slots_submit(&s, frame);
    stamp += 384;
    assert(pwm_slots_next(&s, stamp) == 0);
    stamp += 768;
    assert(pwm_slots_next(&s, stamp) == 1 && s.remaining == 0);
    pwm_slots_submit(&s, frame);
    stamp += 384;
    assert(pwm_slots_next(&s, stamp) == 0);
}
