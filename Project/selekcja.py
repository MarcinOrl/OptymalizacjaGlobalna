from main import Pula_tras
from config import rozmiar_puli_tras, liczba_miast, macierz_odleglosci
import random, copy


def selekcja_turniejowa(pula_tras):
    nowa_pula_tras = []

    for _ in range(len(pula_tras)):
        # Losowanie dwóch osobników bez zwracania
        trasa1, trasa2 = random.sample(pula_tras, 2)

        # Wybór najlepszego osobnika
        najlepszy = trasa1 if trasa1.dlugosc_trasy < trasa2.dlugosc_trasy else trasa2

        nowa_pula_tras.append(copy.deepcopy(najlepszy))

    return nowa_pula_tras


def selekcja_rankingu(pula_tras):
    nowa_pula_tras = []

    pula_tras = sorted(pula_tras, key=lambda x: x.dlugosc_trasy)
    for _ in range(len(pula_tras)):
        losowa_liczba = random.randint(0, random.randint(0, len(pula_tras) - 1))
        nowa_pula_tras.append(copy.deepcopy(pula_tras[losowa_liczba]))

    return nowa_pula_tras


def selekcja_ruletki(pula_tras):
    # Odwrócenie wartości funkcji przystosowania dla minimalizacji
    max_wartosc = max(trasa.dlugosc_trasy for trasa in pula_tras)
    wartosc_dopasowania = sum(max_wartosc - trasa.dlugosc_trasy for trasa in pula_tras)

    # Sprawdzanie, czy suma wartości dopasowania wynosi zero
    if wartosc_dopasowania == 0:
        print("Suma wartości dopasowania wynosi zero. Wybieramy trasę losowo.")
        return [copy.deepcopy(random.choice(pula_tras)) for _ in range(len(pula_tras))]

    prawdopodobienstwa = [
        (max_wartosc - trasa.dlugosc_trasy) / wartosc_dopasowania for trasa in pula_tras
    ]

    # Obliczanie dystrybuanty
    dystrybuanta = [
        sum(prawdopodobienstwa[: i + 1]) for i in range(len(prawdopodobienstwa))
    ]

    nowa_pula_tras = []

    # Tworzenie nowej populacji poprzez losowanie
    for _ in range(len(pula_tras)):
        losowa_liczba = random.random()
        for i, dystrybuanta_i in enumerate(dystrybuanta):
            if losowa_liczba <= dystrybuanta_i:
                nowa_pula_tras.append(copy.deepcopy(pula_tras[i]))
                break

    return nowa_pula_tras


if __name__ == "__main__":
    # Tworzenie puli tras
    pula_tras = Pula_tras(rozmiar_puli_tras, liczba_miast, macierz_odleglosci)

    # Wykonywanie selekcji
    print("Długości tras wszystkich tras:")
    for i, trasa in enumerate(pula_tras.trasy, 1):
        print(f"Osobnik {i}: {trasa.dlugosc_trasy}")

    nowa_pula_tras_turniejowa = selekcja_turniejowa(pula_tras.trasy)
    print(
        "Nowa pula tras (turniej):",
        [trasa.dlugosc_trasy for trasa in nowa_pula_tras_turniejowa],
    )

    nowa_pula_tras_rankingu = selekcja_rankingu(pula_tras.trasy)
    print(
        "Nowa pula tras (ranking):",
        [trasa.dlugosc_trasy for trasa in nowa_pula_tras_rankingu],
    )

    nowa_pula_tras_ruletka = selekcja_ruletki(pula_tras.trasy)
    print(
        "Nowa pula tras (ruletka):",
        [trasa.dlugosc_trasy for trasa in nowa_pula_tras_ruletka],
    )
