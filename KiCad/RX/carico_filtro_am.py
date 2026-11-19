"""Ammettenza vista dal terminale marcato di FL102 a centro banda."""
from itertools import product
from math import pi

OMEGA = 2 * pi * 10.695e6


def carico(l, c, r, q, ingresso):
    z_uscita = 1 / (1 / r + ingresso)
    z_bobina = OMEGA * l / q + 1j * OMEGA * l
    y = 1j * OMEGA * c + 1 / (z_bobina + z_uscita)
    return 1 / y.real, y.imag / OMEGA * 1e12


if __name__ == '__main__':
    for scenario, q, ingresso in [('ideale', float('inf'), 0),
                                  ('sensibilità Q=60 e 2k || 10pF', 60, 1/2000 + 1j*OMEGA*10e-12)]:
        nominale = carico(4.4e-6, 54e-12, 49.9, q, ingresso)
        vertici = [carico(4.4e-6*l, 54e-12*c, 49.9*r, q, ingresso)
                   for l,c,r in product((.95,1.05),(.95,1.05),(.99,1.01))]
        rp, cp = zip(*vertici)
        print(scenario, 'nominale:', nominale, 'Rp:', min(rp), max(rp), 'Cp (pF):', min(cp), max(cp))
