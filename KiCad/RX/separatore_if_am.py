"""Piccolo segnale Q104 con carico del rivelatore a portante prossima a zero."""
from itertools import product
import numpy as np
from guadagno_if_am import stadio, W

def separatore(vcc,ie3,vce3,beta,vbe,ft,cmu,is_d,*, y_extra=0j):
    # Equivalente DC del collettore Q103, includendo R135 approssimata in serie a R138.
    vb0 = vce3 + ie3*338
    ie = (vb0-vbe)/(1000+1247/(beta+1))
    ic = ie*beta/(beta+1)
    gm = ic/.02585
    vce = vcc-47*ic-1000*ie
    jw = 1j*W
    zd = 1/(is_d/.030+jw*8e-12) + 1/(1/47000+jw*120e-12)
    ze = 1/(1/6800+1/zd) + 1/(jw*10e-9)
    ypi = gm/beta + jw*(gm/(2*np.pi*ft)-cmu)
    yc = jw*cmu
    # Base imponibile a 1 V. Incognite emettitore e collettore.
    ve,vc = np.linalg.solve([[1/1000+1/ze+y_extra+ypi+gm,0],[-gm,1/47+jw*100e-9+yc]],
                            [ypi+gm,yc-gm])
    zin = 1/(ypi*(1-ve)+yc*(1-vc))
    return ie,vce,ve,zin

if __name__ == '__main__':
    casi=[]
    for v, b3, vb3, b4, vb4, ft4, cm4, is_d in product(
            (4.75,5.25),(80,200),(.60,.75),(80,200),(.60,.75),(100e6,300e6),
            (2e-12,4e-12),(1e-8,1e-7)):
        ie3,vce3,*_ = stadio(v,b3,vb3,200e6,3e-12,float('inf'),0)
        ie4,vce4,av4,z4 = separatore(v,ie3,vce3,b4,vb4,ft4,cm4,is_d)
        for ft3,cm3,ft2,cm2,b2,vb2 in product((100e6,300e6),(2e-12,4e-12),
                (100e6,300e6),(2e-12,4e-12),(80,200),(.60,.75)):
            _,_,av3,z3 = stadio(v,b3,vb3,ft3,cm3,float('inf'),0,carico_extra=1/z4)
            _,_,av2,_ = stadio(v,b2,vb2,ft2,cm2,float('inf'),0,carico_extra=1/z3)
            casi.append((1000*ie4,vce4,abs(z4),abs(av4),abs(av2*av3*av4)))
    print('Ie mA, Vce V, |Zin| ohm, |Ae|, uV buffer per 1 uV al nodo IF')
    for col in zip(*casi):print(f'{min(col):.3f} .. {max(col):.3f}')
