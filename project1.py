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
    def __init__(self, statels, g, last, lstate, goal):
        # no private members for simplicity
        self.state = statels    # stored as a list
        self.lastMove = last    # last move, e.g., "U", used to prune a returning move
        self.lastState = lstate # reference to the last state
        self.g = g              # cost to get here
        self.heuristic = 0      # heuristic value of the current state
        self.f = 0              # utility function value
        self.nextstates = []    # the collection of next states, heuristic value is the key, ref. to the State is value
        self.goalState = goal   # reference to goal state object
        self.calcHeuristic()    # automatically calculate heuristic and f after instanciated

    def genNextStates(self):
        """
        This method generates the next states and put into a list
        :return:
        """
        posZero = self.state.index(0)
        for d in DIRECTIONS[posZero]:
            if OPPOSITE_MOVES[self.lastMove] == DIRECTIONS[posZero][d]:  # prune the returning move
                continue
            next = deepcopy(self.state)
            next[posZero], next[d] = next[d], next[posZero]  # swap the item in the list to make a move

            nextState = State(next, self.g+1, DIRECTIONS[posZero][d], self, self.goalState)
            self.nextstates.append(nextState)

    def calcHeuristic(self):
        """
        this method calculates the heuristic value and update utility f
        :return:
        """
        if self.goalState is None or self.state == self.goalState.state:
            return
        goalList = self.goalState.state
        totalManDist = 0
        for s in self.state:
            for g in goalList:
                if(self.state[s]==goalList[g]):
                    totalManDist += MAN_DISTANCES[s][g]
        self.heuristic = totalManDist
        self.f= self.heuristic+self.g

    def __lt__(self, other):
        """
        overloading less than to enable sorting on utility f
        :param other:
        :return:
        """
        return (self.f < other.f)

    def __eq__(self, other):
        """
        overloading equal comparison in order to compare states
        :param other:
        :return:
        """
        if isinstance(other, State):
            return self.state == other.state
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class Puzzle:
    def __init__(self, initState, goalState):
        self.goalstate = State(goalState,0, "", None, None)
        self.initstate = State(initState,0, "", None,self.goalstate)
        self.currstate = self.initstate
        self.queue = [self.currstate]   # this is the queue for visiting the next smallest utility f
        self.goalpath = []              # this is a list for storing the goal path
        self.visited=[self.currstate.state]    # this is a list to keep track of visited states
        self.depth = 0
        self.treesize = 1

    def solvePuzzle(self):
        """
        this function will go through the queue to find the goal path
        :return:
        """
        while self.queue:
            self.queue.sort(key=lambda state: state.f)
            self.currstate = self.queue.pop(0)
            if(self.currstate.g>self.depth):
                self.depth = self.currstate.g
            if (self.currstate == self.goalstate):
                self.goalpath = self.getGoalPath(self.currstate)
                return
            self.currstate.genNextStates()
            self.treesize += len(self.currstate.nextstates)
            for next in self.currstate.nextstates:
                if next.state not in self.visited:
                    self.queue.append(next)
                    self.visited.append(next.state)

    def getGoalPath(self, state):
        """
        when the goal state is reached, this function traces back the states to generate the goal path
        :param state:
        :return:
        """
        curr = state
        path = []
        while curr!=self.initstate:
            path.insert(0,curr.lastMove)
            curr = curr.lastState
        return path

    def getResult(self):
        """
        this is for writing and printing; it generates a string that conforms to the format
        :return:
        """
        result = str(self.depth)+"\n"+str(self.treesize)+"\n"
        for s in self.goalpath:
            result += s+" "
        return result


def main():
    fname = sys.argv[1]
    outname = sys.argv[2]
    initState=[]
    goalState=[]

    try:
        file = open(fname,"r")                    # file handling
    except IOError:
        print("File does not exist, or could not open file.")
        sys.exit()

    outf = open(outname,"w")
    with file:                                  # reads through the input file and takes whats useful
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

    puzzle = Puzzle(initState,goalState)        # initializes the puzzle object and solves puzzle, then presents
    puzzle.solvePuzzle()
    outf.write("\n\n"+puzzle.getResult())
    outf.close()

def test():
    """
    for testing purpose
    :return:
    """
    puzzle = Puzzle([2,8,3,1,6,4,7,0,5], [1,2,3,8,0,4,7,6,5])
    puzzle.solvePuzzle()
    print("\n\n" + puzzle.getResult())
    puzzle = Puzzle([2,8,3,7,1,6,0,5,4], [1,2,3,8,0,4,7,6,5])
    puzzle.solvePuzzle()
    print("\n\n" + puzzle.getResult())
    puzzle = Puzzle([1,0,6,4,2,3,7,5,8], [7,4,3,5,0,6,2,8,1])
    puzzle.solvePuzzle()
    print("\n\n" + puzzle.getResult())
    puzzle = Puzzle([8,1,2,3,6,4,5,0,7], [4,2,1,8,7,0,3,5,6])
    puzzle.solvePuzzle()
    print("\n\n" + puzzle.getResult())


main()
#test()


    
