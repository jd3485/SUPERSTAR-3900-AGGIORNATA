"""Modello RC nominale e NAND ideali ricostruite dalla netlist MAIN."""
from itertools import product
from math import exp, log
from pathlib import Path
from xml.etree import ElementTree

xml = Path(__file__).resolve().parents[1] / 'KiCad' / 'MAIN.xml'
root = ElementTree.parse(xml)
pins = {(p.get('ref'), int(p.get('pin'))): net.get('name')
        for net in root.findall('.//nets/net') for p in net if p.get('ref') in ('U105', 'R126', 'C123', 'D103', 'R128')}
gates = [(1, 2, 3), (4, 5, 6), (9, 10, 8), (12, 13, 11)]
def component(ref, suffix, scale):
    value = root.findtext(f'.//components/comp[@ref="{ref}"]/value')
    assert value.endswith(suffix)
    return float(value[:-len(suffix)]) * scale

assert pins['R126', 2] == pins['C123', 1] == pins['U105', 4]
assert pins['C123', 2] == '/CONTROL_RETURN'

assert pins['U105', 3] == pins['R128', 1] == pins['R126', 1]
assert pins['R128', 2] == pins['D103', 2]
assert pins['D103', 1] == pins['C123', 1]
slow_r = component('R126', 'k', 1000)
fast_r = component('R128', 'k', 1000)
cap = component('C123', 'n', 1e-9)


def rc_step(voltage, target, diode_drop, resistance, recharge, capacitance, enhanced):
    """Tensioni normalizzate; diodo a caduta costante con spegnimento nel passo."""
    dt = 1e-5
    cutoff = target - diode_drop
    if enhanced and voltage < cutoff:
        parallel = 1 / (1 / resistance + 1 / recharge)
        limit = parallel * (target / resistance + cutoff / recharge)
        fast_tau = parallel * capacitance
        crossing = fast_tau * log((limit - voltage) / (limit - cutoff))
        if crossing >= dt:
            return limit + (voltage - limit) * exp(-dt / fast_tau)
        voltage = cutoff
        dt -= crossing
    return target + (voltage - target) * exp(-dt / (resistance * capacitance))


def trajectory(sequence, initial_cap, *, enhanced=True, capacitance=cap,
               resistance=slow_r, recharge=fast_r, low_threshold=0.35,
               high_drive=1.0, diode_drop=0.14):
    voltage = initial_cap
    schmitt = initial_cap >= 0.5
    logic = {net: False for net in pins.values()}
    results = []
    for milliseconds, reset_n, released in sequence:
        logic['/LOGIC_RESET_N'] = reset_n
        logic['/PTT_RELEASE_VALID'] = released
        samples = []
        for _ in range(round(milliseconds * 100)):
            a, b, y = gates[0]
            logic[pins['U105', y]] = not (logic[pins['U105', a]] and logic[pins['U105', b]])
            target = int(logic[pins['R126', 1]])
            voltage = rc_step(voltage, high_drive * target, diode_drop, resistance,
                              recharge, capacitance, enhanced)
            if voltage >= 0.60:
                schmitt = True
            elif voltage <= low_threshold:
                schmitt = False
            logic[pins['U105', 4]] = schmitt
            for _ in range(3):
                for a, b, y in gates[1:]:
                    logic[pins['U105', y]] = not (logic[pins['U105', a]] and logic[pins['U105', b]])
            samples.append(logic['/PTT_ARMED'])
        results.append(samples)
    return results

if __name__ == '__main__':
    phases = [(80, False, False), (40, True, False), (1, True, True),
              (30, True, False), (30, True, True), (30, True, False),
              (80, False, True), (1, True, True), (30, True, True)]
    for start in (0, 1):
        runs = trajectory(phases, start)
        assert all(not any(runs[i]) for i in (0, 1, 2, 3, 6, 7))
        assert runs[4][-1] and all(runs[5]) and runs[8][-1]
    burst = [(80, False, False)] + [(1, True, True), (0.2, True, False)] * 20
    # Partenza a regime, armamento azzerato, condensatore carico.
    assert any(any(r) for r in trajectory(burst, 1, enhanced=False))
    for cm, rm, fm, threshold, drive, drop in product(
            (0.9, 1.1), (0.99, 1.01), (0.99, 1.01),
            (0.20, 0.45), (0.85, 1.0), (0.10, 0.21)):
        runs = trajectory(burst + [(30, True, True)], drive, capacitance=cap*cm,
                          resistance=slow_r*rm, recharge=fast_r*fm,
                          low_threshold=threshold, high_drive=drive, diode_drop=drop)
        assert all(not any(run) for run in runs[:-1]) and runs[-1][-1]
    print('64 combinazioni: raffica respinta; rilascio successivo riconosciuto.')
    print('Sequenze nominali superate con condensatore inizialmente carico e scarico.')
