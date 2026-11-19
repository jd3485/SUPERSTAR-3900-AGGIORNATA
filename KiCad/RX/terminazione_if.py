"""Carico visto dalla porta IF e perdita riferita alla potenza disponibile su 50 Ω."""
from itertools import product
from math import log10, pi


def risposta(frequenza, induttanza, capacita, utile, assorbente, ingresso):
    jw = 2j * pi * frequenza
    carico = 1 / (1 / utile + ingresso)
    ramo_utile = jw * induttanza + carico
    ramo_assorbente = 1 / (jw * capacita) + assorbente
    zin = 1 / (1 / ramo_utile + 1 / ramo_assorbente)
    tensione = zin / (50 + zin) * carico / ramo_utile
    perdita = -10 * log10(4 * 50 * abs(tensione) ** 2 / utile)
    riflessione = abs((zin - 50) / (zin + 50))
    return perdita, -20 * log10(riflessione)


if __name__ == '__main__':
    frequenza = 10.695e6
    for nome, ingresso in [('alta Z ideale', 0), ('2 kohm || 10 pF', 1/2000 + 2j*pi*frequenza*10e-12)]:
        valori = [risposta(frequenza, 390e-9*l, 160e-12*c, 49.9*a, 49.9*b, ingresso)
                  for l,c,a,b in product((.95,1.05),(.95,1.05),(.99,1.01),(.99,1.01))]
        perdita, ritorno = zip(*valori)
        print(f'{nome}: perdita {min(perdita):.3f}–{max(perdita):.3f} dB, return loss minimo {min(ritorno):.2f} dB')
