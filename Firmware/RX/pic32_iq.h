#ifndef RX_PIC32_IQ_H
#define RX_PIC32_IQ_H
#include "iq_frame.h"
#ifdef RX_SPI_OVERLAP
void rx_process_pending(void);
#endif
#ifdef RX_AUDIO_OC1
uint16_t rx_audio_slot(uint32_t now);
#endif
bool pic32_iq_init(void);
enum iq_status pic32_iq_poll(struct iq_pair *out);
#endif
