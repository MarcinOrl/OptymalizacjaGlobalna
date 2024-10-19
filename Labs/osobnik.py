from rastrigin import dekoduj_osobnika, rastrigin
from config import granice


class Osobnik:
    def __init__(self, genotyp, liczba_bitow):
        self.genotyp = genotyp
        self.wartosci = dekoduj_osobnika(genotyp, granice, liczba_bitow)
        self.wartosc_funkcji = rastrigin(self.wartosci)
