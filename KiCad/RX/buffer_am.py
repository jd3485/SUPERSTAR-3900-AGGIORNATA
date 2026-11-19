"""Analisi candidata del buffer AM con modello ibrido-pi, a 10,695 MHz."""
from itertools import product
from math import pi
from terminazione_if import risposta


def valuta(vcc, beta, vbe, ft, cmu):
    # Soluzione continua del partitore, includendo la caduta sul filtro da 47 ohm.
    k = 1 / (680 + 11000 / (beta + 1))
    rapporto = 1 - 1 / (2 * (beta + 1))
    ie = k * (0.5 * vcc / (1 + 47/44000) - vbe) / (
        1 + k * 0.5 * 47 * rapporto / (1 + 47/44000))
    gm = ie * beta / (beta + 1) / 0.02585
    jw = 2j * pi * 10.695e6
    cpi = gm / (2*pi*ft) - cmu
    ypi = gm/beta + jw*cpi
    # Modello AC con collettore disaccoppiato e ritorno RF ideale.
    zcap = 1/(jw*10e-9)
    ye = 1/680 + 1/(zcap + 39 + 50)
    av = (gm + ypi) / (gm + ypi + ye)
    yin = 1/11000 + jw*cmu + ypi*(1-av)
    zin = zcap + 1/yin
    # Sorgente IF disattivata: impedenza a monte di C119.
    zshunt = 1/(1/50 + 1/(49.9 + 1/(jw*160e-12)))
    zdriver = 1/(1/49.9 + 1/(jw*390e-9 + zshunt))
    ybase = 1/11000 + jw*cmu + 1/(zcap + zdriver)
    zout = zcap + 39 + 1/(1/680 + (gm+ypi)*ybase/(ybase+ypi))
    perdita, ritorno = risposta(10.695e6, 390e-9, 160e-12, 49.9, 49.9, 1/zin)
    return ie*1000, abs(zin), zout.real, zout.imag, perdita, ritorno


if __name__ == '__main__':
    casi = [valuta(*v) for v in product((4.75,5.25),(80,200),(.60,.75),
                                         (100e6,300e6),(2e-12,5e-12))]
    for nome,colonna in zip(('Ie mA','modulo Zin ohm','Re Zout ohm','Im Zout ohm','perdita IF nominale dB','return loss IF nominale dB'),zip(*casi)):
        print(f'{nome}: {min(colonna):.2f} .. {max(colonna):.2f}')
