"""C196 e R304. Sorgente di Thévenin dopo D106, un ponte ideale su 8 ohm."""
from math import exp, expm1, pi, sin, sqrt


def carica(tensione, capacita, resistenza, sorgente):
    totale = resistenza + sorgente
    picco = tensione / totale
    integrale = capacita * tensione**2 / (2 * totale)
    return picco, integrale, resistenza * integrale


def profilo_audio(tensione, frequenza, potenza, capacita, resistenza, sorgente, passi=1000):
    totale = resistenza + sorgente
    picco = sqrt(2 * potenza / 8)
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
    return valori


def audio(tensione, frequenza, potenza, capacita, resistenza, sorgente):
    valori = profilo_audio(tensione, frequenza, potenza, capacita, resistenza, sorgente)
    totale = resistenza + sorgente
    perdita = resistenza * sum(((tensione - v) / totale)**2 for v in valori) / len(valori)
    return min(valori), max(valori) - min(valori), perdita


def impulso_comune(v, rs, r304, c_main, c_audio):
    """Integrale della corrente unica del fusibile, con due rail inizialmente scariche.

    Diodi ideali e un solo ingresso attivo. C_main direttamente dopo Rs,
    C_audio dopo R304. La corrente è la somma di due esponenziali.
    """
    somma = (1 / rs + 1 / r304) / c_main + 1 / (r304 * c_audio)
    prodotto = 1 / (rs * r304 * c_main * c_audio)
    veloce = (somma + sqrt(somma**2 - 4 * prodotto)) / 2
    lento = prodotto / veloce
    i0 = v / rs
    # Derivata iniziale: tutta la corrente carica C_main.
    a = i0 * (1 / (rs * c_main) - lento) / (veloce - lento)
    b = i0 - a
    return a*a / (2*veloce) + b*b / (2*lento) + 2*a*b / (veloce+lento)


def margine_audio(r304, passi=1000):
    potenza = 5.38
    valori = profilo_audio(11., 300., potenza, 376e-6, 1.05*r304, .10, passi)
    # Il campione di rail e la tensione richiesta sono alla stessa fase.
    picco = sqrt(2*8*potenza)
    return min(v - picco*sin(pi*(i+1)/passi) for i, v in enumerate(valori))


if __name__ == '__main__':
    for r in (0., 1.):
        print('R304 nominale [ohm]', r, 'carica a 16 V [A, A²s, J]',
              carica(16., 470e-6, r, .10))
    print('Vertice spunto [A, A²s, J]', carica(16., 564e-6, .95, 0.))
    for hz in (300., 1000., 4000.):
        print(hz, 'Hz, 11 V dopo D106 [Vmin, Vpp, W su R304]',
              audio(11., hz, 5.38, 376e-6, 1.05, .10))

    # Sensibilità: C103+C105+C182 e C196+C197, tutte a +20% ipotizzato.
    # Correnti dei regolatori, capacità dopo R153 e carichi attivi esclusi.
    for r in (.68, .82, 1., 1.2):
        margine = margine_audio(r)
        print(f"R304 {r:.2f} ohm, margine ideale sincrono {margine:.3f} V")
        for rs in (.05, .10, .25):
            i2t = impulso_comune(16., rs, .95*r, 1.32e-6*1.2, 470.1e-6*1.2)
            print(f"  Rs {rs:.2f} ohm: {i2t:.4f} A²s, {100*i2t/.405:.1f}% di fusione nominale")
            # Sensibilità al termine incrociato con una corrente costante
            # sovrapposta. Esclude la sua dissipazione continua e l'effetto
            # del preriscaldamento; non qualifica la durata del fusibile.
            carica_totale = 16 * (1.32e-6 + 470.1e-6) * 1.2
            residuo = .22 * .405 - i2t
            if residuo > 0:
                print(f"    Corrente sovrapposta che esaurisce il residuo al 22%: "
                      f"{residuo / (2 * carica_totale):.3f} A")
