# Python3 program to create target string, starting from 
# random string using Genetic Algorithm 
  
import random, json
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
  
# Number of individuals in each generation 
POPULATION_SIZE = 100

MIN_PRODUTOS = 10 # Quantidade minima de produtos
MAX_PRODUTOS = 30 # Quantidade maxima de produtos
MAX_DISTANCIA = 15 # Distancia em KM
MAX_PESO_PRODUTO = 43 # Peso Maximo de produto
MAX_PESO = 650 # Peso maximo do veiculo
AUTONOMIA = 200 # Autonomia do veiculo

PRODUTO = {
    "PESO": 20,
    "DISTANCIA": 15,
}

  
# Target string to be generated 
# PRECISO Q SEJA 50 % eficiente
  
class Individual(object): 
    ''' 
    Class representing individual in population 
    '''
    def __init__(self, chromosome): 
        self.chromosome = chromosome  
        self.fitness = self.cal_fitness() 
  
    @classmethod
    def mutated_genes(self): 
        ''' 
        create random genes for mutation 
        '''
        global PRODUTO
        TMPPRODUTO = PRODUTO.copy()
        TMPPRODUTO['DISTANCIA'] = random.randint(1,MAX_DISTANCIA)
        TMPPRODUTO['PESO'] = random.randint(1,MAX_PESO_PRODUTO)
        gene = TMPPRODUTO
        return gene 
  
    @classmethod
    def create_gnome(self): 
        ''' 
        create chromosome or string of genes 
        '''
        global MIN_PRODUTOS, MAX_PRODUTOS
        random_PRODUTOS = random.randint(MIN_PRODUTOS, MAX_PRODUTOS * 1.4)
        mutated = [self.mutated_genes() for _ in range(random_PRODUTOS)] 
        return mutated
  
    def mate(self, par2): 
        ''' 
        Perform mating and produce new offspring 
        '''
  
        # chromosome for offspring 
        child_chromosome = [] 
        for gp1, gp2 in zip(self.chromosome, par2.chromosome):     
  
            # random probability   
            prob = random.random() 
  
            # if prob is less than 0.45, insert gene 
            # from parent 1  
            if prob < 0.45: 
                child_chromosome.append(gp1) 
  
            # if prob is between 0.45 and 0.90, insert 
            # gene from parent 2 
            elif prob < 0.90: 
                child_chromosome.append(gp2) 
  
            # otherwise insert random gene(mutate),  
            # for maintaining diversity 
            else: 
                child_chromosome.append(self.mutated_genes()) 
  
        # create new Individual(offspring) using  
        # generated chromosome for offspring 
        return Individual(child_chromosome) 
  
    def cal_fitness(self): 
        ''' 
        Calculate fittness score, it is the number of 
        characters in string which differ from target 
        string. 
        '''
        global AUTONOMIA, MAX_PESO
        fitness = 0
        
        SUM_PESO = 0
        SUM_DISTANCIA = 0 
        
        if (len(self.chromosome) > MAX_PRODUTOS):
            return 13
        
        for produto in self.chromosome:
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
  
# Driver code 
def main(): 
    global POPULATION_SIZE 
  
    #current generation 
    generation = 1
  
    found = False
    population = [] 
  
    # create initial population 
    for _ in range(POPULATION_SIZE): 
        gnome = Individual.create_gnome() 
        population.append(Individual(gnome)) 
  
    while not found: 
  
        # sort the population in increasing order of fitness score 
        population = sorted(population, key = lambda x:x.fitness) 
  
        # if the individual having lowest fitness score ie.  
        # 0 then we know that we have reached to the target 
        # and break the loop 
        if population[0].fitness <= 0: 
            found = True
            break
  
        # Otherwise generate new offsprings for new generation 
        new_generation = [] 
  
        # Perform Elitism, that mean 10% of fittest population 
        # goes to the next generation 
        s = int((10*POPULATION_SIZE)/100) 
        new_generation.extend(population[:s]) 
  
        # From 50% of fittest population, Individuals  
        # will mate to produce offspring 
        s = int((90*POPULATION_SIZE)/100) 
        for _ in range(s): 
            parent1 = random.choice(population[:50]) 
            parent2 = random.choice(population[:50]) 
            child = parent1.mate(parent2) 
            new_generation.append(child) 
  
        population = new_generation 

        print(f"Generation: {generation}\tString: {len(population[0].chromosome)}\tFitness: {population[0].fitness}") 
        # cls()
        generation += 1
  
    print(f"Generation: {generation}\tProdutos: {population[0].chromosome}\tFitness: {population[0].fitness}") 
    
    
    qutProdutos = len(population[0].chromosome)
    sumPeso = 0
    sumDistancia = 0
    for produto in population[0].chromosome:
        sumDistancia = produto['DISTANCIA'] + sumDistancia
        sumPeso = produto['PESO'] + sumPeso
    print("Estatisticas: ")
    print(f"QUT PRODUTOS: {qutProdutos}  PESO TOTAL: {sumPeso}  DISTANCIA TOTAL: {sumDistancia}")
  
if __name__ == '__main__': 
    main() 