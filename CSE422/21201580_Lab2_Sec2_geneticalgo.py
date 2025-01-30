import random as ran

f=open('./input2.txt','r')
w=open("./output2.txt",'w')
nums=list(map(int,f.readline().split()))
N=nums[0]
T=nums[1]
courses=[f.readline().strip() for i in range(N)]
print(N,T,courses)
def beginner_population(N,T):
    population=[]
    size=20
    for j in range(size):
        c=''
        for i in range(N*T):
            pop=str(ran.randint(0,1))
            c+=pop
        population.append(c)
    return population
def penalty(population,T,N):
    const=0
    overlap=0
    schedule=[]
    for i in range(T):
        index=i*N
        row=population[index:index+N]
        schedule.append(row)
    for j in schedule:
        course_sched=j.count('1')
        if course_sched>1:
            overlap+=(course_sched-1)
    for i in range(N):
        s=0
        for j in schedule:
            s+=int(j[i])
        const+=abs(s-1)
    total_penalty=overlap+const
    return (-total_penalty)
        
def selection(dictonary, size):
    random_ind=ran.sample(range(size), 2)
    offspring=crossover(random_ind,dictonary)
    return offspring

def crossover(rand, dictonary):
    keys=list(dictonary.keys()) 
    parent1=keys[rand[0]] 
    parent2=keys[rand[1]]
    point=ran.randint(1,len(parent1)-1)  
    offspring1=parent1[:point]+parent2[point:] 
    offspring2=parent2[:point]+parent1[point:] 

    return offspring1,offspring2

def mutation(b,N,T):
    mutated=[]
    for j in b:
        s=list(j)
        #print(s)
        ranind=ran.randint(0,N*T-1)
        if s[ranind]=='0':
            s[ranind]='1'
        elif s[ranind]=='1':
            s[ranind]='0'
        d=(''.join(s))
        mutated.append(d)

    return mutated

def fitness(c,N,T):
    temp={}
    for i in c:
        g=penalty(i,T,N)
        temp[i]=g
    minkey=min(temp,key=temp.get)
    minvalue=temp[minkey]
    return minkey,minvalue

#part1
def genetic_algorithm(N,T,total_loop=50):
    population=beginner_population(N,T)
    dictonary={}
    for k in population:
        a=penalty(k,T,N)
        dictonary[k]=a
    best_fitness=float('-inf')
    best_chromosome=None
    for j in range(total_loop):
        new_population=[]
        new_dict={}
        for i in range(20):
            b=selection(dictonary, len(dictonary))
            c=mutation(b,N,T)
            d,e=fitness(c,N,T)
            new_population.append(d)
            new_dict[d] = e
            if e>best_fitness:
                best_fitness=e
                best_chromosome=d
            if e==0:
                return new_population,new_dict,best_chromosome,best_fitness
        dictonary=new_dict
    
    return new_population,new_dict,best_fitness,best_chromosome
        
g1,g2,g3,g4=genetic_algorithm(N,T)
a=f"fittest at {g3} and it is in {g4} "
print(a)
#part2
def crossover2(rand,list1,sizechrom):
    keys=list1 
    parent1=keys[rand[0]] 
    parent2=keys[rand[1]]
    points=sorted(ran.sample(range(sizechrom), 2))  
    point1,point2=points
    offspring1=parent1[:point1]+parent2[point1:point2]+parent1[point2:]
    offspring2=parent2[:point1]+parent1[point1:point2]+parent2[point2:]
    
    return parent1,parent2, offspring1,offspring2
def selection_2(list1, size,sizechrom):
    random_ind=ran.sample(range(size), 2)
    offspring=crossover2(random_ind,list1,sizechrom)
    return offspring
def twopointcrossover(N,T):
    population2 = beginner_population(N, T)
    #print(population2)
    h1,h2,h3,h4=selection_2(population2,len(population2),N*T)

    a2=f'random parents {h1} and {h2} and 2point crossover is {h3} and {h4}.'
    return a2
part2=twopointcrossover(N,T)
print(part2)
w.write(a+'\n'+part2)
f.close()
w.close()