"""Stadio U117 fra le reti RC e un futuro ADC. Tensioni in V, frequenze in Hz.

Sorgente al nodo AM_I_PRE o AM_Q_PRE a impedenza nulla. Rumore proprio
calcolato esclusivamente a valle di quel punto. Non include rumore 1/f,
alimentazione reale, capacità parassite, nonlinearità o carica del SAR.
"""
from itertools import product
import numpy as np
from filtro_uscita_iq import ladder


def transfer(f):
    s = 2j*np.pi*np.asarray(f)
    r1,r2,c1,c2 = 330,3300,39e-9,3.9e-9
    feedback = 1e6/(1+s*1e6*6.8e-12)
    h_open = ladder(f,r1,r2,c1,c2)
    z_filter = r2 + r1/(1+s*r1*c1)
    z_filter /= 1+s*c2*z_filter
    z_input = 68e3 + z_filter
    gain = -h_open * feedback/z_input
    noise_gain = 1 + feedback/z_input
    return gain, noise_gain, z_input, feedback


def dc(rail, upstream, offset, signs):
    # Coppie di resistori dello stadio allo 0,1%, RC a monte all'1%.
    rin,rf,rt,rb = np.array([68e3,1e6,28.7e3,1e3])*(1+.001*np.array(signs[:4]))
    source = 330*(1+.01*signs[4]) + 3300*(1+.01*signs[5])
    ratio = rf/(rin+source)
    return (1+ratio)*(rail*rb/(rt+rb)+offset) - ratio*upstream


if __name__ == '__main__':
    for f in (0,4000,12000,92000):
        print('Guadagno da PRE a LEVEL [Hz, V/V]:', f, abs(transfer(f)[0]))
    limits = []
    margins = []
    for rail, upstream, off, signs in product((4.71,5.25),(-.0735,.0735),
                                               (-.0005,.0005),product((-1,1),repeat=6)):
        v = dc(rail,upstream,off,signs)
        limits.append(v)
        # Finestra di progetto prudenziale per il carico ancora da scegliere.
        margins.append(min(v-.2,rail-.2-v))
    print('Offset ±73,5 mV a PRE: intervallo LEVEL, margine minimo [V]',
          min(limits), max(limits), min(margins))
    f = np.linspace(0,4000,4001)
    _,ng,zi,zf = transfer(f)
    s = 2j*np.pi*f
    z_bias = 1/(1/28700 + 1/1000 + s*1e-6)
    kt4 = 4*1.380649e-23*290
    psd = kt4*(abs(zf/zi)**2*zi.real + abs(zf)**2/1e6 + abs(ng)**2*z_bias.real)
    psd += abs(ng)**2*(8.7e-9)**2
    white = np.sqrt(np.trapezoid(psd,f))
    print('Rumore bianco proprio in uscita [uV RMS, 0..4 kHz]:',white*1e6)
    print('Segnale debole a bassa frequenza [mV RMS]:',
          np.array([48,199])*1e-3*abs(transfer(0)[0]))
    # Rumore uniforme scorrelato per ADC ideale, senza armoniche né perdita ENOB.
    for bits in (12,14,16):
        lsb = 5/2**bits
        rms = lsb/np.sqrt(12)*np.sqrt(4000/(96000/2))
        print('ADC ideale: bit, LSB [uV], rumore in banda [uV RMS]:',
              bits,lsb*1e6,rms*1e6)
