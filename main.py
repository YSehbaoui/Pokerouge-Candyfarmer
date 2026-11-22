import tkinter as tk
from key_logger import start_recording, stop_recording, start_execution, stop_execution
import config

BUTTON_SIZE = (20, 5)
WINDOW_SIZE = (1280, 720)

def update_option(*args):
    option = selected_option.get()
    config.set_selected_option(option)
    print(f"Option updated: {config.get_selected_option()}")
    
    if option == "PokeRogue":
        config.set_relevant_inputs(config.POKEROUGE_INPUTS)
    elif option == "Letters Only":
        config.set_relevant_inputs(config.LETTERS_ONLY_INPUTS)
    elif option == "Whole Keyboard":
        config.set_relevant_inputs(config.WHOLE_KEYBOARD_INPUTS)
    
    print(f"Relevant inputs updated: {config.get_relevant_inputs()}")

def update_switch():
    state = switch_var.get()
    config.set_clear_on_record(state)
    print(f"Switch state updated: {config.get_clear_on_record()}")

def create_gui():
    root = tk.Tk()
    root.title("Key Logger GUI")

    root.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")

    # Erstellen der Frames und Einfärben
    left_frame = tk.Frame(root, bg="lightblue")
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    right_frame = tk.Frame(root, bg="lightgreen")
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    upper_left_frame = tk.Frame(left_frame, bg="lightcoral")
    upper_left_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    lower_left_frame = tk.Frame(left_frame, bg="lightyellow")
    lower_left_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # Buttons im oberen linken Frame
    record_button = tk.Button(upper_left_frame, text="Start Recording", command=start_recording, width=BUTTON_SIZE[0], height=BUTTON_SIZE[1])
    record_button.grid(row=0, column=0, padx=10, pady=10)

    stop_record_button = tk.Button(upper_left_frame, text="Stop Recording", command=stop_recording, width=BUTTON_SIZE[0], height=BUTTON_SIZE[1])
    stop_record_button.grid(row=1, column=0, padx=10, pady=10)

    # Buttons im unteren linken Frame
    execute_button = tk.Button(lower_left_frame, text="Start Execution", command=start_execution, width=BUTTON_SIZE[0], height=BUTTON_SIZE[1])
    execute_button.grid(row=0, column=0, padx=10, pady=10)

    stop_execute_button = tk.Button(lower_left_frame, text="Stop Execution", command=stop_execution, width=BUTTON_SIZE[0], height=BUTTON_SIZE[1])
    stop_execute_button.grid(row=1, column=0, padx=10, pady=10)

    # Dropdown Menü und Schalter im oberen linken Frame
    dropdown_label = tk.Label(upper_left_frame, text="Keys to Record:")
    dropdown_label.grid(row=0, column=1, padx=10, pady=10, sticky='e')

    options = ["PokeRogue", "Letters Only", "Whole Keyboard"]
    global selected_option
    selected_option = tk.StringVar()
    selected_option.set(config.get_selected_option())
    selected_option.trace_add("write", update_option)
    dropdown_menu = tk.OptionMenu(upper_left_frame, selected_option, *options)
    dropdown_menu.grid(row=0, column=2, padx=10, pady=10)

    global switch_var
    switch_var = tk.BooleanVar()
    switch_var.set(config.get_clear_on_record())
    switch_button = tk.Checkbutton(upper_left_frame, text="Clear on Record", variable=switch_var, command=update_switch)
    switch_button.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
