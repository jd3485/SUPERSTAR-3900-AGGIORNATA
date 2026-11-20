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
    # Riferimento delle capacità: RX_RF_RETURN. Positivo del serbatoio a massa, due condensatori di filtro bipolari.
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

    # Q105, configurazione TI fig. 30. Tensioni espresse in modulo.
    # 4,0 V al pin 5 è un punto di verifica da dimostrare alla corrente totale.
    rb = 1500
    base_min = (4.0 - .85) / (rb * 1.01)
    base_max = (5.25 - .65) / (rb * .99)
    pump_load = load + base_max
    print("Q105 Ib [mA] a regime, beta forzato massimo a 10 mA",
          round(1000 * base_min, 3), round(1000 * base_max, 3),
          round(load / base_min, 2))
    print("Minimo modulo pin 5 per Ib >= 1 mA [V]", round(.85 + .001 * rb * 1.01, 3))
    print("Modulo rail a pin 5 di -4 V, VCE 0,2 V, R +1% [V]",
          round(4 - .2 - 2 * 10.1 * load, 3))
    # U117 sul solo ramo positivo: due sezioni, divisore e 0,1 mA
    # di carico aggiuntivo ipotizzato prima della scelta ADC.
    iq_stage = 2 * .00135 + 5.25 / (29700 * .999) + .0001
    # Scenario ADC: 2 x 450 uA, riferimento 100 uA, 2 x 150 uA
    # di carico VREF, due pull da 10k all’estremo e carico uscite ipotizzato.
    adc_stage = 2*.00045 + .0001 + 2*.00015 + 2*5.25/9900 + .0002
    # U122: scenario di budget per quattro ingressi AHCT pilotati a 3,3 V,
    # capacità totale commutata equivalente 200 pF a 1,152 MHz, 50 uA statici.
    # Le correnti addizionali reali dipendono da VIH, carico, duty cycle e PVT.
    # U121 prende energia dalla rail MCU; i due pull dati restano sul ramo ADC.
    logic_5v = 4*.002 + 200e-12*5.25*1.152e6 + .00005 + 2*5.25/46530
    print("Scenario aggiuntivo interfaccia a 5 V [mA]", round(1000*logic_5v, 3))
    total_protected = load + 1.2 * pump_load + .005 + iq_stage + adc_stage + logic_5v
    cases = [budget(16, .075, vo, series, preload, .0085, .030, total_protected)
             for vo, series, preload in product((4.75, 5.25), (4.653, 4.747),
                                                (900.9, 919.1))]
    print("Con Q105, U117 e ADC: P U114 [W], bus minimo [V], tono rail [uV picco, BJT ideale in AC]",
          round(max(c[1] for c in cases), 3), round(max(c[3] for c in cases), 3),
          round(max_in_band[0] * 1e6 * pump_load / load, 3))
    # Un gradino ideale a valle del collettore darebbe inizialmente V/R166.
    # Serve un modello di avvio a corrente limitata, oltre al bilancio DC.
    print("Gradino 5,25 V su R166 -1%, C158 scarico: corrente ideale [A]",
          round(5.25 / 9.9, 3))
