import random
from rastrigin import oblicz_bity, generuj_populacje


def mutacja(populacja, prawdopodobienstwo):
    for osobnik in populacja:
        print(f"{osobnik} przed")
        for i in range(0, len(osobnik)):
            if random.random() < prawdopodobienstwo:
                if osobnik[i] == 0:
                    osobnik[i] = 1
                    print(f"zamieniono {i} na 1")
                else:
                    osobnik[i] = 0
                    print(f"zamieniono {i} na 0")
        print(f"{osobnik} po")
    return populacja


def inwersja(osobnik, prawdopodobienstwo):
    pass


# Parametry algorytmu
rozmiar_populacji = 3
dokladnosci = [1] * 3
granice = [(-1, 1)] * 3

liczba_bitow = [oblicz_bity(a, b, d) for (a, b), d in zip(granice, dokladnosci)]

populacja = generuj_populacje(rozmiar_populacji, liczba_bitow)

mutacja = mutacja(populacja, 0.1)
