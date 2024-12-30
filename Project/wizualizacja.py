import matplotlib.pyplot as plt
import networkx as nx
from main import Pula_tras, rozmiar_puli_tras, liczba_miast, macierz_odleglosci
from sukcesja import sukcesja


class GrafTrasy:
    def rysuj_graf(trasa, liczba_miast, macierz_odleglosci):
        G = nx.Graph()

        # Dodanie węzłów
        G.add_nodes_from(range(1, liczba_miast + 1))

        # Dodanie krawędzi zgodnie z trasą i ich wag (odległości)
        permutacja = trasa.permutacja_miast
        edges_in_trasa = [
            (
                permutacja[i],
                permutacja[(i + 1) % liczba_miast],
                {
                    "weight": macierz_odleglosci[permutacja[i] - 1][
                        permutacja[(i + 1) % liczba_miast] - 1
                    ]
                },
            )
            for i in range(len(permutacja))
        ]
        G.add_edges_from(edges_in_trasa)

        # Dodanie pozostałych krawędzi (nie w trasie) z innym kolorem
        all_edges = [
            (i + 1, j + 1, {"weight": macierz_odleglosci[i][j]})
            for i in range(liczba_miast)
            for j in range(i + 1, liczba_miast)
        ]
        edges_outside_trasa = [edge for edge in all_edges if edge not in edges_in_trasa]
        G.add_edges_from(edges_outside_trasa)

        # miasta
        pos = nx.spring_layout(G, seed=42)  # Układ węzłów

        # węzły
        nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=500)

        # krawędzie z trasy
        nx.draw_networkx_edges(
            G, pos, edgelist=[(u, v) for u, v, d in edges_in_trasa], edge_color="blue"
        )

        # pozostałe krawędzi
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=[(u, v) for u, v, d in edges_outside_trasa],
            edge_color="gray",
            style="dashed",
        )

        # wagi
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels={(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)},
        )

        # etykiety węzłów
        nx.draw_networkx_labels(G, pos)

        plt.title("Graf trasy z odległościami")
        plt.show()


class Statystyki:
    def __init__(self):
        self.dlugosci_trasy = (
            []
        )  # Lista przechowująca średnie długości tras w każdej epoce
        self.najlepsza_trasa = None  # Najlepsza znaleziona trasa

    def zbierz_statystyki(self, pula_tras, epoka):
        dlugosci = [trasa.dlugosc_trasy for trasa in pula_tras.trasy]
        srednia_dlugosc = sum(dlugosci) / len(dlugosci)
        najlepsza = min(pula_tras.trasy, key=lambda t: t.dlugosc_trasy)

        self.dlugosci_trasy.append((epoka, srednia_dlugosc))

        if (
            self.najlepsza_trasa is None
            or najlepsza.dlugosc_trasy < self.najlepsza_trasa.dlugosc_trasy
        ):
            self.najlepsza_trasa = najlepsza

        print(f"Epoka {epoka}: Średnia długość trasy = {srednia_dlugosc}")

    def rysuj_statystyki(self):
        epoki, srednie_dlugosci = zip(*self.dlugosci_trasy)

        plt.plot(epoki, srednie_dlugosci, marker="o", label="Średnia długość trasy")
        plt.xlabel("Epoka")
        plt.ylabel("Średnia długość trasy")
        plt.title("Statystyki z kolejnych epok")
        plt.legend()
        plt.grid()
        plt.show()


if __name__ == "__main__":

    pula_tras = Pula_tras(rozmiar_puli_tras, liczba_miast, macierz_odleglosci)
    statystyki = Statystyki()

    liczba_epok = 100
    for epoka in range(1, liczba_epok + 1):

        sukcesja(pula_tras, 1, "elitarna", "turniejowa")

        statystyki.zbierz_statystyki(pula_tras, epoka)

    statystyki.rysuj_statystyki()

    # Rysowanie grafu najlepszej trasy
    if statystyki.najlepsza_trasa:
        print(
            "Najlepsza znaleziona trasa:", statystyki.najlepsza_trasa.permutacja_miast
        )
        GrafTrasy.rysuj_graf(
            statystyki.najlepsza_trasa, liczba_miast, macierz_odleglosci
        )
