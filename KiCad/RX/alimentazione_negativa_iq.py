"""Studio LT1054CP per U115. Valori in SI. Solo regime periodico di piccolo segnale."""
from itertools import product
from math import pi

from alimentazione_lo_am import budget


def capacitor(frequency, capacitance, esr):
    return esr + 1 / (2j * pi * frequency * capacitance)


def ladder(frequency, resistance, capacitance, esr):
    # Due celle identiche non bufferizzate. U115 è un carico AC ad alta impedenza.
    zc = capacitor(frequency, capacitance, esr)
    first_node = 1 / (1 / zc + 1 / (resistance + zc))
    return first_node / (resistance + first_node) * zc / (resistance + zc)


def alias(frequency, sample_rate):
    return abs((frequency + sample_rate / 2) % sample_rate - sample_rate / 2)


if __name__ == "__main__":
    # Topologia TI: condensatore volante 10 uF, serbatoio 100 uF.
    # Ramo dopo il serbatoio: due celle 10 ohm / 100 uF.
    # Riferimento delle capacità: RX_RF_RETURN. Positivo dei tre elettrolitici a massa.
    load = .010
    max_tone = (0, 0, 0)
    max_in_band = (0, 0, 0)
    for frequency, harmonic in product(range(15000, 35001, 100), range(1, 32, 2)):
        # C -20%, ESR 0,25 ohm, R -1% (scenari, da qualificare con MPN).
        # Corrente quadrata +/- I nel serbatoio. Coefficiente di picco di Fourier.
        tone = frequency * harmonic
        amplitude = 4 * load / (pi * harmonic) * abs(capacitor(tone, 80e-6, .25))
        residual = amplitude * abs(ladder(tone, 9.9, 80e-6, .25))
        entry = (residual, frequency, harmonic)
        max_tone = max(max_tone, entry)
        if alias(tone, 16000) <= 4000:
            max_in_band = max(max_in_band, entry)

    print("Picco massimo [uV], f pompa [Hz], armonica")
    for peak, osc, harmonic in (max_tone, max_in_band):
        print(round(peak * 1e6, 3), osc, harmonic)
    print("Caduta DC delle due celle a 10 mA, R +1% [V]", 2 * 10.1 * load)
    # 10 mA rail positiva, altri 10 mA rail negativa. Pompa: 1,2 Iout + 5 mA
    # come scenario prudenziale, non massimo garantito. Riusa il modello U114.
    total = load + 1.2 * load + .005
    cases = [budget(16, .075, vo, series, preload, .0085, .030, total)
             for vo, series, preload in product((4.75, 5.25), (4.653, 4.747),
                                                (900.9, 919.1))]
    print("P U114 massima [W], bus minimo [V]",
          round(max(c[1] for c in cases), 3), round(max(c[3] for c in cases), 3))
