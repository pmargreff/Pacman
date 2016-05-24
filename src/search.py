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

import util
import math
import random

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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    start = problem.getStartState()
    visited = []
    actionList = []
    priorityQueue = util.PriorityQueue()
 
    priorityQueue.push((start, actionList), nullHeuristic)
     
    while not priorityQueue.isEmpty():
     	node,actions = priorityQueue.pop()
     	
     	if not node in visited:
     		visited.append(node)
    		if problem.isGoalState(node):
    			return actions
    		for coord, direction, cost in problem.getSuccessors(node):
    			if not coord in visited:
    				newActions = actions + [direction]
    				priorityQueue.push((coord, newActions), problem.getCostOfActions(newActions))

    return actions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    nodosVisitados = []
    fila = util.PriorityQueue()
    nodoInicial = problem.getStartState()
    fila.push( (nodoInicial, []), heuristic(nodoInicial,problem))
    while not fila.isEmpty():
        
        nodoAtual, caminho = fila.pop()

        if problem.isGoalState(nodoAtual):
            return caminho

        nodosVisitados.append(nodoAtual)
        

        for sucessor, direcao, custo in problem.getSuccessors(nodoAtual):
            if not sucessor in nodosVisitados:
                novoCaminho = caminho + [direcao]
                score = problem.getCostOfActions(novoCaminho) + heuristic(sucessor, problem)
                fila.push( (sucessor, novoCaminho), score)
               
    return caminho

def hillClimbing(problem, heuristic=nullHeuristic):
    caminho = []
    #pega nodo inicial
    nodoAtual = problem.getStartState()
    nodoAtual = ( (nodoAtual, []), heuristic(nodoAtual,problem))
    
    while True:
        custoEscolhido = nodoAtual[1]
        
        fila = util.PriorityQueue()
        
        #pega vizinhos e coloca em fila de prioridade
        for state, direction, cost in problem.getSuccessors(nodoAtual[0][0]):
           novoCaminho = [direction]
           score = problem.getCostOfActions(novoCaminho) + heuristic(state, problem)

           fila.push((state, novoCaminho), score)
        
        #analisa primeiro da fila
        analisado = []
        analisado = fila.pop()

        custoAnalisado = problem.getCostOfActions(analisado[1]) + heuristic(analisado[0], problem) - 1
        
        if (custoEscolhido > custoAnalisado):
            caminho = caminho + (analisado[1])
            nodoAtual = ( (analisado[0], analisado[1]), custoAnalisado)
        else:
            break
                   
    return caminho    

def simulatedAnnealing(problem):
    caminho = []
    nodoAtual = problem.getStartState()
    actionNodoAtual = []
    T = 1.0
    alpha = 1.2
    
    while True:
        i = 0
        fila = util.Queue()
        for state, direction, cost in problem.getSuccessors(nodoAtual):
            novoCaminho = [direction]
            fila.push((state,novoCaminho))
            i = i + 1

        sucessorAleatorio = random.randint(0,i-1)
        
        if sucessorAleatorio > 0:
            for j in range(0, sucessorAleatorio+1):
                nodoProximo, action = fila.pop()
        else:
            nodoProximo, action = fila.pop()

        E = problem.getCostOfActions(action) - problem.getCostOfActions(actionNodoAtual)
        if E < 0:
            nodoAtual = nodoProximo
            actionNodoAtual = action
            caminho = caminho + actionNodoAtual
        else:
            if math.exp(-E/T):
                nodoAtual = nodoProximo
                actionNodoAtual = action
                caminho = caminho + actionNodoAtual
        

        if problem.isGoalState(nodoAtual):
            return caminho

        T = T*alpha


    return caminho

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
hc = hillClimbing
sa = simulatedAnnealing
