f=open('./input1.txt','r')
w=open("./output1.txt",'w')
lines=f.readlines()
graph_data = []

for i in lines:
    line =i.split()
    parent =line[0]
    hrst =int(line[1])
    n = []
    for j in range(2, len(line), 2):
        nct= line[j]
        distance= int(line[j + 1])
        n.append((nct, distance))
    graph_data.append([(parent, hrst)] + n)
print(graph_data)
visited = []

def astar(start, goal, place, visited):
    min=float('inf') 
    dmin=0
    s=start
    while s!=goal:
        for i in range(len(place)):
            if place[i][0][0]!=s:
                continue           
            best=None
            for j in range(1, len(place[i])):
                m=float('inf')
                for k in range(len(place)):
                    if place[i][j][0] ==place[k][0][0]:
                        m=place[k][0][1]
                        break
                h =m+place[i][j][1]
                if h<min: 
                    min=h
                    best=place[i][j][0]
                    edge=place[i][j][1]         
            if best is None:
                return "NO PATH FOUND"        
            dmin +=edge 
            visited.append(s) 
            s=best
            break
        else:
            return "NO PATH FOUND"
    visited.append(goal)
    return dmin

start ='Bucharest'
goal ='Bucharest'
a=astar(start,goal,graph_data,visited)
c = "Path: " + " -> ".join(visited)
b = "Total Distance: " + str(a)
print(c)
print(b)
w.write(c + "\n")
w.write(b + "\n")
f.close()
w.close()