#ifndef RX_AUDIO_MONITOR_H
#define RX_AUDIO_MONITOR_H
#include "audio_gate.h"

struct audio_monitor {
    struct audio_gate gate;
    uint32_t last;
    bool streaming;
    uint16_t duty[3];
};

void audio_monitor_sample(struct audio_monitor *s, uint32_t now, int32_t carrier, int32_t audio);
void audio_monitor_poll(struct audio_monitor *s, uint32_t now, bool lost);
#endif
