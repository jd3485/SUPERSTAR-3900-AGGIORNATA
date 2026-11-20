"""Verifica J102 e budget di due ricevitori SPI. Eseguire dalla checkout CAD."""
from fractions import Fraction
from pathlib import Path
import xml.etree.ElementTree as ET

from acquisizione_iq import decode


def verifica_interfaccia():
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


    # Connettore lato MCU, alimentato dalla stessa rail del ricevitore.
    percorso = {
        "MCU_3V3": ("J103.4", "U121.1", "U121.20", "C176.1"),
        "MCU_DI": ("J103.5", "U121.18"),
        "MCU_DQ": ("J103.6", "U121.17"),
        "ADC_DI": ("U118.6", "U121.2", "R184.1"),
        "ADC_DQ": ("U119.6", "U121.3", "R185.1"),
        "IQ_SELECT": ("J103.2", "U122.1", "U122.2", "U122.5", "R186.1"),
        "MCU_SCK": ("J103.3", "U122.4", "R187.1"),
        "CLK_N_INT": ("U122.6", "U122.9", "U122.10"),
        "ADC_CLK": ("U122.8", "U118.7", "U119.7"),
        "ADC_CS_N": ("U122.3", "U118.5", "U119.5"),
        "ADC_VDD": ("U122.14", "C177.1"),
        "/RX_RF_RETURN": ("J103.1", "U121.19", "U121.10", "U122.7", "U122.12",
                          "U122.13", "C176.2", "C177.2", "R184.2", "R185.2",
                          "R186.2", "R187.2", *(f"U121.{n}" for n in range(4, 10))),
    }
    for nome, terminali in percorso.items():
        rete = nome if nome.startswith("/") else "/Condizionamento IQ/" + nome
        for terminale in terminali:
            if reti.get(tuple(terminale.split("."))) != rete:
                raise ValueError(f"{terminale}: attesa {rete}")


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
    verifica_interfaccia()
    verifica_coppie()
    for frequenza in (48000, 96000):
        frame, impulso, dati = margini(36864000, frequenza, 10)
        print(f"{frequenza} coppie/s: attesa disponibile {frame:.1f} ns, "
              f"eccedenza semiperiodo {impulso:.1f} ns, "
              f"budget dati dopo tDO {dati:.1f} ns")

    # 48 kHz con BRG=15: più margine sui fronti dopo U122.
    frame, impulso, dati = margini(36864000, 48000, 15)
    # Fino a 9 ns per NAND a 50 pF, 6,3 ns per il 245 a 3,3 V ±0,3
    # e fino a 85 °C. Due porte sul clock, una su CS. Riservare altri
    # 18 ns sul budget di CS alto e 9 ns sul setup in modo conservativo.
    print("48 kHz con traslatori: budget [ns] per trama, semiperiodo e dati",
          round(frame - 27, 1), round(impulso - 18, 1), round(dati - 18 - 6.3, 1))
