"""Sensibilità al carico dei due mixer. Conversione a basso IF: ipotesi da misurare."""
from itertools import product
from math import sqrt
from guadagno_if_am import stadio, W
from separatore_if_am import separatore

def scenari():
    for v,b3,vb3,b4,vb4,ft4,cm4,is_d in product((4.75,5.25),(80,200),(.60,.75),
            (80,200),(.60,.75),(100e6,300e6),(2e-12,4e-12),(1e-8,1e-7)):
        ie3,vce3,*_ = stadio(v,b3,vb3,200e6,3e-12,float('inf'),0)
        # Porte RF pompate nominali a 50 ohm; la resistenza di ciascun ramo è 49,9 ohm.
        zp = (49.9+50)/2
        zin = zp+1/(1j*W*10e-9)
        ie4,_,av4,z4 = separatore(v,ie3,vce3,b4,vb4,ft4,cm4,is_d,y_extra=1/zin)
        for ft3,cm3,ft2,cm2,b2,vb2 in product((100e6,300e6),(2e-12,4e-12),
                (100e6,300e6),(2e-12,4e-12),(80,200),(.60,.75)):
            _,_,av3,z3 = stadio(v,b3,vb3,ft3,cm3,float('inf'),0,carico_extra=1/z4)
            _,_,av2,_ = stadio(v,b2,vb2,ft2,cm2,float('inf'),0,carico_extra=1/z3)
            ae = abs(av2*av3*av4)
            yield ae, ae*abs((zp/zin)*50/(49.9+50)), ie4*abs(1/(1/zin+1/1000))

if __name__ == '__main__':
    ve,vrf,lim = zip(*scenari())
    print('Per 1 uV RMS al nodo IF, uV RMS emettitore e porta RF:', 
          [(round(min(v),3),round(max(v),3)) for v in (ve,vrf)])
    print('Stima di interdizione Q104, mV picco, senza carico del diodo:',
          round(1000*min(lim),1),round(1000*max(lim),1))
    # Un singolo tono con piccolo offset dal LO; nessuna specifica di guadagno a DC.
    bbmin = min(vrf)*10**(-8/20)
    bbmax = max(vrf)*10**(-5.6/20)
    print('Uscita ciascun canale, uV RMS per perdita ipotizzata 5.6..8 dB:', bbmin,bbmax)
    print('Rumore termico a vuoto della sola terminazione, 290 K / 4 kHz, uV RMS:',
          1e6*sqrt(4*1.380649e-23*290*49.9*4000))
    print('Guadagno per 100 mV RMS ADC di scenario, V/V:',1e5/bbmax,1e5/bbmin)
