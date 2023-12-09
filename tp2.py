import tsplib95
import sys
from algoritmos import TwiceAroundTheTree, Christofides, BranchAndBound
import datetime
from memory_profiler import memory_usage
import threading


# lendo o nome do arquivo de entrada
if len(sys.argv) < 2:
    print('Usage: python3 t2.py datasets/<input_file.tsp>')
    sys.exit(1)
if not sys.argv[1].endswith('.tsp') or len(sys.argv[1]) < 13:
    print('Usage: python3 t2.py datasets/<input_file.tsp>')
    sys.exit(1)
caminho_arquivo = sys.argv[1]
try:
    with open(caminho_arquivo, 'r') as file:
        pass
except FileNotFoundError:
    print('dataset nao encontrado.')
    sys.exit(1)

# grafo e numero de vertices
grafo = tsplib95.load(caminho_arquivo).get_graph()
num_vertices = len(grafo.nodes)

# pegando o peso otimo
arquivo_escolhido = caminho_arquivo[9:-4]
encontrou = False
with open(f'auxilio/solucoes.txt', 'r') as file:
    linhas = file.readlines()
    for linha in linhas:
        if linha.startswith(arquivo_escolhido):
            encontrou = True
            peso_otimo = int(linha.split()[2])
            break
if not encontrou:
    print('Nao foi possivel encontrar o peso otimo para esse grafo, verifique o nome do arquivo.')
    sys.exit(1)
print(f'Grafo: {arquivo_escolhido}')
print(f'Peso otimo: {peso_otimo}')
print(f'Numero de vertices: {num_vertices}')
print()

# calculando o peso da solucao para cada algoritmo se possivel
def run_twice_around_tree(grafo, peso_otimo):
    print("TwiceAroundTheTree:")
    try:
        tempo_inicial = datetime.datetime.now()
        memoria = memory_usage((TwiceAroundTheTree, (grafo,)))
        peso_solucao = TwiceAroundTheTree(grafo)
        memoria = max(memoria)
        tempo_final = datetime.datetime.now()
        if (tempo_final - tempo_inicial).total_seconds() > 30 * 60:
            print('Tempo limite excedido para TwiceAroundTheTree.')
        else:
            print(f'Peso da solucao: {peso_solucao}')
            print(f'Desvio percentual: {(peso_solucao - peso_otimo) / peso_otimo * 100:.2f}%')
            print(f'Tempo de execucao: {(tempo_final - tempo_inicial).total_seconds():.2f}s')
            print(f'Memoria utilizada: {memoria:.2f}MB')
    except Exception as e:
        print(f'Erro ao executar TwiceAroundTheTree: {e}')
    print()
    
def run_christofides(grafo, peso_otimo):
    print("Christofides:")
    try:
        tempo_inicial = datetime.datetime.now()
        memoria = memory_usage((Christofides, (grafo,)))
        peso_solucao = Christofides(grafo)
        memoria = max(memoria)
        tempo_final = datetime.datetime.now()

        if (tempo_final - tempo_inicial).total_seconds() > 30 * 60:
            print('Tempo limite excedido para Christofides.')
        else:
            print(f'Peso da solucao Christofides: {peso_solucao}')
            print(f'Desvio percentual: {(peso_solucao - peso_otimo) / peso_otimo * 100:.2f}%')
            print(f'Tempo de execucao: {(tempo_final - tempo_inicial).total_seconds():.2f}s')
            print(f'Memoria utilizada: {memoria:.2f}MB')
    except Exception as e:
        print(f'Erro ao executar Christofides: {e}')
    print()

def run_branch_and_bound(grafo, peso_otimo):
    print("BranchAndBound:")
    try:
        tempo_inicial = datetime.datetime.now()
        memoria = memory_usage((Christofides, (grafo,)))
        peso_solucao = BranchAndBound(grafo)
        memoria = max(memoria)
        tempo_final = datetime.datetime.now()

        if (tempo_final - tempo_inicial).total_seconds() > 30 * 60:
            print('Tempo limite excedido para BranchAndBound.')
        else:
            print(f'Peso da solucao BranchAndBound: {peso_solucao}')
            print(f'Desvio percentual: {(peso_solucao - peso_otimo) / peso_otimo * 100:.2f}%')
            print(f'Tempo de execucao: {(tempo_final - tempo_inicial).total_seconds():.2f}s')
            print(f'Memoria utilizada: {memoria:.2f}MB')
    except Exception as e:
        print(f'Erro ao executar BranchAndBound: {e}')
    print()

thread_twice_around_tree = threading.Thread(target=run_twice_around_tree, args=(grafo, peso_otimo))
thread_twice_around_tree.start()
thread_twice_around_tree.join(timeout=30 * 60)
if thread_twice_around_tree.is_alive():
    print("TwiceAroundTheTree excedeu o tempo limite de 30 minutos.")
    
thread_christofides = threading.Thread(target=run_christofides, args=(grafo, peso_otimo))
thread_christofides.start()
thread_christofides.join(timeout=30 * 60)
if thread_christofides.is_alive():
    print("Christofides excedeu o tempo limite de 30 minutos.")
    
# Branch and Bound consome muita memoria e demanda bastante tempo
# So executamos para grafos pequenos ou quando passamos -b como 3o argumento
if num_vertices <= 15 or (len(sys.argv) == 3 and sys.argv[2] == '-b'):
    thread_branch_and_bound = threading.Thread(target=run_branch_and_bound, args=(grafo, peso_otimo))
    thread_branch_and_bound.start()
    thread_branch_and_bound.join(timeout=30 * 60)
    if thread_branch_and_bound.is_alive():
        print("BranchAndBound excedeu o tempo limite de 30 minutos.")