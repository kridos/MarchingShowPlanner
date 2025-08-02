import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import time


fig = plt.gcf()
ax = plt.axes(xlim = (0, 120), ylim = (0, 53.33333))
fps = 60
animations = []
anime = None
currentPath = 0

def createCircle(position):
    circle = plt.Circle(
        position,        # Center at (x=5, y=5)
        radius=1,     # Radius of 2.0 units
        color='red',     # Fill color
        alpha=1.0,       # Make fill transparent
        ec='black',    # Edge color
        lw=1             # Line width of the edge
    )
    
    ax.add_patch(circle)
    
    return circle

def getPathAtTime(currTime, player):
    global currentPath
    
    for i in range(currentPath, len(player.nextPath)):
        path = player.nextPath[i]
        if path.start_time <= currTime and currTime < path.start_time + path.duration:
            currentPath = i
            return


def updatePosition(frame, players):
    
    if frame == 0:
        global start_time
        start_time = time.time()
        
    if frame == animation_frames - 1:
        print("Animation duration:", time.time() - start_time, "seconds")
        
    currTime = time.time() - start_time
    
    getPathAtTime(currTime, players[0])
    
    drawing_circles = []
    for player in players:
        center = (player.getPath(currentPath).functionX(currTime), player.getPath(currentPath).functionY(currTime))
        player.circle.circle.set_center(center)
        drawing_circles.append(player.circle.circle)

    return drawing_circles

def finalUpdatePosition(players):
    
    for player in players:
        print(player.getLastPath().end)
        player.circle.circle.set_center(player.getLastPath().end)
        
        


def createStatic():
    global anime
    anime = None
    
    ax.set_aspect('equal')
    ax.set_xticks(np.arange(0, 120 + 1, 5))
    ax.set_yticks(np.arange(0, 54, 5))
    ax.grid(True, linestyle='--', alpha=0.6)
    
    
    fig.canvas.draw()
    
def get_global_path_index(current_time, players):
    """
    Assuming all players have the same timing and number of paths.
    Find the index i such that current_time is within players[0].nextPath[i].
    """
    for i, path in enumerate(players[0].nextPath):
        if path.start_time <= current_time < path.start_time + path.duration:
            return i
    # If time beyond last path, return last path index
    return len(players[0].nextPath) - 1
    
def run_manual_animation(players, duration):
    start_time = time.time()
    current_time = 0
    
    while current_time < duration:
        current_time = time.time() - start_time
        path_index = get_global_path_index(current_time, players)
        
        for player in players:
            if path_index < len(player.nextPath):
                path = player.nextPath[path_index]
                # Check if current time is within this path duration for player (optional safety)
                if path.start_time <= current_time < path.start_time + path.duration:
                    x = path.functionX(current_time)
                    y = path.functionY(current_time)
                    player.circle.circle.set_center((x, y))
                else:
                    # Path exists but current_time outside its interval — freeze at end
                    x, y = path.end
                    player.circle.circle.set_center((x, y))
            else:
                # Player doesn't have this path index — stay at last known position
                x, y = player.getLastPath().end
                player.circle.circle.set_center((x, y))
        
        time.sleep(0.01)  # pause briefly to update the plot
        
    # Final update
    for player in players:
        player.circle.circle.set_center(player.getLastPath().end)
        
    fig.canvas.draw()
    
    
def createAnimation(duration, players):
    global anime, start, animation_frames

    ax.set_aspect('equal')
    ax.set_xticks(np.arange(0, 120 + 1, 5))
    ax.set_yticks(np.arange(0, 54, 5))
    ax.grid(True, linestyle='--', alpha=0.6)
    animation_frames = round(duration * fps)

    anime = animation.FuncAnimation(
        fig, updatePosition,
        fargs=(players,),
        frames = animation_frames,
        interval = 1000 / fps,              
        repeat=False,       
        blit = True                   
    )

    fig.canvas.draw()
    
def getFig():
    return fig
