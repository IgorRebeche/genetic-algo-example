# Python3 program to create target string, starting from 
# random string using Genetic Algorithm 
  
import random 
  
# Number of individuals in each generation 
POPULATION_SIZE = 100
  
# Valid genes 
GENES = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP 
QRSTUVWXYZ 1234567890, .-;:_!"#%&/()=?@${[]}'''

MIN_PRODUTOS = 10
MAX_PRODUTOS = 200
MAX_PESO = 300
AUTONOMIA = 200

PRODUTO = {
    "PESO": 20,
    "DISTANCIA": 15,
}

  
# Target string to be generated 
# PRECISO Q SEJA 50 % eficiente
TARGE_NEW = 0.5
TARGET = "STRING TESTE"
  
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
        global GENES, PRODUTO
        PRODUTO['DISTANCIA'] = random.randint(1,15)
        PRODUTO['PESO'] = random.randint(1,50)
        # gene = random.choice(GENES) 
        gene = PRODUTO
        return gene 
  
    @classmethod
    def create_gnome(self): 
        ''' 
        create chromosome or string of genes 
        '''
        global TARGET, MIN_PRODUTOS, MAX_PRODUTOS 
        gnome_len = len(TARGET) 
        random_PRODUTOS = random.randint(MIN_PRODUTOS, MAX_PRODUTOS)
        return [self.mutated_genes() for _ in range(random_PRODUTOS)] 
  
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
        global TARGET, AUTONOMIA, MAX_PESO
        fitness = 0
        
        SUM_PESO = 0
        SUM_DISTANCIA = 0 
        for produto in self.chromosome:
            SUM_DISTANCIA += produto['DISTANCIA']
            SUM_PESO += produto['PESO']
        
        
        
        if (SUM_DISTANCIA/AUTONOMIA > 0.9 and SUM_PESO/MAX_PESO > 0.9):
            # print("0.9 REGRA",SUM_DISTANCIA/AUTONOMIA, SUM_PESO/MAX_PESO)
            fitness = 1
        
        elif (SUM_DISTANCIA/AUTONOMIA > 0.5 and SUM_PESO/MAX_PESO > 0.5):
            # print("0.5 REGRA",SUM_DISTANCIA/AUTONOMIA, SUM_PESO/MAX_PESO)
            fitness = 3

        elif (SUM_DISTANCIA/AUTONOMIA > 0.2 and SUM_PESO/MAX_PESO > 0.2):
            # print("0.2 REGRA",SUM_DISTANCIA/AUTONOMIA, SUM_PESO/MAX_PESO)
            fitness = 5

        return fitness   

        # for gs, gt in zip(self.chromosome, TARGET): 
        #     if gs != gt: fitness+= 1
        # return fitness 
  
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
        # tmp = "".join(population[0].chromosome)
        print(f"Generation: {generation}\tString: {len(population[0].chromosome)}\tFitness: {population[0].fitness}") 
  
        generation += 1
  
    # tmp = "".join(population[0].chromosome)
    print(f"Generation: {generation}\tString: {population[0].chromosome}\tFitness: {population[0].fitness}") 
  
if __name__ == '__main__': 
    main() 