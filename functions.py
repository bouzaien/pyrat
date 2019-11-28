TEAM_NAME = "Greedy"

MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

import matplotlib.pyplot as plt
import time
import heapq
from operator import itemgetter, attrgetter


def locationsToMove (location1, location2) :

    difference = (location2[0] - location1[0], location2[1] - location1[1])
    if difference == (-1, 0) :
        return MOVE_LEFT
    elif difference == (1, 0) :
        return MOVE_RIGHT
    elif difference == (0, 1) :
        return MOVE_UP
    elif difference == (0, -1) :
        return MOVE_DOWN
    else :
        raise Exception("Invalid location provided")
    

def dijkstra (mazeMap, initialLocation) :

    minHeap = [(0, initialLocation, None)]
    distances = {}
    routes = {}
    
    while len(minHeap) != 0 :
        (distance, location, predecessor) = heapq.heappop(minHeap)
        if location not in distances :
            distances[location] = distance
            routes[location] = predecessor
            for neighbor in mazeMap[location] :
                newDistanceToNeighbor = distance + mazeMap[location][neighbor]
                heapq.heappush(minHeap, (newDistanceToNeighbor, neighbor, location))
    return (routes, distances)


def Dijkstra(maze_graph,initial_vertex):

    explored_vertices = list()
    heap = list()
    parent_dict = dict()
    distances = dict()
    initial_vertex = (initial_vertex, 0, initial_vertex)#vertex to visit, distance from origin, parent
    heap_add_or_replace(heap,initial_vertex)
    while len(heap) > 0:
        smallest = heapq.heappop(heap)
        if not is_explored(explored_vertices, smallest[0]):
            parent_dict[smallest[0]] = smallest[2]
            add_to_explored_vertices(explored_vertices, smallest[0])
            distances[smallest[0]] = smallest[1]
            for i in maze_graph[smallest[0]]:
                if not is_explored(explored_vertices, i):
                    heapq.heappush(heap, (i, distances[smallest[0]] + maze_graph[smallest[0]][i], smallest[0]))
    return explored_vertices, parent_dict, distances


def routesToPath (routes, targetNode) :
    
    if not targetNode :
        return []
    elif targetNode in routes :
        return routesToPath(routes, routes[targetNode]) + [targetNode]
    else :
        raise Exception("Impossible to reach target")


def pathToMoves (path) :
    
    if len(path) <= 1 :
        return []
    else :
        return [locationsToMove(path[0], path[1])] + pathToMoves(path[1:])


def findClosestPieceOfCheese (distances, piecesOfCheese) :
    
    distancesToCheese = {cheese : distances[cheese] for cheese in piecesOfCheese}
    return min(distancesToCheese, key=distancesToCheese.get)


def chemin(mazeMap, piecesOfCheese ) : 
    resultChemin = []
    for i in range (len(piecesOfCheese) - 1) : 
        dji = Dijkstra (mazeMap, piecesOfCheese[i])[1] 
        walk = create_walk_from_parents (dji,piecesOfCheese[i],piecesOfCheese[i+1])
        ajout = walk_to_route(walk,piecesOfCheese[i]) 
        for element in ajout : 
            resultChemin.append(element) 
    print (resultChemin)
    return resultChemin


def walk_to_route(walk,source_node):
    
    route = list()
    for node in walk:
        direction = get_direction(source_node,node)
        route.append(direction)
        source_node = node
    return route
        

def swap2opt(piecesOfCheese, i, k):
    t0 = time.time()
    newRoute = piecesOfCheese[0:i]
    newRoute.extend(reversed(piecesOfCheese[i:k+1]))
    newRoute.extend(piecesOfCheese[k+1:])
    return newRoute


def totalDistance(mazeMap, playerLocation, piecesOfCheese):
    meta = create_edge_weight_maze_graph(mazeMap, [playerLocation] + piecesOfCheese)
    S = meta[playerLocation][piecesOfCheese[0]]
    for i in range(len(piecesOfCheese)-1):
        S += meta[piecesOfCheese[i]][piecesOfCheese[i+1]]
    return S


def create_edge_weight_maze_graph(maze_graph, vertices):
    adjacency_matrix={}
    for initial_vertex in vertices:
        explored_vertices,_, distances = Dijkstra(maze_graph,initial_vertex)
        adjacency_matrix[initial_vertex] = {}
        for vertex in vertices:
            if vertex != initial_vertex : 
                adjacency_matrix[initial_vertex][vertex] = distances[vertex]
    return adjacency_matrix

def swap3opt(mazeMap, playerLocation, piecesOfCheese, i, j, k):
    "If reversing tour[i:j] would make the tour shorter, then do it."
    # Given tour [...A-B...C-D...E-F...]
    A, B, C, D, E, F = piecesOfCheese[i-1], piecesOfCheese[i], piecesOfCheese[j-1], piecesOfCheese[j], piecesOfCheese[k-1], piecesOfCheese[k % len(piecesOfCheese)]
    meta = create_edge_weight_maze_graph(mazeMap, [playerLocation] + piecesOfCheese)
    d0 = meta[A][B] + meta[C][D] + meta[E][F]
    d1 = meta[A][C] + meta[B][D] + meta[E][F]
    d2 = meta[A][B] + meta[C][E] + meta[D][F]
    d3 = meta[A][D] + meta[E][B] + meta[C][F]
    d4 = meta[F][B] + meta[C][D] + meta[E][A]
    # print(d0,d1,d2,d3,d4)

    if d0 > d1:
      piecesOfCheese[i:j] = reversed(piecesOfCheese[i:j])
      return -d0 + d1
    elif d0 > d2:
      piecesOfCheese[j:k] = reversed(piecesOfCheese[j:k])
      return -d0 + d2
    elif d0 > d4:
      piecesOfCheese[i:k] = reversed(piecesOfCheese[i:k])
      return -d0 + d4
    elif d0 > d3:
      tmp = piecesOfCheese[j:k], piecesOfCheese[i:j]
      piecesOfCheese[i:k] = tmp
      return -d0 + d3
    return 0


def run3opt(mazeMap, playerLocation, piecesOfCheese):
    pieces = piecesOfCheese
    "Iterative improvement based on 3 exchange."
    delta = 0
    for (a,b,c) in all_segments(len(pieces)):
        
        delta += swap3opt(mazeMap, playerLocation, pieces, a, b, c)

    if delta < 0:
        return run3opt(mazeMap, playerLocation, pieces)
    print(piecesOfCheese)
    print(pieces)
    return pieces

def all_segments(N):
    "Generate all segments combinations"
    return [(i, j, k) for i in range(N) for j in range(i+2, N) for k in range(j+2, N+(i>0))]

def run2opt(mazeMap,playerLocation,piecesOfCheese, timeAllowed):
    improvement = True
    bestRoute = piecesOfCheese
    bestDistance = totalDistance(mazeMap, playerLocation, piecesOfCheese)
    td = [bestDistance]
    te = [0]
    t0 = time.time()
    while improvement and time.time()-t0 < timeAllowed/1000: 
        improvement = False
        for i in range(len(bestRoute) - 1):
            for k in range(i+1, len(bestRoute)):
                newRoute = swap2opt(bestRoute, i, k)
                newDistance = totalDistance(mazeMap, playerLocation, newRoute)
                if newDistance < bestDistance:
                    td.append(newDistance)
                    te.append(time.time()-t0)
                    bestDistance = newDistance
                    bestRoute = newRoute
                    improvement = True
                    break #improvement found, return to the top of the while loop
            if improvement:
                break
    '''plt.plot(te, td, color = 'r', label='Distance totale à effectuer')
    plt.xlabel('Temps')
    plt.ylabel('Distance')
    plt.legend()
    plt.title("L'amélioration de la distance en fonction du temps")
    plt.show()'''
    return bestRoute


def create_vertices_meta_graph(piece_of_cheese, player_location):
    return piece_of_cheese + [player_location]


def create_walk_from_parents(parent_dict,initial_vertex,target_vertex):
    temp = parent_dict[target_vertex]
    walk = [target_vertex]
    while temp != initial_vertex:
        walk.append(temp)
        temp = parent_dict[temp]
    return walk[::-1]


def walkToAll(mazeMap, playerLocation, vertices):
    w = [create_walk_from_parents(Dijkstra(mazeMap, playerLocation)[1], playerLocation, vertices[0])]
    for i in range (len(vertices)-1):
        w.append(create_walk_from_parents(Dijkstra(mazeMap, vertices[i])[1], vertices[i], vertices[i+1]))
    return w
     

def insertionSort(heap, alist):
    for index in range(1, len(alist)):
        currentvalue = alist[index]
        heapcurrentvalue = heap[index]
        position = index
        while position > 0 and alist[position-1] > currentvalue:
            alist[position] = alist[position-1]
            heap[position] = heap[position-1]
            position = position-1
        alist[position] = currentvalue
        heap[position] = heapcurrentvalue
        

def heap_add_or_replace(heap, triplet):
    heapDict = {trip[0]:trip[1] for trip in heap}
    if len(heap) == 0:
        heap.append(triplet)
    else:
        if triplet[0] in heapDict:
            if triplet[1] < heapDict[triplet[0]]:
                heapDict[triplet[0]] = triplet[1]
                for k in range(len(heap)):
                    if heap[k][0] == triplet[0]:
                        heap[k] = triplet
        else:
            heap.append(triplet)
    insertionSort(heap, [trip[1] for trip in heap])


def is_explored(explored_vertices,vertex):
    return vertex in explored_vertices


def add_to_explored_vertices(explored_vertices,vertex):
    explored_vertices.append(vertex)

def get_direction(source_node,end_node):
    if get_position_above(source_node) == end_node:
        return MOVE_UP
    elif get_position_below(source_node) == end_node:
        return MOVE_DOWN
    elif get_position_left(source_node) == end_node:
        return MOVE_LEFT
    elif get_position_right(source_node) == end_node:
        return MOVE_RIGHT
    else:
        raise Exception("Nodes are not connected")

def get_position_above(original_position):
    """
    Given a position (x,y) returns the position above the original position, defined as (x,y+1)
    """
    (x,y) = original_position
    return (x,y+1)


def get_position_below(original_position):
    """
    Given a position (x,y) returns the position below the original position, defined as (x,y-1)
    """
    (x,y) = original_position
    return (x,y-1)

def get_position_right(original_position):
    """
    Given a position (x,y) returns the position to the right of the original position, defined as (x+1,y)
    """
    (x,y) = original_position
    return (x+1,y)

def get_position_left(original_position):
    """
    Given a position (x,y) returns the position to the left of the original position, defined as (x-1,y)
    """
    (x,y) = original_position
    return (x-1,y)

def sortCheese(piecesOfCheese):
   return sorted(piecesOfCheese, key=itemgetter(0))


def A_to_B(maze_graph,initial_vertex,target_vertex):
    parent_dictionary = Dijkstra(maze_graph,initial_vertex)[1]
    walk = create_walk_from_parents(parent_dictionary, initial_vertex, target_vertex)
    return walk_to_route(walk, initial_vertex)

def mergeSort(playerLocation, alist):
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(playerLocation, lefthalf)
        mergeSort(playerLocation, righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if distance(playerLocation, lefthalf[i]) < distance(playerLocation, righthalf[j]):
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1
    return alist

def distance(playerLocation, couple):
    return (playerLocation[0]-couple[0])**2+(playerLocation[1]-couple[1])**2
