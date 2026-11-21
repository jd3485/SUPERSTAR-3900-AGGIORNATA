#include "iq_iir.h"

/* Due biquad ellittici a guadagno unitario in continua. Stato Q3 e
   coefficienti Q12. b2=b0 riduce a quattro i prodotti per sezione. */
static const int16_t sos[2][4] = {
    {231,135,5641,-2142}, {1364,-1299,6055,-3388}
};

static int16_t elliptic_sample(struct biquad_state state[2], int16_t input)
{
    int32_t x = 8 * input;
    for (unsigned j = 0; j < 2; ++j) {
        struct biquad_state *s = &state[j];
        const int16_t *k = sos[j];
        int32_t acc = k[0]*(x+s->x2) + k[1]*s->x1 + k[2]*s->y1 + k[3]*s->y2;
        int32_t y = (acc + (acc < 0 ? -2048 : 2048))/4096;
        y = y > 65535 ? 65535 : y < -65535 ? -65535 : y;
        s->x2 = s->x1;
        s->x1 = x;
        s->y2 = s->y1;
        s->y1 = y;
        x = y;
    }
    x = (x + (x < 0 ? -4 : 4))/8;
    return x > 4095 ? 4095 : x < -4096 ? -4096 : (int16_t)x;
}

struct iq_pair iq_iir_filter(struct iq_iir *s, struct iq_pair pair)
{
    pair.i = elliptic_sample(s->axis[0], pair.i);
    pair.q = elliptic_sample(s->axis[1], pair.q);
    return pair;
}

void iq_iir_reset(struct iq_iir *s)
{
    *s = (struct iq_iir){0};
}

bool iq_iir_am_sample(struct iq_iir *s, struct am_sync *am, struct iq_pair pair,
                      uint32_t stamp, int32_t *audio)
{
    if (s->warm && !am_interval_valid(stamp - s->previous)) {
        iq_iir_reset(s);
        am_sync_reset(am, am->offset);
    }
    s->previous = stamp;
    pair = iq_iir_filter(s, pair);
    if (s->warm < 30) {
        ++s->warm;
        return false;
    }
    return am_sync_sample(am, pair, stamp, audio);
}
