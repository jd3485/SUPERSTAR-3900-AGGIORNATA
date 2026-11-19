"""Perdita di inserzione del passa-alto RX, sorgente e carico resistivi da 50 ohm."""
from itertools import product
from math import log10, pi

NOMINALI = (270e-12, 240e-9, 82e-12, 240e-9, 270e-12)


def perdita_db(mhz, valori, bobina_reale=False):
    """Propagazione tensione/corrente dal carico verso il generatore."""
    jw = 2j * pi * mhz * 1e6
    tensione, corrente = 1.0, 1 / 50
    for indice in reversed(range(len(valori))):
        if indice % 2 == 0:
            tensione += corrente / (jw * valori[indice])
        else:
            induttanza = valori[indice]
            ammettenza = 1 / (jw * induttanza)
            if bobina_reale:
                # Scenario a ESR costante, ricavata dal Q a 25 MHz.
                esr = 2 * pi * 25e6 * induttanza / 70
                cp = 1 / ((2 * pi * 440e6) ** 2 * induttanza)
                ammettenza = 1 / (esr + jw * induttanza) + jw * cp
            corrente += tensione * ammettenza
    return 20 * log10(abs(tensione + 50 * corrente) / 2)


if __name__ == '__main__':
    for modello, bobina, reale in [('ideale', 240e-9, False), ('132-13L', 246e-9, True)]:
        nominali = (NOMINALI[0], bobina, NOMINALI[2], bobina, NOMINALI[4])
        vertici = [tuple(v * k for v, k in zip(nominali, fattori))
                   for fattori in product((0.95, 1.05), repeat=5)]
        for banda, inizio in [('ricezione', 25.615), ('immagine', 25.615 - 2 * 10.695)]:
            perdite = [perdita_db(inizio + i * 0.010, valori, reale)
                       for i in range(270) for valori in vertici]
            print(f'{modello} {banda}: {min(perdite):.3f} … {max(perdite):.3f} dB')
