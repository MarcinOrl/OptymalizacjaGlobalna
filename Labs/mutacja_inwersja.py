from rastrigin import oblicz_bity, generuj_populacje
from config import rozmiar_populacji, dokladnosci, granice
import random


# Funkcja mutacji odwracająca bity w zależności od prawdopodobienstwa
def mutacja(populacja, prawdopodobienstwo):
    for osobnik in populacja:
        print(f"Przed mutacja: {osobnik}")
        for i in range(0, len(osobnik)):
            if random.random() < prawdopodobienstwo:
                if osobnik[i] == 0:
                    osobnik[i] = 1
                else:
                    osobnik[i] = 0
        print(f"Po mutacji:    {osobnik}\n------------------------")
    return populacja


# Funkcja inwersji odwracająca kolejność bitów w wylosowanym przedziale
def inwersja(osobnik, prawdopodobienstwo):
    for osobnik in populacja:
        if random.random() < prawdopodobienstwo:
            print(f"Przed inwersją: {osobnik}")
            start = random.randint(0, len(osobnik) - 2)
            end = random.randint(start + 1, len(osobnik) - 1)
            osobnik[start : end + 1] = osobnik[start : end + 1][::-1]
            print(f"Po inwersji:    {osobnik}\n------------------------")
    return populacja


if __name__ == "__main__":

    liczba_bitow = [oblicz_bity(a, b, d) for (a, b), d in zip(granice, dokladnosci)]

    populacja = generuj_populacje(rozmiar_populacji, liczba_bitow)

    mutacja = mutacja(populacja, 0.1)

    inwersja = inwersja(populacja, 0.1)
