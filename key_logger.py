import threading
import time
import csv
from pynput import keyboard
from pynput.keyboard import Controller
from tkinter import messagebox

log_file = "key_log.csv"

last_time = None
stop_program = False
SAFETY_SLEEP = 0
lock = threading.Lock()
first_key_logged = False

record_thread = None
execute_thread = None

listener = None
relevant_inputs = ['w', 'a', 's', 'd', 'space', 'x', 'enter', 'f5', 'r', 'f']
keyboard_controller = Controller()

def on_press(key):
    global last_time, stop_program, first_key_logged

    if stop_program:
        return False

    current_time = time.time() * 1000

    try:
        log = key.char
    except AttributeError:
        log = str(key.name)

    if log not in relevant_inputs: 
        return

    with lock:
        with open(log_file, "a", newline='') as f:
            writer = csv.writer(f)
            if not first_key_logged:
                writer.writerow([log, 0])
                print(f"{log} with 0ms delay")
                first_key_logged = True
            else:
                time_difference = current_time - last_time
                writer.writerow([log, int(time_difference)])
                print(f"{log} with {int(time_difference)}ms delay")

        last_time = current_time

def start_listener():
    global listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()

def clear_log_file(file_path):
    with open(file_path, 'w', newline='') as file:
        pass

def record_new_log_file():
    global stop_program, listener_thread
    stop_program = False
    clear_log_file(log_file)
    listener_thread = threading.Thread(target=start_listener)
    listener_thread.start()
    return listener_thread

def execute_log_file():
    global stop_program, execute_thread
    stop_program = False
    print("Executing logfile...")
    time.sleep(5)

    print("Started Execution")
    with open(log_file, "r") as f:
        reader = csv.reader(f)
        for keystroke, timestamp in reader:
            if stop_program:
                break
            time.sleep((int(timestamp) / 1000) + SAFETY_SLEEP)
            keystroke = keystroke.strip()
            print(f"Pressed {keystroke} with {timestamp.strip()}ms delay")
            
            if len(keystroke) == 1:
                keyboard_controller.press(keystroke)
                keyboard_controller.release(keystroke)
            else:
                keyboard_controller.press(eval(f"keyboard.Key.{keystroke}"))
                keyboard_controller.release(eval(f"keyboard.Key.{keystroke}"))

    print("Execution complete!")
    threading.Thread(target=stop_execution).start()

def stop_listener():
    global stop_program
    stop_program = True
    print("Listener stopped.")

def stop_listener_explicitly():
    global listener
    global first_key_logged
    if listener is not None:
        listener.stop()
        listener = None
        first_key_logged = False
    print("Listener explicitly stopped.")

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
        execute_thread.join()
        execute_thread = None
    messagebox.showinfo("Ausführung", "Die Ausführung wurde gestoppt.")
