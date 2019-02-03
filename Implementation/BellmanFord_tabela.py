import pandas as pd
import matplotlib.pyplot as plt

def praviTabelu(niz, fig, ax, br_redova, indeks_promjene, kolona_promjene=1):
    df = pd.DataFrame(niz)
    boje_kolona =  ["#AB0101","#AB0101","#AB0101"]
    boje_redova =  [["#2C7BEE"]*3]*br_redova
    t = ax.table(cellText=df.values, 
            cellColours=boje_redova, 
            cellLoc='center', 
            colWidths=[0.1, 0.1, 0.4],
            colLabels=df.columns, 
            colColours=boje_kolona, 
            loc='center')
    t.scale(2,2)
    if indeks_promjene != -1:
        t._cells[(indeks_promjene+1, kolona_promjene)].set_facecolor("#D32C2C")
        
    plt.show(block = False)
    plt.pause(0.001)
    #plt.hold()

class Graf:
    
    def __init__(self, cvorovi, daLiJeDigraf):
        self._V = cvorovi
        self._graf = []
        self._daLijeDigraf = daLiJeDigraf
        
    def getDaLiJeDigraf(self):
        return self._daLijeDigraf
        
    def dodajGranu(self, u, v, w):
        self._graf.append((u, v, w))
        if self.getDaLiJeDigraf():
            self._graf.append((v, u, w))
    
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
                #print("%d\t\t" % (i), end = '')
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
        
        #print(len(self._graf))
        
        udaljenosti = []
        for i in range(self._V):
            udaljenosti.append(float("Inf")) 
        udaljenosti[izvor] = 0
        
        prethodnici = []
        for i in range(self._V):
            prethodnici.append(float("Inf"))
        prethodnici[izvor] = izvor
        
        korigiraneUdaljenosti = self._graf
        
        kolona0 = []
        kolona1 = []
        kolona2 = []
        for i in range(self._V):
            kolona0.append(str(i))
            kolona1.append('inf')
            kolona2.append(str(0))
        niz = {'Cilj': kolona0, 'Duzina': kolona1, 'Put': kolona2}   
            
        fig, ax = plt.subplots()
        fig.patch.set_visible(False)
        ax.axis('off')
        praviTabelu(niz, fig, ax, self._V, -1)
        
        kolona1[izvor] = 0
        kolona2[izvor] = str(izvor)
        niz = {'Cilj': kolona0, 'Duzina': kolona1, 'Put': kolona2}
        praviTabelu(niz, fig, ax, self._V, izvor)
        
        #self.ispisiMinimalneUdaljenosti(udaljenosti)
        
        for i in range(self._V-1):
            
            dosloDoKorekcije = False
            
            for u, v, w in korigiraneUdaljenosti:
                
                if udaljenosti[u] != float("Inf") and udaljenosti[u] + w < udaljenosti[v]:
                    udaljenosti[v] = udaljenosti[u] + w
                    kolona1[v] = str(udaljenosti[v])
                    niz = {'Cilj': kolona0, 'Duzina': kolona1, 'Put': kolona2}
                    praviTabelu(niz, fig, ax, self._V, v)                                             
                    prethodnici[v] = u
                    dosloDoKorekcije = True
                    
                    korigiraneUdaljenosti.append((u, v, w))
                    if self.getDaLiJeDigraf():
                        korigiraneUdaljenosti.append((v, u, w))
                    
            if dosloDoKorekcije == False:
                break
            
            #self.ispisiMinimalneUdaljenosti(udaljenosti)

        if not self.getDaLiJeDigraf():
            for u, v, w in self._graf:
                if udaljenosti[u] != float("Inf") and udaljenosti[u] + w < udaljenosti[v]:
                    raise TypeError("Graf sadrzi ciklus negativne tezine!")
                    return
        
        #self.ispisiPuteveDoCvorova(izvor, prethodnici)
        
        for i in range(self._V):
            if prethodnici[i] == float("Inf"):
                kolona2[i] = 'inf'
                niz = {'Cilj': kolona0, 'Duzina': kolona1, 'Put': kolona2}
                praviTabelu(niz, fig, ax, self._V, i, 2)
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
                praviTabelu(niz, fig, ax, self._V, i, 2)
      


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

'''
g1 = Graf(7, True)

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



g2 = Graf(12, False)

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


            '''