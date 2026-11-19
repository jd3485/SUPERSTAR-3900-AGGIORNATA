"""Bilancio DC di U114. Le correnti del driver sono scenari, non misure."""
from itertools import product


def budget(bus, driver, vo, series, preload, iq, oscillator=0, preamp=0):
    output_current = driver + oscillator + preamp + vo / preload
    input_current = output_current + iq
    vin = bus - input_current * series
    return (vin, (vin - vo) * output_current + vin * iq,
            input_current**2 * series, 7.5 + input_current * series)


if __name__ == "__main__":
    print("Bus [V], driver [mA] + XO 30 mA + U115 10 mA, Vin minimo [V], P U114 max [W], P R153 max [W], bus minimo [V]")
    for bus, driver in product((9, 13.8, 16), (.025, .050, .075)):
        cases = [budget(bus, driver, vo, series, preload, .0085, oscillator=.030, preamp=.010)
                 for vo, series, preload in product((4.75, 5.25),
                                                     (4.7*.99, 4.7*1.01),
                                                     (910*.99, 910*1.01))]
        vin, preg, pres, required = zip(*cases)
        print(bus, round(1000*driver), *(round(x, 3) for x in
              (min(vin), max(preg), max(pres), max(required))))
