"""Ibrido a quattro porte a 10,695 MHz. Ordine: ingresso, I, Q, isolamento."""
from itertools import product

import numpy as np

OMEGA = 2 * np.pi * 10.695e6
ZREF = 50.0
INDUCTANCE = np.array([560, 820, 560, 820]) * 1e-9


def response(inductance, capacitance, quality, termination):
    # Carichi I/Q e impedenza interna del generatore ideali, tutti da 50 ohm.
    y = np.diag(1j * OMEGA * capacitance)
    for start, value in enumerate(inductance):
        end = (start + 1) % 4
        arm = 1 / (OMEGA * value * (1j + 1 / quality))
        y[start, start] += arm
        y[end, end] += arm
        y[start, end] -= arm
        y[end, start] -= arm
    y += np.diag([1 / ZREF] * 3 + [1 / termination])
    v = np.linalg.solve(y, [2 / ZREF, 0, 0, 0])
    loss = -20 * np.log10(abs(v[1:3]))
    return [*loss, np.angle(v[2] / v[1], deg=True),
            -20 * np.log10(abs(v[0] - 1)), max(loss) + 7]


def main():
    print('Perdita I/Q [dB], fase Q/I [gradi], return loss [dB], ingresso per +7 dBm sul ramo debole [dBm]')
    print('Nominale', np.round(response(INDUCTANCE, np.full(4, 680e-12), 45, 49.9), 2))
    corners = []
    for signs in product([-1, 1], repeat=10):
        l = INDUCTANCE * (1 + 0.10 * np.array(signs[:4]))
        c = 680e-12 * (1 + 0.02 * np.array(signs[4:8]))
        q = 45 + 15 * signs[8]
        corners.append(response(l, c, q, 49.9 * (1 + 0.01 * signs[9])))
    print('Minimi ai vertici', np.round(np.min(corners, axis=0), 2))
    print('Massimi ai vertici', np.round(np.max(corners, axis=0), 2))


if __name__ == '__main__':
    main()
