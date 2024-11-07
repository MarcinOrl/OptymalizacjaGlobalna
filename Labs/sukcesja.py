from main import Populacja
from config import rozmiar_populacji, dokladnosci, granice
from selekcja import selekcja_turniejowa, selekcja_rankingu, selekcja_ruletki
from mutacja_inwersja import mutacja, inwersja
from krzyzowanie import krzyzowanie
import random, copy


# Sukcesja z całkowitym zastąpieniwm - trywialna
def sukcesja_trywialna(populacja, liczba_epok, typ_selekcji, minimum):
    for epoka in range(liczba_epok):
        print(f"Epoka {epoka + 1}:")
        print(
            "Bazowa populacja:",
            *[f"{osobnik.wartosc_funkcji}" for osobnik in populacja.osobniki],
        )

        # Selekcja na podstawie wybranego typu
        match typ_selekcji:
            case "turniejowa":
                populacja.osobniki = selekcja_turniejowa(populacja.osobniki, minimum)
            case "rankingowa":
                populacja.osobniki = selekcja_rankingu(populacja.osobniki, minimum)
            case "ruletkowa":
                populacja.osobniki = selekcja_ruletki(populacja.osobniki, minimum)
            case _:
                raise ValueError("Nieznany typ selekcji")

        # Operacje genetyczne
        populacja.osobniki = mutacja(populacja.osobniki, 0.1)
        for osobnik in populacja.osobniki:
            populacja.dekoduj_osobnika(osobnik)

        populacja.osobniki = inwersja(populacja.osobniki, 0.1)
        for osobnik in populacja.osobniki:
            populacja.dekoduj_osobnika(osobnik)

        populacja.osobniki = krzyzowanie(populacja.osobniki, 0.5, "jednopunktowe")
        for osobnik in populacja.osobniki:
            populacja.dekoduj_osobnika(osobnik)

        # Aktualizacja wartości rzeczywistych i funkcji dla każdego osobnika po operacjach genetycznych
        for osobnik in populacja.osobniki:
            populacja.dekoduj_osobnika(osobnik)

    return populacja


# Sukcesja z częściowym zastępowaniem – elitarna
def sukcesja_elitarna(populacja, liczba_epok, typ_selekcji, minimum):
    for epoka in range(liczba_epok):
        print(f"Epoka {epoka + 1}:")

        # Zapamiętaj osobniki startowe przed selekcją
        osobniki_startowe = copy.deepcopy(populacja.osobniki)
        print(
            "Bazowa populacja:",
            *[f"{osobnik.wartosc_funkcji}" for osobnik in osobniki_startowe],
        )

        # Selekcja na podstawie wybranego typu
        match typ_selekcji:
            case "turniejowa":
                osobniki_selekcja = copy.deepcopy(
                    selekcja_turniejowa(populacja.osobniki, minimum)
                )
            case "rankingowa":
                osobniki_selekcja = copy.deepcopy(
                    selekcja_rankingu(populacja.osobniki, minimum)
                )
            case "ruletkowa":
                osobniki_selekcja = copy.deepcopy(
                    selekcja_ruletki(populacja.osobniki, minimum)
                )
            case _:
                raise ValueError("Nieznany typ selekcji")

        # Operacje genetyczne
        mutowane_osobniki = [
            os
            for os, os_orig in zip(
                mutacja(copy.deepcopy(osobniki_selekcja), 0.1), osobniki_selekcja
            )
            if os.genotyp != os_orig.genotyp
        ]
        for osobnik in mutowane_osobniki:
            populacja.dekoduj_osobnika(osobnik)

        inwertowane_osobniki = [
            os
            for os, os_orig in zip(
                inwersja(copy.deepcopy(osobniki_selekcja), 0.1), osobniki_selekcja
            )
            if os.genotyp != os_orig.genotyp
        ]
        for osobnik in inwertowane_osobniki:
            populacja.dekoduj_osobnika(osobnik)

        krzyzowane_osobniki = [
            os
            for os, os_orig in zip(
                krzyzowanie(copy.deepcopy(osobniki_selekcja), 0.5, "jednopunktowe"),
                osobniki_selekcja,
            )
            if os.genotyp != os_orig.genotyp
        ]
        for osobnik in krzyzowane_osobniki:
            populacja.dekoduj_osobnika(osobnik)

        # Aktualizacja wartości rzeczywistych i funkcji po operacjach
        for osobnik in (
            populacja.osobniki
            + mutowane_osobniki
            + inwertowane_osobniki
            + krzyzowane_osobniki
        ):
            populacja.dekoduj_osobnika(osobnik)

        # Kompilacja wszystkich osobników do selekcji elitarnej
        wszystkie_osobniki = (
            osobniki_startowe
            + mutowane_osobniki
            + inwertowane_osobniki
            + krzyzowane_osobniki
        )

        # print(
        #     f"{len(osobniki_startowe)}, {len(mutowane_osobniki)}, {len(inwertowane_osobniki)}, {len(krzyzowane_osobniki)}, {len(wszystkie_osobniki)}"
        # )

        # Sortowanie według funkcji przystosowania i wybór najlepszych
        wszystkie_osobniki.sort(key=lambda x: x.wartosc_funkcji, reverse=not minimum)
        populacja.osobniki = wszystkie_osobniki[: len(populacja.osobniki)]

        print(
            "Nowa populacja:", *[f"{os.wartosc_funkcji}" for os in populacja.osobniki]
        )

    return populacja


# Sukcesja z częściowym zastępowaniem – ze ściskiem
def sukcesja_ze_sciskiem(populacja, liczba_epok, typ_selekcji, minimum):
    # Usuwa podobnych osobników na podstawie progu podobieństwa
    pass


# Sukcesja z częściowym zastępowaniem – losowa
def sukcesja_losowa(populacja, liczba_epok, typ_selekcji, minimum):
    # Losowo usuwa określoną liczbę osobników, resztę uzupełnia potomną populacją
    pass


# Główna funkcja sukcesji
def sukcesja(populacja, liczba_epok, typ_sukcesji, typ_selekcji, minimum=True):
    match typ_sukcesji:
        case "trywialna":
            return sukcesja_trywialna(populacja, liczba_epok, typ_selekcji, minimum)
        case "elitarna":
            return (sukcesja_elitarna(populacja, liczba_epok, typ_selekcji, minimum),)
        case "ze_sciskiem":
            return (
                sukcesja_ze_sciskiem(populacja, liczba_epok, typ_selekcji, minimum),
            )
        case "losowa":
            return (sukcesja_losowa(populacja, liczba_epok, typ_selekcji, minimum),)
        case _:
            raise ValueError("Nieznany typ sukcesji")


if __name__ == "__main__":

    populacja = Populacja(rozmiar_populacji, granice, dokladnosci)
    sukcesja(populacja, 10, "elitarna", "ruletkowa", True)
