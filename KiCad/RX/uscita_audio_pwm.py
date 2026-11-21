"""R191-R194/C186-C189. Tensioni a RX_AF_LINE con generatore PWM ideale."""
from cmath import exp
from itertools import product
from math import floor, gcd, log10, pi, sin


ORIGINAL = ((1000, 15e-9), (4700, 3.3e-9))
FILTER = ((470, 22e-9), (1500, 6.8e-9), (3300, 2.7e-9))


def transfer(freq, load, stages=FILTER):
    s = 2j * pi * freq
    output = 1 / (1 / 100000 + 1 / load)
    coupling = 1 / (s * 1e-6)
    impedance = coupling + output
    gain = output / impedance
    for resistance, capacitance in reversed(stages):
        shunt = 1 / (s * capacitance + 1 / impedance)
        impedance = resistance + shunt
        gain *= shunt / impedance
    return gain



# FIR interpolatore x3: finestra utile 0–4 kHz, banda oscura da 12 kHz.
# Ogni fase ha guadagno unitario in continua. Ritardo: 9 tick a 48 kHz.
TAPS = (30, 86, 78, -113, -427, -481, 197, 1643, 3197, 3868,
        3197, 1643, 197, -481, -427, -113, 78, 86, 30)


def hold(freq, rate):
    phase = pi * freq / rate
    return abs(sin(phase) / phase)


def digital_gain(freq, interpolate):
    if not interpolate:
        return hold(freq, 16000)
    angle = -2j*pi*freq/48000
    fir = sum(tap*exp(angle*k) for k, tap in enumerate(TAPS)) / (3*4096)
    return abs(fir) * hold(freq, 48000)


def pwm_period(tone, phase, amplitude, interpolate):
    """Una sequenza periodica a regime. Ampiezza in conteggi duty su 256."""
    length = 16000 // gcd(tone, 16000)
    samples = [amplitude*sin(2*pi*tone*n/16000 + phase) for n in range(length)]
    duties = []
    for n, sample in enumerate(samples):
        if interpolate:
            for k in range(3):
                value = sum(tap*samples[(n-i) % length]
                            for i, tap in enumerate(TAPS[k::3])) / 4096
                duties.extend([floor(128.5 + value)]*3)
        else:
            duties.extend([floor(128.5 + sample)]*9)
    assert all(0 <= duty <= 256 for duty in duties)
    return duties


def pwm_peak(duties, freq):
    """Fondamentale o armonica: integrazione esatta degli impulsi 0–3,3 V."""
    angle = -2j*pi*freq/144000
    coefficient = sum(exp(angle*n)*(exp(angle*duty/256)-1)
                      for n, duty in enumerate(duties)) / (angle*len(duties))
    return 2*3.3*abs(coefficient)


def db(ratio):
    return 20*log10(ratio)


if __name__ == "__main__":
    assert all(sum(TAPS[k::3]) == 4096 for k in range(3))
    assert TAPS == TAPS[::-1]
    for load in (10000, 47000, 100000):
        print(f"Carico esterno {load} ohm")
        for name, stages in (("due poli", ORIGINAL), ("tre poli", FILTER)):
            residue = pwm_peak([128], 144000)*abs(transfer(144000, load, stages))
            voice = db(abs(transfer(4000, load, stages))*digital_gain(4000, True))
            print(f"  {name}: {1000*residue:.2f} mV picco PWM, tono 4 kHz {voice:.2f} dB")
        for interpolate in (False, True):
            for tone in (300, 1000, 4000):
                gain = abs(transfer(tone, load))*digital_gain(tone, interpolate)
                print(f"  x3={interpolate} {tone} Hz: {db(gain):.2f} dB")
            image = abs(transfer(12000, load))*digital_gain(12000, interpolate)
            wanted = abs(transfer(4000, load))*digital_gain(4000, interpolate)
            print(f"  immagine lineare a 12 kHz: {db(image/wanted):.2f} dBc")
            for amplitude in (4, 64):
                values = []
                for k in range(32):
                    duties = pwm_period(4000, 2*pi*k/32, amplitude, interpolate)
                    values.append(db(pwm_peak(duties, 12000)*abs(transfer(12000, load)) /
                                     (pwm_peak(duties, 4000)*abs(transfer(4000, load)))))
                print(f"  PWM, ampiezza {amplitude}, immagine peggiore: {max(values):.2f} dBc")
        ripple = pwm_peak([128], 144000)*abs(transfer(144000, load))
        assert abs(pwm_peak([128], 144000) - 2*3.3/pi) < 1e-12
        print(f"  Fondamentale PWM a riposo: {1000*ripple:.2f} mV picco")
    # Scenari AM del confronto I/Q: tono al 60%, obiettivo di prova ±64 tick.
    for carrier in (4, 180):
        audio_peak_codes = .6*carrier
        ticks_per_code = 64 / audio_peak_codes
        print(f"  Portante {carrier} codici: {ticks_per_code:.3f} tick/codice,"
              f" fondo scala a {128/ticks_per_code:.2f} codici audio di picco")

    # Estremi discreti: R ±1%, C dei tre poli ±5%, uscita GPIO ideale o 50 ohm.
    # C188, R193 e carico restano nominali.
    ripple_values, voice_values = [], []
    for signs in product((-1, 1), repeat=6):
        for source in (0, 50):
            stages = [(r*(1+.01*signs[2*i]), c*(1+.05*signs[2*i+1]))
                      for i, (r, c) in enumerate(FILTER)]
            stages[0] = (stages[0][0] + source, stages[0][1])
            ripple_values.append(1000*pwm_peak([128], 144000)*abs(transfer(144000, 47000, stages)))
            voice_values.append(db(abs(transfer(4000, 47000, stages))*digital_gain(4000, True)))
    print(f"  47 kohm, 128 casi: residuo {min(ripple_values):.2f}..{max(ripple_values):.2f} mV,"
          f" tono 4 kHz {min(voice_values):.2f}..{max(voice_values):.2f} dB")

    # RV201: posizione elettrica del cursore, indipendente dalla legge meccanica.
    # R195=470 kΩ. Ingresso amplificatore ipotizzato 100 kΩ; cavo 200 pF per linea.
    for position in (0, .1, .5, 1):
        for freq in (1000, 4000):
            s = 2j*pi*freq
            low = 50000*position
            high = 50000-low
            bottom = low/(1 + low*(1/470000 + 1/100000 + s*200e-12))
            branch = high + bottom
            load = 1/(1/branch + s*200e-12)
            gain = abs(transfer(freq, load)*bottom/branch)*digital_gain(freq, True)
            print(f"  RV201 {position:.0%}, {freq} Hz: {gain:.4f} V/V")
