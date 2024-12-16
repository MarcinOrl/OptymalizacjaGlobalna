from config import rozmiar_puli_tras, liczba_miast, macierz_odleglosci
import random


class Trasa:
    def __init__(self, permutacja_miast):
        self.permutacja_miast = permutacja_miast
        self.dlugosc_trasy = None


class Pula_tras:
    def __init__(self, rozmiar, liczba_miast, macierz_odleglosci):
        self.liczba_miast = liczba_miast
        self.macierz_odleglosci = macierz_odleglosci
        self.trasy = [Trasa(self.generuj_permutacje()) for _ in range(rozmiar)]

        for trasa in self.trasy:
            self.oblicz_dlugosc_trasy(trasa)

    # Generuje losową permutację miast
    def generuj_permutacje(self):
        return random.sample(range(self.liczba_miast), self.liczba_miast)

    # Oblicza długość trasy dla danej trasy
    def oblicz_dlugosc_trasy(self, trasa):
        permutacja_miast = trasa.permutacja_miast
        dlugosc = 0
        for i in range(len(permutacja_miast)):
            miasto_a = permutacja_miast[i]
            miasto_b = permutacja_miast[(i + 1) % len(permutacja_miast)]
            dlugosc += self.macierz_odleglosci[miasto_a][miasto_b]
        trasa.dlugosc_trasy = dlugosc

    # Wyswietla permutacje i wartości dla wszystkich tras
    def wyswietl_pule_tras(self):
        for i, trasa in enumerate(self.trasy):
            print(
                f"Trasa {i + 1}: {trasa.permutacja_miast}, Długość trasy: {trasa.dlugosc_trasy}"
            )


if __name__ == "__main__":

    pula_tras = Pula_tras(rozmiar_puli_tras, liczba_miast, macierz_odleglosci)
    pula_tras.wyswietl_pule_tras()
