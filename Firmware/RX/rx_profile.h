#ifndef RX_PROFILE_H
#define RX_PROFILE_H
#include <stdbool.h>
#include <stdint.h>

enum rx_work { RX_ACQUIRE, RX_DEMOD, RX_FIR, RX_WORK_COUNT };

struct rx_profile {
    uint32_t work_max[RX_WORK_COUNT];
    uint32_t previous_stamp, interval_max, long_intervals;
    bool started;
};

/* stamp indica la cattura. work misura solo il servizio DSP, in tick CP0.
   Sottrazioni modulo 2^32, con intervalli minori di un giro del contatore. */
static inline void rx_profile_record(volatile struct rx_profile *p,
                                     enum rx_work stage,
                                     uint32_t stamp, uint32_t work)
{
    if (work > p->work_max[stage])
        p->work_max[stage] = work;
    if (p->started) {
        uint32_t interval = stamp - p->previous_stamp;
        if (interval > p->interval_max)
            p->interval_max = interval;
        if (interval >= 576u)
            ++p->long_intervals;
    }
    p->previous_stamp = stamp;
    p->started = true;
}
#endif
