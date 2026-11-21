"""C196 e R304. Sorgente di Thévenin dopo D106, un ponte ideale su 8 ohm."""
from math import exp, expm1, pi, sin, sqrt


def carica(tensione, capacita, resistenza, sorgente):
    totale = resistenza + sorgente
    picco = tensione / totale
    integrale = capacita * tensione**2 / (2 * totale)
    return picco, integrale, resistenza * integrale


def audio(tensione, frequenza, potenza, capacita, resistenza, sorgente):
    totale = resistenza + sorgente
    picco = sqrt(2 * potenza / 8)
    passi = 1000
    dt = 1 / (2 * frequenza * passi)
    frazione = -expm1(-dt / (totale * capacita))
    # Soluzione periodica: dopo un semiperiodo il carico raddrizzato si ripete.
    obiettivi = [tensione - totale * (.065 + picco * sin(pi * (i + .5) / passi))
                 for i in range(passi)]
    v = 0.
    for obiettivo in obiettivi:
        v += (obiettivo - v) * frazione
    v /= 1 - exp(-passi * dt / (totale * capacita))
    valori = []
    for obiettivo in obiettivi:
        v += (obiettivo - v) * frazione
        valori.append(v)
    perdita = resistenza * sum(((tensione - v) / totale)**2 for v in valori) / passi
    return min(valori), max(valori) - min(valori), perdita


if __name__ == '__main__':
    for r in (0., 1.):
        print('R304 nominale [ohm]', r, 'carica a 16 V [A, A²s, J]',
              carica(16., 470e-6, r, .10))
    print('Vertice spunto [A, A²s, J]', carica(16., 564e-6, .95, 0.))
    for hz in (300., 1000., 4000.):
        print(hz, 'Hz, 11 V dopo D106 [Vmin, Vpp, W su R304]',
              audio(11., hz, 5.38, 376e-6, 1.05, .10))
