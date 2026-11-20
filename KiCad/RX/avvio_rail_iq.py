"""Avvio medio della rail I/Q. Tensioni rispetto a RX_RF_RETURN, unità SI.

Scenari ingegneristici, senza macromodelli OEM. C157 è sul pin 5, C158 si
trova dopo Q105 e R166, C159 presso U115 dopo rame e R167. Il carico fra le
due rail approssima il possibile trascinamento positivo a pompa ferma.
"""
from itertools import product

import numpy as np
from scipy.integrate import solve_ivp


def simulate(delay, limit, beta, capacitance, load, step=0.0002, duration=.12):
    supply = 4.75
    ramp = .001
    resistance = 16.0   # Thévenin medio della pompa, ipotesi di scenario
    filter_r = 10.1
    # Rame andata + ritorno dedicato, 35 µm a 20 °C, resistività 1,72e-8 Ω m.
    copper_r = 1.72e-8 / 35e-6 * (.250392 / .00050 + .255220 / .00075)

    def currents(t, state):
        raw, first, out = state
        pos = supply * min(t / ramp, 1.0)
        # Ingresso sopra soglia di modello e oscillatore abilitato dopo delay.
        pump = (np.clip((pos + raw) / resistance, 0, limit)
                if t >= delay and pos >= 3.5 else 0.)
        base = max((-raw - .85) / 3030., 0.)
        # Modello a tratti in conduzione diretta: VCE(sat) ipotizzata.
        collector = min(beta * base, max((first - raw - .2) / filter_r, 0.))
        between = (out - first) / (filter_r + copper_r)
        injection = max(min((pos - out) / 100., load), 0.)
        return pump, base, collector, between, injection

    def derivative(t, state):
        pump, base, collector, between, injection = currents(t, state)
        return np.array([base + collector - pump, between - collector,
                         injection - between]) / capacitance

    # Suddivisione in tratti alle discontinuità di abilitazione e fine rampa.
    points = sorted({0., ramp * 3.5 / supply, ramp, delay, duration})
    initial = np.zeros(3)
    times, states = [], []
    for start, stop in zip(points, points[1:]):
        result = solve_ivp(derivative, (start, stop), initial, max_step=step,
                           rtol=2e-6, atol=1e-9)
        if not result.success:
            raise RuntimeError(result.message)
        times.extend(result.t[1:])
        states.extend(result.y.T[1:])
        initial = result.y[:, -1]

    times = np.array(times)
    states = np.array(states)
    active = [currents(t, s) for t, s in zip(times, states)]
    # Tempo dopo il quale V- resta sotto -3 V fino a fine finestra.
    late = np.flatnonzero(states[:, 2] > -3)
    if late.size and late[-1] == len(times) - 1:
        settled = np.nan
    else:
        settled = times[late[-1] + 1] if late.size else 0.
    return np.array([states[:, 2].max(), settled * 1000,
                     1000 * max(i[2] for i in active), states[-1, 2]])


if __name__ == '__main__':
    cases = list(product((0., .010), (.025, .075), (10., 50.),
                         (80e-6, 120e-6), (.005, .010)))
    results = np.array([simulate(*case) for case in cases])
    # I casi censurati restano inclusi nel conteggio e nella tensione finale.
    print('Casi che raggiungono -3 V:', np.isfinite(results[:, 1]).sum())
    print('Scenari:', len(results))
    for name, column in zip(('Picco positivo V- [V]', 'Attraversamento -3 V [ms]',
                             'Picco Ic Q105 [mA]', 'V- a 120 ms [V]'), results.T):
        print(f'{name}: {np.nanmin(column):.3f} .. {np.nanmax(column):.3f}')
    worst = cases[int(np.argmax(results[:, 0]))]
    print('Caso di massimo trascinamento:', worst)
    worst_result = simulate(*worst)
    refined = simulate(*worst, step=.0001)
    assert abs(refined[0] - worst_result[0]) < .001
    print('Scarto sul picco con passo dimezzato [mV]:',
          1000 * abs(refined[0] - worst_result[0]))
    slow = cases[int(np.argmax(results[:, 3]))]
    print('Caso con rail meno negativa a 120 ms:', slow)
    print('Caso esteso a 650 ms, tempo soglia [ms] e V- finale [V]:',
          simulate(*slow, duration=.65)[[1, 3]])
