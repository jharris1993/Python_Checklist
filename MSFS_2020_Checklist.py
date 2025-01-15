import tkinter as tk
from tkinter import messagebox
import subprocess
import pickle
import os

# Constants for storing window position
POSITION_FILE = "Flight_Simulator_2020.pkl"

# Function to save window position
def save_window_position(window):
    try:
        with open(POSITION_FILE, "wb") as f:
            f.write(pickle.dumps(window.geometry()))
    except Exception as e:
        print(f"Error saving window position: {e}")

# Function to load window position
def load_window_position(window):
    if os.path.exists(POSITION_FILE):
        try:
            with open(POSITION_FILE, "rb") as f:
                geometry = pickle.loads(f.read())
                window.geometry(geometry)
        except Exception as e:
            print(f"Error loading window position: {e}")

def create_checklist_window(title, checklist_title, checklist_items, external_program):
    def update_continue_button():
        if all(var.get() for var in checklist_vars):
            continue_button["state"] = "normal"
        else:
            continue_button["state"] = "disabled"

    def on_continue():
        save_window_position(root)
        root.destroy()
        try:
            subprocess.run(external_program, check=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run the program: {e}")

    root = tk.Tk()
    root.title(title)

    load_window_position(root)

    # Create the main frame
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(expand=True, fill="both")

    # Checklist title
    title_label = tk.Label(frame, text=checklist_title, font=("Arial", 16))
    title_label.pack(pady=(0, 10))

    # Checklist items
    checklist_vars = []
    for item in checklist_items:
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(frame, text=item, variable=var, command=update_continue_button, wraplength=400, anchor="w", justify="left")
        checkbox.pack(fill="x", padx=10, pady=5)
        checklist_vars.append(var)

    # Continue and Cancel buttons (added Cancel)
    button_frame = tk.Frame(frame)
    button_frame.pack(pady=(20, 0))

    continue_button = tk.Button(
        button_frame, text="Continue", state="disabled", command=on_continue, font=("Arial", 12)
    )
    continue_button.pack(side="left", padx=(0, 10))

    cancel_button = tk.Button(
        button_frame, text="Cancel", command=lambda: (save_window_position(root), root.destroy()), font=("Arial", 12)
    )
    cancel_button.pack(side="left")

    # Resize window to fit content
    root.update_idletasks()
    root.minsize(root.winfo_reqwidth(), root.winfo_reqheight())

    # Run the main event loop
    root.protocol("WM_DELETE_WINDOW", lambda: (save_window_position(root), root.destroy()))
    root.mainloop()

if __name__ == "__main__":
    window_title = "Flight Simulator 2020 Checklist"
    checklist_window_title = "MSFS 2020 Pre-Start\nCHECKLIST VERIFICATION:"
    items = [
        "Move the keyboard out of the way.",
        "Verify that all cables are firmly attached\nto their respective controller's connectors.",
        "Verify that no cables are resting on the keyboard.",
        "Move all axis and trim controls to reduce noise.",
        "Verify that all trim controls are centered.",
        "Verify that the throttle has been pulled\nall the way back to the stop."     # last line doesn't get a comma
    ]
    external_program_path = "C:\XboxGames\Microsoft Flight Simulator\Content\FlightSimulator.exe"  # Change to your program's path

    create_checklist_window(window_title, checklist_window_title, items, external_program_path)
