"""Selezione a centro banda di R117/C125 e R112/C126. Nessun modello interno del filtro."""
from itertools import product
from math import pi
from buffer_am import valuta
from carico_filtro_am import terminazione_tcal

# Valori E24 candidati; ogni componente selezionato è assunto misurato.
RESISTENZE = (22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82)
CAPACITA_PF = (3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2,
               9.1, 10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30)


def seleziona(l, srf, c_fissa, impedenza):
    esr = 2*pi*7.96e6*l/45
    # La capacità parallela non modifica la conduttanza del modello.
    prove = []
    for r in RESISTENZE:
        rp, cp = terminazione_tcal(l, c_fissa, impedenza(r), srf, esr)
        prove.append((abs(1/rp - 1/1800), r, rp, cp))
    _, r, rp, cp = min(prove)
    c = min(CAPACITA_PF, key=lambda valore: abs(cp + valore - 5))
    return r, c, rp, cp + c


if __name__ == '__main__':
    def sorgente(z):
        return lambda r: z - 39 + r

    def carico(y):
        return lambda r: 1 / (1/r + y)

    driver = [sorgente(complex(*valuta(*p)[2:4])) for p in
              product((4.75,5.25), (80,200), (.60,.75), (100e6,300e6), (2e-12,5e-12))]
    from carico_filtro_am import OMEGA
    for porta, modelli in [('ingresso', driver), ('uscita', [carico(0), carico(1/2000+1j*OMEGA*10e-12)])]:
        casi = [seleziona(4.7e-6*k, srf, 33e-12*t + par, z)
                for k,srf,t,par,z in product((.9,1,1.1),(50e6,float('inf')),
                       (.95,1,1.05),(1e-12,2e-12,3e-12),modelli)]
        print(porta, [(round(min(v),2),round(max(v),2)) for v in zip(*casi)])
