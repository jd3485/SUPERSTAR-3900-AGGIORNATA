#ifndef RX_IQ_IIR_H
#define RX_IQ_IIR_H
#include "am_sync.h"

struct biquad_state { int32_t x1, x2, y1, y2; };
struct iq_iir {
    struct biquad_state axis[2][2];
    uint32_t previous;
    unsigned warm;
};

struct iq_pair iq_iir_filter(struct iq_iir *s, struct iq_pair pair);
void iq_iir_reset(struct iq_iir *s);
/* Falso durante i 30 ingressi di preriscaldamento e l'acquisizione PLL. */
bool iq_iir_am_sample(struct iq_iir *s, struct am_sync *am, struct iq_pair pair,
                      uint32_t stamp, int32_t *audio);
#endif
