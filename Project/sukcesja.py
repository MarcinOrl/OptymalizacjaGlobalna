from main import Pula_tras
from config import rozmiar_puli_tras, liczba_miast, macierz_odleglosci
from selekcja import selekcja_turniejowa, selekcja_rankingu, selekcja_ruletki
from inwersja import inwersja
from krzyzowanie import krzyzowanie_tsp
import random, copy


# Sukcesja z całkowitym zastąpieniwm - trywialna
def sukcesja_trywialna(pula_tras, liczba_epok, typ_selekcji):
    print(
        "Bazowa pula tras:",
        *[f"{trasa.dlugosc_trasy}" for trasa in pula_tras.trasy],
    )
    for epoka in range(liczba_epok):
        print(f"Epoka {epoka + 1}:")

        # Selekcja na podstawie wybranego typu
        match typ_selekcji:
            case "turniejowa":
                pula_tras.trasy = selekcja_turniejowa(pula_tras.trasy)
            case "rankingowa":
                pula_tras.trasy = selekcja_rankingu(pula_tras.trasy)
            case "ruletkowa":
                pula_tras.trasy = selekcja_ruletki(pula_tras.trasy)
            case _:
                raise ValueError("Nieznany typ selekcji")

        # Operacje genetyczne
        pula_tras.trasy = inwersja(pula_tras.trasy, 0.1)

        pula_tras.trasy = krzyzowanie_tsp(pula_tras.trasy, 0.5, "OX", pula_tras)

        for trasa in pula_tras.trasy:
            pula_tras.oblicz_dlugosc_trasy(trasa)

        print("Nowa pula tras:", *[f"{os.dlugosc_trasy}" for os in pula_tras.trasy])

    return pula_tras


# Sukcesja z częściowym zastępowaniem – elitarna
def sukcesja_elitarna(pula_tras, liczba_epok, typ_selekcji):
    print(
        "Bazowa pula tras:",
        *[f"{trasa.dlugosc_trasy}" for trasa in pula_tras.trasy],
    )
    for epoka in range(liczba_epok):
        print(f"Epoka {epoka + 1}:")

        # Zapamiętaj trasy startowe przed selekcją
        trasy_startowe = copy.deepcopy(pula_tras.trasy)

        # Selekcja na podstawie wybranego typu
        match typ_selekcji:
            case "turniejowa":
                trasy_selekcja = copy.deepcopy(selekcja_turniejowa(pula_tras.trasy))
            case "rankingowa":
                trasy_selekcja = copy.deepcopy(selekcja_rankingu(pula_tras.trasy))
            case "ruletkowa":
                trasy_selekcja = copy.deepcopy(selekcja_ruletki(pula_tras.trasy))
            case _:
                raise ValueError("Nieznany typ selekcji")

        # Operacje genetyczne
        inwertowane_trasy = [
            os
            for os, os_orig in zip(
                inwersja(copy.deepcopy(trasy_selekcja), 0.1), trasy_selekcja
            )
            if os.permutacja_miast != os_orig.permutacja_miast
        ]

        krzyzowane_trasy = [
            os
            for os, os_orig in zip(
                krzyzowanie_tsp(copy.deepcopy(trasy_selekcja), 0.5, "OX", pula_tras),
                trasy_selekcja,
            )
            if os.permutacja_miast != os_orig.permutacja_miast
        ]

        # Kompilacja wszystkich osobników do selekcji elitarnej
        wszystkie_trasy = trasy_startowe + inwertowane_trasy + krzyzowane_trasy

        for trasa in wszystkie_trasy:
            pula_tras.oblicz_dlugosc_trasy(trasa)

        # Sortowanie według funkcji przystosowania i wybór najlepszych
        wszystkie_trasy.sort(key=lambda x: x.dlugosc_trasy, reverse=False)
        pula_tras.trasy = wszystkie_trasy[: len(pula_tras.trasy)]

        print("Nowa pula tras:", *[f"{os.dlugosc_trasy}" for os in pula_tras.trasy])

    return pula_tras


# Sukcesja z częściowym zastępowaniem – losowa
def sukcesja_losowa(pula_tras, liczba_epok, typ_selekcji):
    print(
        "Bazowa pula tras:",
        *[f"{trasa.dlugosc_trasy}" for trasa in pula_tras.trasy],
    )
    for epoka in range(liczba_epok):
        print(f"Epoka {epoka + 1}:")

        # Zapamiętaj trasy startowe przed selekcją
        trasy_startowe = copy.deepcopy(pula_tras.trasy)

        # Selekcja na podstawie wybranego typu
        match typ_selekcji:
            case "turniejowa":
                trasy_selekcja = copy.deepcopy(selekcja_turniejowa(pula_tras.trasy))
            case "rankingowa":
                trasy_selekcja = copy.deepcopy(selekcja_rankingu(pula_tras.trasy))
            case "ruletkowa":
                trasy_selekcja = copy.deepcopy(selekcja_ruletki(pula_tras.trasy))
            case _:
                raise ValueError("Nieznany typ selekcji")

        # Operacje genetyczne
        inwertowane_trasy = [
            os
            for os, os_orig in zip(
                inwersja(copy.deepcopy(trasy_selekcja), 0.1), trasy_selekcja
            )
            if os.permutacja_miast != os_orig.permutacja_miast
        ]

        krzyzowane_trasy = [
            os
            for os, os_orig in zip(
                krzyzowanie_tsp(copy.deepcopy(trasy_selekcja), 0.5, "OX", pula_tras),
                trasy_selekcja,
            )
            if os.permutacja_miast != os_orig.permutacja_miast
        ]

        # Kompilacja wszystkich osobników do selekcji elitarnej
        wszystkie_trasy = trasy_startowe + inwertowane_trasy + krzyzowane_trasy

        for trasa in wszystkie_trasy:
            pula_tras.oblicz_dlugosc_trasy(trasa)

        # Częściowe zastępowanie: usuwanie losowo wybranych osobników
        liczba_do_usuniecia = len(wszystkie_trasy) - len(pula_tras.trasy)
        indeksy_do_usuniecia = random.sample(
            range(len(wszystkie_trasy)), liczba_do_usuniecia
        )

        # Nowa pula_tras po eliminacji losowej
        pula_tras.trasy = [
            trasa
            for i, trasa in enumerate(wszystkie_trasy)
            if i not in indeksy_do_usuniecia
        ][: len(pula_tras.trasy)]

        print("Nowa pula tras:", *[f"{os.dlugosc_trasy}" for os in pula_tras.trasy])

    return pula_tras


# Główna funkcja sukcesji
def sukcesja(pula_tras, liczba_epok, typ_sukcesji, typ_selekcji):
    match typ_sukcesji:
        case "trywialna":
            return sukcesja_trywialna(pula_tras, liczba_epok, typ_selekcji)
        case "elitarna":
            return sukcesja_elitarna(pula_tras, liczba_epok, typ_selekcji)
        case "losowa":
            return sukcesja_losowa(pula_tras, liczba_epok, typ_selekcji)
        case _:
            raise ValueError("Nieznany typ sukcesji")


if __name__ == "__main__":

    typ_sukcesji = "trywialna"
    typ_selekcji = "turniejowa"
    liczba_epok = 10

    pula_tras = Pula_tras(rozmiar_puli_tras, liczba_miast, macierz_odleglosci)
    pula_tras = sukcesja(pula_tras, liczba_epok, typ_sukcesji, typ_selekcji)
