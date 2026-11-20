#ifndef RX_PIC32_IQ_H
#define RX_PIC32_IQ_H
#include "iq_frame.h"
bool pic32_iq_init(void);
enum iq_status pic32_iq_poll(struct iq_pair *out);
#endif
