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
    return A_to_B(maze_graph=mazeMap,initial_vertex=playerLocation,target_vertex=piecesOfCheese[0])[0]

def BFS(maze_graph, initial_vertex) :
    explored_vertices = list()
    queuing_structure = list()
    parent_dict = dict()    
    add_to_explored_vertices(explored_vertices,initial_vertex)#   explored_vertices = {start_vertex}
    FIFO_push(queuing_structure,initial_vertex) # push the initial vertex to the queuing_structure
    while len(queuing_structure) > 0: #   while queuing_structure is not empty:
        current_vertex = queuing_structure.pop(0)
        neighbors_costs = maze_graph[current_vertex]
        for neighbor in neighbors_costs:
            if neighbor not in explored_vertices:
                explored_vertices.append(neighbor)
                queuing_structure.append(neighbor)
                parent_dict[neighbor] = current_vertex
    return explored_vertices,parent_dict

def add_to_explored_vertices(explored_vertices,vertex):
    explored_vertices.append(vertex)

def is_explored(explored_vertices,vertex):
    return vertex in explored_vertices

def FIFO_push(FIFO_list,element):
    FIFO_list.append(element)

def FIFO_pop(FIFO_list):
    return FIFO_list.pop(0)

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

def A_to_B(maze_graph,initial_vertex,target_vertex):
    return walk_to_route(create_walk_from_parents(BFS(maze_graph, initial_vertex)[1], initial_vertex, target_vertex), initial_vertex)
