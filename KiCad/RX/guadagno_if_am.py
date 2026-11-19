"""Q102, risposta lineare a 10,695 MHz per scenari di transistor e carico."""
from itertools import product
from math import log10, pi
import numpy as np
from taratura_am import seleziona

W = 2*pi*10.695e6


def stadio(vcc, beta, vbe, ft, cmu, rl, cl):
    # Partitore 15k/4k7, 47 ohm comuni al collettore e al partitore.
    frazione = 4700/(15000+4700)
    rth = 15000*frazione
    alpha = beta/(beta+1)
    re = 68+270
    # I_alim = Ic + (Vs - Vb)/15k; Vb = Vbe + Ie*Re.
    vs0 = (vcc + 47*vbe/15000)/(1+47/15000)
    caduta = 47*(alpha-re/15000)/(1+47/15000)
    ie = (frazione*vs0-vbe)/(re+rth/(beta+1)+frazione*caduta)
    vs = vs0-caduta*ie
    vc = vs-1200*alpha*ie
    gm = alpha*ie/.02585
    cpi = gm/(2*pi*ft)-cmu
    assert cpi > 0
    # Nodi: base, emettitore, collettore, alimentazione locale, giunzione Re.
    y = np.zeros((5,5),dtype=complex)
    def ramo(a,b,g):
        y[a,a] += g
        if b is not None:
            y[b,b] += g
            y[a,b] -= g
            y[b,a] -= g
    ramo(0,3,1/15000)
    ramo(0,None,1/4700)
    ramo(0,1,gm/beta+1j*W*cpi)
    ramo(0,2,1j*W*cmu)
    ramo(1,4,1/68)
    ramo(4,None,1/270+1j*W*10e-9)
    ramo(2,3,1/1200)
    ramo(3,None,1/47+1j*W*100e-9)
    ramo(2,None,1/rl+1j*W*cl)
    y[2,0] += gm
    y[2,1] -= gm
    y[1,0] -= gm
    y[1,1] += gm
    vb,_,vo,_,_ = np.linalg.solve(y,[1,0,0,0,0])
    zin = vb+1/(1j*W*10e-9)
    return ie,vc-ie*re,vo/zin,zin


if __name__ == '__main__':
    casi = [stadio(*p) for p in product((4.75,5.25),(80,200),(.60,.75),
            (100e6,300e6),(2e-12,4e-12),(2000,10000),(5e-12,15e-12))]
    print('Ie mA, Vce V, guadagno dB, modulo Zin ohm')
    for col in zip(*[(ie*1000,vce,20*log10(abs(av)),abs(z)) for ie,vce,av,z in casi]):
        print(round(min(col),2),round(max(col),2))
    carichi = [seleziona(4.7e-6*k,srf,33e-12*t+par,lambda r: 1/(1/r+1/z))
               for _,_,_,z in casi for k,srf,t,par in
               product((.9,1.1),(50e6,float('inf')),(.95,1.05),(1e-12,3e-12))]
    print('R112, C126 pF, Rp ohm, Cp pF')
    print([(round(min(v),2),round(max(v),2)) for v in zip(*carichi)])
