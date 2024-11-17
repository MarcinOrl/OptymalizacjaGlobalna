from main import Populacja, Osobnik
from config import rozmiar_populacji, dokladnosci, granice
import random


def krzyzowanie(populacja, prawdopodobienstwo, typ):
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
            case "jednopunktowe":
                punkt = random.randint(0, len(rodzic1.genotyp) - 1)
                # print(f"Punkt: {punkt}")
                # print(f"Przed krzyżowaniem: {rodzic1.genotyp}, {rodzic2.genotyp}")
                rodzic1.genotyp[punkt:], rodzic2.genotyp[punkt:] = (
                    rodzic2.genotyp[punkt:],
                    rodzic1.genotyp[punkt:],
                )
                # print(f"Po krzyżowaniu:     {rodzic1.genotyp}, {rodzic2.genotyp}")
            case "dwupunktowe":
                punkt1, punkt2 = sorted(random.sample(range(len(rodzic1.genotyp)), 2))
                # print(f"Punkty: {punkt1}, {punkt2}")
                # print(f"Przed krzyżowaniem: {rodzic1.genotyp}, {rodzic2.genotyp}")
                rodzic1.genotyp[punkt1:punkt2], rodzic2.genotyp[punkt1:punkt2] = (
                    rodzic2.genotyp[punkt1:punkt2],
                    rodzic1.genotyp[punkt1:punkt2],
                )
                # print(f"Po krzyżowaniu:     {rodzic1.genotyp}, {rodzic2.genotyp}")
            case "wielopunktowe":
                liczba_punktow = random.randint(1, len(rodzic1.genotyp))
                punkty = sorted(
                    random.sample(range(len(rodzic1.genotyp)), liczba_punktow)
                )
                # print(f"Punkty: {punkty}")
                # print(f"Przed krzyżowaniem: {rodzic1.genotyp}, {rodzic2.genotyp}")
                start = 0
                for i, punkt in enumerate(punkty):
                    if i % 2 == 0:
                        rodzic1.genotyp[start:punkt], rodzic2.genotyp[start:punkt] = (
                            rodzic2.genotyp[start:punkt],
                            rodzic1.genotyp[start:punkt],
                        )
                    start = punkt
                # print(f"Po krzyżowaniu:     {rodzic1.genotyp}, {rodzic2.genotyp}")
            case "rownomierne":
                wzorzec = [random.randint(0, 1) for _ in range(len(rodzic1.genotyp))]
                # print(f"Wzorzec: {wzorzec}")
                # print(f"Przed krzyżowaniem: {rodzic1.genotyp}, {rodzic2.genotyp}")
                nowy_genotyp1 = [
                    rodzic1.genotyp[i] if wzorzec[i] == 0 else rodzic2.genotyp[i]
                    for i in range(len(rodzic1.genotyp))
                ]
                nowy_genotyp2 = [
                    rodzic2.genotyp[i] if wzorzec[i] == 0 else rodzic1.genotyp[i]
                    for i in range(len(rodzic2.genotyp))
                ]
                rodzic1.genotyp = nowy_genotyp1
                rodzic2.genotyp = nowy_genotyp2
                # print(f"Po krzyżowaniu:     {rodzic1.genotyp}, {rodzic2.genotyp}")
            case _:
                raise ValueError(f"Nieznany typ krzyzowania: {typ}")

    return populacja


if __name__ == "__main__":
    # Tworzenie populacji
    populacja = Populacja(rozmiar_populacji, granice, dokladnosci)

    # for i, osobnik in enumerate(populacja.osobniki):
    #     print(f"Osobnik {i + 1}: {osobnik.genotyp}")
    # Wykonywanie krzyzowania
    krzyzowanie(populacja.osobniki, 0.5, "jednopunktowe")

    # for i, osobnik in enumerate(populacja.osobniki):
    #     print(f"Osobnik {i + 1}: {osobnik.genotyp}")
