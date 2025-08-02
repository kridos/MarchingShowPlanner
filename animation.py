import time
import tkinter as tk

# Constants
FPS = 60
FRAME_DELAY = int(1000 / FPS)  # milliseconds

# Canvas global (or pass it as argument)
canvas = None  # You need to assign this to your actual canvas instance somewhere

def create_circle(position, radius=10, color='red'):
    """
    Create a circle on the Tkinter canvas at position (x, y).
    Returns the canvas oval ID.
    """
    x, y = position
    r = radius
    oval_id = canvas.create_oval(x - r, y - r, x + r, y + r,
                                 fill=color, outline='black', width=1)
    return oval_id


def get_path_index_at_time(curr_time, player):
    """
    Find which path index the current time fits in for this player.
    """
    for i, path in enumerate(player.nextPath):
        if path.start_time <= curr_time < path.start_time + path.duration:
            return i
    # If current time is beyond last path, return last path index
    return len(player.nextPath) - 1


def update_positions(players, start_time, duration):
    """
    Update player positions based on elapsed time since start_time.
    Schedule next update using Tkinter's after().
    """
    current_time = time.time() - start_time
    
    if current_time > duration:
        # Animation ended: set all players to last position and stop updating
        for player in players:
            x, y = player.getLastPath().end
            canvas.coords(player.circle_id, x - 10, y - 10, x + 10, y + 10)
        return  # Stop animation
    
    for player in players:
        path_idx = get_path_index_at_time(current_time, player)
        path = player.nextPath[path_idx]
        
        if path.start_time <= current_time < path.start_time + path.duration:
            x = path.functionX(current_time)
            y = path.functionY(current_time)
        else:
            x, y = path.end
        
        # Update the oval's position on canvas
        canvas.coords(player.circle_id, x - 10, y - 10, x + 10, y + 10)
    
    # Schedule next frame
    canvas.after(FRAME_DELAY, update_positions, players, start_time, duration)


def run_animation(players, duration):
    """
    Starts the animation loop.
    Each player should have their circle created and stored as player.circle_id.
    """
    start_time = time.time()
    update_positions(players, start_time, duration)
