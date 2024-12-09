from main import Populacja, Osobnik
from config import rozmiar_populacji, liczba_miast, macierz_odleglosci
import random


def krzyzowanie_tsp(populacja, prawdopodobienstwo, typ, instancja_populacji):
    wylosowana_populacja = [
        osobnik for osobnik in populacja if random.random() < prawdopodobienstwo
    ]

    if len(wylosowana_populacja) % 2 == 1:
        wylosowana_populacja.pop(random.randint(0, len(wylosowana_populacja) - 1))

    random.shuffle(wylosowana_populacja)
    pary = [
        (wylosowana_populacja[i], wylosowana_populacja[i + 1])
        for i in range(0, len(wylosowana_populacja), 2)
    ]

    for rodzic1, rodzic2 in pary:
        match typ:
            case "OX":
                # Krzyżowanie jednokrotne (Order Crossover)
                punkt1, punkt2 = sorted(random.sample(range(len(rodzic1.genotyp)), 2))
                print(f"Punkty: {punkt1}, {punkt2}")
                fragment1 = rodzic1.genotyp[punkt1:punkt2]
                fragment2 = rodzic2.genotyp[punkt1:punkt2]

                potomny1 = fragment1 + [
                    gen for gen in rodzic2.genotyp if gen not in fragment1
                ]
                potomny2 = fragment2 + [
                    gen for gen in rodzic1.genotyp if gen not in fragment2
                ]

                rodzic1.genotyp = potomny1
                rodzic2.genotyp = potomny2

            case "PMX":
                # Krzyżowanie częściowo mieszane (Partially Mapped Crossover)
                punkt1, punkt2 = sorted(random.sample(range(len(rodzic1.genotyp)), 2))
                potomny1 = rodzic1.genotyp[:]
                potomny2 = rodzic2.genotyp[:]

                mapa1 = dict(
                    zip(rodzic1.genotyp[punkt1:punkt2], rodzic2.genotyp[punkt1:punkt2])
                )
                mapa2 = dict(
                    zip(rodzic2.genotyp[punkt1:punkt2], rodzic1.genotyp[punkt1:punkt2])
                )

                for i in range(len(rodzic1.genotyp)):
                    if i < punkt1 or i >= punkt2:
                        while potomny1[i] in mapa1:
                            potomny1[i] = mapa1[potomny1[i]]
                        while potomny2[i] in mapa2:
                            potomny2[i] = mapa2[potomny2[i]]

                potomny1[punkt1:punkt2] = rodzic2.genotyp[punkt1:punkt2]
                potomny2[punkt1:punkt2] = rodzic1.genotyp[punkt1:punkt2]

                rodzic1.genotyp = potomny1
                rodzic2.genotyp = potomny2

            case "CX":
                # Krzyżowanie cykliczne (Cycle Crossover)
                potomny1, potomny2 = [None] * len(rodzic1.genotyp), [None] * len(
                    rodzic2.genotyp
                )
                cykl = 0
                indeks = 0
                while None in potomny1:
                    if potomny1[indeks] is None:
                        cykl += 1
                        start = indeks
                        while True:
                            potomny1[indeks] = (
                                rodzic1.genotyp[indeks]
                                if cykl % 2 == 1
                                else rodzic2.genotyp[indeks]
                            )
                            potomny2[indeks] = (
                                rodzic2.genotyp[indeks]
                                if cykl % 2 == 1
                                else rodzic1.genotyp[indeks]
                            )
                            indeks = rodzic1.genotyp.index(rodzic2.genotyp[indeks])
                            if indeks == start:
                                break
                    indeks = potomny1.index(None) if None in potomny1 else indeks

                rodzic1.genotyp = potomny1
                rodzic2.genotyp = potomny2

            case _:
                raise ValueError(f"Nieznany typ krzyzowania: {typ}")

    # Aktualizacja długości tras po krzyżowaniu
    for osobnik in populacja:
        osobnik.dlugosc_trasy = None  # Resetuj długość trasy
        instancja_populacji.oblicz_dlugosc_trasy(osobnik)

    return populacja


if __name__ == "__main__":

    populacja = Populacja(rozmiar_populacji, liczba_miast, macierz_odleglosci)

    print("Przed krzyżowaniem:")
    for i, osobnik in enumerate(populacja.osobniki):
        print(
            f"Osobnik {i + 1}: {osobnik.genotyp}, Długosc trasy: {osobnik.dlugosc_trasy}"
        )

    typ_krzyzowania = "OX"  # Do wyboru: "OX", "PMX" lub "CX"
    prawdopodobienstwo = 0.8
    populacja.osobniki = krzyzowanie_tsp(
        populacja.osobniki, prawdopodobienstwo, typ_krzyzowania, populacja
    )

    print("\nPo krzyżowaniu:")
    for i, osobnik in enumerate(populacja.osobniki):
        print(
            f"Osobnik {i + 1}: {osobnik.genotyp}, Długosc trasy: {osobnik.dlugosc_trasy}"
        )
