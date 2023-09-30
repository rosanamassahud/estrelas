import math
class Cluster:
    def __init__(self,x_centro, y_centro, raio):
        self.__xc = x_centro
        self.__yc = y_centro
        self.__raio = raio
        #self.__densidade = 0
        self.__estrelas = []
    
    @property
    def xc(self):
        return self.__xc
    
    @xc.setter
    def xc(self,x):
        self.__xc = x

    @property
    def yc(self):
        return self.__yc
    
    @yc.setter
    def yc(self,y):
        self.__yc = y
    
    @property
    def raio(self):
        return self.__raio
    
    @raio.setter
    def raio(self,r):
        self.__raio = r    
    
    @property
    def estrelas(self):
        return self.__estrelas
    
    @estrelas.setter
    def estrelas(self, est):
        self.__estrelas = est
    
    def area(self):
        return math.pi * (self.__raio**2)
    
    def densidade(self):
        return len(self.__estrelas)/self.area()
    
    def __str__(self) -> str:
        return 'Cc({},{})  Raio:{}  N.Estrelas:{}  Area:{}  Densidade:{}'.format(self.xc,self.yc, self.raio, len(self.__estrelas), self.area(), self.densidade())

class Amostra:
    def __init__(self,elementos):
        self.__elementos = elementos
    
    @property
    def elementos(self):
        return self.__elementos
    
    @elementos.setter
    def elementos(self, elementos):
        self.__elementos = elementos

    def euclidian_distance(self, j):
        sum = 0
        for i in range (len(self.elementos)):
            d = self.elementos[i] - j.elementos[i]
            sum = sum + d * d
        return pow(sum,0.5)

    def __str__(self):
        return '({},{})'.format(self.__elementos[0], self.__elementos[1])
    
if(__name__=='__main__'):
    c1 = Cluster(1,1,2)
    print(c1)
    j = Amostra([5,2])
    d = j.euclidian_distance(Amostra([c1.xc,c1.yc]))
    print("distancia: ", d)