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


def terminazione_tcal(l, c, z_ext, srf, esr):
    """Equivalente parallelo visto dal quarzo, a centro banda, con Cp della bobina."""
    cp_l = 1 / ((2*pi*srf)**2 * l)
    z_l = 1 / (1 / (esr + 1j*OMEGA*l) + 1j*OMEGA*cp_l)
    y = 1j*OMEGA*c + 1 / (z_l + z_ext)
    return 1/y.real, y.imag/OMEGA*1e12


if __name__ == '__main__':
    from buffer_am import valuta
    # Esempi con ESR costante estratta dal Q minimo a 7,96 MHz.
    # I parassiti di 1..3 pF rappresentano ipotesi di layout, escluso Ct del filtro.
    driver = [complex(*valuta(*p)[2:4]) for p in product((4.75,5.25), (80,200),
              (.60,.75), (100e6,300e6), (2e-12,5e-12))]
    carichi = [1 / (1/(56.2*r) + y) for r,y in product((.99,1.01),
               (0, 1/2000 + 1j*OMEGA*10e-12))]
    for lato, impedenze in [('FL101 ingresso', driver), ('FL102 uscita', carichi)]:
        casi = []
        for l_rel,c_rel,stray,srf,z in product((.9,1.1),(.95,1.05),(1e-12,3e-12),
                                                (50e6,float('inf')),impedenze):
            l = 4.7e-6*l_rel
            casi.append(terminazione_tcal(l,47e-12*c_rel+stray,z,srf,2*pi*7.96e6*l/45))
        rp,cp = zip(*casi)
        print(f'{lato}: Rp {min(rp):.0f}..{max(rp):.0f} ohm, Cp {min(cp):.2f}..{max(cp):.2f} pF')
