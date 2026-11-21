"""Primo stadio I/Q, modello lineare ideale per la banda base."""
from itertools import product

import numpy as np

FREQ = np.linspace(0, 4000, 4001)


def transfers(frequency, source, series, shunt, feedback, ground, bypass):
    s = 2j * np.pi * frequency
    zf = feedback / (1 + s * feedback * bypass)
    noise_gain = 1 + zf / ground
    input_filter = 1 / (1 + s * (series + source) * shunt)
    return noise_gain * input_filter, noise_gain, zf


if __name__ == '__main__':
    # Il mixer mantiene R147/R148. Resistenza di sorgente equivalente di scenario 25 ohm.
    source = 25
    gain, ng, zf = transfers(FREQ, source, 100, 4.7e-9, 2000, 100, 10e-9)
    thermal = 4 * 1.380649e-23 * 290
    # Sorgente resistiva e rumore bianco OEM tipico, esclusi flicker e rumore del mixer pompato.
    psd = (abs(gain)**2 * thermal * (source + 100)
           + abs(ng)**2 * (8e-9)**2
           + thermal * abs(zf)**2 * (1 / 100 + 1 / 2000))
    rms = np.sqrt(np.trapezoid(psd, FREQ))
    print('Guadagno DC e a 4 kHz, fase a 4 kHz, rumore RMS uscita [uV]')
    print(abs(gain[0]), abs(gain[-1]), np.angle(gain[-1], deg=True), rms * 1e6)
    values = []
    for signs in product((-1, 1), repeat=5):
        nominal = np.array([100, 4.7e-9, 2000, 100, 10e-9])
        tolerances = np.array([.01, .05, .01, .01, .05])
        h, _, _ = transfers(4000, source, *(nominal * (1 + tolerances * signs)))
        values.append(h)
    amps = np.abs(values)
    angles = np.angle(values, deg=True)
    print('Differenza massima I/Q ai vertici a 4 kHz [dB, gradi]')
    print(20*np.log10(amps.max()/amps.min()), np.ptp(angles))
