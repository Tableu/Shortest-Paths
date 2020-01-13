import math
import random
class Vertex:
    def __init__(self, name, x, y):     #Store coords, adjacent vertices and distance in one object
        self.coords = [x,y]
        self.adj = []
        self.name = name
        self.dist = math.inf
    def add_adj(self, num):
        self.adj.append(num)
    def update_dist(self, dist):
        self.dist = dist
def Read_File(f, Graph):
    line = 'string'
    x_cord = 'xc'
    y_cord = 'yc'
    i = 0
    st = 0
    end = 0
    #Scan through the list of vertices and store the selected ones in Graph as Vertex objects
    for x in range(0,1000):
        line = f.readline()
        
        i = 0
        while(line[i] != ':'): #Locate start of first number
            i+=1
        i+=2
        st = i
        while(line[i] != ','): #Find end of first number
            i+=1
        end = i
        x_cord = line[st:end]
        #print(x_cord)
        i+=2
        st = i
        while(line[i] != '\n'): #Find end of second number
            i+=1
        end = i
        y_cord = line[st:end]
        #print(y_cord)
        Graph.append(Vertex(x+1, float(x_cord), float(y_cord))) #Store these as a vertex object
    line = f.readline()
        
    for x in range(0,1000):
        line = f.readline()
        i = 0
        #print(target)
        while(line[i] != ':'): #Locate start of first number
            i+=1
        i+=1
        while(line[i] != '\n'): #Add adjacency list to the vertex object, exit loop if EOF is reached
            st = i+1
            while(line[i] != ',' and line[i] != '\n'):
                i+=1
            end = i
            if(line[i] != '\n'):
                i+=1
                #print(int(line[st:end],10))
                Graph[x].add_adj(int(line[st:end], 10))

def distance(q1, q2):
    dlat = 2*math.pi*(q2[0] - q1[0])/360
    mlat = 2 * math.pi * (q1[0] + q2[0]) / 2 / 360
    dlon = 2 * math.pi * (q2[1] - q1[1]) / 360
    return 6371009 * (dlat ** 2 + (math.cos(mlat) * dlon) ** 2) ** 0.5

class Heap:
    def __init__(self, graph):
        self.heap = []          #Store dist values as keys
        self.output = []        #Append the calculated distance by the algorithms here
        self.visited = []       #Append the number of vertices visited by each algorithm
        self.index = list(range(len(graph))) #Mirrors heap so each dist has a vertex assigned to it
        self.graph = graph      #Store the graph for easy access

        #Calculate Landmarks
        self.selection = [588, 915, 602]
        self.r = [[], [], []]
        for x in range(3):
            self.reset(self.selection[x])
            self.Dijkstra()
            for y in range(len(self.graph)):
                self.r[x].append(self.graph[y].dist)
    def insert(self, dist):
        self.heap.append(dist)
        n = math.floor((len(self.heap)-1)/2)
        while(n >= 0):
            self.heapify()
            n = math.floor((n-1)/2)
    def max(self,u,v):
        m = 0.0
        temp = 0.0
        for x in range(len(self.r)):
            temp = abs(self.r[x][u] - self.r[x][v])
            if(temp > m):
                m = temp
        return m
    def reset(self,u):
        for x in range(len(self.graph)):    #Set dist values to inf
            self.heap.append(math.inf)      #Initial heap is [inf,inf,inf...]
            self.graph[x].dist = math.inf
        self.index = list(range(len(self.graph))) #Set index values [0,1,2...] matches vertex index with dist
        self.graph[u-1].dist = 0                #Set target dist to 0
        self.heap[u-1] = 0
        for x in range(math.floor((len(self.graph)/2)-1),-1,-1): #heapify bottom to top before calling algorithms
            self.heapify(x)
    def heapify(self,n):
        if(n >= len(self.heap) or n < 0):
            return
        largest = n
        left = (2*n)+1
        right = (2*n)+2
        #print(largest, left, right)
        if(left < len(self.heap) and self.heap[largest] > self.heap[left]):
            largest = left    
        if(right < len(self.heap) and self.heap[largest] > self.heap[right]):
            largest = right
        if(largest != n):
            temp = self.heap[largest]           #swap parent and child
            self.heap[largest] = self.heap[n] 
            self.heap[n] = temp

            temp = self.index[largest]          #Must do the same for index heap
            self.index[largest] = self.index[n]
            self.index[n] = temp
            self.heapify(largest)
            #print(self.heap)
            #print(self.index)
    def decrease_key(self, n, dist):
        #print('decrease_key')
        try:
            n = self.index.index(n)
        except:
            return
        self.heap[n] = dist
        n = math.floor((n-1)/2)
        while(n >= 0):
            self.heapify(n)
            n = math.floor((n-1)/2)
        #self.print_heap()
    def delete_min(self):
        #print('delete_min')
        self.heap[0] = self.heap[len(self.heap)-1]
        self.index[0] = self.index[len(self.index)-1]
        del(self.heap[len(self.heap)-1])
        del(self.index[len(self.index)-1])
        self.heapify(0)
        #self.print_heap()
    def print_heap(self):
        for x in range(len(self.heap)):
            print(self.heap[x], self.index[x])
        print('\n')
    def Dijkstra(self):
        least = graph[0]
        graph_len = len(self.graph)
        visited = 0
        while(len(self.heap) != 0):
            least = self.graph[self.index[0]]
            self.delete_min()
            for y in range(len(least.adj)):
                adj = self.graph[least.adj[y]-1]
                edge_length = least.dist + distance(least.coords, adj.coords) 
                visited += 1
                if(edge_length < adj.dist):
                    adj.update_dist(edge_length)
                    self.decrease_key(least.adj[y]-1, edge_length)
                    #print(adj.dist)
        return visited
    def A(self,u,v):
        least = graph[0]
        graph_len = len(self.graph)
        visited = 0
        while(len(self.heap) != 0):
            least = self.graph[self.index[0]]
            if(self.index[0] == v-1):
                return visited
            self.delete_min()
            for y in range(len(least.adj)):
                adj = self.graph[least.adj[y]-1]
                edge_length = least.dist + distance(least.coords, adj.coords) 
                visited += 1
                if(edge_length < adj.dist):
                    adj.update_dist(edge_length)
                    self.decrease_key(least.adj[y]-1, edge_length + distance(adj.coords,self.graph[v-1].coords))
                    #print(adj.dist)
        return visited
    def Landmark(self,u,v):
        least = graph[0]
        graph_len = len(self.graph)
        visited = 0
        while(len(self.heap) != 0):
            least = self.graph[self.index[0]]
            if(self.index[0] == v-1):
                return visited
            self.delete_min()
            for y in range(len(least.adj)):
                adj = self.graph[least.adj[y]-1]
                edge_length = least.dist + distance(least.coords, adj.coords) 
                visited += 1
                if(edge_length < adj.dist):
                    adj.update_dist(edge_length)
                    self.decrease_key(least.adj[y]-1, edge_length + self.max(least.adj[y]-1, v-1))
                    #print(adj.dist)
        return visited
select = random.sample(range(1,1001),40)
graph = []
f = open('graph1000.txt')
Read_File(f, graph)
f.close()
visited = [[], [], []]
y = 0
for x in range(0,39,2):
    print("U:",select[x], "V:",select[x+1])
    heap = Heap(graph)
    #Dijkstra
    heap.reset(select[x])
    visited[0].append(heap.Dijkstra())
    heap.output.append(heap.graph[select[x+1]-1].dist)

    #A
    heap.reset(select[x])
    visited[1].append(heap.A(select[x],select[x+1]))
    heap.output.append(heap.graph[select[x+1]-1].dist)

    #Landmark
    heap.reset(select[x])
    visited[2].append(heap.Landmark(select[x],select[x+1]))
    heap.output.append(heap.graph[select[x+1]-1].dist)
    print("Dist:",heap.output, "\nVisited:",visited[0][y], visited[1][y], visited[2][y]) #Print distances calculated by each algorithm for correctness
    y += 1
print("\nAverage of Dijkstra:", sum(visited[0]) / len(visited[0]))
print("Average of A*:", sum(visited[1]) / len(visited[1]))
print("Average of Landmark:", sum(visited[2]) / len(visited[2]))
#for x in range(len(graph)):
#    print(graph[x].name, graph[x].dist)
