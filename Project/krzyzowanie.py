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
                rozmiar = len(rodzic1.genotyp)

                potomstwo1 = [None] * rozmiar
                potomstwo2 = [None] * rozmiar

                punkt1, punkt2 = sorted(random.sample(range(rozmiar), 2))

                potomstwo1[punkt1 : punkt2 + 1] = rodzic1.genotyp[punkt1 : punkt2 + 1]
                potomstwo2[punkt1 : punkt2 + 1] = rodzic2.genotyp[punkt1 : punkt2 + 1]

                idx = (punkt2 + 1) % rozmiar
                for miasto in rodzic2.genotyp:
                    if miasto not in potomstwo1:
                        potomstwo1[idx] = miasto
                        idx = (idx + 1) % rozmiar

                idx = (punkt2 + 1) % rozmiar
                for miasto in rodzic1.genotyp:
                    if miasto not in potomstwo2:
                        potomstwo2[idx] = miasto
                        idx = (idx + 1) % rozmiar

                rodzic1.genotyp = potomstwo1
                rodzic2.genotyp = potomstwo2

            case "PMX":
                # Krzyżowanie częściowo mieszane (Partially Mapped Crossover)
                rozmiar = len(rodzic1.genotyp)

                potomstwo1 = [None] * rozmiar
                potomstwo2 = [None] * rozmiar

                punkt1, punkt2 = sorted(random.sample(range(rozmiar), 2))

                for i in range(punkt1, punkt2 + 1):
                    if rodzic2.genotyp[i] in potomstwo1[punkt1 : punkt2 + 1]:
                        continue
                    value = rodzic2.genotyp[i]
                    while value in potomstwo1:
                        index = rodzic1.genotyp.index(value)
                        value = rodzic2.genotyp[index]
                    potomstwo1[rodzic2.genotyp.index(value)] = rodzic2.genotyp[i]

                for i in range(punkt1, punkt2 + 1):
                    if rodzic1.genotyp[i] in potomstwo2[punkt1 : punkt2 + 1]:
                        continue
                    value = rodzic1.genotyp[i]
                    while value in potomstwo2:
                        index = rodzic2.genotyp.index(value)
                        value = rodzic1.genotyp[index]
                    potomstwo2[rodzic1.genotyp.index(value)] = rodzic1.genotyp[i]

                for i in range(rozmiar):
                    if potomstwo1[i] is None:
                        potomstwo1[i] = rodzic2.genotyp[i]
                    if potomstwo2[i] is None:
                        potomstwo2[i] = rodzic1.genotyp[i]

                rodzic1.genotyp = potomstwo1
                rodzic2.genotyp = potomstwo2

            case "CX":
                # Krzyżowanie cykliczne (Cycle Crossover)
                rozmiar = len(rodzic1.genotyp)

                potomstwo1 = [None] * rozmiar
                potomstwo2 = [None] * rozmiar

                cykl = []
                indeks = 0

                while indeks not in cykl:
                    cykl.append(indeks)
                    miasto = rodzic1.genotyp[indeks]
                    indeks = rodzic2.genotyp.index(miasto)

                for i in cykl:
                    potomstwo1[i] = rodzic1.genotyp[i]

                for i in cykl:
                    potomstwo2[i] = rodzic2.genotyp[i]

                idx = 0
                for miasto in rodzic2.genotyp:
                    if miasto not in cykl:
                        while potomstwo1[idx] is not None:
                            idx = (idx + 1) % rozmiar
                        potomstwo1[idx] = miasto

                idx = 0
                for miasto in rodzic1.genotyp:
                    if miasto not in cykl:
                        while potomstwo2[idx] is not None:
                            idx = (idx + 1) % rozmiar
                        potomstwo2[idx] = miasto

                rodzic1.genotyp = potomstwo1
                rodzic2.genotyp = potomstwo2

            case _:
                raise ValueError(f"Nieznany typ krzyzowania: {typ}")

    # Aktualizacja długości tras po krzyżowaniu
    for osobnik in populacja:
        osobnik.dlugosc_trasy = None
        instancja_populacji.oblicz_dlugosc_trasy(osobnik)

    return populacja


if __name__ == "__main__":

    populacja = Populacja(rozmiar_populacji, liczba_miast, macierz_odleglosci)

    print("Przed krzyżowaniem:")
    for i, osobnik in enumerate(populacja.osobniki):
        print(
            f"Osobnik {i + 1}: {osobnik.genotyp}, Długosc trasy: {osobnik.dlugosc_trasy}"
        )

    typ_krzyzowania = "CX"  # Do wyboru: "OX", "PMX" lub "CX"
    prawdopodobienstwo = 0.8
    populacja.osobniki = krzyzowanie_tsp(
        populacja.osobniki, prawdopodobienstwo, typ_krzyzowania, populacja
    )

    print("\nPo krzyżowaniu:")
    for i, osobnik in enumerate(populacja.osobniki):
        print(
            f"Osobnik {i + 1}: {osobnik.genotyp}, Długosc trasy: {osobnik.dlugosc_trasy}"
        )
