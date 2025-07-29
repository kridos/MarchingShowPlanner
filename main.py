import time
from functions import returnLinearFunction
from animation import createCircle, createAnimation, finalUpdatePosition

class Field:
    def __init__(self):
        self.players = {}

    def add_player(self, player):
        self.players[player.id] = player

    def get_player(self, player_id):
        return self.players.get(player_id)

    def updateSinglePosition(self, player_id, next_position):
        player = get_player(player_id)
        player.setNextPosition(next_position)

    def updateNextPositions(self, duration):
        for player in self.players.values():
            print(f'{player.id} ({player.currentX}, {player.currentY})')
            x = float(input("Enter the next x position: "))
            y = float(input("Enter the next y position: "))
            print()
            player.setNextPosition((x, y))
            player.determineNextPath(duration)
            
   


    def run_simulation(self, duration):
        createAnimation(duration, self.players.values())
        finalUpdatePosition(self.players.values())
        
        for player in self.players.values():
                player.finalUpdate()
                


class Player:
    def __init__(self, coords, id):
        self.currentX = coords[0]
        self.currentY = coords[1]
        self.nextX = self.currentX
        self.nextY = self.currentY
        self.id = id
        self.circle = createCircle((self.currentX, self.currentY))
        self.nextPath = Path((self.currentX, self.currentY), (self.nextX, self.nextY), "Straight", 1)

    def setNextPosition(self, coords):
        self.nextX = coords[0]
        self.nextY = coords[1]

    def determineNextPath(self, duration):
        self.nextPath = Path((self.currentX, self.currentY), (self.nextX, self.nextY), "Straight", duration)

    def startMovement(self):
        startTime = time.time()
        currentTime = time.time()

        while(currentTime - startTime < self.nextPath.duration):
            self.currentX, self.currentY = self.nextPath.currentPosition(currentTime - startTime)

            self.printCoords()
            currentTime = time.time()

        self.currentX = self.nextX
        self.currentY = self.nextY

    def updateMovement(self, time):
        self.currentX, self.currentY = self.nextPath.currentPosition(time)

    def finalUpdate(self):
        self.currentX = self.nextX
        self.currentY = self.nextY

    
    def printCoords(self):
        print(f'({self.currentX}, {self.currentY})')


class Path:
    #change type into an enum later
    def __init__(self, start, end, pathType, duration):
        self.start = start
        self.end = end
        self.duration = duration

        if pathType == "Straight":
            self.functionX = returnLinearFunction(start[0], end[0], duration)
            self.functionY = returnLinearFunction(start[1], end[1], duration)

    def currentPosition(self, currentTime):
        return (self.functionX(currentTime), self.functionY(currentTime))


currField = Field()
currField.add_player(Player((0,0), "Player 1"))
currField.add_player(Player((0,10), "Player 2"))
currField.updateNextPositions(5)
currField.run_simulation(5)
currField.updateNextPositions(5)



# Call the function to display the circle









