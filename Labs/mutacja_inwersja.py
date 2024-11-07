from main import Populacja
from config import rozmiar_populacji, dokladnosci, granice
import random


# Funkcja mutacji odwracająca bity w zależności od prawdopodobieństwa
def mutacja(populacja, prawdopodobienstwo):
    for osobnik in populacja:
        # print(f"Przed mutacją: {osobnik.genotyp}")
        for i in range(len(osobnik.genotyp)):
            if random.random() < prawdopodobienstwo:
                osobnik.genotyp[i] = 1 - osobnik.genotyp[i]  # Odwracanie bitu
        # print(f"Po mutacji:    {osobnik.genotyp}\n------------------------")

    return populacja


# Funkcja inwersji odwracająca kolejność bitów w wylosowanym przedziale
def inwersja(populacja, prawdopodobienstwo):
    for osobnik in populacja:
        if random.random() < prawdopodobienstwo:
            # print(f"Przed inwersją: {osobnik.genotyp}")
            start = random.randint(0, len(osobnik.genotyp) - 2)
            end = random.randint(start + 1, len(osobnik.genotyp) - 1)
            osobnik.genotyp[start : end + 1] = osobnik.genotyp[start : end + 1][::-1]
            # print(f"Po inwersji:    {osobnik.genotyp}\n------------------------")

    return populacja


if __name__ == "__main__":
    # Tworzenie populacji osobników
    populacja = Populacja(rozmiar_populacji, granice, dokladnosci)

    for i, osobnik in enumerate(populacja.osobniki):
        print(f"Wartość funkcji {i}: {osobnik.wartosc_funkcji}")
    # Wykonywanie mutacji i inwersji
    populacja.osobniki = mutacja(populacja.osobniki, 0.1)

    for osobnik in populacja.osobniki:
        populacja.dekoduj_osobnika(osobnik)

    for i, osobnik in enumerate(populacja.osobniki):
        print(f"Wartość funkcji {i}: {osobnik.wartosc_funkcji}")

    # inwertowana_populacja = inwersja(populacja.osobniki, 0.1)
