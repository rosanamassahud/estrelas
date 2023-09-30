from sklearn.datasets import make_blobs # meka_blobs cria cluesters sintéticos
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from classes import Cluster, Amostra
from statistics import mean, median
import time
import math
import csv

def gera_dados():
    # geração de dados --------------
    centers = [[0, 0]]#, [-1, -1], [1, -1]] # pontos centrais dos clusters
    #print("centros: ", centers)
    X, labels_true = make_blobs(
        n_samples=720, centers=centers, cluster_std=0.4, random_state=0
    )

    #print("X: ", X)
    #print("labels_true", labels_true)

    # StandardScaler é um método de preprocessamento 
    # que padroniza os dados removendo a média e dimensionando para a variação unitária.
    # Algo como: z = (x - u) /s, onde u é a média e s o desvio padrão
    X = StandardScaler().fit_transform(X)
    #print("{}, X:{}".format(type(X),X))
    #print('x0',X[0])
    #print('x1',X[1])
    #print(len(X))
    #plt.scatter(X[:, 0], X[:, 1])
    #plt.grid()
    #plt.show()
    
    return X 

def le_dados():
    X = []
    with open('tabela_skymap_NGC6811.csv') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            X.append( [ float(row['ColunaX']), float(row['ColunaY']) ])
            #print(row['ColunaX'])  
            #print(row['ColunaY'])
    return X

def define_clusters_circunscritos(n_clusters, centro, Rthr, clusters=[]):
    clusters.append(Cluster(centro.elementos[0],centro.elementos[1], 0)) # cluster 0 é o próprio centro
    div = Rthr/(n_clusters)
    #print(div)
    raio = div
    for i in range(1,n_clusters+1):
        #print("Criando o cluster {}, raio={}".format(i, raio))
        clusters.append(Cluster(centro.elementos[0],centro.elementos[1],raio))
        raio+=div

def imprime_clusters(clusters):
    for i in range(1, n_clusters+1):
        print('Cluster {}:{}'.format(i,clusters[i]))

def le_estrelas(dados, amostras):
    for ponto in dados:
        amostras.append(Amostra(ponto))

def emc_algoritm(p_centro, n_clusters=1,clusters=[], amostras=[]):
    start = time.time()

    centro = p_centro#Cluster(dados[0,0],dados[0,1],0)
    #print(centro)
    #clusters.append(c)
    
    distancias = []
    for i in amostras:
        for j in amostras:
            d = i.euclidian_distance(j)
            distancias.append(d)
        d = i.euclidian_distance(centro)
        distancias.append(d)

    distancias.sort()
    #print(distancias)
    distancia_maxima = distancias[len(distancias)-1]
    print(distancia_maxima)
    Dthr = distancia_maxima*1.1
    print('Dthr', Dthr)
    Rthr = Dthr/2
    print('Rthr', Rthr)
    define_clusters_circunscritos(n_clusters=n_clusters, centro=centro, 
                                  Rthr=Rthr, clusters=clusters)
    
    for estrela in amostras:
        #i = 1 # começa pelo cluster mais externo
        for j in range(1,n_clusters+1):
            if(estrela.euclidian_distance(centro) < clusters[j].raio):
                # achou o cluster ! uhuu!
                clusters[j].estrelas.append(estrela)
                break

    end = time.time()
    print("Tempo proc. EMC: ", end - start)


def resultados(amostras, clusters):
    x = []
    y = []
    a = []
    d = []
    for amostra in amostras:
        x.append(amostra.elementos[0])
        y.append(amostra.elementos[1])
    #print(len(x))    
    #print(len(y))
    for i in range(1,len(clusters)):
        a.append(clusters[i].area())
        d.append(clusters[i].densidade())
    labels = []
    for i in d:
        label = "{:.2f}".format(i)
        labels.append(label)

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20, 8))
    ax1.plot(clusters[0].xc,clusters[0].yc, 'ro')
    limite = (clusters[len(clusters)-1].raio)
    ax1.set_ylim(-limite, limite)
    ax1.set_xlim(-limite, limite)
    ax1.scatter(x,y)
    ax1.set_title('Clusters')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.grid()
    #figure, axes = plt.subplots(1,2) 
    for i in range(1,len(clusters)):
        '''
        Drawing_uncolored_circle = plt.Circle( (0.6, 0.6 ), 
                                            0.3 , 
                                            fill = False ) 
        '''
        
        circle = plt.Circle( (clusters[i].xc, clusters[i].yc ), 
                                            clusters[i].raio , 
                                            fill = True, color='purple', alpha=0.15 )
        
        
        ax1.set_aspect( 1 ) 
        ax1.add_artist( circle ) 

    ax2.plot(a,d, color='purple', marker='o', linestyle='solid')
    ax2.grid()
    ax2.set_xlabel('Área do cluster')
    ax2.set_ylabel('Densidade do cluster')
    ax2.set_title('Densidade')
    plt.show() 


if __name__ == "__main__":
    
    #dados = gera_dados()
    dados = le_dados()

    n_clusters = 12
    
    clusters = []
    amostras = [] # estrelas
    
    #define a lista de estrelas
    le_estrelas(dados, amostras)
    #print('Estrela 519: ', amostras[519])
    emc_algoritm(p_centro=(amostras[519]), n_clusters=n_clusters, clusters=clusters, amostras=amostras)
    
    imprime_clusters(clusters)

    resultados(amostras, clusters)


    
