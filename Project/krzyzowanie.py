from main import Pula_tras, Trasa
from config import rozmiar_puli_tras, liczba_miast, macierz_odleglosci
import random


def krzyzowanie_tsp(pula_tras, prawdopodobienstwo, typ, instancja_populacji):
    wylosowana_pula_tras = [
        trasa for trasa in pula_tras if random.random() < prawdopodobienstwo
    ]

    if len(wylosowana_pula_tras) % 2 == 1:
        wylosowana_pula_tras.pop(random.randint(0, len(wylosowana_pula_tras) - 1))

    random.shuffle(wylosowana_pula_tras)
    pary = [
        (wylosowana_pula_tras[i], wylosowana_pula_tras[i + 1])
        for i in range(0, len(wylosowana_pula_tras), 2)
    ]

    for rodzic1, rodzic2 in pary:
        match typ:
            case "OX":
                # Krzyżowanie jednokrotne (Order Crossover)
                rozmiar = len(rodzic1.permutacja_miast)

                potomstwo1 = [None] * rozmiar
                potomstwo2 = [None] * rozmiar

                punkt1, punkt2 = sorted(random.sample(range(rozmiar), 2))

                potomstwo1[punkt1 : punkt2 + 1] = rodzic1.permutacja_miast[
                    punkt1 : punkt2 + 1
                ]
                potomstwo2[punkt1 : punkt2 + 1] = rodzic2.permutacja_miast[
                    punkt1 : punkt2 + 1
                ]

                idx = (punkt2 + 1) % rozmiar
                for miasto in rodzic2.permutacja_miast:
                    if miasto not in potomstwo1:
                        potomstwo1[idx] = miasto
                        idx = (idx + 1) % rozmiar

                idx = (punkt2 + 1) % rozmiar
                for miasto in rodzic1.permutacja_miast:
                    if miasto not in potomstwo2:
                        potomstwo2[idx] = miasto
                        idx = (idx + 1) % rozmiar

                rodzic1.permutacja_miast = potomstwo1
                rodzic2.permutacja_miast = potomstwo2

            case "PMX":
                # Krzyżowanie częściowo mieszane (Partially Mapped Crossover)
                rozmiar = len(rodzic1.permutacja_miast)

                potomstwo1 = [None] * rozmiar
                potomstwo2 = [None] * rozmiar

                punkt1, punkt2 = sorted(random.sample(range(rozmiar), 2))

                for i in range(punkt1, punkt2 + 1):
                    if rodzic2.permutacja_miast[i] in potomstwo1[punkt1 : punkt2 + 1]:
                        continue
                    value = rodzic2.permutacja_miast[i]
                    while value in potomstwo1:
                        index = rodzic1.permutacja_miast.index(value)
                        value = rodzic2.permutacja_miast[index]
                    potomstwo1[rodzic2.permutacja_miast.index(value)] = (
                        rodzic2.permutacja_miast[i]
                    )

                for i in range(punkt1, punkt2 + 1):
                    if rodzic1.permutacja_miast[i] in potomstwo2[punkt1 : punkt2 + 1]:
                        continue
                    value = rodzic1.permutacja_miast[i]
                    while value in potomstwo2:
                        index = rodzic2.permutacja_miast.index(value)
                        value = rodzic1.permutacja_miast[index]
                    potomstwo2[rodzic1.permutacja_miast.index(value)] = (
                        rodzic1.permutacja_miast[i]
                    )

                for i in range(rozmiar):
                    if potomstwo1[i] is None:
                        potomstwo1[i] = rodzic2.permutacja_miast[i]
                    if potomstwo2[i] is None:
                        potomstwo2[i] = rodzic1.permutacja_miast[i]

                rodzic1.permutacja_miast = potomstwo1
                rodzic2.permutacja_miast = potomstwo2

            case "CX":
                # Krzyżowanie cykliczne (Cycle Crossover)
                rozmiar = len(rodzic1.permutacja_miast)

                potomstwo1 = [None] * rozmiar
                potomstwo2 = [None] * rozmiar

                cykl = []
                indeks = 0

                while indeks not in cykl:
                    cykl.append(indeks)
                    miasto = rodzic1.permutacja_miast[indeks]
                    indeks = rodzic2.permutacja_miast.index(miasto)

                for i in cykl:
                    potomstwo1[i] = rodzic1.permutacja_miast[i]

                for i in cykl:
                    potomstwo2[i] = rodzic2.permutacja_miast[i]

                idx = 0
                for miasto in rodzic2.permutacja_miast:
                    if miasto not in cykl:
                        while potomstwo1[idx] is not None:
                            idx = (idx + 1) % rozmiar
                        potomstwo1[idx] = miasto

                idx = 0
                for miasto in rodzic1.permutacja_miast:
                    if miasto not in cykl:
                        while potomstwo2[idx] is not None:
                            idx = (idx + 1) % rozmiar
                        potomstwo2[idx] = miasto

                rodzic1.permutacja_miast = potomstwo1
                rodzic2.permutacja_miast = potomstwo2

            case _:
                raise ValueError(f"Nieznany typ krzyzowania: {typ}")

    # Aktualizacja długości tras po krzyżowaniu
    for trasa in pula_tras:
        trasa.dlugosc_trasy = None
        instancja_populacji.oblicz_dlugosc_trasy(trasa)

    return pula_tras


if __name__ == "__main__":

    pula_tras = Pula_tras(rozmiar_puli_tras, liczba_miast, macierz_odleglosci)

    print("Przed krzyżowaniem:")
    for i, trasa in enumerate(pula_tras.trasy):
        print(
            f"Trasa {i + 1}: {trasa.permutacja_miast}, Długosc trasy: {trasa.dlugosc_trasy}"
        )

    typ_krzyzowania = "CX"  # Do wyboru: "OX", "PMX" lub "CX"
    prawdopodobienstwo = 0.8
    pula_tras.trasy = krzyzowanie_tsp(
        pula_tras.trasy, prawdopodobienstwo, typ_krzyzowania, pula_tras
    )

    print("\nPo krzyżowaniu:")
    for i, trasa in enumerate(pula_tras.trasy):
        print(
            f"Trasa {i + 1}: {trasa.permutacja_miast}, Długosc trasy: {trasa.dlugosc_trasy}"
        )
