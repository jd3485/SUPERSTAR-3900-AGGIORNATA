#include "../../Firmware/RX/audio_monitor.h"
#include <assert.h>
#include <string.h>

int main(void)
{
    /* Wrap CP0 durante il vuoto. Confronta polling fitto e recupero in un passo. */
    uint32_t now = UINT32_MAX - 128u*1152u - 100u;
    struct audio_monitor a = {.duty = {128,128,128}};
    for (unsigned n = 0; n < 128; ++n) {
        now += 1152u;
        audio_monitor_sample(&a, now, 512, 10000);
    }
    assert(a.gate.open && a.duty[2] == 192);
    for (unsigned frames = 2; frames <= 256; ++frames) {
        struct audio_monitor slow = a, fast = a;
        uint32_t duration = frames*1152u + 77u;
        for (uint32_t t = 0; t < duration; t += 100u)
            audio_monitor_poll(&fast, now+t, false);
        audio_monitor_poll(&fast, now+duration, false);
        audio_monitor_poll(&slow, now+duration, false);
        assert(memcmp(slow.duty, fast.duty, sizeof fast.duty) == 0);
        assert(!slow.streaming && !slow.gate.open);
        if (frames >= 23)
            assert(slow.duty[0] == 128 && slow.duty[2] == 128);
    }
    struct audio_monitor timed = a;
    audio_monitor_poll(&timed, now+1727u, false);
    assert(timed.gate.open);
    audio_monitor_poll(&timed, now+1728u, false);
    assert(!timed.gate.open && timed.duty[0] == 191);
    audio_monitor_poll(&a, now+10u, true);
    assert(!a.gate.open && a.duty[2] == 189);
    audio_monitor_poll(&a, now+10u, true);
    assert(a.duty[2] == 189);
    for (unsigned n=1; n<=100; ++n) {
        audio_monitor_sample(&a, now+10u+n*1152u, 512, 0);
        if (n>=32)
            assert(a.gate.open && a.duty[2]==128);
    }
}
