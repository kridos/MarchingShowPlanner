import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

interval_amt = 50
fig = plt.gcf()
ax = plt.axes(xlim = (0, 120), ylim = (0, 53.33333))

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

def updatePosition(frame, players):
    drawing_circles = []
    for player in players:
        center = (player.nextPath.functionX(frame * (interval_amt / 1000)), player.nextPath.functionY(frame * (interval_amt / 1000)))
        player.circle.set_center(center)
        drawing_circles.append(player.circle)

    return drawing_circles

def finalUpdatePosition(players):
    
    for player in players:
        player.circle.set_center((player.nextX, player.nextY))
        


def createAnimation(duration, players, static):
    
    ax.set_aspect('equal')
    ax.set_xticks(np.arange(0, 120 + 1, 5))
    ax.set_yticks(np.arange(0, 54, 5))
    ax.grid(True, linestyle='--', alpha=0.6)
    
    
        
    
    if not static:
        anime = animation.FuncAnimation(
            fig, updatePosition,
            fargs=(players,),
            frames = (duration * 1000 // interval_amt) + 1,
            interval = interval_amt,              
            repeat=False                          
        )
    
    plt.show()
