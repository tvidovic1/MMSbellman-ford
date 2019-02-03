import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

'''
def praviTabelu(niz, fig, ax, br_redova, indeks_promjene, kolona_promjene=1):
    df = pd.DataFrame(niz)
    boje_kolona = ["#AB0101", "#AB0101", "#AB0101"]
    boje_redova = [["#2C7BEE"] * 3] * br_redova
    t = ax.table(cellText=df.values,
                 cellColours=boje_redova,
                 cellLoc='center',
                 colWidths=[0.1, 0.1, 0.4],
                 colLabels=df.columns,
                 colColours=boje_kolona,
                 loc='center')
    t.scale(2, 2)
    if indeks_promjene != -1:
        t._cells[(indeks_promjene + 1, kolona_promjene)].set_facecolor("#D32C2C")

    plt.show(block=False)
    #plt.pause(0.001)
'''
class Graf:

    def __init__(self, cvorovi, daLiJeDigraf):
        self._V = cvorovi
        self._graf = []
        self.G = nx.Graph()
        self.valjda_valja = dict()
        self._daLijeDigraf = daLiJeDigraf
        self.prviput = True
        self.pos = None
    
    def getDaLiJeDigraf(self):
        return self._daLijeDigraf
        
    def dodajGranu(self, u, v, w):
        self._graf.append((u, v, w))
        self.G.add_edge(u, v, weight=w)
        self.valjda_valja[(u, v)] = w
        if self.getDaLiJeDigraf():
            self._graf.append((v, u, w))
            self.valjda_valja[(v, u)] = w
    
    def ispisiMinimalneUdaljenosti(self, udaljenosti):
        print("Cvor        Udaljenost od izvora")
        for i in range(self._V):
            if udaljenosti[i] == float("Inf"):
                print("%d\t\t\tinf" % (i))
            else:
                print("%d\t\t\t%d" % (i, udaljenosti[i]))
        return
    
    def ispisiPuteveDoCvorova(self, izvor, prethodnici):
        print("Cvor        Put do cvora")
        for i in range(self._V):
            if prethodnici[i] == float("Inf"):
                print("%d\t\tPut do cvora ne postoji!" % (i))
            else:
                print("%d\t\t" % (i), end = '')
                print(self.pronadjiPutDoCvora(i, izvor, prethodnici))
        return
        
    def pronadjiPutDoCvora(self, cvor, izvor, prethodnici):
        
        put = []
        
        if cvor == izvor:
            put = [izvor]
        else:
            put.append(cvor)
            trenutniCvor = cvor
            while True:
                
                put.append(prethodnici[trenutniCvor])
                trenutniCvor = prethodnici[trenutniCvor]
                if trenutniCvor == izvor:
                    break
 
        return self.okreniListu(put)
    
    def okreniListu(self, lista):
        novaLista = []
        
        for i in range(len(lista)):
            novaLista.append(lista[len(lista) - i - 1])
        
        return novaLista
            
    def Bellman_Ford(self, izvor):
        
        print(len(self._graf))
        
        udaljenosti = []
        for i in range(self._V):
            udaljenosti.append(float("Inf"))
        udaljenosti[izvor] = 0
        
        prethodnici = []
        for i in range(self._V):
            prethodnici.append(float("Inf"))
        prethodnici[izvor] = izvor

        korigiraneUdaljenosti = self._graf

        self.ispisiMinimalneUdaljenosti(udaljenosti)
        
        for i in range(self._V-1):
            
            dosloDoKorekcije = False
            
            for u, v, w in korigiraneUdaljenosti:
                
                if udaljenosti[u] != float("Inf") and udaljenosti[u] + w < udaljenosti[v]:
                    udaljenosti[v] = udaljenosti[u] + w
                    #kolona1[v] = str(udaljenosti[v])
                    #niz = {'Cilj': kolona0, 'Duzina': kolona1, 'Put': kolona2}
                    #praviTabelu(niz, fig, ax1, self._V, v)
                    prethodnici[v] = u
                    dosloDoKorekcije = True
                    
                    korigiraneUdaljenosti.append((u, v, w))

                    if self.getDaLiJeDigraf():
                        korigiraneUdaljenosti.append((v, u, w))
                    self.Crtaj(udaljenosti, (u, v))

            if dosloDoKorekcije == False:
                break

            #OVO JE EDNIN DIOOO, ISPISUJE TRENUTNE LAMBDE ZA SVAKU ITERACIJU
            self.ispisiMinimalneUdaljenosti(udaljenosti)
            
            
        
        if not self.getDaLiJeDigraf():
            for u, v, w in self._graf:
                if udaljenosti[u] != float("Inf") and udaljenosti[u] + w < udaljenosti[v]:
                    raise TypeError("Graf sadrzi ciklus negativne tezine!")
                    return
        
        self.ispisiPuteveDoCvorova(izvor, prethodnici)
        '''
        for i in range(self._V):
            if prethodnici[i] == float("Inf"):
                kolona2[i] = 'inf'
                niz = {'Cilj': kolona0, 'Duzina': kolona1, 'Put': kolona2}
                praviTabelu(niz, fig, ax1, self._V, i, 2)
            else:
                kolona2[i] = str(izvor)
                put = self.pronadjiPutDoCvora(i, izvor, prethodnici)
                prvi = 1
                for k in put:
                    if prvi != 1:
                        kolona2[i] = kolona2[i] + ' - '
                    kolona2[i] = kolona2[i] + str(k)
                    prvi = 0
                kolona2[i]= kolona2[i][1:]
                niz = {'Cilj': kolona0, 'Duzina': kolona1, 'Put': kolona2}
                praviTabelu(niz, fig, ax1, self._V, i, 2)
                '''

    def Crtaj(self, udaljenosti, par=0):
        elarge = [(u, v) for (u, v, d) in self.G.edges(data=True) if d['weight'] > 0 and (u,v) != par]
        esmall = [(u, v) for (u, v, d) in self.G.edges(data=True) if d['weight'] <= 0 and (u,v) != par]

        if self.prviput == True:
            self.pos = nx.spring_layout(self.G)  # positions for all nodes
            self.prviput = False
        # nodes
        nx.draw_networkx_nodes(self.G, self.pos, node_size=700, node_color='#21BAC9')
        # labels
        nx.draw_networkx_labels(self.G, self.pos, font_size=20, font_family='sans-serif')


        # edges
        #od_izvora = dict(zip([(0, v) for v in range(self._V)], udaljenosti)) #dictionary koji povezuje udaljenosti od izvora do svakog vrha, moze se iskoristiti za tabelu
        nx.draw_networkx_edges(self.G, self.pos, edgelist=elarge, width=4, alpha=0.5)
        nx.draw_networkx_edges(self.G, self.pos, edgelist=esmall, width=4, alpha=0.5)
        if par!= 0:
            nx.draw_networkx_edges(self.G, self.pos, edgelist=[par], width=4, alpha=1, edge_color='#BC1507')
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=self.valjda_valja)


        plt.axis('off')
        plt.show(block = False)
        #plt.draw() # draw the plot
        plt.pause(1)  # show it for
        plt.clf()

        return
      

'''
g = Graf(5, False) 
g.dodajGranu(0, 1, -1) 
g.dodajGranu(0, 2, 4) 
g.dodajGranu(1, 2, 3) 
g.dodajGranu(1, 3, 2) 
g.dodajGranu(1, 4, 2) 
g.dodajGranu(3, 2, 5) 
g.dodajGranu(3, 1, 1) 
g.dodajGranu(4, 3, -3) 
  

g.Bellman_Ford(0)


g1 = Graf(7, False)

g1.dodajGranu(0, 1, 6)
g1.dodajGranu(0, 2, 2)
g1.dodajGranu(0, 3, 16)
g1.dodajGranu(1, 3, 5)
g1.dodajGranu(1, 4, 4)
g1.dodajGranu(2, 1, 7)
g1.dodajGranu(2, 4, 3)
g1.dodajGranu(2, 5, 8)
g1.dodajGranu(3, 6, 3)
g1.dodajGranu(4, 3, 4)
g1.dodajGranu(4, 6, 10)
g1.dodajGranu(5, 6, 1)
    
g1.Bellman_Ford(1)

'''

g2 = Graf(12, True)

g2.dodajGranu(0, 1, 10)
g2.dodajGranu(0, 4, 2)
g2.dodajGranu(0, 5, 8)
g2.dodajGranu(1, 2, 2)
g2.dodajGranu(1, 5, 3)
g2.dodajGranu(2, 3, 2)
g2.dodajGranu(2, 5, 5)
g2.dodajGranu(2, 6, 1)
g2.dodajGranu(3, 6, 2)
g2.dodajGranu(3, 7, 9)
g2.dodajGranu(4, 5, 6)
g2.dodajGranu(4, 8, 1)
g2.dodajGranu(4, 9, 3)
g2.dodajGranu(5, 6, 3)
g2.dodajGranu(5, 9, 2)
g2.dodajGranu(6, 7, 10)
g2.dodajGranu(6, 9, 6)
g2.dodajGranu(6, 10, 9)
g2.dodajGranu(6, 11, 4)
g2.dodajGranu(7, 11, 5)
g2.dodajGranu(8, 9, 3)
g2.dodajGranu(9, 10, 2)
g2.dodajGranu(10, 11, 1)

g2.Bellman_Ford(0)




            