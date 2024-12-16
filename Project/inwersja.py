from main import Pula_tras
from config import rozmiar_puli_tras, liczba_miast, macierz_odleglosci
import random


# Funkcja inwersji odwracająca kolejność bitów w wylosowanym przedziale
def inwersja(pula_tras, prawdopodobienstwo):
    for trasa in pula_tras:
        if random.random() < prawdopodobienstwo:
            start = random.randint(0, len(trasa.permutacja_miast) - 2)
            end = random.randint(start + 1, len(trasa.permutacja_miast) - 1)
            trasa.permutacja_miast[start : end + 1] = trasa.permutacja_miast[
                start : end + 1
            ][::-1]

    return pula_tras


if __name__ == "__main__":
    # Tworzenie puli tras
    pula_tras = Pula_tras(rozmiar_puli_tras, liczba_miast, macierz_odleglosci)

    print("Przed inwersją:")
    for i, trasa in enumerate(pula_tras.trasy):
        print(
            f"Trasa {i + 1}: {trasa.permutacja_miast}, Długość trasy: {trasa.dlugosc_trasy}"
        )

    # Wykonywanie inwersji
    pula_tras.trasy = inwersja(pula_tras.trasy, 0.8)

    for trasa in pula_tras.trasy:
        pula_tras.oblicz_dlugosc_trasy(trasa)

    print("\nPo inwersji:")
    for i, trasa in enumerate(pula_tras.trasy):
        print(
            f"Trasa {i + 1}: {trasa.permutacja_miast}, Długość trasy: {trasa.dlugosc_trasy}"
        )
