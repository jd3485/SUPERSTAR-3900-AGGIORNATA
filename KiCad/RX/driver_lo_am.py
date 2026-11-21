"""Stima fondamentale del driver a fronti trapezoidali e carico nominale I/Q."""
from itertools import product

import numpy as np

from pilotaggio_lo_am import mixer_losses

FREQ = 10.695e6


def levels(vdd, rout, duty, edge):
    # Rout simmetrica, duty misurato ai punti medi, edge da 0 a 100%.
    series = rout + 60.4
    shunt = 196
    rth = series * shunt / (series + shunt)
    vpk = 2 * vdd / np.pi * np.sin(np.pi * duty) * np.sinc(FREQ * edge)
    voc_rms = vpk * shunt / (series + shunt) / np.sqrt(2)
    # mixer_losses usa 2 V RMS a vuoto, restituisce -20 log10(Vmix / 1 V).
    losses = mixer_losses(np.zeros((1, 16)), source_resistance=rth)[0]
    powers = 10 * np.log10((voc_rms / 2)**2 / 50 / .001) - losses
    return [rth, 2*np.sqrt(2)*voc_rms, *powers]


if __name__ == '__main__':
    print('Rth [ohm], Vpp fondamentale a vuoto, P I/Q [dBm]')
    print('Nominale ipotizzato', np.round(levels(5, 7, .5, 8e-9), 2))
    rows = [levels(*args) for args in product((4.75, 5.25), (4, 15),
                                              (.45, .50, .55), (4e-9, 20e-9))]
    print('Scenari min/max, filtro e ibrido nominali')
    print(np.round(np.min(rows, axis=0), 2), np.round(np.max(rows, axis=0), 2))
