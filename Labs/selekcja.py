from rastrigin import generuj_populacje, oblicz_bity
from config import rozmiar_populacji, dokladnosci, granice
from osobnik import Osobnik
import random


def selekcja_turniejowa(populacja, minimum=True):

    nowa_populacja = []
    for _ in range(len(populacja)):
        # Losowanie dwóch osobników bez zwracania
        osobnik1, osobnik2 = random.sample(populacja, 2)

        # Wybór najlepszego osobnika
        najlepszy = (
            osobnik1
            if (minimum and osobnik1.wartosc_funkcji < osobnik2.wartosc_funkcji)
            or (not minimum and osobnik1.wartosc_funkcji > osobnik2.wartosc_funkcji)
            else osobnik2
        )

        nowa_populacja.append(najlepszy)

    return nowa_populacja


def selekcja_rankingu(populacja, minimum=True):

    nowa_populacja = []
    populacja = sorted(populacja, key=lambda x: x.wartosc_funkcji, reverse=not minimum)
    for _ in range(len(populacja)):
        losowa_liczba = random.randint(0, random.randint(0, len(populacja) - 1))
        nowa_populacja.append(populacja[losowa_liczba])
    return nowa_populacja


def selekcja_ruletki(populacja, minimum=True):

    if minimum:
        # Odwrócenie wartości funkcji przystosowania dla minimalizacji
        max_wartosc = max(osobnik.wartosc_funkcji for osobnik in populacja)
        wartosc_dopasowania = sum(
            max_wartosc - osobnik.wartosc_funkcji for osobnik in populacja
        )
        prawdopodobienstwa = [
            (max_wartosc - osobnik.wartosc_funkcji) / wartosc_dopasowania
            for osobnik in populacja
        ]
    else:
        # Obliczanie sumy wartości funkcji przystosowania
        wartosc_dopasowania = sum(osobnik.wartosc_funkcji for osobnik in populacja)
        prawdopodobienstwa = [
            osobnik.wartosc_funkcji / wartosc_dopasowania for osobnik in populacja
        ]

    # Obliczanie dystrybuanty
    dystrybuanta = [
        sum(prawdopodobienstwa[: i + 1]) for i in range(len(prawdopodobienstwa))
    ]

    nowa_populacja = []

    # Tworzenie nowej populacji poprzez losowanie
    for _ in range(len(populacja)):
        losowa_liczba = random.random()
        for i, dystrybuanta_i in enumerate(dystrybuanta):
            if losowa_liczba <= dystrybuanta_i:
                nowa_populacja.append(populacja[i])
                break

    return nowa_populacja


if __name__ == "__main__":
    # Tworzenie populacji osobników
    liczba_bitow = [oblicz_bity(a, b, d) for (a, b), d in zip(granice, dokladnosci)]
    populacja = generuj_populacje(rozmiar_populacji, liczba_bitow)

    # Tworzenie instancji Osobnik
    populacja_osobnikow = [Osobnik(genotyp, liczba_bitow) for genotyp in populacja]

    print("Wartości funkcji wszystkich osobników:")
    for i, osobnik in enumerate(populacja_osobnikow, 1):
        print(f"Osobnik {i}: {osobnik.wartosc_funkcji}")

    nowa_populacja_turniejowa = selekcja_turniejowa(populacja_osobnikow, minimum=True)
    print(
        "Nowa populacja (turniej):",
        [osobnik.wartosc_funkcji for osobnik in nowa_populacja_turniejowa],
    )

    nowa_populacja_rankingu = selekcja_rankingu(populacja_osobnikow, minimum=True)
    print(
        "Nowa populacja (ranking):",
        [osobnik.wartosc_funkcji for osobnik in nowa_populacja_rankingu],
    )

    nowa_populacja_ruletka = selekcja_ruletki(populacja_osobnikow, minimum=True)
    print(
        "Nowa populacja (ruletka):",
        [osobnik.wartosc_funkcji for osobnik in nowa_populacja_ruletka],
    )
