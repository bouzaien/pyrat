
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
import random
import numpy

###############################
# Please put your global variables here
visitedCells = []
MOVES = [MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, MOVE_UP]


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
    global visitedCells
    visitedCells = [playerLocation]
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
        currentPosition = visitedCells[-1]
        if len(listDiscoveryMoves(mazeMap, currentPosition)) == 0:
            possible = list(mazeMap[currentPosition].keys())
            m = moveFromLocation(currentPosition, random.choice(possible))
        else:
            m = random.choice(listDiscoveryMoves(mazeMap, visitedCells[-1]))
        visitedCells.append(step(currentPosition, m))
        return m            

def randomMove(mazeMap, currentPosition):
    positionList = [(x,y) for (x,y) in mazeMap[currentPosition]]
    return random.choice(positionList)

def step(currentPosition, move):
    D = {'D':(0,-1), 'L':(-1,0), 'R':(1,0), 'U':(0,1)}
    return tuple(numpy.add(currentPosition, D[move]))
    

def moveFromLocation(originPosition, destinationPosition):
    difference = tuple(numpy.subtract(destinationPosition, originPosition))
    moves = {(0,1):'U', (1,0):'R', (0,-1):'D', (-1,0):'L'}
    return moves[difference]

def listDiscoveryMoves(mazeMap, currentPosition):
    final = []
    possible = [(x,y) for (x,y) in mazeMap[currentPosition]]
    for (x,y) in possible:
        if (x,y) not in visitedCells:
            final.append(moveFromLocation(currentPosition, (x,y)))
    return final
