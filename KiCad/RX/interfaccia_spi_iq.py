"""Verifica J102 e budget di due ricevitori SPI. Eseguire dalla checkout CAD."""
from fractions import Fraction
from pathlib import Path
import xml.etree.ElementTree as ET

from acquisizione_iq import decode


def verifica_j102():
    xml = Path(__file__).resolve().parents[2] / "Verifiche/KiCad/MAIN.xml"
    reti = {}
    for net in ET.parse(xml).findall(".//nets/net"):
        for node in net.findall("node"):
            reti[node.get("ref"), node.get("pin")] = net.get("name")
    for pin, nome, altri in [
        ("1", "/RX_RF_RETURN", [("J102", "4"), ("U118", "4"), ("U119", "4")]),
        ("2", "/Condizionamento IQ/ADC_CS_N", [("U118", "5"), ("U119", "5")]),
        ("3", "/Condizionamento IQ/ADC_CLK", [("U118", "7"), ("U119", "7")]),
        ("5", "/Condizionamento IQ/ADC_DI", [("U118", "6")]),
        ("6", "/Condizionamento IQ/ADC_DQ", [("U119", "6")]),
    ]:
        for pad in [("J102", pin), *altri]:
            if reti.get(pad) != nome:
                raise ValueError(f"{pad}: attesa {nome}, trovata {reti.get(pad)}")


def verifica_coppie():
    # Q percorre tutti i codici in un ordine diverso da I. Prefissi indipendenti.
    for i in range(-4096, 4096):
        q = ((i * 73 + 41) % 8192) - 4096
        for prefix in range(4):
            parole = [prefix << 14 | (i & 8191), (3 - prefix) << 14 | (q & 8191)]
            ricevute = [0, 0]
            for bit in reversed(range(16)):
                for canale, parola in enumerate(parole):
                    ricevute[canale] = 2 * ricevute[canale] + ((parola >> bit) & 1)
            if tuple(map(decode, ricevute)) != (i, q):
                raise ValueError(f"Coppia corrotta: {i}, {q}")


def margini(pbclk, frequenza, brg):
    # Margine conservativo: riservare setup anche prima del primo semiperiodo.
    tick_ns = Fraction(10**9, pbclk)
    frame, resto = divmod(pbclk, frequenza)
    if resto:
        raise ValueError("Il timer non genera un periodo intero")
    mezzo = brg + 1
    def ticks(ns):
        return -(-ns // tick_ns)
    liberi = frame - 32 * mezzo - ticks(100) - ticks(580)
    return (float(liberi * tick_ns), float(mezzo * tick_ns - 275),
            float(mezzo * tick_ns - 125))


if __name__ == "__main__":
    verifica_j102()
    verifica_coppie()
    for frequenza in (48000, 96000):
        frame, impulso, dati = margini(36864000, frequenza, 10)
        print(f"{frequenza} coppie/s: attesa disponibile {frame:.1f} ns, "
              f"eccedenza semiperiodo {impulso:.1f} ns, "
              f"budget dati dopo tDO {dati:.1f} ns")
