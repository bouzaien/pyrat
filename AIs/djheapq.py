# Template file to create an AI for the game PyRat
# http://formations.telecom-bretagne.eu/pyrat

###############################
# When the player is performing a move, it actually sends a character to the main program
# The four possibilities are defined here
MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

###############################
# Please put your imports here
import heapq

###############################
# Please put your global variables here


###############################
# Preprocessing function
# The preprocessing function is called at the start of a game
# It can be used to perform intensive computations that can be
# used later to move the player in the maze.
###############################
# Arguments are:
# mazeMap : dict(pair(int, int), dict(pair(int, int), int))
# mazeWidth : int
# mazeHeight : int
# playerLocation : pair(int, int)
# opponentLocation : pair(int,int)
# piecesOfCheese : list(pair(int, int))
# timeAllowed : float
###############################
# This function is not expected to return anything
def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    pass

###############################
# Turn function
# The turn function is called each time the game is waiting
# for the player to make a decision (a move).
###############################
# Arguments are:
# mazeMap : dict(pair(int, int), dict(pair(int, int), int))
# mazeWidth : int
# mazeHeight : int
# playerLocation : pair(int, int)
# opponentLocation : pair(int, int)
# playerScore : float
# opponentScore : float
# piecesOfCheese : list(pair(int, int))
# timeAllowed : float
###############################
# This function is expected to return a move
def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    return A_to_B(mazeMap, playerLocation, piecesOfCheese[0])[0]

# heap_pop function returns the first element of the list implementing the heap, providing the heap is not empty
def heap_pop(heap):
    if heap != []:
        vertex,weight,parent = heap.pop(0)
        return (vertex, weight, parent)
    else:
        raise

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
    
def Dijkstra(maze_graph,initial_vertex):
    # Variable storing the exploredled vertices vertexes not to go there again
    explored_vertices = list()
    
    # Stack of vertexes
    heap = list()
    
    #Parent dictionary
    parent_dict = dict()
    # Distances dictionary
    distances = dict()
    
    # First call
    initial_vertex = (initial_vertex, 0, initial_vertex)#vertex to visit, distance from origin, parent
    heap_add_or_replace(heap,initial_vertex)
    while len(heap) > 0:
        # get the triplet (vertex, distance, parent) with the smallest distance from heap list using heap_pop function.
        # if the vertex of the triplet is not explored:
        #     map the vertex to its corresponding parent
        #     add vertex to explored vertices.
        #     set distance from inital_vertex to vertex
        #     for each unexplored neighbor i of the vertex, connected through an edge of weight wi
        #         add (i, distance + wi, vertex) to the heap
        
        smallest = heapq.heappop(heap)
        if not is_explored(explored_vertices, smallest[0]):
            parent_dict[smallest[0]] = smallest[2]
            add_to_explored_vertices(explored_vertices, smallest[0])
            distances[smallest[0]] = smallest[1]
            for i in maze_graph[smallest[0]]:
                if not is_explored(explored_vertices, i):
                    heapq.heappush(heap, (i, distances[smallest[0]] + maze_graph[smallest[0]][i], smallest[0]))
    return explored_vertices, parent_dict, distances

def A_to_B(maze_graph,initial_vertex,target_vertex):
    # use the Dijkstra algorithm to generate parent_dictionary
    # use the parent_dictionary, the source vertex, and end vertex to generate a walk between these two points using the utils.create_walk_from_parents function.
    # return a list of movements using the utils.walk_to_route function.
    parent_dictionary = Dijkstra(maze_graph,initial_vertex)[1]
    walk = create_walk_from_parents(parent_dictionary, initial_vertex, target_vertex)
    return walk_to_route(walk, initial_vertex)

def create_walk_from_parents(parent_dict,initial_vertex,target_vertex):
    temp = parent_dict[target_vertex]
    walk = [target_vertex]
    while temp != initial_vertex:
        walk.append(temp)
        temp = parent_dict[temp]
    return walk[::-1]

def get_direction(initial_vertex,target_vertex):
    if get_position_above(initial_vertex) == target_vertex:
        return MOVE_UP
    elif get_position_below(initial_vertex) == target_vertex:
        return MOVE_DOWN
    elif get_position_left(initial_vertex) == target_vertex:
        return MOVE_LEFT
    elif get_position_right(initial_vertex) == target_vertex:
        return MOVE_RIGHT
    else:
        raise Exception("vertices are not connected")

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

def walk_to_route(walk,initial_vertex):
    walkToRoute = [get_direction(initial_vertex,walk[0])]
    for i in range(len(walk)-1):
        walkToRoute.append(get_direction(walk[i],walk[i+1]))
    return walkToRoute