#include "../../Firmware/RX/rx_profile.h"
#include <assert.h>

int main(void)
{
    struct rx_profile p = {0};
    uint32_t t = UINT32_MAX - 9u;
    rx_profile_record(&p, RX_ACQUIRE, t, 20u);
    assert(p.work_max[RX_ACQUIRE] == 20 && p.interval_max == 0);
    t += 384u;
    rx_profile_record(&p, RX_DEMOD, t, 40u);
    assert(p.interval_max == 384 && p.long_intervals == 0);
    t += 575u;
    rx_profile_record(&p, RX_FIR, t, 75u);
    assert(p.interval_max == 575 && p.long_intervals == 0);
    t += 576u;
    rx_profile_record(&p, RX_FIR, t, 30u);
    assert(p.interval_max == 576 && p.long_intervals == 1);
    t += 384u;
    rx_profile_record(&p, RX_DEMOD, t, 50u);
    assert(p.work_max[RX_DEMOD] == 50 && p.work_max[RX_FIR] == 75);
    assert(p.interval_max == 576 && p.long_intervals == 1);
}
