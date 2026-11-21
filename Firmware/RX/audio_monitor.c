#include "audio_monitor.h"

/* CP0 a 18,432 MHz. Un intervallo audio vale 1152 tick. */
void audio_monitor_poll(struct audio_monitor *s, uint32_t now, bool lost)
{
    uint32_t elapsed = now - s->last;
    if (s->streaming) {
        if (!lost && elapsed < 1728u)
            return;
        audio_gate_step(&s->gate, false, 0, 384, 256, 0, s->duty);
        s->streaming = false;
        if (elapsed < 1152u) {
            s->last = now;
            return;
        }
        s->last += 1152u;
        elapsed -= 1152u;
    }
    if (elapsed < 1152u)
        return;
    uint32_t frames = elapsed / 1152u;
    s->last += frames * 1152u;
    /* Salta le fasi già trascorse senza ripubblicare una raffica di campioni. */
    int offset = s->gate.last_offset;
    uint32_t skip = (frames-1u)*3u;
    unsigned magnitude = (unsigned)(offset < 0 ? -offset : offset);
    magnitude = magnitude > skip ? magnitude-skip : 0;
    s->gate.last_offset = offset < 0 ? -(int)magnitude : (int)magnitude;
    audio_gate_step(&s->gate, false, 0, 384, 256, 0, s->duty);
}

void audio_monitor_sample(struct audio_monitor *s, uint32_t now, int32_t carrier, int32_t audio)
{
    audio_monitor_poll(s, now, false);
    audio_gate_step(&s->gate, true, carrier, 384, 256, audio, s->duty);
    s->streaming = true;
    s->last = now;
}
