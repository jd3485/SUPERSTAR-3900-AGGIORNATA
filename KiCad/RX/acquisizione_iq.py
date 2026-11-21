"""Coppia MCP3301 con SCK e CS comuni, DOUT separati. Calcoli di scenario."""
from itertools import product
from math import sqrt, log10

import numpy as np
from scipy.linalg import expm


def decode(word):
    """Frame SPI a 16 clock, due bit iniziali indeterminati, null e 13 bit dati."""
    value = word & 0x1fff
    return value - 8192 if value & 4096 else value


def residual(driver_r, switch_r, sample_c, local_c, aperture):
    # Pin già al valore del segnale, capacità del SAR a distanza iniziale di 5 V.
    # Sorgente di Thévenin costante durante l'acquisizione. Resteranno da
    # verificare l'uscita reale di U117 e il movimento del segnale in apertura.
    series = 47 + driver_r
    matrix = np.array([[(-1/series-1/switch_r)/local_c, 1/(switch_r*local_c)],
                       [1/(switch_r*sample_c), -1/(switch_r*sample_c)]])
    return abs((expm(matrix*aperture) @ [0., 5.])[1])


if __name__ == '__main__':
    lsb = 2.5/4096
    for sampling, clock in [(96000,1.68e6),(48000,.84e6)]:
        # Dati a 5 V: setup CS 100 ns, CS alto minimo 580 ns. Usare il
        # corrispondente limite di clock per la reale alimentazione e temperatura.
        available = 1/sampling - 16/clock - 100e-9 - 580e-9
        aperture = 1.5/clock
        cases = list(product((5.,50.,200.),(800.,1200.),(20e-12,35e-12),
                             (.95*220e-12,1.05*220e-12)))
        errors = [residual(*c,aperture)/lsb for c in cases]
        print('Fs, margine frame [ns], acquisizione [us], errore massimo [LSB]:',
              sampling, available*1e9, aperture*1e6, max(errors))
        print('Rumore quantizzazione bianco ideale 0..4 kHz [uV RMS]:',
              lsb/sqrt(12)*sqrt(4000/(sampling/2))*1e6)
    for driver_r in (5.,50.,200.):
        print('R driver, errore [LSB] con 1 kohm, 25 pF, 220 pF a 96 kS/s:',
              driver_r, residual(driver_r,1000,25e-12,220e-12,1.5/1.68e6)/lsb)
    # Margine preliminare rispetto ai limiti di codice e alle due sorgenti.
    limits = [(v - ref)/ref*4096 for v,ref in product((1.331,3.692),(2.475,2.525))]
    print('Codici DC ai vertici:', min(limits), max(limits))
    print('Segnale debole [LSB RMS]:', .670e-3/lsb, 2.778e-3/lsb)
    q_rms = lsb/sqrt(12)*sqrt(4000/48000)
    print('Incremento sopra il solo rumore proprio U117 [dB]:',
          10*log10(1+(q_rms/31.93e-6)**2))
    for code in range(-4096,4096):
        for prefix in range(4):
            assert decode(prefix << 14 | (code & 8191)) == code
