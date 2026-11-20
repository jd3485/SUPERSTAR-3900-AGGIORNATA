#include "iq_frame.h"

static enum iq_status abort_frame(const struct iq_port *port, enum iq_status why)
{
    port->reset();
    return why;
}

static int16_t signed_sample(uint16_t word)
{
    int value = word & 0x1fff;
    return (int16_t)((value & 0x1000) ? value - 8192 : value);
}

enum iq_status iq_capture(const struct iq_port *port, struct iq_pair *out)
{
    struct iq_snapshot s = port->status();
    if (s.invalid_slot || s.tick > 64 || s.busy || s.ready_i || s.ready_q || s.overrun)
        return abort_frame(port, IQ_NOT_READY);

    port->select(true);
    s = port->status();
    if (s.invalid_slot || s.tick > 80)
        return abort_frame(port, IQ_LATE);

    /* Minimo 16 tick tra selezione e scrittura SPI. Limite di iterazioni
       indipendente dal timer periferico se questo si arresta. */
    for (unsigned poll = 0; s.tick < 96 && poll < 128; ++poll) {
        s = port->status();
        if (s.invalid_slot)
            return abort_frame(port, IQ_LATE);
    }
    if (s.tick < 96 || s.tick > 144)
        return abort_frame(port, IQ_LATE);

    port->launch();
    for (unsigned poll = 0; poll < 768; ++poll) {
        s = port->status();
        if (s.invalid_slot || s.tick >= 704)
            return abort_frame(port, IQ_LATE);
        if (s.overrun)
            return abort_frame(port, IQ_SPI_ERROR);
        if (!s.ready_i || !s.ready_q || s.busy)
            continue;

        uint16_t i, q;
        port->read(&i, &q);
        port->select(false);
        s = port->status();
        if (s.invalid_slot || s.tick >= 736 || s.overrun || s.ready_i || s.ready_q)
            return abort_frame(port, IQ_SPI_ERROR);
        if ((i | q) & 0x2000)
            return abort_frame(port, IQ_BAD_NULL);
        *out = (struct iq_pair){signed_sample(i), signed_sample(q)};
        return IQ_OK;
    }
    return abort_frame(port, IQ_LATE);
}
