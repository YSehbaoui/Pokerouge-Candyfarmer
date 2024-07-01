import tkinter as tk
from key_logger import start_recording, stop_recording, start_execution, stop_execution

def create_gui():
    root = tk.Tk()
    root.title("Key Logger GUI")

    record_button = tk.Button(root, text="Start Recording", command=start_recording)
    record_button.pack(pady=10)

    stop_record_button = tk.Button(root, text="Stop Recording", command=stop_recording)
    stop_record_button.pack(pady=10)

    execute_button = tk.Button(root, text="Start Execution", command=start_execution)
    execute_button.pack(pady=10)

    stop_execute_button = tk.Button(root, text="Stop Execution", command=stop_execution)
    stop_execute_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
