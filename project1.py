class State:
    

class Puzzle:
    def __init__(self, statels, curr_cost):
        self.state = statels
        self.next_states = []
        self.currentcost=curr_cost
        self.heuristic = 0
        

    def getCurrentState(self):
        return self.state

    def setCurrentState(self,statels):
        self.state = statels

    def setNextPuzzle(self, nextstate):
        


    
