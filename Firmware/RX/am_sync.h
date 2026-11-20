#ifndef RX_AM_SYNC_H
#define RX_AM_SYNC_H
#include "iq_frame.h"

/* Modello a virgola fissa a 48 kHz. Ingressi e offset in codici ADC signed 13 bit. */
struct am_sync {
    struct iq_pair offset;
    uint32_t previous_count;
    int32_t sum_i[2], sum_q[2];
    unsigned count;
    uint32_t phase_q12;
    int32_t rate_q12, dc_q10;
    bool audio_started;
};

static inline bool am_interval_valid(uint32_t elapsed)
{
    return elapsed >= 192u && elapsed < 576u;
}

void am_sync_reset(struct am_sync *s, struct iq_pair offset);
/* core_count: CP0 Count libero a SYSCLK/2, letto al completamento della coppia.
   Un falso indica riacquisizione. Il valore di uscita resta intatto. */
bool am_sync_sample(struct am_sync *s, struct iq_pair sample, uint32_t core_count,
                    int32_t *audio_q7);
#endif
