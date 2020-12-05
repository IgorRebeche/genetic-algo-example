
import random, json

# Numero de elementos para cada geração
POPULATION_SIZE = 100

MIN_PRODUTOS = 10 # Quantidade minima de produtos
MAX_PRODUTOS =30 # Quantidade maxima de produtos
MAX_DISTANCIA = 15 # Distancia em KM
MAX_PESO_PRODUTO = 43 # Peso Maximo de produto
MAX_PESO = 650 # Peso maximo do veiculo
AUTONOMIA = 200 # Autonomia do veiculo

PRODUTO = {
    "PESO": 20,
    "DISTANCIA": 15,
}
  
class Elemento(object): 
    ''' 
    Classe representando um elemento na população
    '''
    def __init__(self, cromossomo): 
        self.cromossomo = cromossomo  
        self.fitness = self.cal_fitness() 
  
    @classmethod
    def mutar_genes(self): 
        ''' 
        Criar genes randomicos para mutação 
        '''
        global PRODUTO
        TMPPRODUTO = PRODUTO.copy()
        TMPPRODUTO['DISTANCIA'] = random.randint(1,MAX_DISTANCIA)
        TMPPRODUTO['PESO'] = random.randint(1,MAX_PESO_PRODUTO)
        gene = TMPPRODUTO
        return gene 
  
    @classmethod
    def criar_gnoma(self): 
        ''' 
        Criar cromossomos (Genes de produtos) 
        '''
        global MIN_PRODUTOS, MAX_PRODUTOS
        random_PRODUTOS = random.randint(MIN_PRODUTOS, MAX_PRODUTOS * 1.4)
        mutated = [self.mutar_genes() for _ in range(random_PRODUTOS)] 
        return mutated
  
    def reproduzir(self, par2): 
        ''' 
        Realizar reprodução e produzir novos descendentes 
        '''
  
        # chromosome for offspring 
        cromossomo_filho = [] 
        for gp1, gp2 in zip(self.cromossomo, par2.cromossomo):     
  
            # gerar uma probabilidade randomica  
            prob = random.random() 
  
            # Se a probabilidade for menor que 45%, inserir gene do primeiro parente 
            if prob < 0.45: 
                cromossomo_filho.append(gp1) 
  
            # Se a probabilidade for entre 45% e 90%, inserir genes do parente 2
            elif prob < 0.90: 
                cromossomo_filho.append(gp2) 
  
            # Caso nao, inserir genes randomicos para manter diversidade
            else: 
                cromossomo_filho.append(self.mutar_genes()) 
  
        # Retornar novo elemento para proxima geração
        return Elemento(cromossomo_filho) 
  
    def cal_fitness(self): 
        ''' 
        Calcular o score de fitness dos elementos criados
        baseando-se em diversas regras
        '''
        global AUTONOMIA, MAX_PESO
        fitness = 0
        
        SUM_PESO = 0
        SUM_DISTANCIA = 0 
        
        if (len(self.cromossomo) > MAX_PRODUTOS):
            return 13
        
        for produto in self.cromossomo:
            SUM_DISTANCIA += produto['DISTANCIA']
            SUM_PESO += produto['PESO']

        DIST_AUTO_RELATION = SUM_DISTANCIA/AUTONOMIA
        PESO_LIMIT_RELATION = SUM_PESO/MAX_PESO
        
        if ((DIST_AUTO_RELATION >= 1 or DIST_AUTO_RELATION <= 0) or (PESO_LIMIT_RELATION >= 1 or PESO_LIMIT_RELATION <= 0)):
            return 13

        if (DIST_AUTO_RELATION >= 0.8 and DIST_AUTO_RELATION <= 1):
            fitness += 1
        
        if (DIST_AUTO_RELATION >= 0.5 and DIST_AUTO_RELATION <= 0.8):
            fitness += 3
        
        if (DIST_AUTO_RELATION >= 0.2 and DIST_AUTO_RELATION <= 0.5):
            fitness += 5

        
        if (PESO_LIMIT_RELATION >= 0.8 and PESO_LIMIT_RELATION <= 1):
            fitness += 1
        
        if (PESO_LIMIT_RELATION >= 0.5 and PESO_LIMIT_RELATION <= 0.8):
            fitness += 3

        if (PESO_LIMIT_RELATION >= 0.2 and PESO_LIMIT_RELATION <= 0.5):
            fitness += 5

        if ((PESO_LIMIT_RELATION + DIST_AUTO_RELATION)/2 >= 0.98):
            fitness = 0

        return fitness   
  
def showResult(population, generation):
    print('Lista de produtos:')
    for i, produto in enumerate(population[0].cromossomo, start=1):
        peso = produto['PESO']
        distancia = produto['DISTANCIA']
        print(f'Produto {i} -> Peso: {peso} Distancia: {distancia}')
    print('----------------------------------')
    qutProdutos = len(population[0].cromossomo)
    sumPeso = 0
    sumDistancia = 0
    for produto in population[0].cromossomo:
        sumDistancia = produto['DISTANCIA'] + sumDistancia
        sumPeso = produto['PESO'] + sumPeso
    
    print("Estatisticas: ")
    print(f'Ultima Geração: {generation} Fitness: {population[0].fitness}')
    print(f"QUT PRODUTOS: {qutProdutos}  PESO TOTAL: {sumPeso}  DISTANCIA TOTAL: {sumDistancia}")

def main(): 
    global POPULATION_SIZE
    geracao = 1
  
    found = False
    populacao = [] 
  
    #  Criar população incial 
    for _ in range(POPULATION_SIZE): 
        gnome = Elemento.criar_gnoma() 
        populacao.append(Elemento(gnome)) 
  
    while not found: 
  
        # Ordenar a população em ordem crescente de score do fitness
        populacao = sorted(populacao, key = lambda x:x.fitness) 
  
        # Se o elemento possuir o score zero
        # paramos a geração pois encontramos o melhor cenario dentre as regras
        if populacao[0].fitness <= 0: 
            found = True
            break
  
        # Caso nao, gerar novos descendentes
        nova_geracao = [] 
  
        # Coletar 10% dos elementos mais adaptados para a proxima geração
        s = int((10*POPULATION_SIZE)/100) 
        nova_geracao.extend(populacao[:s]) 
  
        # Dos 50% dos elementos mais adapatos, 
        # geraremos novas reproduções para gerar novos descendentes
        s = int((90*POPULATION_SIZE)/100) 
        for _ in range(s): 
            parente1 = random.choice(populacao[:50]) 
            parente2 = random.choice(populacao[:50]) 
            filho = parente1.reproduzir(parente2) 
            nova_geracao.append(filho) 
  
        populacao = nova_geracao 

        print(f"Generation: {geracao}\tQuantidade de Produtos: {len(populacao[0].cromossomo)}\tFitness: {populacao[0].fitness}") 
        geracao += 1
    print("Busca finalizada!\n\n")
    showResult(population=populacao, generation=geracao)
  
if __name__ == '__main__': 
    main() 