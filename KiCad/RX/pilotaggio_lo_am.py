"""Sorgente Thevenin 50 ohm, filtro LO e ibrido MAIN, carichi I/Q resistivi."""
from itertools import product, islice

import numpy as np


def mixer_losses(signs, harmonic=1):
    w = 2 * np.pi * 10.695e6 * harmonic
    n = len(signs)
    y = np.zeros((n, 6, 6), complex)
    # Nodi 0..3: anello ingresso/I/Q/isolato. Nodi 4 e 5: C141 e C142.
    q = 45 + 15 * signs[:, 8]

    def series(a, b, impedance):
        conductance = 1 / impedance
        y[:, a, a] += conductance
        y[:, b, b] += conductance
        y[:, a, b] -= conductance
        y[:, b, a] -= conductance

    def coil(nominal, index):
        return w * nominal * (1 + .1 * signs[:, index]) * (1j + 1 / q)

    for i, l in enumerate([560e-9, 820e-9, 560e-9, 820e-9]):
        series(i, (i + 1) % 4, coil(l, i))
        y[:, i, i] += 1j * w * 680e-12 * (1 + .02 * signs[:, 4+i])
    y[:, 1, 1] += 1 / 50
    y[:, 2, 2] += 1 / 50
    y[:, 3, 3] += 1 / (49.9 * (1 + .01 * signs[:, 9]))
    for node, index in [(4, 13), (5, 14)]:
        y[:, node, node] += 1j * w * 330e-12 * (1 + .02 * signs[:, index])
    series(4, 5, coil(1e-6, 11))
    series(5, 0, coil(330e-9, 12))
    block = 1 / (1j * w * 10e-9 * (1 + .05 * signs[:, 15]))
    source_y = 1 / (50 + block + coil(330e-9, 10))
    y[:, 4, 4] += source_y
    current = np.zeros((n, 6, 1), complex)
    current[:, 4, 0] = 2 * source_y  # 1 V RMS di riferimento su carico adattato.
    voltage = np.linalg.solve(y, current)[:, 1:3, 0]
    return -20 * np.log10(abs(voltage))


def main():
    nominal = np.zeros((1, 16))
    loss = mixer_losses(nominal)[0]
    print('Perdita nominale I/Q [dB]', loss.round(2))
    for harmonic in [3, 5]:
        ratio_db = -20*np.log10(harmonic) + loss - mixer_losses(nominal, harmonic)[0]
        print('Armonica ideale onda quadra', harmonic, '[dBc]', ratio_db.round(1))
    cases = product([-1, 1], repeat=16)
    bounds = []
    while batch := list(islice(cases, 512)):
        losses = mixer_losses(np.asarray(batch))
        bounds.append([losses.min(), losses.max()])
    low, high = np.min(bounds, axis=0)[0], np.max(bounds, axis=0)[1]
    power = 7 + (low + high) / 2
    vpp = 4 * np.sqrt(2 * 50 * 1e-3 * 10**(power/10))
    print('Perdite ai vertici [dB]', round(low, 2), round(high, 2))
    print('Compromesso fisso [dBm], tensione sinusoidale a vuoto [Vpp]', round(power, 2), round(vpp, 2))
    print('Potenza ai mixer ai vertici [dBm]', round(power-high, 2), round(power-low, 2))


if __name__ == '__main__':
    main()
