"""Rete RC non bufferizzata per I e Q. Confronto fra frequenze di campionamento.

Ingresso da U115 a bassa impedenza. Il carico comprende resistenza e capacità
statiche di scenario. Il circuito di acquisizione di un ADC richiede un modello
commutato separato. Il FIR è un confronto numerico dopo acquisizione a 96 kS/s.
"""
from itertools import product

import numpy as np
from scipy.signal import firwin, freqz


def ladder(f, r1, r2, c1, c2, source_r=0, load_r=np.inf, load_c=0):
    s = 2j*np.pi*np.asarray(f)
    z1 = r1 + source_r
    y2 = 1/load_r + s*(c2 + load_c)
    return 1 / ((1 + z1*s*c1)*(1 + r2*y2) + z1*y2)


def db(voltage):
    return 20*np.log10(np.abs(voltage))


if __name__ == '__main__':
    nominal = np.array([330, 3300, 39e-9, 3.9e-9])
    for f in (0, 4000, 12000, 15000, 25000, 35000, 60000, 92000):
        print(f, 'Hz, dB:', round(db(ladder(f, *nominal)), 3))
    # Stessa sorgente e stesso carico sui due canali per il confronto di fase.
    corners = [ladder(4000, *(nominal*(1+np.array(sign)*[.01,.01,.05,.05])))
               for sign in product((-1,1), repeat=4)]
    print('Sbilanciamento I/Q max a 4 kHz [dB, gradi]:',
          np.ptp(db(corners)), np.ptp(np.angle(corners,deg=True)))
    for load in (100e3, 1e6):
        gain = ladder([0,4000], *nominal, source_r=10, load_r=load, load_c=100e-12)
        print('Carico [ohm] e guadagni DC/4 kHz [dB]:', load, db(gain))
    # A 96 kS/s, ogni riga analogica a 92 kHz è già in banda dopo il primo ADC.
    # Il FIR può invece attenuare 12..48 kHz prima della decimazione per sei.
    fs = 96000
    taps = firwin(97, 8000, window=('kaiser',8), fs=fs)
    f, h = freqz(taps, worN=65536, fs=fs, include_nyquist=True)
    print('FIR 96 -> 16 kS/s: ripple 0..4k e picco 12..48k [dB], ritardo [ms]:',
          np.ptp(db(h[f<=4000])), np.max(db(h[f>=12000])), 1000*(len(taps)-1)/(2*fs))
    assert abs(ladder(0,*nominal)-1)<1e-12
    assert np.max(db(h[f>=12000])) < -70
