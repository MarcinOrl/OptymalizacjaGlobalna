import math


def rastrigin(x, A=10, omega=20 * math.pi, ranges=None, precision=None):
    if not isinstance(x, (list, tuple)):
        raise TypeError("Wektor x musi być listą lub krotką liczb.")

    n = len(x)

    # Jeśli ranges i precision nie zostały podane, ustaw domyślne wartości
    if ranges is None:
        ranges = [(-1, 1)] * n  # Domyślny zakres dla każdej zmiennej to [-1, 1]
    if precision is None:
        precision = [1] * n  # Domyślna precyzja (1 miejsce po przecinku)

    # Przekształcenie wartości x na podstawie kodowania binarnego i zakresów
    transformed_x = []
    for i, xi in enumerate(x):
        a, b = ranges[i]
        d = precision[i]

        # Liczba możliwych wartości na przedziale z dokładnością d miejsc po przecinku
        num_values = int((b - a) * 10**d) + 1

        # Zmienna xi powinna być w zakresie [0, num_values - 1] - konwersja do przedziału [a, b]
        xi_transformed = a + (b - a) * xi / (num_values - 1)
        transformed_x.append(xi_transformed)

    # Obliczenie wartości funkcji Rastrigina dla przekształconych wartości
    return A * n + sum([(xi**2 - A * math.cos(omega * xi)) for xi in transformed_x])


x = [1.0, 1.0]
result = rastrigin(x, ranges=[(-2, 2), (-2, 2)], precision=[1, 1])
print(f"Wynik dla x = {x}: {result}")
