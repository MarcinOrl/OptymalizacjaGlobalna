from config import rozmiar_populacji, dokladnosci, granice
import random
import math


class Osobnik:
    def __init__(self, genotyp):
        self.genotyp = genotyp
        self.wartosci_rzeczywiste = []
        self.wartosc_funkcji = None


class Populacja:
    def __init__(self, rozmiar, granice, dokladnosci):
        self.granice = granice
        self.dokladnosci = dokladnosci
        self.liczba_bitow = [
            self.oblicz_bity(a, b, d) for (a, b), d in zip(granice, dokladnosci)
        ]
        self.osobniki = [Osobnik(self.generuj_genotyp()) for _ in range(rozmiar)]

        for osobnik in self.osobniki:
            self.dekoduj_osobnika(osobnik)

    # Oblicza liczbe bitów potrzebnych do przedstawienia liczby z zakresu [a, b] z dokładnością d
    def oblicz_bity(self, a, b, d):
        liczba_wartosci = (b - a) * (10**d) + 1
        m = 1
        while not (2 ** (m - 1) <= liczba_wartosci <= 2**m):
            m += 1
        return m

    # Generuje pojedynczy genotyp o odpowiedniej liczbie bitów
    def generuj_genotyp(self):
        return [
            random.randint(0, 1)
            for bity_zmiennej in self.liczba_bitow
            for _ in range(bity_zmiennej)
        ]

    # Dekoduje wartości genotypu osobnika i oblicza jego wartość funkcji
    def dekoduj_osobnika(self, osobnik):
        zdekodowane = []
        start = 0
        for i, bity_zmiennej in enumerate(self.liczba_bitow):
            binarna_zmienna = osobnik.genotyp[start : start + bity_zmiennej]
            wartosc = self.binarna_na_float(binarna_zmienna, self.granice[i])
            zdekodowane.append(round(wartosc, 4))
            start += bity_zmiennej
        osobnik.wartosci_rzeczywiste = zdekodowane
        osobnik.wartosc_funkcji = round(rastrigin(zdekodowane), 4)

    # Dekoduje binarny lancuch na float
    def binarna_na_float(self, binarny_lancuch, granica):
        wartosc_dziesietna = int("".join(map(str, binarny_lancuch)), 2)
        dolna_granica, gorna_granica = granica
        maks_wartosc = 2 ** len(binarny_lancuch) - 1
        return (
            dolna_granica
            + (gorna_granica - dolna_granica) * wartosc_dziesietna / maks_wartosc
        )

    # Wyswietla genotypy i wartości dla wszystkich osobnikow
    def wyswietl_populacje(self):
        for i, osobnik in enumerate(self.osobniki):
            self.dekoduj_osobnika(osobnik)
            print(
                f"Osobnik {i + 1}:\n    Binarnie: {osobnik.genotyp}\n    Wartości rzeczywiste: {osobnik.wartosci_rzeczywiste}"
            )
            print(f"    Wartość funkcji Rastrigina: {osobnik.wartosc_funkcji}")


# Funkcja Rastrigina
def rastrigin(x):
    return 10 * len(x) + sum([xi**2 - 10 * math.cos(20 * math.pi * xi) for xi in x])


if __name__ == "__main__":
    populacja = Populacja(rozmiar_populacji, granice, dokladnosci)
    populacja.wyswietl_populacje()
