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
from operator import itemgetter

###############################
# Please put your global variables here
movements = list()
newPieces = list()
N = list()

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
    global movements
    global newPieces
    global N
    l1, l2, l3, l4 = diviseMap(mazeWidth, mazeHeight, piecesOfCheese, 4)
    # this function computes the list of movements from the previous exercise
    # and store them in the variable movements
    n1 = backtrackTSP(mazeMap, l1, playerLocation)[0]
    n2 = backtrackTSP(mazeMap, l2, playerLocation)[0]
    n3 = backtrackTSP(mazeMap, l3, playerLocation)[0]
    n4 = backtrackTSP(mazeMap, l4, playerLocation)[0]
    print(n1)
    print(n2)
    print(n3)
    print(n4)
    N = n1 + n2 + n4 + n3
    # movements = A_to_all(mazeMap, playerLocation, newPieces)
    # Example prints that appear in the shell only at the beginning of the game
    # Remove them when you write your own program


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
    lastPieces = [piece for piece in N if piece in piecesOfCheese]
    lastMouvements = A_to_all(mazeMap, playerLocation, lastPieces)
    print(lastPieces)
    return FIFO_pop(lastMouvements)

def create_vertices_meta_graph(piece_of_cheese, player_location):
    return piece_of_cheese + [player_location]

def create_edge_weight_maze_graph(maze_graph,vertices):
    adjacency_matrix={}
    # for each initial_vertex in vertices:
    #     considere this vertex as source vertex
    #     use this source vertex and maze_graph to browse the graph with dijkstra algorithm
    #     for each vertex in vertices:
        #     use adjacency_matrix to store distances between source vertex and each vertex in the graph.
        #     remember to not store the distance from the source vertex to itself.
    for initial_vertex in vertices:
        explored_vertices, _, distances = Dijkstra(maze_graph,initial_vertex)
        adjacency_matrix[initial_vertex] = {}
        for vertex in vertices:
            if vertex != initial_vertex:
                adjacency_matrix[initial_vertex][vertex] = distances[vertex]
    return adjacency_matrix

def auxbt(current_walk, best_walk, adjacency_matrix, vertices, current_distance, best_distance):
    # First we test if the current walk have gone through all vertices
    # if that is the case, we compare the current distance to the best distance
    # and in the case it is better we update the best distance and the best walk
    # if the current_walk is not finished, for each possible vertex not explored,
    # we add it and call ourself recursively    
    
    if(len(current_walk) > len(vertices)):
        if(current_distance < best_distance):
            best_distance = current_distance
            best_walk = current_walk            
    elif current_distance < best_distance:
        for next_vertex in vertices:
            if not (next_vertex in current_walk):                            
                best_walk_temp, best_distance_temp = auxbt(current_walk + [next_vertex], best_walk, adjacency_matrix, vertices, current_distance + adjacency_matrix[current_walk[-1]][next_vertex], best_distance)
                
                if best_distance_temp < best_distance:
                    best_distance = best_distance_temp
                    best_walk = best_walk_temp
    
    return best_walk,best_distance
                    
def backtrackTSP(maze_graph, pieces_of_cheese, player_location):
    # first we compute the vertices of the meta_graph:
    vertices = create_vertices_meta_graph(pieces_of_cheese, player_location)
    # then we create the adjacency matrix of the meta graph
    adjacency_matrix = create_edge_weight_maze_graph(maze_graph, vertices)
    
    # now we can start defining our variables
    # current_distance is the length of the walk for the current exploration branch
    current_distance = 0
    # current_walk is a container for the current exploration branch
    current_walk = [player_location]
    # best_distance is an indicator of the shortest walk found so far
    best_distance = float('inf')
    # best_walk is a container for the corresponding walk
    best_walk = []
    
    # we start the exploration:
    best_walk, best_distance = auxbt(current_walk, best_walk, adjacency_matrix, pieces_of_cheese, current_distance, best_distance)
    return best_walk, best_distance

def A_to_all(maze_graph, initial_vertex, vertices):
    list_of_movement = list(A_to_B(maze_graph, initial_vertex, vertices[0]))
    for i in range(len(vertices)-1):
        list_of_movement += A_to_B(maze_graph, vertices[i], vertices[i+1])
    return list_of_movement

def FIFO_pop(FIFO_queue):
    return FIFO_queue.pop(0)
   

###############################
# utils.py

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

def reset_game(pyrat,game,starting_point,end_point):
    pyrat.pieces = 1
    game.pieces_of_cheese = [end_point]
    game.player1_location = starting_point
    game.history["pieces_of_cheese"] = [game.convert_cheeses()]
    game.history["player1_location"] = [list(starting_point)]
    game.play_match()
    return game

def create_walk_from_parents(parent_dict,source_node,end_node):
    
    route = list()
    next_node = end_node
    while next_node != source_node:
        route.append(next_node)
        next_node = parent_dict[next_node]
    return list(reversed(route))
   
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

def walk_to_route(walk,source_node):
    
    route = list()
    for node in walk:
        direction = get_direction(source_node,node)
        route.append(direction)
        source_node = node
    return route

def is_labeled(labeled_vertices,vertex):
    return vertex in labeled_vertices

def add_to_labeled_vertices(labeled_vertices,vertex):
    labeled_vertices.append(vertex)

def heap_pop(heap):

    node,weight,parent = heap.pop(0)
    
    return (node, weight, parent)


def heap_add_or_replace(heap, triplet):
    
    add=False
    if(len(heap)==0):
        heap.append(triplet)
    
    else:
        index=len(heap)
        for i in range(len(heap)):
            if(heap[i][0]==triplet[0]):
                
                if(heap[i][1]<=triplet[1]):
                    return 0
                else:
                    heap.pop(i)
                    if(add==False):
                        index=i
                    break
                        
            if(add==False):
                if(heap[i][1]>triplet[1]):
                    index=i
                    add=True
             
        heap.insert(index,triplet)

def Dijkstra(maze_graph,sourceNode):
    # Variable storing the labeled vertices nodes not to go there again
    labeled_vertices = list()
    
    # Stack of nodes
    heap = list()
    
    #Parent Dictionary
    parent_dict = dict()
    # Distances 
    distances = dict()
    
    # First call
    initial_tuple = (sourceNode, 0, sourceNode)#Node to visit, distance from origin, parent
    heap_add_or_replace(heap,initial_tuple)
    while len(heap) > 0:
        # get the tuple  with the smallest weight from heap list using heap_pop function.
        # if tuple is not labeled:
        #     map the obtained parent in tuple as parent of the node.
        #     add node to labeled vertices.
        #     compute distance from initial point to the node.
        #     get all node's neighbor and their corresponding weights.
        #     add all these neighbor to heap.
        #     repeat this process until we visit all graph's nodes.
        (node, cost, parent) = heap_pop(heap)
        if not (is_labeled(labeled_vertices, node)):
            parent_dict[node] = parent
            add_to_labeled_vertices(labeled_vertices, node)
            distances[node] = cost
            for neighbor in maze_graph[node]:
                if not (is_labeled(labeled_vertices, neighbor)):
                    heap_add_or_replace(heap, (neighbor, cost + maze_graph[node][neighbor], node))
    
    return labeled_vertices, parent_dict, distances

def A_to_B(maze_graph,node_source,node_end):
    
    labeled_vertices,parent_dict,_ = Dijkstra(maze_graph,node_source)
    walk = create_walk_from_parents(end_node=node_end,source_node=node_source,parent_dict=parent_dict)
    return walk_to_route(walk,node_source)

def diviseMap(x, y, cheeses, number):
    L1, L2 = list(), list()
    for cheese in cheeses:
        if cheese[0] <= x//2:
            L1.append(cheese)
        else:
            L2.append(cheese)

    L1 = sorted(L1, key=itemgetter(1))
    L11 = L1[:len(L1)//2]
    L21 = L1[len(L1)//2:]
    L2 = sorted(L2, key=itemgetter(1))
    L12 = L2[:len(L2)//2]
    L22 = L2[len(L2)//2:]
    return L11, L12, L21, L22
