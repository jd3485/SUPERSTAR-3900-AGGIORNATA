"""R191-R193/C186-C188. Tensioni a RX_AF_LINE con generatore PWM ideale."""
from math import log10, pi, sin


def transfer(freq, load):
    s = 2j * pi * freq
    output = 1 / (1 / 100000 + 1 / load)
    coupling = 1 / (s * 1e-6)
    second = 1 / (s * 3.3e-9 + 1 / (coupling + output))
    first = 1 / (s * 15e-9 + 1 / (4700 + second))
    return first / (1000 + first) * second / (4700 + second) * output / (coupling + output)


def hold(freq):
    phase = pi * freq / 16000
    return abs(sin(phase) / phase)


if __name__ == "__main__":
    for load in (10000, 47000, 100000):
        print(f"Carico esterno {load} ohm")
        for freq in (300, 1000, 4000):
            gain = abs(transfer(freq, load)) * hold(freq)
            print(f"  {freq} Hz: {20*log10(gain):.2f} dB")
        image = abs(transfer(12000, load)) * hold(12000)
        wanted = abs(transfer(4000, load)) * hold(4000)
        print(f"  Immagine 12 kHz del tono 4 kHz: {20*log10(image/wanted):.2f} dBc")
        ripple = 2*3.3/pi * abs(transfer(144000, load))
        print(f"  Fondamentale PWM a riposo: {1000*ripple:.2f} mV picco")
