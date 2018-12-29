import matplotlib.pyplot as plt
import networkx as nx
class Graf:

    def __init__(self, cvorovi):
        self._V = cvorovi
        self._graf = []
        self.G = nx.Graph()

    def dodajGranu(self, u, v, w):
        self._graf.append((u, v, w))
        self.G.add_edge(u, v, weight=w)

    def ispisiMinimalneUdaljenosti(self, udaljenosti):
        print("Cvor        Udaljenost od izvora")
        for i in range(self._V):
            print("%d\t\t\t%d" % (i, udaljenosti[i]))
        return

    def Bellman_Ford(self, izvor):

        udaljenosti = []
        for i in range(self._V):
            udaljenosti.append(float("Inf"))
        udaljenosti[izvor] = 0

        korigiraneUdaljenosti = self._graf
        #print(korigiraneUdaljenosti)

        for i in range(self._V - 1):

            dosloDoKorekcije = False
            for u, v, w in korigiraneUdaljenosti:
                if udaljenosti[u] != float("Inf") and udaljenosti[u] + w < udaljenosti[v]:
                    udaljenosti[v] = udaljenosti[u] + w
                    dosloDoKorekcije = True
                    korigiraneUdaljenosti = []
                    korigiraneUdaljenosti.append((u, v, w))
                    print(udaljenosti)
            if dosloDoKorekcije == False:
                break

        for u, v, w in self._graf:
            if udaljenosti[u] != float("Inf") and udaljenosti[u] + w < udaljenosti[v]:
                raise TypeError("Graf sadrzi ciklus negativne tezine!")
                return

        self.ispisiMinimalneUdaljenosti(udaljenosti)
        self.Crtaj(udaljenosti)

    def Crtaj(self, udaljenosti):
        elarge = [(u, v) for (u, v, d) in self.G.edges(data=True) if d['weight'] > 0]
        esmall = [(u, v) for (u, v, d) in self.G.edges(data=True) if d['weight'] <= 0]

        pos = nx.shell_layout(self.G)  # positions for all nodes

        # nodes
        nx.draw_networkx_nodes(self.G, pos, node_size=700)

        # edges
        od_izvora = dict(zip([(0, v) for v in range(self._V)], udaljenosti)) #dictionary koji povezuje udaljenosti od izvora do svakog vrha, moze se iskoristiti za tabelu
        nx.draw_networkx_edges(self.G, pos, edgelist=elarge, width=6)
        nx.draw_networkx_edges(self.G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color='b', style='dashed')
        nx.draw_networkx_edge_labels(self.G, pos)

        # labels
        nx.draw_networkx_labels(self.G, pos, font_size=20, font_family='sans-serif')

        plt.axis('off')
        plt.show()
        #plt.draw() # draw the plot
        #plt.pause(2)  # show it for 5 seconds
        return


g = Graf(5)
g.dodajGranu(0, 1, -1)
g.dodajGranu(0, 2, 4)
g.dodajGranu(1, 2, 3)
g.dodajGranu(1, 3, 2)
g.dodajGranu(1, 4, 2)
g.dodajGranu(3, 2, 5)
g.dodajGranu(3, 1, 1)
g.dodajGranu(4, 3, -3)

g.Bellman_Ford(0)