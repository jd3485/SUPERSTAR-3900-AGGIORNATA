"""Modello logico del sequenziatore RX I/Q (non firmware PIC32).
Avvio solo con periferiche armate, CS alto in idle, SCK basso; coppia atomica.
I tempi sono tick PBCLK nominali: 36_864_000 Hz, PR2=767, SPI1BRG=15.
Non sostituisce la misura di latenza ISR, DMA o clock sui pin reali.
"""
from dataclasses import dataclass

PBCLK = 36_864_000
PERIOD_TICKS = 768
HALF_SCK_TICKS = 16
BITS = 16
FRAME_TICKS = 2 * BITS * HALF_SCK_TICKS
GUARD_TICKS = PERIOD_TICKS - FRAME_TICKS


@dataclass(frozen=True)
class Result:
    valid: bool
    i: int | None
    q: int | None
    cause: str


def receive(i_word, q_word, *, bits_i=16, bits_q=16,
            edges=32, peripheral_ready=True, clock_ok=True,
            cs_stable=True, overrun=False):
    """Modello fail-closed: ogni anomalia osservabile scarta ENTRAMBI i canali.

    L'errore di valore o lo slittamento di un bit NON e' osservabile
    senza ridondanza/protocollo aggiuntivo, e non viene dichiarato rilevato.
    """
    if not peripheral_ready:
        return Result(False, None, None, "not_armed")
    if not clock_ok or edges != 32:
        return Result(False, None, None, "clock_or_edge_count")
    if not cs_stable:
        return Result(False, None, None, "cs_glitch")
    if overrun or bits_i != BITS or bits_q != BITS:
        return Result(False, None, None, "fifo_or_word_count")
    if not 0 <= i_word < (1 << BITS) or not 0 <= q_word < (1 << BITS):
        return Result(False, None, None, "word_range")
    return Result(True, i_word, q_word, "ok")


def test():
    assert PBCLK // PERIOD_TICKS == 48_000
    assert PBCLK // (2 * HALF_SCK_TICKS) == 1_152_000
    assert FRAME_TICKS == 512 and GUARD_TICKS == 256
    assert GUARD_TICKS * 1_000_000 / PBCLK > 6.9

    good = receive(0x5555, 0xA5A5)
    assert good.valid and (good.i, good.q) == (0x5555, 0xA5A5)

    faults = 0
    for edge in range(32):
        # Clock incompleto: entrambe le parole devono essere scartate.
        bad = receive(0x5555, 0xA5A5, edges=edge)
        assert not bad.valid and bad.i is None and bad.q is None
        faults += 1
    for count in range(16):
        for kw in ({"bits_i": count}, {"bits_q": count}):
            bad = receive(0x5555, 0xA5A5, **kw)
            assert not bad.valid and bad.i is None and bad.q is None
            faults += 1
    for kw in ({"peripheral_ready": False}, {"clock_ok": False},
               {"cs_stable": False}, {"overrun": True}):
        assert not receive(0x5555, 0xA5A5, **kw).valid
        faults += 1
    # Una coppia completa successiva non deve riutilizzare dati scartati.
    assert receive(0x1234, 0x5678).valid
    print(f"Clock: {PBCLK} Hz; frame {FRAME_TICKS} tick; guard {GUARD_TICKS} tick")
    print(f"Injection: {faults} casi osservabili scartati; recovery logico OK")
    print("APERTI: ISR/PPS/SPI/DMA; CS/clock ai pin; clock-loss; bit-slip non osservabile")


if __name__ == "__main__":
    test()
