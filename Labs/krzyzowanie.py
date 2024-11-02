from rastrigin import generuj_populacje, oblicz_bity
from config import rozmiar_populacji, dokladnosci, granice
from osobnik import Osobnik
import random


def krzyzowanie(populacja, prawdopodobienstwo, liczba_punktow, liczba_bitow):
    wylosowana_populacja = []
    nowa_populacja = []
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
    for osobnik1, osobnik2 in pary:
        print(f"Przed krzyzowaniem:\n {osobnik1.genotyp}, {osobnik2.genotyp}")
        punkt = random.randint(0, len(osobnik1.genotyp) - 1)
        nowy_osobnik1 = osobnik1.genotyp[:punkt] + osobnik2.genotyp[punkt:]
        nowy_osobnik2 = osobnik2.genotyp[:punkt] + osobnik1.genotyp[punkt:]
        nowa_populacja.append(Osobnik(nowy_osobnik1, liczba_bitow))
        nowa_populacja.append(Osobnik(nowy_osobnik2, liczba_bitow))
        print(f"Po krzyzowaniu:\n {nowy_osobnik1}, {nowy_osobnik2}")
    return nowa_populacja


if __name__ == "__main__":
    liczba_bitow = [oblicz_bity(a, b, d) for (a, b), d in zip(granice, dokladnosci)]

    populacja = generuj_populacje(rozmiar_populacji, liczba_bitow)

    populacja_osobnikow = [Osobnik(genotyp, liczba_bitow) for genotyp in populacja]

    print(krzyzowanie(populacja_osobnikow, 0.5, 1, liczba_bitow))
