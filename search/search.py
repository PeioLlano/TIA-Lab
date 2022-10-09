# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from multiprocessing.connection import wait
from platform import node
from time import sleep, time
import util
import searchAgents

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    frontera = util.Stack()
    examinados = {}
    frontera.push((problem.getStartState(), []))

    while not frontera.isEmpty():
        #nodo -> ((x,y),[lista de coordenadas])
        #nodo -> (((x,y), (lista de corners)),[lista de coordenadas])
        nodo = frontera.pop()

        if problem.isGoalState(nodo[0]):
            return nodo[1]

        #nuevoNodo -> ((x,y),'coordenada', coste)
        for nuevoNodo in problem.getSuccessors(nodo[0]):
            print(nuevoNodo)
            if nuevoNodo[0] not in examinados:
                frontera.push((nuevoNodo[0], nodo[1] + [nuevoNodo[1]]))

        examinados[nodo[0]] = True

    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontera = util.Queue()
    examinados = {}
    frontera.push((problem.getStartState(), []))

    while not frontera.isEmpty():
        #nodo -> ((x,y),[lista de coordenadas])
        #nodo -> (((x,y), (lista de corners)),[lista de coordenadas])
        nodo = frontera.pop()

        if problem.isGoalState(nodo[0]):
            return nodo[1]

        #nuevoNodo -> ((x,y),'coordenada', coste)
        for nuevoNodo in problem.getSuccessors(nodo[0]):
            if nuevoNodo[0] not in examinados:
                frontera.push((nuevoNodo[0], nodo[1] + [nuevoNodo[1]]))
                examinados[nuevoNodo[0]] = True

        examinados[nodo[0]] = True

    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    frontera = util.PriorityQueue()
    examinados = {}
    frontera.push((problem.getStartState(), [], 0),1)

    while not frontera.isEmpty():
        # nodo -> ((x,y),[lista de coordenadas], coste)
            # nodo[0] -> (x,y)
            # nodo[1] -> [lista de coordenadas]
            # nodo[2] -> coste
        # nodo -> (((x,y), (lista de corners)),[lista de coordenadas], coste)
            # nodo[0] -> ((x,y), (lista de corners))
            # nodo[1] -> [lista de coordenadas]
            # nodo[2] -> coste

        nodo = frontera.pop()

        if problem.isGoalState(nodo[0]):
            return nodo[1]


        if nodo[0] not in examinados:
            examinados[nodo[0]] = nodo[2] #añado el coste

            # nuevoNodo -> ((x,y),'coordenada', coste)
                # nuevoNodo[0] -> (x,y)
                # nuevoNodo[1] -> coordenada
                # nuevoNodo[2] -> coste
            # nuevoNodo -> (((x,y), (corners)),'coordenada', coste)
                # nuevoNodo[0] -> ((x,y), (corners))
                # nuevoNodo[1] -> coordenada
                # nuevoNodo[2] -> coste
            for nuevoNodo in problem.getSuccessors(nodo[0]):
                if nuevoNodo[0] not in examinados:
                    frontera.push((nuevoNodo[0], nodo[1] + [nuevoNodo[1]], nuevoNodo[2]+nodo[2]), nuevoNodo[2]+nodo[2])
        
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    frontera = util.PriorityQueue()
    examinados = {}
    frontera.push((problem.getStartState(), [], 0),1)

    while not frontera.isEmpty():
        # nodo -> ((x,y),[lista de coordenadas], coste)
            # nodo[0] -> (x,y)
            # nodo[1] -> [lista de coordenadas]
            # nodo[2] -> coste
        # nodo -> (((x,y), (lista de corners)),[lista de coordenadas], coste)
            # nodo[0] -> ((x,y), (lista de corners))
            # nodo[1] -> [lista de coordenadas]
            # nodo[2] -> coste

        nodo = frontera.pop()

        if problem.isGoalState(nodo[0]):
            return nodo[1]


        if nodo[0] not in examinados:
            examinados[nodo[0]] = nodo[2] #añado el coste

            # nuevoNodo -> ((x,y),'coordenada', coste)
                # nuevoNodo[0] -> (x,y)
                # nuevoNodo[1] -> coordenada
                # nuevoNodo[2] -> coste
            # nuevoNodo -> (((x,y), (corners)),'coordenada', coste)
                # nuevoNodo[0] -> ((x,y), (corners))
                # nuevoNodo[1] -> coordenada
                # nuevoNodo[2] -> coste
            for nuevoNodo in problem.getSuccessors(nodo[0]):
                if nuevoNodo[0] not in examinados:
                    frontera.push((nuevoNodo[0], nodo[1] + [nuevoNodo[1]], nuevoNodo[2]+nodo[2]), nuevoNodo[2]+nodo[2]+heuristic(nuevoNodo[0],problem))
    coordenadas = []

    '''
    print('Encontrado? ' + str(encontrado))
    print('Nodo final: ' + str(nodo))
    print('Coste: ' + str(camino[nodo[0]][1]))
    
    dictionary_items = camino.items()
    for item in dictionary_items:
        print(item)
    '''
        
    while nodo[0] != problem.getStartState() and encontrado:
        coordenadas.insert(0,nodo[1])
        nodo = camino[nodo[0]][0]

    return coordenadas 


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
