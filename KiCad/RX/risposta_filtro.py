"""Perdita di inserzione del passa-alto RX, sorgente e carico resistivi da 50 ohm."""
from itertools import product
from math import log10, pi

NOMINALI = (270e-12, 240e-9, 82e-12, 240e-9, 270e-12)


def perdita_db(mhz, valori, bobina_reale=False, q=70, test_mhz=25, srf_mhz=440):
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
                # Scenario a ESR costante, ricavata dal Q alla frequenza di prova.
                esr = 2 * pi * test_mhz * 1e6 * induttanza / q
                cp = 1 / ((2 * pi * srf_mhz * 1e6) ** 2 * induttanza)
                ammettenza = 1 / (esr + jw * induttanza) + jw * cp
            corrente += tensione * ammettenza
    return 20 * log10(abs(tensione + 50 * corrente) / 2)


if __name__ == '__main__':
    # Profilo: valore nominale, tolleranza L, Q, frequenza di prova e SRF (MHz).
    profili = [
        ('ideale', 240e-9, .05, None, 25, 440),
        ('132-13L', 246e-9, .05, 70, 25, 440),
        ('TCAL0307-R22M', 220e-9, .20, 30, 25.2, 380),
        ('TCAL0307-R27M', 270e-9, .20, 30, 25.2, 360),
    ]
    for modello, bobina, tol_l, q, test_mhz, srf_mhz in profili:
        nominali = (NOMINALI[0], bobina, NOMINALI[2], bobina, NOMINALI[4])
        tolleranze = (.05, tol_l, .05, tol_l, .05)
        vertici = [tuple(v * (1 + segno * t) for v, segno, t in zip(nominali, segni, tolleranze))
                   for segni in product((-1, 1), repeat=5)]
        for banda, inizio in [('ricezione', 25.615), ('immagine', 25.615 - 2 * 10.695)]:
            perdite = [perdita_db(inizio + i * .010, valori, q is not None, q, test_mhz, srf_mhz)
                       for i in range(270) for valori in vertici]
            print(f'{modello} {banda}: {min(perdite):.3f} … {max(perdite):.3f} dB')
