import time
from functions import returnLinearFunction
from animation import createCircle, createAnimation, finalUpdatePosition
import tkinter as tk
from tkinter import ttk
import matplotlib.colors as mcolors

def rgba_to_named(rgba):
    for name, hex_val in mcolors.CSS4_COLORS.items():
        if mcolors.to_rgba(hex_val) == tuple(rgba):
            return name
    return None  # No exact name match

class DraggableCircle:
    dragging_circle = None
    
    def __init__(self, circle, player):
        self.circle = circle
        self.player = player
        self.press = None
        self.cid_press = circle.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = circle.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = circle.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if DraggableCircle.dragging_circle is not None:
            return
        
        if event.inaxes != self.circle.axes:
            return
        contains, _ = self.circle.contains(event)
        if not contains:
            return

        update_player.config(state="normal")
        player_color.config(text=rgba_to_named(self.circle.get_facecolor()))
        player_id.config(text=self.player.id)
        DraggableCircle.dragging_circle = self
        x0, y0 = self.circle.center
        self.press = (x0, y0, event.xdata, event.ydata)

    def on_motion(self, event):
        if DraggableCircle.dragging_circle != self:
            return
        
        if self.press is None or event.inaxes != self.circle.axes:
            return
        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.circle.center = (x0 + dx, y0 + dy)
        self.circle.figure.canvas.draw()

    def on_release(self, event):
        if DraggableCircle.dragging_circle != self:
            return
        
        DraggableCircle.dragging_circle = None
        
        self.press = None
        self.player.x, self.player.y = self.circle.center
        self.circle.figure.canvas.draw()

class Field:
    def __init__(self):
        self.players = {}

    def add_player(self, player):
        self.players[player.id] = player

    def get_player(self, player_id):
        return self.players.get(player_id)

    def updateSinglePosition(self, player_id, next_position):
        player = self.get_player(player_id)
        player.setNextPosition(next_position)

    def updateNextPositions(self, duration):
        for player in self.players.values():
            print(f'{player.id} ({player.currentX}, {player.currentY})')
            x = float(input("Enter the next x position: "))
            y = float(input("Enter the next y position: "))
            print()
            player.setNextPosition((x, y))
            player.determineNextPath(duration)
            
    def display_static(self):
       createAnimation(0, self.players.values(), True)


    def run_simulation(self, duration):
        createAnimation(duration, self.players.values(), False)
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
        self.circle = DraggableCircle(createCircle((self.currentX, self.currentY)), self)
        self.nextPath = []

    def setNextPosition(self, coords):
        self.nextX = coords[0]
        self.nextY = coords[1]

    def determineNextPath(self, duration):
        self.nextPath.append(Path((self.currentX, self.currentY), (self.nextX, self.nextY), "Straight", duration))

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
"""currField.add_player(Player((0,0), "Player 1"))
currField.add_player(Player((0,10), "Player 2"))
currField.updateNextPositions(5)
currField.run_simulation(5)
currField.updateNextPositions(5)"""

window = tk.Tk()

def open():
    global players_input
    global show_preferences
    
    window.withdraw()
    
    show_preferences = tk.Toplevel()
    show_preferences.title("Show Preferences")
    show_preferences.geometry("600x400")
    
    
    player_amt = ttk.Label(master=show_preferences, text = "Enter Amount of Players", font= 'Arial 20')
    player_amt.pack()
    
    players_input = ttk.Entry(show_preferences, width=50)
    players_input.pack()
    
    done_button = ttk.Button(master=show_preferences, text="Done", command=submit)
    done_button.pack()

def submit():
    global player_id, player_color, change_id, change_color, update_player
    
    
    player_amt = players_input.get()
    
    show_preferences.destroy()
    
    for i in range(int(player_amt)):
        currField.add_player(Player((60,30), "Player " + str(i + 1)))
        print(i)
        
    new_show = tk.Toplevel()
    new_show.title("New Show")
    new_show.geometry("600x600")
    
    player_id = ttk.Label(master=new_show, text = "No Player Selected", font= 'Arial 24')
    player_id.pack()
    
    change_id = ttk.Entry(new_show, width=50)
    change_id.pack()
    
    player_color = ttk.Label(master=new_show, text = "No Player Selected", font= 'Arial 24')
    player_color.pack()
    
    #Change to dropdown
    change_color = ttk.Entry(new_show, width=50)
    change_color.pack()
    
    update_player = ttk.Button(master=new_show, text="Update Player", command=update_player_event, state="disabled")
    update_player.pack()
    
    currField.display_static()
    
    
def update_player_event():
    new_player_id = change_id.get()
    new_player_color = change_color.get()
    
    if new_player_id != "":
        player = currField.players.pop(player_id.cget("text"))
        
        if new_player_color != "":
            player.circle.circle.set_facecolor(new_player_color)
            player_color.config(text=new_player_color)
        
        player.id = new_player_id
        currField.add_player(player)
        player_id.config(text=new_player_id)
        
    else:
        
        if new_player_color != "":
            player = currField.get_player(player_id.cget("text"))
            player.circle.circle.set_facecolor(new_player_color)
            player_color.config(text=new_player_color)
            
    change_id.delete(0, tk.END)
    change_color.delete(0, tk.END)

            
    currField.display_static()

    
    
        
    
    
        


#window
window.title("Create a Marching Show")
window.geometry('600x600')

#title
title_label = ttk.Label(master=window, text = "Home Screen", font= 'Arial 50 bold')
title_label.pack()

#buttons
button_frame = ttk.Frame(master=window)
new_project_bt = ttk.Button(master=button_frame, text="Start New Project", command=open)
saved_project_bt = ttk.Button(master=button_frame, text="View Saved Projects")

new_project_bt.pack(side = 'left', padx = 10)
saved_project_bt.pack(side = 'left')
button_frame.pack(pady = 10)


window.mainloop()









