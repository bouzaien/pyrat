# Template file to create an AI for the game PyRat
# http://formations.telecom-bretagne.eu/pyrat

###############################
# When the player is performing a move, it actually sends a character to the main program
# The four possibilities are defined here
MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

import random

def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    return
##############################
#Useful functions to implement the algotihm

def add_to_explored_vertices(explored_vertices,vertex):
    explored_vertices.append(vertex)

def FIFO_push(FIFO_list,element):
    return FIFO_list.append(element)

def FIFO_pop(FIFO_list):
    return FIFO_list.pop(0)

def is_explored(explored_vertices,vertex):
    return vertex in list(explored_vertices)

def get_position_below(original_position):
    """
    Given a position (x,y) returns the position below the original position, defined as (x,y-1)
    """

    (x,y) = original_position
        
    return(x,y-1)

def get_position_right(original_position):
    """
    Given a position (x,y) returns the position to the right of the original position, defined as (x+1,y)
    """
    (x,y) = original_position
        
    return(x+1,y)

def get_position_left(original_position):
    """
    Given a position (x,y) returns the position to the left of the original position, defined as (x-1,y)
    """
    (x,y) = original_position
        
    return(x-1,y)

def get_position_above(original_position):
	(x,y) = original_position
	return (x,y+1)

def LIFO_push(LIFO_list,element):
	LIFO_list.append(element)

def LIFO_pop(LIFO_list):
	return LIFO_list.pop(-1)

def add_to_explored_vertices(explored_vertices,vertex):
    explored_vertices.append(vertex)

def is_explored(explored_vertices,vertex):
    return vertex in list(explored_vertices)

def add_to_explored_vertices(explored_vertices,vertex):
    explored_vertices.append(vertex)

def is_explored(explored_vertices,vertex):
    return vertex in list(explored_vertices)

def DFS(start_vertex, graph):

  ## First we create either a LIFO a FIFO
  queuing_structure = list()

  ## Add the starting vertex with NULL as parent
  LIFO_push(queuing_structure, start_vertex) 

  ## Initialize the outputs 
  explored_vertices = [] 
  routing_table = {} 
  while len(queuing_structure) > 0:
    (current_vertex, parent) = LIFO_pop(queuing_structure) 
    
    ## Tests whether the current vertex is
    ## in the list of explored vertices
    if not (current_vertex in explored_vertices): 
       ## Mark the current_vertex as explored
       explored_vertices.push(current_vertex) 
       
       ## Update the routing table accordingly
       routing_table[current_vertex] = parent 
       
       ## Examine neighbors of the current vertex
       for neighbor in neighbors(graph, current_vertex): 
    	   ## We push all unexplored neighbors to the queue
           if neighbor not in explored_vertices:              
              LIFO_push(neighbor, current_vertex) 
              
  return explored_vertices,routing_table   

def create_walk_from_parents(parent_dict,initial_vertex,target_vertex):
    W = []
    current_vertex = target_vertex
    while current_vertex != initial_vertex :
        W.append(current_vertex)
        current_vertex = parent_dict[current_vertex]
    return W[::-1]  

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

def walk_to_route(walk,initial_vertex):
#the function walk_to_route receives the walk as input and a vertex and returns a list of movements using the get_direction function
    M = []
    current_vertex = initial_vertex
    for move in walk :
        m = get_direction(current_vertex,move)
        M.append(m)
        current_vertex = move
        
    return M

def A_to_B(maze_graph,initial_vertex,target_vertex):
    #the function A_to_B which receives a initial vertex A and a target vertex B and returns the list of movements that should be done.
    parent_dict = DFS(maze_graph, initial_vertex)[1]
    walk = create_walk_from_parents(parent_dict,initial_vertex,target_vertex)
    return walk_to_route(walk,initial_vertex)





################################
def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):    
	LIST_OF_MOVES = A_to_B(mazeMap, playerLocation, piecesOfCheese[0])    
	return LIST_OF_MOVES[0]
