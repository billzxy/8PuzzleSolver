direction={0:{1:"R",3:"D"}
           1:{0:"L",2:"R",4:"D"}
           2:{1:"L",5:"D"}
           3:{0:"U",4:"R",6:"D"}
           4:{1:"U",3:"L",5:"R",7:"D"}
           5:{2:"U",4:"L",8:"D"}
           6:{3:"U",7:"R"}
           7:{6:"L",4:"U",8:"R"}
           8:{5:"U",7:"L"}
}
man_distance={0:[0,1,2,1,2,3,2,3,4]
           1:[1,0,1,2,1,2,3,2,3]
           2:[2,1,0,3,2,1,4,3,3]
           3:[1,2,3,0,1,2,1,2,3]
           4:[2,1,2,1,0,1,2,1,2]
           5:[3,2,1,2,1,0,3,2,1]
           6:[2,3,4,1,2,3,0,1,2]
           7:[3,2,3,2,1,2,1,0,1]
           8:[4,3,2,3,2,1,2,1,0]
}
class State:
    def __init__(self, statels, heu):
        #no private members for simplicity
        self.state = statels
        self.heuristic = heu
        self.nextstates = []

    def genNextStates(self, nextstate):
        
    def calcHeuristic(self, goalState):
        goalList = goalState.state
        totalManDist = 0
        for s in self.state:
            for g in goalList:
                

    def makeDecision(self):
        
        return 

    def __eq__(self, other):
        if isinstance(other, State):
            return self.state == other.state
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

class Puzzle:
    def __init__(self, initState, goalState):
        self.initstate = State(initState)
        self.currstate = initstate
        self.goalstate = State(goalState)
        self.goalpath = []
        self.currcost = 0
        self.treesize = 1
        

    
        


    
