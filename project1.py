import sys
from copy import deepcopy


DIRECTIONS=[{1:"R",3:"D"},              # A list of dictionary, index of the list is the position of zero on the puzzle(Because only zero on the puzzle
           {0:"L",2:"R",4:"D"},         # is allowed to perform a move). The position of zero has only limited directions to move: L R U D.
           {1:"L",5:"D"},               # So the directions(to move) at specific positions are the values of the dictionary, and the keys are the
           {0:"U",4:"R",6:"D"},         # corresponding destination (index of the target tile in the list).
           {1:"U",3:"L",5:"R",7:"D"},
           {2:"U",4:"L",8:"D"},
           {3:"U",7:"R"},
           {6:"L",4:"U",8:"R"},
           {5:"U",7:"L"}
]
MAN_DISTANCES=[[0,1,2,1,2,3,2,3,4],     # this is a list of lists(matrix), used to determine manhattan distance from A to B
           [1,0,1,2,1,2,3,2,3],         # usage: MAN_DISTANCES[A][B]
           [2,1,0,3,2,1,4,3,3],
           [1,2,3,0,1,2,1,2,3],
           [2,1,2,1,0,1,2,1,2],
           [3,2,1,2,1,0,3,2,1],
           [2,3,4,1,2,3,0,1,2],
           [3,2,3,2,1,2,1,0,1],
           [4,3,2,3,2,1,2,1,0]
]
OPPOSITE_MOVES={"L":"R","R":"L","U":"D","D":"U","":""} # this is used for pruning the returning move


class State:
    def __init__(self, statels, last, goal):
        # no private members for simplicity
        self.state = statels    # stored as a list
        self.lastMove = last    # last move, e.g., "U", used to prune a returning move
        self.heuristic = 0      # heuristic value of the current state
        self.nextstates = []    # the collection of next states, heuristic value is the key, ref. to the State is value
        self.goalState = goal   # reference to goal state object
        self.calcHeuristic()

    def genNextStates(self):
        posZero = self.state.index(0)
        for d in DIRECTIONS[posZero]:
            if OPPOSITE_MOVES[self.lastMove] == DIRECTIONS[posZero][d]:  # prune the returning move
                continue
            next = deepcopy(self.state)
            next[posZero], next[d] = next[d], next[posZero]  # swap the item in the list to make a move

            nextState = State(next, DIRECTIONS[posZero][d], self.goalState)
            self.nextstates.append([nextState.heuristic, nextState])

    def calcHeuristic(self):
        if self.goalState is None or self.state == self.goalState.state:
            return
        goalList = self.goalState.state
        totalManDist = 0
        for s in self.state:
            for g in goalList:
                if(self.state[s]==goalList[g]):
                    totalManDist += MAN_DISTANCES[s][g]
        self.heuristic = totalManDist

    def makeDecision(self):
        return min(self.nextstates)[1]  # make the decision of which path to go down based on heuristics

    def __lt__(self, other):
        return (self.heuristic < other.heuristic)

    def __eq__(self, other):
        if isinstance(other, State):
            return self.state == other.state
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class Puzzle:
    def __init__(self, initState, goalState):
        self.goalstate = State(goalState, "", None)
        self.initstate = State(initState, "", self.goalstate)
        self.currstate = self.initstate
        self.goalpath = []
        self.currcost = 0
        self.treesize = 1

    def solvePuzzle(self):
        if(self.currstate==self.goalstate):
            return
        self.currstate.genNextStates()
        self.treesize += len(self.currstate.nextstates)
        next = self.currstate.makeDecision()
        self.goalpath.append(next.lastMove)
        self.currstate = next
        self.currcost += 1
        self.solvePuzzle()

    def getResult(self):
        result = str(self.currcost)+"\n"+str(self.treesize)+"\n"
        for s in self.goalpath:
            result += s+" "
        return result


def main():
    fname = sys.argv[1]
    outname = sys.argv[2]
    initState=[]
    goalState=[]
    try:
        file = open(fname,"r")
    except IOError:
        print("File does not exist, or could not open file.")
        sys.exit()

    outf = open(outname,"w")
    with file:
        for i in range(0,3):
            line = file.readline()
            outf.write(line)
            for s in line.rstrip().split(" "):
                initState.append(int(s))
        outf.write(file.readline())
        for i in range(0,3):
            line = file.readline()
            outf.write(line)
            for s in line.rstrip().split(" "):
                goalState.append(int(s))
    puzzle = Puzzle(initState,goalState)
    puzzle.solvePuzzle()
    outf.write("\n\n"+puzzle.getResult())

    outf.close()
main()


    
