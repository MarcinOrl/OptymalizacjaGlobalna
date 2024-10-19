from rastrigin import oblicz_bity, generuj_populacje
from config import rozmiar_populacji, dokladnosci, granice
from osobnik import Osobnik
import random


# Funkcja mutacji odwracająca bity w zależności od prawdopodobieństwa
def mutacja(populacja, prawdopodobienstwo):
    for osobnik in populacja:
        print(f"Przed mutacją: {osobnik.genotyp}")
        for i in range(len(osobnik.genotyp)):
            if random.random() < prawdopodobienstwo:
                osobnik.genotyp[i] = 1 - osobnik.genotyp[i]  # Odwracanie bitu
        print(f"Po mutacji:    {osobnik.genotyp}\n------------------------")
    return populacja


# Funkcja inwersji odwracająca kolejność bitów w wylosowanym przedziale
def inwersja(populacja, prawdopodobienstwo):
    for osobnik in populacja:
        if random.random() < prawdopodobienstwo:
            print(f"Przed inwersją: {osobnik.genotyp}")
            start = random.randint(0, len(osobnik.genotyp) - 2)
            end = random.randint(start + 1, len(osobnik.genotyp) - 1)
            osobnik.genotyp[start : end + 1] = osobnik.genotyp[start : end + 1][::-1]
            print(f"Po inwersji:    {osobnik.genotyp}\n------------------------")
    return populacja


if __name__ == "__main__":
    # Tworzenie populacji osobników
    liczba_bitow = [oblicz_bity(a, b, d) for (a, b), d in zip(granice, dokladnosci)]
    populacja = generuj_populacje(rozmiar_populacji, liczba_bitow)

    # Tworzenie instancji Osobnik
    populacja_osobnikow = [Osobnik(genotyp, liczba_bitow) for genotyp in populacja]

    # Wykonywanie mutacji i inwersji
    mutowana_populacja = mutacja(populacja_osobnikow, 0.1)
    inwertowana_populacja = inwersja(mutowana_populacja, 0.1)
