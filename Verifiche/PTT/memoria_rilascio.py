"""Modello RC nominale e NAND ideali ricostruite dalla netlist MAIN."""
from math import exp
from pathlib import Path
from xml.etree import ElementTree

xml = Path(__file__).resolve().parents[1] / 'KiCad' / 'MAIN.xml'
root = ElementTree.parse(xml)
pins = {(p.get('ref'), int(p.get('pin'))): net.get('name')
        for net in root.findall('.//nets/net') for p in net if p.get('ref') in ('U105', 'R126', 'C123')}
gates = [(1, 2, 3), (4, 5, 6), (9, 10, 8), (12, 13, 11)]
def component(ref, suffix, scale):
    value = root.findtext(f'.//components/comp[@ref="{ref}"]/value')
    assert value.endswith(suffix)
    return float(value[:-len(suffix)]) * scale

tau = component('R126', 'k', 1000) * component('C123', 'n', 1e-9)
assert pins['R126', 2] == pins['C123', 1] == pins['U105', 4]
assert pins['C123', 2] == '/CONTROL_RETURN'

def trajectory(sequence, initial_cap):
    voltage = initial_cap
    schmitt = initial_cap >= 0.5
    logic = {net: False for net in pins.values()}
    results = []
    for milliseconds, reset_n, released in sequence:
        logic['/LOGIC_RESET_N'] = reset_n
        logic['/PTT_RELEASE_VALID'] = released
        samples = []
        for _ in range(round(milliseconds * 100)):
            for a, b, y in gates[:1]:
                logic[pins['U105', y]] = not (logic[pins['U105', a]] and logic[pins['U105', b]])
            target = int(logic[pins['R126', 1]])
            voltage = target + (voltage - target) * exp(-1e-5 / tau)
            if voltage >= 0.60:
                schmitt = True
            elif voltage <= 0.35:
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
    print('Sequenze nominali superate con condensatore inizialmente carico e scarico.')
