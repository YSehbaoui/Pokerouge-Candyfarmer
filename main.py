import tkinter as tk
from key_logger import start_recording, stop_recording, start_execution, stop_execution

def create_gui():
    root = tk.Tk()
    root.title("Key Logger GUI")

    WIDTH = 1280
    HEIGHT = 720

    root.geometry((f"{WIDTH}x{HEIGHT}"))

    # Erstellen der Frames
    left_frame = tk.Frame(root)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    right_frame = tk.Frame(root)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    upper_left_frame = tk.Frame(left_frame)
    upper_left_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    lower_left_frame = tk.Frame(left_frame)
    lower_left_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # Buttons im oberen linken Frame
    record_button = tk.Button(upper_left_frame, text="Start Recording", command=start_recording)
    record_button.grid(row=0, column=0, padx=10, pady=10)

    stop_record_button = tk.Button(upper_left_frame, text="Stop Recording", command=stop_recording)
    stop_record_button.grid(row=0, column=1, padx=10, pady=10)

    # Buttons im unteren linken Frame
    execute_button = tk.Button(lower_left_frame, text="Start Execution", command=start_execution)
    execute_button.grid(row=0, column=0, padx=10, pady=10)

    stop_execute_button = tk.Button(lower_left_frame, text="Stop Execution", command=stop_execution)
    stop_execute_button.grid(row=0, column=1, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
