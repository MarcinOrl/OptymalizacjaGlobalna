from main import Populacja
from config import rozmiar_populacji, dokladnosci, granice
from selekcja import selekcja_turniejowa, selekcja_rankingu, selekcja_ruletki
from mutacja_inwersja import mutacja, inwersja
from krzyzowanie import krzyzowanie
import random, copy


# Sprawdzanie podobieństwa genotypów
def porownaj_osobniki(osobnik1, osobnik2, prog_podobienstwa=0.1):
    roznice = sum(g1 != g2 for g1, g2 in zip(osobnik1.genotyp, osobnik2.genotyp))
    procent_roznicy = roznice / len(osobnik1.genotyp)
    return procent_roznicy < prog_podobienstwa


# Sukcesja z całkowitym zastąpieniwm - trywialna
def sukcesja_trywialna(populacja, liczba_epok, typ_selekcji, minimum):
    print(
        "Bazowa populacja:",
        *[f"{osobnik.wartosc_funkcji}" for osobnik in populacja.osobniki],
    )
    for epoka in range(liczba_epok):
        print(f"Epoka {epoka + 1}:")

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

        populacja.osobniki = inwersja(populacja.osobniki, 0.1)

        populacja.osobniki = krzyzowanie(populacja.osobniki, 0.5, "jednopunktowe")

        # Aktualizacja wartości rzeczywistych i funkcji dla każdego osobnika po operacjach genetycznych
        for osobnik in populacja.osobniki:
            populacja.dekoduj_osobnika(osobnik)

        print(
            "Nowa populacja:", *[f"{os.wartosc_funkcji}" for os in populacja.osobniki]
        )

    return populacja


# Sukcesja z częściowym zastępowaniem – elitarna
def sukcesja_elitarna(populacja, liczba_epok, typ_selekcji, minimum):
    print(
        "Bazowa populacja:",
        *[f"{osobnik.wartosc_funkcji}" for osobnik in populacja.osobniki],
    )
    for epoka in range(liczba_epok):
        print(f"Epoka {epoka + 1}:")

        # Zapamiętaj osobniki startowe przed selekcją
        osobniki_startowe = copy.deepcopy(populacja.osobniki)

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

        inwertowane_osobniki = [
            os
            for os, os_orig in zip(
                inwersja(copy.deepcopy(osobniki_selekcja), 0.1), osobniki_selekcja
            )
            if os.genotyp != os_orig.genotyp
        ]

        krzyzowane_osobniki = [
            os
            for os, os_orig in zip(
                krzyzowanie(copy.deepcopy(osobniki_selekcja), 0.5, "jednopunktowe"),
                osobniki_selekcja,
            )
            if os.genotyp != os_orig.genotyp
        ]

        # Kompilacja wszystkich osobników do selekcji elitarnej
        wszystkie_osobniki = (
            osobniki_startowe
            + mutowane_osobniki
            + inwertowane_osobniki
            + krzyzowane_osobniki
        )

        # Aktualizacja wartości rzeczywistych i funkcji po operacjach
        for osobnik in wszystkie_osobniki:
            populacja.dekoduj_osobnika(osobnik)

        # Sortowanie według funkcji przystosowania i wybór najlepszych
        wszystkie_osobniki.sort(key=lambda x: x.wartosc_funkcji, reverse=not minimum)
        populacja.osobniki = wszystkie_osobniki[: len(populacja.osobniki)]

        print(
            "Nowa populacja:", *[f"{os.wartosc_funkcji}" for os in populacja.osobniki]
        )

    return populacja


# Sukcesja z częściowym zastępowaniem – losowa
def sukcesja_losowa(populacja, liczba_epok, typ_selekcji, minimum):
    print(
        "Bazowa populacja:",
        *[f"{osobnik.wartosc_funkcji}" for osobnik in populacja.osobniki],
    )
    for epoka in range(liczba_epok):
        print(f"Epoka {epoka + 1}:")

        # Zapamiętaj osobniki startowe przed selekcją
        osobniki_startowe = copy.deepcopy(populacja.osobniki)

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

        inwertowane_osobniki = [
            os
            for os, os_orig in zip(
                inwersja(copy.deepcopy(osobniki_selekcja), 0.1), osobniki_selekcja
            )
            if os.genotyp != os_orig.genotyp
        ]

        krzyzowane_osobniki = [
            os
            for os, os_orig in zip(
                krzyzowanie(copy.deepcopy(osobniki_selekcja), 0.5, "jednopunktowe"),
                osobniki_selekcja,
            )
            if os.genotyp != os_orig.genotyp
        ]

        # Kompilacja wszystkich osobników do selekcji elitarnej
        wszystkie_osobniki = (
            osobniki_startowe
            + mutowane_osobniki
            + inwertowane_osobniki
            + krzyzowane_osobniki
        )

        # Aktualizacja wartości rzeczywistych i funkcji po operacjach
        for osobnik in wszystkie_osobniki:
            populacja.dekoduj_osobnika(osobnik)

        # Częściowe zastępowanie: usuwanie losowo wybranych osobników
        liczba_do_usuniecia = len(wszystkie_osobniki) - len(populacja.osobniki)
        indeksy_do_usuniecia = random.sample(
            range(len(wszystkie_osobniki)), liczba_do_usuniecia
        )

        # Nowa populacja po eliminacji losowej
        populacja.osobniki = [
            osobnik
            for i, osobnik in enumerate(wszystkie_osobniki)
            if i not in indeksy_do_usuniecia
        ][: len(populacja.osobniki)]

        print(
            "Nowa populacja:", *[f"{os.wartosc_funkcji}" for os in populacja.osobniki]
        )

    return populacja


# Główna funkcja sukcesji
def sukcesja(populacja, liczba_epok, typ_sukcesji, typ_selekcji, minimum=True):
    match typ_sukcesji:
        case "trywialna":
            return sukcesja_trywialna(populacja, liczba_epok, typ_selekcji, minimum)
        case "elitarna":
            return sukcesja_elitarna(populacja, liczba_epok, typ_selekcji, minimum)
        case "losowa":
            return sukcesja_losowa(populacja, liczba_epok, typ_selekcji, minimum)
        case _:
            raise ValueError("Nieznany typ sukcesji")


if __name__ == "__main__":

    typ_sukcesji = "elitarna"
    typ_selekcji = "ruletkowa"
    minimum = True
    liczba_epok = 10

    populacja = Populacja(rozmiar_populacji, granice, dokladnosci)
    populacja = sukcesja(populacja, liczba_epok, typ_sukcesji, typ_selekcji, minimum)
