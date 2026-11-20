#include "am_sync.h"
#include <stdlib.h>

/* Un giro = 65536 unità; accumulatore NCO con altri 12 bit frazionari. */
static const int16_t quarter_sine[65] = {
    0, 804, 1608, 2410, 3212, 4011, 4808, 5602,
    6393, 7179, 7962, 8739, 9512, 10278, 11039, 11793,
    12539, 13279, 14010, 14732, 15446, 16151, 16846, 17530,
    18204, 18868, 19519, 20159, 20787, 21403, 22005, 22594,
    23170, 23731, 24279, 24811, 25329, 25832, 26319, 26790,
    27245, 27683, 28105, 28510, 28898, 29268, 29621, 29956,
    30273, 30571, 30852, 31113, 31356, 31580, 31785, 31971,
    32137, 32285, 32412, 32521, 32609, 32678, 32728, 32757,
    32767
};

static int32_t sine_q15(uint16_t phase)
{
    unsigned pos = phase & 16383u;
    if (phase & 16384u)
        pos = 16384u - pos;
    unsigned index = pos / 256u;
    int32_t y = quarter_sine[index];
    if (index < 64)
        y += (quarter_sine[index + 1] - y) * (int32_t)(pos % 256u) / 256;
    return phase & 32768u ? -y : y;
}

/* Approssimazione di atan2. Il rapporto Q10 rimane nel primo ottante. */
static int32_t angle(int32_t x, int32_t y)
{
    int32_t ax = abs(x), ay = abs(y);
    if (ax + ay == 0)
        return 0;
    int32_t ratio = ax >= ay ? ay * 1024 / ax : ax * 1024 / ay;
    int32_t phi = ratio * (8192 + 2847 * (1024 - ratio) / 1024) / 1024;
    if (ay > ax)
        phi = 16384 - phi;
    if (x < 0)
        phi = 32768 - phi;
    return y < 0 ? -phi : phi;
}

void am_sync_reset(struct am_sync *s, struct iq_pair offset)
{
    *s = (struct am_sync){ .offset = offset };
}

static void acquire(struct am_sync *s, int32_t i, int32_t q)
{
    unsigned half = s->count / 16;
    s->sum_i[half] += i;
    s->sum_q[half] += q;
    if (++s->count != 32)
        return;
    if ((!s->sum_i[0] && !s->sum_q[0]) || (!s->sum_i[1] && !s->sum_q[1])) {
        am_sync_reset(s, s->offset);
        return;
    }
    int32_t first = angle(s->sum_i[0], s->sum_q[0]);
    int32_t second = angle(s->sum_i[1], s->sum_q[1]);
    int32_t delta = (uint16_t)(second - first);
    if (delta >= 32768)
        delta -= 65536;
    s->rate_q12 = delta * 256;      /* distanza tra i centri: 16 campioni */
    s->phase_q12 = (uint32_t)(second * 4096 + s->rate_q12 * 17 / 2);
}

bool am_sync_sample(struct am_sync *s, struct iq_pair sample, uint32_t core_count,
                    int32_t *audio_q7)
{
    /* Un periodo vale 384 tick CP0. La finestra copre la variazione della
       fase di completamento ammessa da iq_capture, anche al wrap di Count. */
    uint32_t elapsed = core_count - s->previous_count;
    if (s->count && !am_interval_valid(elapsed))
        am_sync_reset(s, s->offset);
    s->previous_count = core_count;
    int32_t i = sample.i - s->offset.i, q = sample.q - s->offset.q;
    if (s->count < 32) {
        acquire(s, i, q);
        return false;
    }
    uint16_t phase = (uint16_t)(s->phase_q12 >> 12);
    int32_t sin_p = sine_q15(phase), cos_p = sine_q15((uint16_t)(phase + 16384));
    int32_t carrier = (i * cos_p + q * sin_p) / 256; /* Q7 */
    /* Mantieni la risoluzione del discriminatore anche sotto pochi LSB. */
    int32_t error = angle(carrier,
                          (q * cos_p - i * sin_p) / 256);
    s->rate_q12 += error;            /* Ki = 1/4096, Kp = 1/32 */
    const int32_t limit = 8388608;   /* ±1500 Hz: limite del rilevatore iniziale */
    if (s->rate_q12 > limit)
        s->rate_q12 = limit;
    if (s->rate_q12 < -limit)
        s->rate_q12 = -limit;
    s->phase_q12 += (uint32_t)(s->rate_q12 + error * 128);
    if (!s->audio_started) {
        s->dc_q10 = carrier * 1024;
        s->audio_started = true;
    }
    int32_t ac = carrier - s->dc_q10 / 1024;
    s->dc_q10 += ac;
    *audio_q7 = ac;
    return true;
}
