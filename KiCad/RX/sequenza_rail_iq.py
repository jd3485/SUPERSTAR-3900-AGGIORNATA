"""Studio del sequenziatore U115: nodi e correnti in SI, ipotesi di circuito.

Comparatore candidato: ingresso + con 47k a Vcc, 68k a V-, 100k al ritorno
e 680k all'uscita open collector. Pull-up 4k7. Ingresso - da 26k1 / 10k.
L'uscita bassa abilita il ramo positivo. Lo stadio di potenza è ideale.
"""
from itertools import product
from math import inf

import numpy as np
from scipy.integrate import solve_ivp

NOMINAL = np.array([47e3, 68e3, 100e3, 680e3, 26.1e3, 10e3, 4.7e3])
WIRE_R = .414
CLAMP = .50
INPUT_R = 125 / 2  # due ingressi non invertenti, sorgenti indipendenti a zero


def detector(vcc, neg, enabled, resistors=NOMINAL, low=.4):
    rp, rn, rg, rf, rt, rb, pull = resistors
    feedback = low if enabled else vcc
    resistance = rf if enabled else rf + pull
    conductance = 1/rp + 1/rn + 1/rg + 1/resistance
    sense = (vcc/rp + neg/rn + feedback/resistance) / conductance
    return sense, vcc*rb/(rt+rb), conductance


def threshold(vcc, enabled, resistors, low, error):
    _, rn, *_ = resistors
    sense, ref, conductance = detector(vcc, 0, enabled, resistors, low)
    return (ref + error - sense) * conductance * rn


def supply_load(source, series, neg, load):
    # V+ quasistatica. Se conduce il clamp degli ingressi a V+, includere
    # la relativa sorgente equivalente e ricalcolare la corrente di U115.
    def solve(v, r):
        current = min(max((v-neg)/(100+r), 0), load)
        return v-r*current, current
    pos, current = solve(source, series)
    if pos < -CLAMP:
        r = 1/(1/series + 1/INPUT_R)
        pos, current = solve((source/series - CLAMP/INPUT_R)*r, r)
    return pos, current


def trial(delay, limit, beta, cap, load, off_r, controlled=True, rb_q105=3030., sense_clamp=False, inhibit=0., diode_knee=None, max_step=.001):
    # Arresto e ripartenza con carica residua; bus forzato con rampe di 1 ms.
    edges = (.0, .001, .160, .161, .181, .182, .390)
    levels = (0, 4.75, 4.75, 0, 0, 4.75, 4.75)
    times = sorted(set(edges + (.001*3.5/4.75, .181+.001*3.5/4.75,
                                max(.001*3.5/4.75, delay),
                                .181+max(.001*3.5/4.75, delay),
                                .160+.001*(1-3.5/4.75), .160+.001*(1-4.3/4.75),
                                .001*4.3/4.75, .181+.001*4.3/4.75)))
    valid_first = .001*4.3/4.75
    times = sorted(set(times + [valid_first+inhibit, .181+valid_first+inhibit]))
    state = np.zeros(3)
    on = False
    transitions = []
    maximum_neg = minimum_pos = max_input = 0.
    min_sense = inf

    for t0, t1 in zip(times, times[1:]):
        mid = (t0+t1)/2
        supply = lambda t: float(np.interp(t, edges, levels))
        valid = supply(mid) >= 4.3  # funzione UVLO ideale, da realizzare
        valid = valid and mid >= (valid_first if mid < .181 else .181+valid_first) + inhibit
        pump_on = supply(mid) >= 3.5 and (mid >= delay if mid < .181 else mid >= .181+delay)
        if not valid and on:
            on = False
            transitions.append((t0, False))
        def evaluate(t, y):
            raw, first, neg = y
            bus = supply(t)
            active = on or not controlled
            pos, iq = supply_load(bus if active else 0., 10.1 if active else off_r, neg, load)
            sense, ref, _ = detector(bus, neg, on)
            if sense_clamp:
                sense = max(sense, -.20)  # clamp esterno ipotetico, solo modello
            # Valutazione del nodo ideale anche fuori campo; la corrente di
            # protezione del comparatore in brownout resta da modellare.
            i_sense = (sense-neg)/NOMINAL[1] if controlled else 0
            pump = min(max((bus+raw)/16., 0.), limit) if pump_on else 0
            # Perdita ipotizzata del serbatoio quando la pompa è spenta.
            leakage = -raw/1000 if not pump_on else 0.
            ib = max((-raw-.85)/rb_q105, 0.)
            ic = min(beta*ib, max((first-raw-.2)/10.1, 0.))
            transfer = (neg-first)/(10.1+WIRE_R)
            lower = max(neg-CLAMP, 0.)/INPUT_R
            upper = max(-CLAMP-pos, 0.)/INPUT_R
            external = max((neg-diode_knee)/8., 0.) if diode_knee is not None else 0.
            dy = np.array([ib+ic-pump+leakage, transfer-ic,
                           iq-transfer+i_sense-lower-external])/cap
            return dy, pos, max(lower,upper)/2, sense, sense-ref
        def switch(t, y):
            return evaluate(t,y)[-1]
        switch.terminal = True
        while t0 < t1-1e-12:
            err = switch(t0,state)
            if controlled and valid and ((on and err > 0) or (not on and err < 0)):
                on = not on
                transitions.append((t0,on))
            switch.direction = 1 if on else -1
            result = solve_ivp(lambda t,y:evaluate(t,y)[0], (t0,t1), state,
                               rtol=1e-5, atol=1e-8, max_step=max_step,
                               events=switch if valid and controlled else None)
            if not result.success:
                raise RuntimeError(result.message)
            for t,y in zip(result.t,result.y.T):
                _,pos,current,sense,_ = evaluate(t,y)
                maximum_neg = max(maximum_neg,y[2])
                minimum_pos = min(minimum_pos,pos)
                max_input = max(max_input,current)
                min_sense = min(min_sense,sense)
            t0 = result.t[-1]
            state = result.y[:,-1]
            if result.status == 1:
                on = not on
                transitions.append((t0,on))
                if len(transitions)>20:
                    raise RuntimeError('commutazioni ripetute')
    return maximum_neg, minimum_pos, max_input*1000, min_sense, transitions


if __name__ == '__main__':
    for enabled in (False,True):
        limits = [threshold(v,enabled,NOMINAL*(1+.01*np.array(s)),lo,err)
                  for v,lo,err in product((4.75,5.25),(.0,.7),(-.020,.020))
                  for s in product((-1,1),repeat=7)]
        print('Soglia', 'OFF' if enabled else 'ON', min(limits), max(limits))
    # Inviluppo lineare di scenario per D105: 0,32 V + 8 Ω I, 0,40 V a 10 mA.
    # Il caso a +100 mV esplora la sensibilità; non è un limite PVT garantito.
    cases = list(product((0,.010),(.025,.075),(10,50),(80e-6,120e-6),(.005,.010)))
    for name, off, control, rb, clamp, inhibit, knee in [
            ('diretto',10,False,3030,False,0,None), ('aperto',100e3,True,3030,False,0,None),
            ('a massa',10,True,3030,False,0,None), ('a massa, R165 1k5 e clamp',10,True,1515,True,0,None),
            ('a massa, 1k5, clamp, interdizione 12 ms',10,True,1515,True,.012,.32),
            ('CAD D105 e R165 1k5',10,False,1515,False,0,.32),
            ('CAD sensibilità Vf +0,1 V',10,False,1515,False,0,.42)]:
        results = [trial(*case,off,control,rb,clamp,inhibit,knee) for case in cases]
        vals = np.array([r[:4] for r in results])
        counts = [sum(on for _,on in r[4]) for r in results]
        print(name, 'max V-, min V+, max mA per ingresso:',
              vals[:, 0].max(), vals[:, 1].min(), vals[:, 2].max())
        if control:
            print('Min V sense, conteggio abilitazioni:', vals[:, 3].min(),
                  min(counts), max(counts))
            clean = [r for r in results if [s for _,s in r[4]] == [True, False, True]
                     and r[4][0][0] < .160 and r[4][2][0] >= .181]
            print('Due abilitazioni distinte con un solo arresto:',len(clean),'/',len(cases))
            if clean:
                print('Prima abilitazione [ms]:', min(r[4][0][0] for r in clean)*1000,
                      max(r[4][0][0] for r in clean)*1000)
        if name.startswith('CAD'):
            case = cases[int(np.argmax(vals[:,0]))]
            fine = trial(*case,off,control,rb,clamp,inhibit,knee,max_step=.00025)
            print('Scarto sul picco con passo ridotto [mV]:',
                  1000*abs(fine[0]-vals[:,0].max()))
