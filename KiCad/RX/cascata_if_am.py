"""Cascata Q102/Q103 a centro banda. Tensioni riferite ad AM_IF_TERMINATED."""
from itertools import product
from math import log10, sqrt
from guadagno_if_am import stadio

DISPOSITIVI = tuple(product((80,200),(.60,.75),(100e6,300e6),(2e-12,4e-12)))


def scenari():
    for vcc, dev2, rl, cl in product((4.75,5.25), DISPOSITIVI, (2000,10000), (5e-12,15e-12)):
        _, _, a2, z2 = stadio(vcc,*dev2,rl,cl)
        for dev1 in DISPOSITIVI:
            _, _, a1, z1 = stadio(vcc,*dev1,float('inf'),0,carico_extra=1/z2)
            yield abs(a1*a2), abs(a1), abs(a2), z1


if __name__ == '__main__':
    casi = list(scenari())
    for i, nome in enumerate(('cascata','Q102 caricato','Q103')):
        db = [20*log10(c[i]) for c in casi]
        print(f'{nome}: {min(db):.2f}..{max(db):.2f} dB')
    guadagni = [c[0] for c in casi]
    # Punti esplorativi al collettore: portante in RMS, inviluppo di picco a m=1.
    for ingresso in (1e-6,1e-4,1e-3):
        estremi = [1e3*ingresso*g for g in (min(guadagni),max(guadagni))]
        print(f'{ingresso*1e6:g} uV RMS in: {estremi[0]:.4f}..{estremi[1]:.4f} mV RMS out')
    # Esempio di soglia AGC, non un requisito né il modello di un rivelatore.
    print('Ingresso RMS per 0.1 V di picco inviluppo, modulazione 100%, mV:',
          [round(1e3*.1/(2*sqrt(2)*g),3) for g in (max(guadagni),min(guadagni))])
    print('Guadagno ulteriore per il medesimo esempio con 1 uV RMS in, dB:',
          [round(20*log10(.1/(2*sqrt(2)*g*1e-6)),2) for g in (max(guadagni),min(guadagni))])
