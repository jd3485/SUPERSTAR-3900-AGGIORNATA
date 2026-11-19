"""Perdita di inserzione del passa-alto RX, sorgente e carico resistivi da 50 ohm."""
from itertools import product
from math import log10, pi

NOMINALI = (270e-12, 240e-9, 82e-12, 240e-9, 270e-12)


def perdita_db(mhz, valori):
    """Propagazione tensione/corrente dal carico verso il generatore."""
    jw = 2j * pi * mhz * 1e6
    tensione, corrente = 1.0, 1 / 50
    for indice in reversed(range(len(valori))):
        if indice % 2 == 0:
            tensione += corrente / (jw * valori[indice])
        else:
            corrente += tensione / (jw * valori[indice])
    return 20 * log10(abs(tensione + 50 * corrente) / 2)


if __name__ == '__main__':
    vertici = [tuple(v * k for v, k in zip(NOMINALI, fattori))
               for fattori in product((0.95, 1.05), repeat=5)]
    for nome, inizio in [('ricezione', 25.615), ('immagine', 25.615 - 2 * 10.695)]:
        valori = [perdita_db(inizio + i * 0.010, componenti)
                  for i in range(270) for componenti in vertici]
        print(f'{nome}: {min(valori):.3f} … {max(valori):.3f} dB')
