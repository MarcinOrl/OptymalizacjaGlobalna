from config import rozmiar_populacji, liczba_miast, macierz_odleglosci
import random


class Osobnik:
    def __init__(self, genotyp):
        self.genotyp = genotyp
        self.dlugosc_trasy = None


class Populacja:
    def __init__(self, rozmiar, liczba_miast, macierz_odleglosci):
        self.liczba_miast = liczba_miast
        self.macierz_odleglosci = macierz_odleglosci
        self.osobniki = [Osobnik(self.generuj_permutacje()) for _ in range(rozmiar)]

        for osobnik in self.osobniki:
            self.oblicz_dlugosc_trasy(osobnik)

    # Generuje losową permutację miast
    def generuj_permutacje(self):
        return random.sample(range(self.liczba_miast), self.liczba_miast)

    # Oblicza długość trasy dla danego osobnika
    def oblicz_dlugosc_trasy(self, osobnik):
        trasa = osobnik.genotyp
        dlugosc = 0
        for i in range(len(trasa)):
            miasto_a = trasa[i]
            miasto_b = trasa[(i + 1) % len(trasa)]  # Powrót do początkowego miasta
            dlugosc += self.macierz_odleglosci[miasto_a][miasto_b]
        osobnik.dlugosc_trasy = dlugosc

    # Wyswietla genotypy i wartości dla wszystkich osobnikow
    def wyswietl_populacje(self):
        for i, osobnik in enumerate(self.osobniki):
            print(
                f"Osobnik {i + 1}: {osobnik.genotyp}, Długosc trasy: {osobnik.dlugosc_trasy}"
            )


if __name__ == "__main__":

    populacja = Populacja(rozmiar_populacji, liczba_miast, macierz_odleglosci)
    populacja.wyswietl_populacje()
