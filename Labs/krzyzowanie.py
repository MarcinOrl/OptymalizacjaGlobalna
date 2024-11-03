from main import Populacja, Osobnik
from config import rozmiar_populacji, dokladnosci, granice
import random


def krzyzowanie_jednopunktowe(pary):
    nowa_populacja = []

    for rodzic1, rodzic2 in pary:
        print(f"Przed krzyzowaniem:\n {rodzic1.genotyp}, {rodzic2.genotyp}")
        punkt = random.randint(0, len(rodzic1.genotyp) - 1)
        nowy_osobnik1 = rodzic1.genotyp[:punkt] + rodzic2.genotyp[punkt:]
        nowy_osobnik2 = rodzic2.genotyp[:punkt] + rodzic1.genotyp[punkt:]
        nowa_populacja.append(Osobnik(nowy_osobnik1))
        nowa_populacja.append(Osobnik(nowy_osobnik2))
        print(
            f"Po krzyzowaniu:\nLosowy punkt: {punkt}\n {nowy_osobnik1}, {nowy_osobnik2}"
        )

    return nowa_populacja


def krzyzowanie_dwupunktowe(pary):
    nowa_populacja = []

    for rodzic1, rodzic2 in pary:
        print(f"Przed krzyzowaniem:\n {rodzic1.genotyp}, {rodzic2.genotyp}")
        punkt1 = random.randint(0, len(rodzic1.genotyp) - 1)
        punkt2 = random.randint(0, len(rodzic1.genotyp) - 1)
        if punkt1 > punkt2:
            punkt1, punkt2 = punkt2, punkt1
        nowy_osobnik1 = (
            rodzic1.genotyp[:punkt1]
            + rodzic2.genotyp[punkt1:punkt2]
            + rodzic1.genotyp[punkt2:]
        )
        nowy_osobnik2 = (
            rodzic2.genotyp[:punkt1]
            + rodzic1.genotyp[punkt1:punkt2]
            + rodzic2.genotyp[punkt2:]
        )
        nowa_populacja.append(Osobnik(nowy_osobnik1))
        nowa_populacja.append(Osobnik(nowy_osobnik2))
        print(
            f"Po krzyzowaniu:\nLosowe punkty: {punkt1}, {punkt2}\n {nowy_osobnik1}, {nowy_osobnik2}"
        )

    return nowa_populacja


def krzyzowanie_wielopunktowe(pary):
    nowa_populacja = []

    for rodzic1, rodzic2 in pary:
        print(f"Przed krzyzowaniem:\n {rodzic1.genotyp}, {rodzic2.genotyp}")
        liczba_punktow = random.randint(1, len(rodzic1.genotyp))
        punkty = sorted(random.sample(range(len(rodzic1.genotyp)), liczba_punktow))
        nowy_osobnik1 = []
        nowy_osobnik2 = []

        start = 0
        for punkt in punkty:
            if start % 2 == 0:
                nowy_osobnik1 += rodzic1.genotyp[start:punkt]
                nowy_osobnik2 += rodzic2.genotyp[start:punkt]
            else:
                nowy_osobnik1 += rodzic2.genotyp[start:punkt]
                nowy_osobnik2 += rodzic1.genotyp[start:punkt]
            start = punkt

        nowy_osobnik1 += rodzic1.genotyp[start:]
        nowy_osobnik2 += rodzic2.genotyp[start:]

        nowa_populacja.append(Osobnik(nowy_osobnik1))
        nowa_populacja.append(Osobnik(nowy_osobnik2))
        print(
            f"Po krzyzowaniu:\nLosowe punkty: {punkty}\n {nowy_osobnik1}, {nowy_osobnik2}"
        )

    return nowa_populacja


def krzyzowanie_rownomierne(pary):
    nowa_populacja = []

    for rodzic1, rodzic2 in pary:
        print(f"Przed krzyzowaniem:\n {rodzic1.genotyp},\n {rodzic2.genotyp}")
        wzorzec = [random.randint(0, 1) for _ in range(len(rodzic1.genotyp))]
        nowy_osobnik1 = [
            rodzic1.genotyp[i] if wzorzec[i] == 0 else rodzic2.genotyp[i]
            for i in range(len(rodzic1.genotyp))
        ]
        nowy_osobnik2 = [
            rodzic2.genotyp[i] if wzorzec[i] == 0 else rodzic1.genotyp[i]
            for i in range(len(rodzic1.genotyp))
        ]
        nowa_populacja.append(Osobnik(nowy_osobnik1))
        nowa_populacja.append(Osobnik(nowy_osobnik2))
        print(
            f"Po krzyzowaniu:\nWzorzec: {wzorzec}\n {nowy_osobnik1},\n {nowy_osobnik2}"
        )

    return nowa_populacja


def krzyzowanie(populacja, prawdopodobienstwo, typ):
    wylosowana_populacja = []

    for osobnik in populacja:
        if random.random() < prawdopodobienstwo:
            wylosowana_populacja.append(osobnik)
    if len(wylosowana_populacja) > 0:
        if len(wylosowana_populacja) % 2 == 1 and len(wylosowana_populacja) > 1:
            wylosowana_populacja.pop(random.randint(0, len(wylosowana_populacja) - 1))
        elif len(wylosowana_populacja) == 1:
            wylosowana_populacja.append()

    random.shuffle(wylosowana_populacja)
    pary = [
        (wylosowana_populacja[i], wylosowana_populacja[i + 1])
        for i in range(0, len(wylosowana_populacja), 2)
    ]

    match typ:
        case "jednopunktowe":
            krzyzowanie_jednopunktowe(pary)
        case "dwupunktowe":
            krzyzowanie_dwupunktowe(pary)
        case "wielopunktowe":
            krzyzowanie_wielopunktowe(pary)
        case "rownomierne":
            krzyzowanie_rownomierne(pary)
        case _:
            raise ValueError(f"Nieznany typ krzyzowania: {typ}")


if __name__ == "__main__":
    # Tworzenie populacji
    populacja = Populacja(rozmiar_populacji, granice, dokladnosci)

    # Wykonywanie krzyzowania
    krzyzowanie(populacja.osobniki, 0.5, "jednopunktowe")
