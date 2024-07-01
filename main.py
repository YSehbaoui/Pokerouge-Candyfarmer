import tkinter as tk
from tkinter import messagebox
import threading
from key_logger import record_new_log_file, execute_log_file, stop_listener, stop_listener_explicitly

record_thread = None
execute_thread = None

def start_recording():
    global record_thread
    if record_thread is None: 
        record_thread = threading.Thread(target=record_new_log_file)
        record_thread.start()
        messagebox.showinfo("Aufzeichnung", "Die Aufzeichnung hat begonnen. Drücken Sie 'Stop Recording', um zu stoppen.")
    else: 
        messagebox.showwarning("Aufzeichnung", "Es wird gerade schon aufgezeichnet.")

def stop_recording():
    global record_thread
    stop_listener()
    if record_thread is not None:
        stop_listener_explicitly()
        record_thread.join()
        record_thread = None
    messagebox.showinfo("Aufzeichnung", "Die Aufzeichnung wurde gestoppt.")

def start_execution():
    global execute_thread
    if execute_thread is None:
        execute_thread = threading.Thread(target=execute_log_file)
        execute_thread.start()
        messagebox.showinfo("Ausführung", "Die Ausführung beginnt in 5 Sekunden. Drücken Sie 'Stop Execution', um zu stoppen.")
    else:
        messagebox.showwarning("Ausführung", "Es wird gerade schon ausgeführt.")

def stop_execution():
    global execute_thread
    stop_listener()
    if execute_thread is not None:
        stop_listener_explicitly()
        execute_thread.join()
        execute_thread = None
    messagebox.showinfo("Ausführung", "Die Ausführung wurde gestoppt.")

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
