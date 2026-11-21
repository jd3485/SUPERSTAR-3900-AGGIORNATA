"""U124, LM317-N: vertici del partitore e scenari termici sul bus protetto."""
from itertools import product


def vertici():
    for ref, toll_alta, toll_bassa, iadj in product(
            (1.20, 1.30), (.999, 1.001), (.999, 1.001), (0., 100e-6)):
        r_alta = 115 * toll_alta
        r_bassa = 187 * toll_bassa
        precarico = ref / r_alta
        yield ref + (precarico + iadj) * r_bassa, precarico, iadj


if __name__ == "__main__":
    casi = list(vertici())
    tensioni = [v for v, _, _ in casi]
    print("Rail [V]:", min(tensioni), max(tensioni))
    print("Precarico minimo [mA]:", min(i for _, i, _ in casi) * 1000)
    print("Ingresso minimo per 3 V di differenziale [V]:", max(tensioni) + 3)
    for carico_ma in (35, 70, 100):
        # Carico digitale totale ipotizzato, inclusivo di PIC e traslatore.
        # Somma conservativa della potenza associata alla corrente di ADJ.
        p = max((16 - v) * (carico_ma / 1000 + i) + 16 * iadj
                for v, i, iadj in casi)
        print(f"{carico_ma} mA, bus 16 V: {p:.3f} W, "
              f"resistenza termica massima per Tj=125 °C e Ta=85 °C: {40/p:.1f} °C/W")
