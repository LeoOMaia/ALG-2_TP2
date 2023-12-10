import networkx as nx
import numpy as np

def TwiceAroundTheTree(grafo):
    arvore_minima = nx.minimum_spanning_tree(grafo)
    caminho = list(nx.dfs_preorder_nodes(arvore_minima, 1))
    caminho.append(caminho[0])
    peso_solucao = 0
    for i in range(len(caminho) - 1):
        peso_solucao += grafo[caminho[i]][caminho[i + 1]]['weight']
    return peso_solucao

def Christofides(grafo):
    def pareamento_minimo(grafo, arvore_minima):
        nao_pares = [v for v, grau in nx.degree(arvore_minima) if grau % 2 == 1]
        pareando = nx.min_weight_matching(nx.subgraph(grafo, nao_pares))
        return pareando
    
    def grafo_multigrafo(grafo, arvore_minima, pareamento):
        multigrafo = nx.MultiGraph(arvore_minima)
        for v1, v2 in pareamento:
            multigrafo.add_edge(v1, v2, weight=grafo[v1][v2]['weight'])
        return multigrafo
    
    def menor_caminho(grafo):
        menor_caminho = [x[0] for x in nx.eulerian_circuit(grafo, 1)]
        return list(dict.fromkeys(menor_caminho)) + [menor_caminho[0]]
    
    arvore_minima = nx.minimum_spanning_tree(grafo)
    pareamento = pareamento_minimo(grafo, arvore_minima)
    multigrafo = grafo_multigrafo(grafo, arvore_minima, pareamento)
    caminho = menor_caminho(multigrafo)
    peso_solucao = 0
    for i in range(len(caminho) - 1):
        peso_solucao += grafo[caminho[i]][caminho[i + 1]]['weight']
    return peso_solucao

def BranchAndBound(grafo):
    class Vertice:
        def __init__(self, limite, limites_arestas, custo, solucao):
            self.limite = limite
            self.limites_arestas = limites_arestas
            self.custo = custo
            self.solucao = solucao
        def __lt__(self, outro):
            if len(self.solucao) == len(outro.solucao):
                return self.limite < outro.limite
            return len(self.solucao) > len(outro.solucao)

    def encontrar_limite(grafo, solucao, limites_arestas, limite):
        arestas_alteradas = np.zeros(grafo.number_of_nodes(), dtype=int)
        novos_limites = np.array(limites_arestas)
        peso_aresta = grafo[solucao[-2]][solucao[-1]]['weight']
        soma = limite * 2
        percorre = []
        if len(solucao) >= 2:
            percorre.append(solucao[-2])
        percorre.append(solucao[-1])
        for no in percorre:
            indice_no = no - 1
            if novos_limites[indice_no][0] != peso_aresta:
                soma -= novos_limites[indice_no][arestas_alteradas[indice_no]]
                soma += peso_aresta
                arestas_alteradas[indice_no] += 1
                novos_limites[indice_no][arestas_alteradas[indice_no]] = peso_aresta
        return soma / 2, novos_limites
    
    limites_arestas_iniciais = np.zeros((grafo.number_of_nodes(), 2), dtype=object)
    percorrer = grafo.number_of_nodes() + 1
    limite = 0
    for i in range(1, percorrer):
        pesos = [grafo[i][j]['weight'] for j in grafo[i]]
        pesos_ordenados = sorted(pesos)[:2]
        min1, min2 = pesos_ordenados + [np.inf] * (2 - len(pesos_ordenados))
        limites_arestas_iniciais[i - 1] = [min1, min2]
        limite += min1 + min2
    limite_inicial = limite / 2
    raiz = Vertice(limite_inicial, limites_arestas_iniciais, 0, [1])
    lista_vertices = [raiz]
    melhor_custo = np.inf
    contador_de_vertices = 0
    while lista_vertices:
        vertice_atual = min(lista_vertices)
        lista_vertices.remove(vertice_atual)
        contador_de_vertices += 1
        nivel = len(vertice_atual.solucao)
        if nivel > grafo.number_of_nodes():
            if melhor_custo > vertice_atual.custo:
                melhor_custo = vertice_atual.custo
        else:
            if vertice_atual.limite < melhor_custo and nivel < grafo.number_of_nodes() - 2:
                for k in range(1, grafo.number_of_nodes() + 1):
                    if k not in vertice_atual.solucao:
                        peso_aresta = grafo[vertice_atual.solucao[-1]][k]['weight']
                        novo_limite, novas_arestas = encontrar_limite(grafo, vertice_atual.solucao + [k], vertice_atual.limites_arestas, vertice_atual.limite)
                        if novo_limite < melhor_custo:
                            novo_vertice = Vertice(novo_limite, novas_arestas, vertice_atual.custo + peso_aresta, vertice_atual.solucao + [k])
                            lista_vertices.append(novo_vertice)
            elif vertice_atual.limite < melhor_custo and nivel >= grafo.number_of_nodes() - 2:
                for k in range(1, grafo.number_of_nodes() + 1):
                    if k not in vertice_atual.solucao:
                        ultimo_no = next(i for i in range(1, grafo.number_of_nodes() + 1) if i not in vertice_atual.solucao + [k] and k != i)
                        peso_aresta = grafo[vertice_atual.solucao[-1]][k]['weight']
                        prox_peso_aresta = grafo[k][ultimo_no]['weight']
                        ultimo_peso_aresta = grafo[ultimo_no][1]['weight']
                        custo = vertice_atual.custo + peso_aresta + prox_peso_aresta + ultimo_peso_aresta
                        if custo < melhor_custo:
                            novo_vertice = Vertice(custo, [], custo, vertice_atual.solucao + [k, ultimo_no, 1])
                            lista_vertices.append(novo_vertice)
    return melhor_custo