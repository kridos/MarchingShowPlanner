import time
from functions import returnLinearFunction, returnCircularFunction, returnQuadraticBezierFunction
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import copy


# --- Animation helper functions (replace your animation.py) ---
FPS = 60
FRAME_DELAY = int(1000 / FPS)  # milliseconds
canvas = None  # will be assigned later

def create_circle(position, radius=5, color='red', tag=None):
    x, y = position
    r = radius
    if tag:
        oval_id = canvas.create_oval(x - r, y - r, x + r, y + r,
                                     fill=color, outline='black', width=1, tags=tag)
    else:
        oval_id = canvas.create_oval(x - r, y - r, x + r, y + r,
                                     fill=color, outline='black', width=1)
    return oval_id

def get_path_index_at_time(curr_time, player):
    for i, path in enumerate(player.nextPath):
        if path.start_time <= curr_time < path.start_time + path.duration:
            return i
    return len(player.nextPath) - 1

def update_positions(players, start_time, duration):
    current_time = time.time() - start_time
    
    if current_time > duration:
        for player in players:
            x, y = player.getLastPath().end
            canvas.coords(player.circle_id, x - 5, y - 5, x + 5, y + 5)
        return
    
    for player in players:
        path_idx = get_path_index_at_time(current_time, player)
        path = player.nextPath[path_idx]
        if path.start_time <= current_time < path.start_time + path.duration:
            x, y = path.currentPosition(current_time)
        else:
            x, y = path.end
        canvas.coords(player.circle_id, x - 5, y - 5, x + 5, y + 5)
    
    canvas.after(FRAME_DELAY, update_positions, players, start_time, duration)

def run_animation(players, duration):
    start_time = time.time()
    update_positions(players, start_time, duration)

# --- End animation helper functions ---

total_duration = 0


class Field:
    def __init__(self):
        self.players = {}

    def add_player(self, player):
        self.players[player.id] = player

    def get_player(self, player_id):
        return self.players.get(player_id)

    # def updateSinglePosition(self, player_id, next_position):
    #     player = self.get_player(player_id)
    #     player.setNextPosition(next_position)


    def run_simulation(self, duration):
        run_animation(list(self.players.values()), duration)
                
# Add this class somewhere near the top, before Player class

class DraggableCircle:
    def __init__(self, canvas, oval_id, player):
        self.canvas = canvas
        self.oval_id = oval_id
        self.player = player
        self._drag_data = {"x": 0, "y": 0}

        canvas.tag_bind(self.oval_id, "<ButtonPress-1>", self.on_press)
        canvas.tag_bind(self.oval_id, "<ButtonRelease-1>", self.on_release)
        canvas.tag_bind(self.oval_id, "<B1-Motion>", self.on_motion)

    def on_press(self, event):
        # Record the initial mouse position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        player_id.config(text=self.player.id)
        player_color.config(text=canvas.itemcget(self.player.circle_id, "fill"))
        update_player.config(state="normal")
        path_mode_var.set(self.player.path_mode)
        

    def on_motion(self, event):
        # Calculate movement delta
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]

        # Move the oval by delta
        self.canvas.move(self.oval_id, dx, dy)

        # Update drag data
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

        # Update player's position based on new oval center coords
        #coords = self.canvas.coords(self.oval_id)  # [x1, y1, x2, y2]
        #new_x = (coords[0] + coords[2]) / 2
        #new_y = (coords[1] + coords[3]) / 2
        #self.player.currentX = new_x
        #self.player.currentY = new_y

    def on_release(self, event):
        # Optional: logic when mouse released
        canvas.delete('possible_path')
        
        
        
        if canvas.gettags(self.oval_id)[0] == 'center_dot':
            path = copy.copy(self.player.getLastPath())
            coords = self.canvas.coords(self.oval_id)
            path.third_point = ((coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2)
            path.calculateFunction()
            
            for i in range(10):
                t = path.start_time + (i / 9) * path.duration
                create_circle(path.currentPosition(t), 2, 'orange', 'possible_path')
            
        
    


# Update Player class __init__:

class Player:
    def __init__(self, coords, id):
        # self.currentX = coords[0]
        # self.currentY = coords[1]
        # self.nextX = self.currentX
        # self.nextY = self.currentY
        self.id = id
        # Create canvas circle and save ID
        self.circle_id = create_circle(coords, color='red')
        # Create draggable handler
        self.draggable = DraggableCircle(canvas, self.circle_id, self)
        self.nextPath = []
        self.path_mode = "Linear"

    # ... rest of Player class unchanged


    # def setNextPosition(self, coords):
    #     self.nextX = coords[0]
    #     self.nextY = coords[1]
        
    def getLastPath(self):
        return self.nextPath[-1]
    
    def getPath(self, i):
        return self.nextPath[i]
        
    def calculateLastPath(self, center=(0,0)):
        self.getLastPath().third_point = center
        self.getLastPath().calculateFunction()
        
    def createNextPath(self, start, duration, start_time, end = (0,0), pathType = "Linear"):
        self.nextPath.append(Path(start, end, pathType, duration, start_time))
        
    def reviseLastPathEnd(self, end):
        self.getLastPath().end = end

    # def finalUpdate(self):
    #     self.currentX = self.nextX
    #     self.currentY = self.nextY

class Path:
    def __init__(self, start, end, pathType, duration, start_time = 0.0, center = None):
        self.start = start
        self.end = end
        self.duration = duration
        self.function = None
        self.pathType = pathType
        self.start_time = start_time
        self.third_point = center

    def calculateFunction(self):
        if self.pathType == "Linear":
            self.function = returnLinearFunction(self.start, self.end, self.duration, self.start_time)
            
        elif self.pathType == "Circular":
            if self.third_point is None:
                raise ValueError("Center not set for circular path.")
            self.function = returnCircularFunction(self.start, self.end, self.duration, self.third_point, self.start_time)
            
        elif self.pathType == "Bezier":
            if self.third_point is None:
                raise ValueError("Third Point not set for Quadratic Bezier path.")
            self.function = returnQuadraticBezierFunction(self.start, self.end, self.duration, self.third_point, self.start_time)

    def currentPosition(self, currentTime):
        if self.function is None:
            raise Exception("No function defined")
        return self.function(currentTime)

# --- UI setup ---

currField = Field()

window = tk.Tk()
window.title("Create a Marching Show")
window.geometry('800x800')

image = Image.open("football_field.jpg")  # use your path here
photo = ImageTk.PhotoImage(image)



def open():
    global players_input, show_preferences
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
    global player_id, player_color, change_id, change_color, update_player, animation_save, new_show, move_duration, total_duration, canvas, display_animation, path_mode_var
    
    player_amt = players_input.get()
    show_preferences.destroy()
    
    
        
    new_show = tk.Toplevel()
    new_show.title("New Show")
    new_show.geometry("600x850")
    
    # Create and pack the canvas
    canvas = tk.Canvas(new_show, width=photo.width(), height=photo.height())
    canvas.pack()
    
    canvas.create_image(0, 0, image=photo, anchor="nw")
    canvas.bg_photo = photo

    
    for i in range(int(player_amt)):
        currField.add_player(Player((60,30), "Player " + str(i + 1)))
    
    player_id = ttk.Label(master=new_show, text = "No Player Selected", font= 'Arial 24')
    player_id.pack()
    
    change_id = ttk.Entry(new_show, width=50)
    change_id.pack()
    
    player_color = ttk.Label(master=new_show, text = "No Player Selected", font= 'Arial 24')
    player_color.pack()
    
    change_color = ttk.Entry(new_show, width=50)
    change_color.pack()
    
    update_player = ttk.Button(master=new_show, text="Update Player", command=update_player_event, state="disabled")
    update_player.pack()
    
    duration_label = ttk.Label(master=new_show, text = "Duration Time (Seconds)", font= 'Arial 24')
    duration_label.pack()
    
    move_duration = ttk.Entry(new_show, width=50)
    move_duration.pack()
    
    path_mode_var = tk.StringVar(value="Linear")
    tk.Radiobutton(new_show, text="Linear", variable=path_mode_var, value="Linear", command=update_path_mode).pack()
    tk.Radiobutton(new_show, text="Circular", variable=path_mode_var, value="Circular", command=update_path_mode).pack()
    tk.Radiobutton(new_show, text="Bezier", variable=path_mode_var, value="Bezier", command=update_path_mode).pack()
   
    animation_save = ttk.Button(master=new_show, text="Save Start", command=save_start)
    animation_save.pack()
    
    display_animation = ttk.Button(master=new_show, text="Display Animation", command=start_animation, state="disabled")
    display_animation.pack()
    
    quit_btn = ttk.Button(master=new_show, text="Quit", command=home_screen)
    quit_btn.pack()
    
def update_path_mode():
    current_player_name = player_id.cget("text")
    if current_player_name == "No Player Selected":
        return  # no update
    selected_mode = path_mode_var.get()
    player = currField.get_player(current_player_name)
    if player:
        player.path_mode = selected_mode
        print(f"Updated {player.id} path_mode to {selected_mode}")
    
def start_animation():
    currField.run_simulation(total_duration)
    
def home_screen():
    new_show.destroy()
    window.deiconify()
    
def save_start():
    global animation_duration, total_duration, animation_save
    
    display_animation.config(state="disabled")
    
    animation_save.config(text="Save End", command=save_end)
    
    animation_duration = float(move_duration.get())
    
    for player in currField.players.values():
        coords = canvas.coords(player.circle_id)
        
        if len(coords) < 4:
            print(f"Warning: Invalid or missing coordinates for player {player.id}")
            continue  # Skip this player or handle differently

        
        cx = (coords[0] + coords[2]) / 2
        cy = (coords[1] + coords[3]) / 2
        
       
        if player.path_mode == "Linear":
            player.createNextPath(start=(cx, cy), duration=animation_duration, start_time=total_duration)
        elif player.path_mode == "Circular":
            player.createNextPath(start=(cx, cy), duration=animation_duration, start_time=total_duration, pathType="Circular")
        elif player.path_mode == "Bezier":
            player.createNextPath(start=(cx, cy), duration=animation_duration, start_time=total_duration, pathType="Bezier")
        
    total_duration += animation_duration
        
        
third_point_draggable = None
third_point_id = None
def save_end():
    global current_center_index, centers_needed, third_point_draggable, third_point_id
    
    save_circular_or_bezier = False
    centers_needed = []
    
    for player in currField.players.values():
        coords = canvas.coords(player.circle_id)
        
        if len(coords) < 4:
            continue  # Skip this player or handle differently

        
        cx = (coords[0] + coords[2]) / 2
        cy = (coords[1] + coords[3]) / 2
        player.reviseLastPathEnd((cx, cy))
        
        if player.path_mode == "Linear":
            player.calculateLastPath()
        elif player.path_mode == "Circular" or player.path_mode == "Bezier":
            save_circular_or_bezier = True
            centers_needed.append(player)
    
    if save_circular_or_bezier:
        centers_needed.sort(key=lambda player: player.path_mode, reverse=True)
        current_center_index = 0
        
        
        player = centers_needed[current_center_index]
        start = player.getLastPath().start
        end = player.getLastPath().end
        midpoint = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
        
        if player.path_mode == "Circular":
            animation_save.config(text="Save Circular Point", command=save_center)
        else:
            animation_save.config(text="Save Bezier Point", command=save_center)
    
        #start
        create_circle(start, color='blue', tag = 'center_dot')
        
        #end
        create_circle(end, color='blue', tag = 'center_dot')
        
        third_point_id = create_circle(midpoint, color = 'purple', tag='center_dot')
        third_point_draggable = DraggableCircle(canvas, third_point_id, player)
        
    else:  
        animation_save.config(text="Save Start", command=save_start)
        display_animation.config(state="normal")
   
def save_center():
    global current_center_index, third_point_id, third_point_draggable
    player = centers_needed[current_center_index]
    coords = canvas.coords(third_point_id)
    center = ((coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2)
    player.calculateLastPath(center)
    print(f"Center assigned for {player.id} at {center}")

    current_center_index += 1
    
    
    
    if current_center_index >= len(centers_needed):
        # Done assigning centers
        canvas.unbind("<Button-1>")
        animation_save.config(text="Save Start", command=save_start)
        display_animation.config(state="normal")
        canvas.delete('center_dot')
        canvas.delete('possible_path')
        third_point_id = None
        third_point_draggable = None
        
        
    else:
        
        player = centers_needed[current_center_index]
        
        start = player.getLastPath().start
        end = player.getLastPath().end
        midpoint = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
            
        #start
        create_circle(start, color='blue', tag='center_dot')
        
        #end
        create_circle(end, color='blue', tag = 'center_dot')
        
        third_point_id = create_circle(midpoint, color = 'purple', tag='center_dot')
        third_point_draggable = DraggableCircle(canvas, third_point_id, player)
    
def update_player_event():
    
    new_player_id = change_id.get()
    new_player_color = change_color.get()
    
    if new_player_id != "":
        player = currField.players.pop(player_id.cget("text"))
        if new_player_color != "":
            canvas.itemconfig(player.circle_id, fill=new_player_color)
            player_color.config(text=new_player_color)
        player.id = new_player_id
        currField.add_player(player)
        player_id.config(text=new_player_id)
    else:
        if new_player_color != "":
            player = currField.get_player(player_id.cget("text"))
            canvas.itemconfig(player.circle_id, fill=new_player_color)
            player_color.config(text=new_player_color)
    
    change_id.delete(0, tk.END)
    change_color.delete(0, tk.END)
    
    currField.display_static()

# Main window UI

title_label = ttk.Label(master=window, text = "Home Screen", font= 'Arial 50 bold')
title_label.pack()

button_frame = ttk.Frame(master=window)
new_project_bt = ttk.Button(master=button_frame, text="Start New Project", command=open)
saved_project_bt = ttk.Button(master=button_frame, text="View Saved Projects")

new_project_bt.pack(side='left', padx=10)
saved_project_bt.pack(side='left')
button_frame.pack(pady=10)

window.mainloop()
