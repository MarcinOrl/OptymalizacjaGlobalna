# Rozmiar puli tras
rozmiar_puli_tras = 10

# Liczba miast
liczba_miast = 5

# Macierze odległości
macierz_odleglosci_4 = [
    [0, 2, 9, 10],
    [2, 0, 6, 4],
    [9, 6, 0, 8],
    [10, 4, 8, 0],
]

macierz_odleglosci_5 = [
    [0, 2, 9, 10, 7],
    [2, 0, 6, 4, 3],
    [9, 6, 0, 8, 11],
    [10, 4, 8, 0, 5],
    [7, 3, 11, 5, 0],
]

macierz_odleglosci_7 = [
    [0, 5, 8, 6, 10, 9, 7],
    [5, 0, 4, 3, 7, 6, 8],
    [8, 4, 0, 7, 11, 10, 6],
    [6, 3, 7, 0, 5, 9, 8],
    [10, 7, 11, 5, 0, 4, 6],
    [9, 6, 10, 9, 4, 0, 5],
    [7, 8, 6, 8, 6, 5, 0],
]

macierz_odleglosci_10 = [
    [0, 2, 9, 10, 7, 11, 8, 13, 4, 6],
    [2, 0, 6, 4, 3, 5, 9, 12, 8, 7],
    [9, 6, 0, 8, 11, 7, 5, 10, 12, 9],
    [10, 4, 8, 0, 5, 9, 6, 8, 7, 11],
    [7, 3, 11, 5, 0, 4, 10, 14, 6, 9],
    [11, 5, 7, 9, 4, 0, 8, 13, 9, 10],
    [8, 9, 5, 6, 10, 8, 0, 7, 11, 12],
    [13, 12, 10, 8, 14, 13, 7, 0, 9, 5],
    [4, 8, 12, 7, 6, 9, 11, 9, 0, 3],
    [6, 7, 9, 11, 9, 10, 12, 5, 3, 0],
]

match liczba_miast:
    case 4:
        macierz_odleglosci = macierz_odleglosci_4
    case 5:
        macierz_odleglosci = macierz_odleglosci_5
    case 7:
        macierz_odleglosci = macierz_odleglosci_7
    case 10:
        macierz_odleglosci = macierz_odleglosci_10
    case _:
        raise ValueError("Nie obsługuję tej ilości miast")
