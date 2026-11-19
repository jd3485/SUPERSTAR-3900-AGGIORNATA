"""Studio in banda base dopo conversione I/Q ideale. Nessun convertitore implicito nel CAD."""
from itertools import product
import numpy as np

FS = 16000
ACQUISIZIONE = 512
DURATA = FS//2


def prova(scarto, modulazione, cn_db, seme):
    rng = np.random.default_rng(seme)
    t = np.arange(DURATA)/FS
    fase = 2*np.pi*scarto*t + rng.uniform(-np.pi,np.pi)
    inviluppo = 1 + modulazione*np.cos(2*np.pi*1000*t)
    sigma = 10**(-cn_db/20)/np.sqrt(2)
    iq = inviluppo*np.exp(1j*fase) + sigma*(rng.standard_normal(len(t))+1j*rng.standard_normal(len(t)))
    # Acquisizione della riga più intensa entro ±750 Hz; evita le bande laterali a 1 kHz
    # solo nei casi dove la portante rimane predominante.
    frequenze = np.fft.fftfreq(ACQUISIZIONE,1/FS)
    spettro = np.fft.fft(iq[:ACQUISIZIONE]*np.hanning(ACQUISIZIONE))
    ammessi = np.flatnonzero(abs(frequenze)<=750)
    indice = ammessi[np.argmax(abs(spettro[ammessi]))]
    omega = 2*np.pi*frequenze[indice]/FS
    fase_stimata = np.angle(spettro[indice]) + omega*ACQUISIZIONE
    wn = 2*np.pi*35/FS
    errore = []
    for i in range(ACQUISIZIONE,DURATA):
        errore.append(fase[i]-fase_stimata)
        # Rivelatore in quadratura con guadagno riferito alla portante unitaria.
        residuo = (iq[i]*np.exp(-1j*fase_stimata)).imag
        omega += wn**2*residuo
        fase_stimata += omega+np.sqrt(2)*wn*residuo
    coda = np.array(errore)[-FS//4:]
    giri = np.floor((coda+np.pi)/(2*np.pi))
    rms = np.sqrt(np.mean(np.angle(np.exp(1j*coda))**2))*180/np.pi
    return rms, int(np.count_nonzero(np.diff(giri)))


if __name__ == '__main__':
    for cn in (-18,-12,-6,0,12):
        casi = [prova(df,m,cn,seme) for df,m,seme in
                product((-480,0,480),(.5,1.),range(3))]
        print(f'C/N {cn:+} dB: max RMS {max(c[0] for c in casi):.1f} gradi, '
              f'casi con salti {sum(c[1]>0 for c in casi)}/{len(casi)}')
