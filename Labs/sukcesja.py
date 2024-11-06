from main import Populacja
from config import rozmiar_populacji, dokladnosci, granice
from selekcja import selekcja_turniejowa, selekcja_rankingu, selekcja_ruletki
import random


# Sukcesja z całkowitym zastąpieniwm - trywialna
def sukcesja_trywialna(populacja_bazowa, liczba_epok, typ_selekcji, minimum):
    populacja = populacja_bazowa
    for epoka in range(liczba_epok):
        print(f"Epoka {epoka + 1}:")
        print(*[f"{osobnik.wartosc_funkcji}" for osobnik in populacja])

        match typ_selekcji:
            case "turniejowa":
                populacja = selekcja_turniejowa(populacja, minimum)
            case "rankingowa":
                populacja = selekcja_rankingu(populacja, minimum)
            case "ruletkowa":
                populacja = selekcja_ruletki(populacja, minimum)
            case _:
                raise ValueError("Nieznany typ selekcji")

    return populacja


# Sukcesja z częściowym zastępowaniem – elitarna
def sukcesja_elitarna(
    populacja_bazowa,
    liczba_epok,
    typ_selekcji,
    minimum,
    liczba_najlepszych,
):
    # Zachowuje najlepszych osobników z bazowej i uzupełnia ich najlepszymi z potomnej
    pass


# Sukcesja z częściowym zastępowaniem – ze ściskiem
def sukcesja_ze_sciskiem(
    populacja_bazowa,
    liczba_epok,
    typ_selekcji,
    minimum,
    próg_podobieństwa,
):
    # Usuwa podobnych osobników na podstawie progu podobieństwa
    pass


# Sukcesja z częściowym zastępowaniem – losowa
def sukcesja_losowa(
    populacja_bazowa,
    liczba_epok,
    typ_selekcji,
    minimum,
    liczba_do_usuniecia,
):
    # Losowo usuwa określoną liczbę osobników, resztę uzupełnia potomną populacją
    pass


# Główna funkcja sukcesji
def sukcesja(populacja_bazowa, liczba_epok, typ_sukcesji, typ_selekcji, minimum=True):
    match typ_sukcesji:
        case "trywialna":
            return sukcesja_trywialna(
                populacja_bazowa, liczba_epok, typ_selekcji, minimum
            )
        case "elitarna":
            return (
                sukcesja_elitarna(populacja_bazowa, liczba_epok, typ_selekcji, minimum),
            )
        case "ze_sciskiem":
            return (
                sukcesja_ze_sciskiem(
                    populacja_bazowa, liczba_epok, typ_selekcji, minimum
                ),
            )
        case "losowa":
            return (
                sukcesja_losowa(populacja_bazowa, liczba_epok, typ_selekcji, minimum),
            )
        case _:
            raise ValueError("Nieznany typ sukcesji")


if __name__ == "__main__":

    populacja = Populacja(rozmiar_populacji, granice, dokladnosci)
    sukcesja(populacja.osobniki, 10, "trywialna", "turniejowa", True)
