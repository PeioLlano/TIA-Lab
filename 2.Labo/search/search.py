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
import util

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
    examinados = {}
    camino = {}
    frontera = util.Stack()
    encontrado = False

    frontera.push((problem.getStartState(),"",None))
    
    while not frontera.isEmpty():
        
        nodo = frontera.pop()
        
        if problem.isGoalState(nodo[0]):
            encontrado = True
            break

        if nodo[0] not in examinados:
            examinados[nodo[0]] = ""
            for nuevoNodo in problem.getSuccessors(nodo[0]):
                frontera.push(nuevoNodo)
                camino[nuevoNodo] = nodo 

    coordenadas = []
    

    while nodo[0] != problem.getStartState() and encontrado:
        coordenadas.insert(0,nodo[1])
        nodo = camino[nodo]

    print(coordenadas)

    return coordenadas 


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    examinados = {}
    camino = {}
    frontera = util.Queue()
    encontrado = False

    frontera.push((problem.getStartState(),"",None))
    
    while not frontera.isEmpty():
        
        nodo = frontera.pop()
        
        if problem.isGoalState(nodo[0]):
            encontrado = True
            break

        if nodo[0] not in examinados:
            examinados[nodo[0]] = ""
            for nuevoNodo in problem.getSuccessors(nodo[0]):
                frontera.push(nuevoNodo)
                camino[nuevoNodo] = nodo 

    coordenadas = []
    

    while nodo[0] != problem.getStartState() and encontrado:
        coordenadas.insert(0,nodo[1])
        nodo = camino[nodo]

    print(coordenadas)

    return coordenadas

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    examinados = {}
    camino = {}
    frontera = util.PriorityQueue()
    encontrado = False

    frontera.push((problem.getStartState(),"",0),1)
    camino[problem.getStartState()] = ((None), 0)
    
    while not frontera.isEmpty():
        
        nodo = frontera.pop()
        
        if problem.isGoalState(nodo[0]):
            encontrado = True
            break

        if nodo[0] not in examinados:
            examinados[nodo[0]] = nodo[2]

            for nuevoNodo in problem.getSuccessors(nodo[0]):

                '''
                print('Nodo: ' + str(nodo))
                print('Nuevo nodo: ' + str(nuevoNodo))
                dictionary_items = camino.items()
                print('Camino: ')
                for item in dictionary_items:
                    print(item)
                '''

                if nuevoNodo[0] not in camino:
                    camino[nuevoNodo[0]] = (nodo,camino[nodo[0]][1]+nuevoNodo[2])
                else:
                    if camino[nuevoNodo[0]][1] > camino[nodo[0]][1]+nodo[2]:
                        camino[nuevoNodo[0]] = (nodo,camino[nodo[0]][1]+nuevoNodo[2])
                frontera.push(nuevoNodo, camino[nuevoNodo[0]][1])

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



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
