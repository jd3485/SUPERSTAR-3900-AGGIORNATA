#include "../../Firmware/RX/audio_gate.h"
#include "../../Firmware/RX/am_sync.h"
#include "../../Firmware/RX/audio_decim.h"
#include <assert.h>
#include <math.h>
#include <stdio.h>

int main(void)
{
    struct am_sync am;
    struct audio_decim d;
    struct audio_gate gate = {0};
    am_sync_reset(&am, (struct iq_pair){0,0});
    audio_decim_reset(&d);
    uint32_t seed = 851;
    unsigned opens = 0, closes = 0, open_n = 0, close_n = 0;
    uint16_t duty[3];
    for (unsigned n = 0; n < 96000; ++n) {
        double t = n / 48000.;
        double envelope = n >= 24000 && n < 72000 ? 4*(1+.6*sin(6283.185307*t)) : 0;
        double phi = 2*3.141592653589793*180*t;
        seed = 1664525u*seed + 1013904223u;
        double ni = sqrt(12.)*((seed >> 8)/16777216.-.5);
        seed = 1664525u*seed + 1013904223u;
        double nq = sqrt(12.)*((seed >> 8)/16777216.-.5);
        struct iq_pair pair = {(int16_t)lround(envelope*cos(phi)+ni),
                               (int16_t)lround(envelope*sin(phi)+nq)};
        int32_t audio, filtered;
        if (!am_sync_sample(&am, pair, n*384u, &audio)) {
            audio_decim_reset(&d);
            continue;
        }
        if (!audio_decim_sample(&d, audio, &filtered))
            continue;
        bool previous = gate.open;
        audio_gate_step(&gate, true, am.dc_q10/1024, 384, 256, filtered, duty);
        if (gate.open && !previous) { ++opens; open_n = n; }
        if (!gate.open && previous) { ++closes; close_n = n; }
        if (n < 24000 || n > 80000)
            assert(!gate.open && duty[0]==128 && duty[1]==128 && duty[2]==128);
    }
    assert(opens == 1 && closes == 1 && open_n >= 24000 && close_n >= 72000);
    printf("Portante debole: apertura %.2f ms, chiusura %.2f ms\n",
           (open_n-24000)/48., (close_n-72000)/48.);
    for (unsigned n=0; n<128; ++n)
        audio_gate_step(&gate,true,512,384,256,10000,duty);
    assert(gate.open);
    int last = duty[2];
    for (unsigned n=0; n<64; ++n) {
        audio_gate_step(&gate,false,512,384,256,INT32_MIN,duty);
        for (unsigned p=0; p<3; ++p) {
            int expected = last + (last<128) - (last>128);
            assert(duty[p]==expected);
            last = expected;
        }
    }
    assert(last == 128);
    for (unsigned n=0; n<80; ++n) {
        audio_gate_step(&gate,true,512,384,256,0,duty);
        assert(duty[0]==128 && duty[1]==128 && duty[2]==128);
    }
    assert(gate.open);
    for (unsigned n=0; n<127; ++n) {
        audio_gate_step(&gate,true,256,384,256,0,duty);
        assert(gate.open);
    }
    audio_gate_step(&gate,true,320,384,256,0,duty);
    assert(gate.open && gate.dwell == 0);
    audio_gate_step(&gate,true,512,256,256,0,duty);
    assert(!gate.open);
    for (unsigned n=0; n<31; ++n) {
        audio_gate_step(&gate,true,384,384,256,0,duty);
        assert(!gate.open);
    }
    audio_gate_step(&gate,true,320,384,256,0,duty);
    assert(!gate.open && gate.dwell == 0);
}
