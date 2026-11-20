/* Immagine RX candidata. Runtime C e vettore di reset forniti da XC32. */
#include <xc.h>
#include "pic32_iq.h"
#include "am_sync.h"

#pragma config FNOSC = PRIPLL, POSCMOD = XT, FPLLIDIV = DIV_2
#pragma config FPLLMUL = MUL_16, FPLLODIV = DIV_2, FPBDIV = DIV_1
#pragma config FSOSCEN = OFF, IESO = OFF, FCKSM = CSECME
#pragma config UPLLEN = OFF, FUSBIDIO = OFF, FVBUSONIO = OFF
#pragma config JTAGEN = OFF, ICESEL = ICS_PGx1, IOL1WAY = ON
#pragma config FWDTEN = OFF

/* Diagnostica al debugger. Una sola scrittura allineata pubblica entrambi
   i campioni; il consumatore DSP dovrà acquisire ogni coppia in tempo. */
volatile uint32_t rx_last_pair;
volatile uint32_t rx_valid_pairs;
volatile uint32_t rx_rejected_frames;
volatile bool rx_initialized;
volatile int32_t rx_am_audio_q7;
volatile bool rx_am_audio_valid;

int main(void)
{
    /* Offset iniziali neutri, da misurare a ingresso RF terminato. */
    const struct iq_pair offset = {0, 0};
    struct am_sync am;
    am_sync_reset(&am, offset);
    rx_initialized = pic32_iq_init();
    if (!rx_initialized)
        for (;;) { }

    for (;;) {
        struct iq_pair pair;
        enum iq_status result = pic32_iq_poll(&pair);
        if (result == IQ_OK) {
            uint32_t stamp = _CP0_GET_COUNT();
            int32_t audio;
            rx_last_pair = ((uint32_t)(uint16_t)pair.i << 16) | (uint16_t)pair.q;
            ++rx_valid_pairs;
            if (am_sync_sample(&am, pair, stamp, &audio)) {
                rx_am_audio_q7 = audio;
                rx_am_audio_valid = true;
            } else {
                rx_am_audio_valid = false;
            }
        } else if (result != IQ_IDLE) {
            ++rx_rejected_frames;
            am_sync_reset(&am, offset);
            rx_am_audio_valid = false;
        }
    }
}
