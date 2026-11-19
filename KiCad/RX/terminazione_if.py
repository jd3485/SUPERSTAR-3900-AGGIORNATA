"""Carico visto dalla porta IF e perdita riferita alla potenza disponibile su 50 Ω."""
from itertools import product
from math import log10, pi


def risposta(frequenza, induttanza, capacita, utile, assorbente, ingresso,
             *, resistenza_ac=0.0, capacita_parassita=0.0):
    jw = 2j * pi * frequenza
    carico = 1 / (1 / utile + ingresso)
    z_avvolgimento = resistenza_ac + jw * induttanza
    z_bobina = z_avvolgimento / (1 + jw * capacita_parassita * z_avvolgimento)
    ramo_utile = z_bobina + carico
    ramo_assorbente = 1 / (jw * capacita) + assorbente
    zin = 1 / (1 / ramo_utile + 1 / ramo_assorbente)
    tensione = zin / (50 + zin) * carico / ramo_utile
    perdita = -10 * log10(4 * 50 * abs(tensione) ** 2 / utile)
    riflessione = abs((zin - 50) / (zin + 50))
    return perdita, -20 * log10(riflessione)


if __name__ == '__main__':
    frequenza = 10.695e6
    for nome, ingresso in [('alta Z ideale', 0), ('2 kohm || 10 pF', 1/2000 + 2j*pi*frequenza*10e-12)]:
        # L103 candidato SMCC-R39K-02, ±10%. Q alla IF è uno scenario.
        valori = []
        for l, c, a, b, q, parassita in product(
                (0.90, 1.10), (0.95, 1.05), (0.99, 1.01), (0.99, 1.01),
                (10, 25, 45), (False, True)):
            induttanza = 390e-9 * l
            r_ac = 2*pi*frequenza*induttanza/q
            # Modello concentrato al limite SRF di catalogo, distinto dal PCB.
            c_p = 1 / ((2*pi*230e6)**2 * induttanza) if parassita else 0.0
            valori.append(risposta(frequenza, induttanza, 160e-12*c, 49.9*a,
                                   49.9*b, ingresso, resistenza_ac=r_ac,
                                   capacita_parassita=c_p))
        perdita, ritorno = zip(*valori)
        print(f'{nome}: perdita {min(perdita):.3f}–{max(perdita):.3f} dB, return loss minimo {min(ritorno):.2f} dB')
