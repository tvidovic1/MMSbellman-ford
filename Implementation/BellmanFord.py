class Graf:
    
    def __init__(self, cvorovi):
        self._V = cvorovi
        self._graf = []
        
    
    def dodajGranu(self, u, v, w):
        self._graf.append((u, v, w))
    
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
        
        for i in range(self._V-1):
            
            dosloDoKorekcije = False
            for u, v, w in korigiraneUdaljenosti:
                if udaljenosti[u] != float("Inf") and udaljenosti[u] + w < udaljenosti[v]:
                    udaljenosti[v] = udaljenosti[u] + w
                    dosloDoKorekcije = True
                    korigiraneUdaljenosti = []
                    korigiraneUdaljenosti.append((u, v, w))
            if dosloDoKorekcije == False:
                break
        
        for u, v, w in self._graf:
            if udaljenosti[u] != float("Inf") and udaljenosti[u] + w < udaljenosti[v]:
                raise TypeError("Graf sadrzi ciklus negativne tezine!")
                return
        
            
        
        self.ispisiMinimalneUdaljenosti(udaljenosti)


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
        
        
    
    
            