#ifndef RX_IQ_FRAME_H
#define RX_IQ_FRAME_H
#include <stdbool.h>
#include <stdint.h>

struct iq_pair { int16_t i, q; };

enum iq_status { IQ_OK, IQ_NOT_READY, IQ_LATE, IQ_SPI_ERROR, IQ_BAD_NULL };
struct iq_snapshot {
    uint16_t tick;                  /* TMR2, 0..767 */
    bool invalid_slot;              /* overflow timer o cambio clock */
    bool ready_i, ready_q, busy, overrun;
};
struct iq_port {
    struct iq_snapshot (*status)(void);
    void (*select)(bool active);
    void (*launch)(void);
    void (*read)(uint16_t *i, uint16_t *q);
    void (*reset)(void);            /* deseleziona, svuota e riarma entrambe */
};
/* Singolo chiamante, una volta per slot Timer2, flag di periodo già azzerato.
   Il chiamante usa la coppia solo dopo IQ_OK. */
enum iq_status iq_capture(const struct iq_port *port, struct iq_pair *out);
#endif
