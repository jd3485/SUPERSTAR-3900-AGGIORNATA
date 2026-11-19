"""Scenari RX riferiti all'antenna, potenze disponibili e temperatura di 290 K."""
from math import log10, sqrt

K_B = 1.380649e-23


def fattore_cascata(stadi):
    guadagno = 1.0
    fattore = 1.0
    for guadagno_db, nf_db in stadi:
        fattore += (10 ** (nf_db / 10) - 1) / guadagno
        guadagno *= 10 ** (guadagno_db / 10)
    return fattore


def scenario(guadagno_rf, perdita_filtro, nf_if):
    # Perdite a 290 K; NF del mixer assunta uguale alla perdita di conversione.
    stadi = [(-0.5, 0.5), (-perdita_filtro, perdita_filtro)]
    if guadagno_rf:
        stadi.append((guadagno_rf, 2.0))
    stadi.extend([(-5.6, 5.6), (-1.1, 1.1), (0, nf_if)])
    return 10 * log10(fattore_cascata(stadi))


def soglia_rms_uv(nf_db, banda_hz, snr_db):
    potenza = K_B * 290 * banda_hz * 10 ** ((nf_db + snr_db) / 10)
    return 1e6 * sqrt(potenza * 50)


if __name__ == '__main__':
    for guadagno in (0, 6, 10, 12, 15):
        nf = scenario(guadagno, 0.894, 6)
        estremi = [scenario(guadagno, perdita, nf_if)
                   for perdita in (0.193, 0.894) for nf_if in (3, 9)]
        print(f'G={guadagno:2d} dB: NF={nf:.2f} dB; '
              f'scenari {min(estremi):.2f}–{max(estremi):.2f} dB; '
              f'soglia RF {soglia_rms_uv(nf, 2400, 10):.3f} µV RMS')
