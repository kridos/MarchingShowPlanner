import time
from functions import returnLinearFunction
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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
            
    def create_single_circle_plot(self, circles):
        """
        Demonstrates how to create and display a single circle using Matplotlib.
        """
        # 1. Create a figure and a set of subplots (axes)
        #    The 'fig' is the overall window, 'ax' is the plotting area.
        fig, ax = plt.subplots(figsize=(6, 6))

        # 2. Set axis limits and aspect ratio
        #    Setting equal aspect ratio ensures the circle looks like a circle, not an ellipse.
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal', adjustable='box') # Very important for circles!

        # Optional: Add a grid for better visualization of coordinates
        #ax.grid(True, linestyle='--', alpha=0.6)

        # 3. Create the Circle patch object
        #    Parameters:
        #    - (x_center, y_center): The coordinates of the circle's center
        #    - radius: The radius of the circle
        #    - color: The fill color of the circle (e.g., 'blue', 'red', hex codes like '#FF5733')
        #    - alpha: Transparency (0.0 fully transparent, 1.0 fully opaque)
        #    - ec (edgecolor): Color of the circle's border
        #    - lw (linewidth): Thickness of the circle's border

        # 4. Add the circle patch to the axes
        for circle in circles:
            ax.add_patch(circle)
        

        # 5. Add labels and title (optional, but good practice)
        ax.set_xlabel("X-coordinate")
        ax.set_ylabel("Y-coordinate")
        ax.set_title("A Single Matplotlib Circle")

        # 6. Display the plot
        plt.show()

    def run_simulation(self, duration):
        startTime = time.time()
        currentTime = startTime
        circles = []

        while(currentTime - startTime < duration):
            for player in self.players.values():
                player.updateMovement(currentTime - startTime)
                circles.append(patches.Circle(
                    (player.currentX, player.currentY),          # Center at (x=5, y=5)
                    radius=0.25,      # Radius of 2.0 units
                    color='red', # Fill color
                    alpha=1.0,       # Make fill transparent
                    ec='darkred',    # Edge color
                    lw=1             # Line width of the edge
                ))

            #draw all the circles
            self.create_single_circle_plot(circles)

            currentTime = time.time()
        
        for player in self.players.values():
                player.finalUpdate()


class Player:
    def __init__(self, coords, id):
        self.currentX = coords[0]
        self.currentY = coords[1]
        self.nextX = self.currentX
        self.nextY = self.currentY
        self.id = id
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
currField.add_player(Player((0,1), "Player 2"))
currField.updateNextPositions(5)
currField.run_simulation(5)
currField.updateNextPositions(5)



# Call the function to display the circle









