from config import rozmiar_populacji, dokladnosci, granice
import random
import math


# Funkcja Rastrigina
def rastrigin(x):
    return 10 * len(x) + sum([xi**2 - 10 * math.cos(20 * math.pi * xi) for xi in x])


# Funkcja obliczająca minimalną liczbę bitów dla danego przedziału i dokładności
def oblicz_bity(a, b, d):
    liczba_wartosci = (b - a) * (10**d) + 1
    m = 1
    while not (2 ** (m - 1) <= liczba_wartosci <= 2**m):
        m += 1
    return m


# Funkcja tworząca losową populację binarną z różną liczbą bitów dla każdej zmiennej
def generuj_populacje(rozmiar_populacji, liczba_bitow):
    return [
        [
            random.randint(0, 1)
            for bity_zmiennej in liczba_bitow
            for _ in range(bity_zmiennej)
        ]
        for _ in range(rozmiar_populacji)
    ]


# Funkcja zamieniająca łańcuch binarny na wartość zmiennej w danym przedziale
def binarna_na_float(binarny_lancuch, granice):
    wartosc_dziesietna = int("".join(map(str, binarny_lancuch)), 2)
    dolna_granica, gorna_granica = granice
    maks_wartosc = 2 ** len(binarny_lancuch) - 1
    return (
        dolna_granica
        + (gorna_granica - dolna_granica) * wartosc_dziesietna / maks_wartosc
    )


# Funkcja konwertująca binarną reprezentację osobnika na wartości zmiennych w wielu wymiarach
def dekoduj_osobnika(osobnik, granice, liczba_bitow):
    zdekodowane = []
    start = 0
    for i, bity_zmiennej in enumerate(liczba_bitow):
        binarna_zmienna = osobnik[start : start + bity_zmiennej]
        wartosc = binarna_na_float(binarna_zmienna, granice[i])
        zdekodowane.append(wartosc)
        start += bity_zmiennej
    return zdekodowane


# Funkcja wyświetlająca populację z wartościami zmiennych
def wyswietl_populacje(populacja, granice, liczba_bitow):
    for i, osobnik in enumerate(populacja):
        wartosci_rzeczywiste = dekoduj_osobnika(osobnik, granice, liczba_bitow)
        print(
            f"Osobnik {i + 1}:\n    Binarnie: {osobnik}\n    Wartości rzeczywiste: {wartosci_rzeczywiste}"
        )
        print(f"    Wartość funkcji Rastrigina: {rastrigin(wartosci_rzeczywiste)}")


if __name__ == "__main__":
    # Obliczanie minimalnej liczby bitów dla każdej zmiennej
    liczba_bitow = [oblicz_bity(a, b, d) for (a, b), d in zip(granice, dokladnosci)]

    # Generowanie populacji
    populacja = generuj_populacje(rozmiar_populacji, liczba_bitow)

    # Wyświetlenie populacji
    wyswietl_populacje(populacja, granice, liczba_bitow)
