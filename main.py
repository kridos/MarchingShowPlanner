class Player:
    def __init__(self, coords, positions):
        self.currentX = coords[0]
        self.currentY = coords[1]
        self.nextX = currentX
        self.nextY = currentY
        self.positions = positions

    def setNextPosition(self, coords):
        self.nextX = coords[0]
        self.nextY = coords[1]

    def moveToNextPosition(self, time):

        #Placeholder for type of path
        nextPath = Path((currentX, currentY), (nextX, nextY), "Straight")

        #Placeholder for time
        positions = calculateSteps(10)

        #subtracting 1 might give a problem if there is only 1 position or if the position
        #stays the same
        timeSteps = time / (range(positions) - 1)

        currTime = 0

        while(currTime < time):

            currTime += timeSteps

            
            

    

    def printCoords(self):
        print(f'({self.x}, {self.y})')

class Path:
    #change type into an enum later
    def __init__(self, start, end, pathType):
        self.steps = 100
        self.start = start
        self.end = end
        self.pathType = pathType

    def calculateSteps(self):

        #Maybe see if I can return a function instead
        return [(start[0] + ((end[0] - start[0]) * i), start[1] + ((end[1] - start[1]) * i)) for i in range(steps + 1)]


one = Player((1, 2))
one.printCoords()
one.translateX(2)
one.translateY(3)
one.printCoords()







