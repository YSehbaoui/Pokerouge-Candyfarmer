import threading
import time
from pynput import keyboard
from pyautogui import press

# Definieren Sie die Datei, in der die Tastenanschläge gespeichert werden sollen
log_file = "key_log.txt"
time_log_file = "time_log.txt"

# Definieren Sie die Zuordnung der Tasten
key_mappings = {
    keyboard.Key.enter: 'enter',
    keyboard.Key.esc: 'esc',
    keyboard.Key.shift: 'shiftleft',  # or 'shiftright' depending on the side
    keyboard.Key.ctrl_l: 'ctrlleft',
    keyboard.Key.ctrl_r: 'ctrlright',
    keyboard.Key.alt_l: 'altleft',
    keyboard.Key.alt_r: 'altright',
    keyboard.Key.tab: 'tab',
    keyboard.Key.backspace: 'backspace',
    keyboard.Key.delete: 'delete',
    keyboard.Key.home: 'home',
    keyboard.Key.end: 'end',
    keyboard.Key.page_down: 'pagedown',
    keyboard.Key.page_up: 'pageup',
    keyboard.Key.left: 'left',
    keyboard.Key.right: 'right',
    keyboard.Key.up: 'up',
    keyboard.Key.down: 'down',
    keyboard.Key.print_screen: 'printscreen',
    keyboard.Key.pause: 'pause',
    keyboard.Key.caps_lock: 'capslock',
    keyboard.Key.num_lock: 'numlock',
    keyboard.Key.scroll_lock: 'scrolllock',
    keyboard.Key.insert: 'insert',
    keyboard.Key.f1: 'f1',
    keyboard.Key.f2: 'f2',
    keyboard.Key.f3: 'f3',
    keyboard.Key.f4: 'f4',
    keyboard.Key.f5: 'f5',
    keyboard.Key.f6: 'f6',
    keyboard.Key.f7: 'f7',
    keyboard.Key.f8: 'f8',
    keyboard.Key.f9: 'f9',
    keyboard.Key.f10: 'f10',
    keyboard.Key.f11: 'f11',
    keyboard.Key.f12: 'f12',
    keyboard.Key.space: 'space'
}

last_time = None
stop_program = False
SAFETY_SLEEP = 0.0
lock = threading.Lock()
first_key_logged = False
relevant_inputs = ['w', 'a', 's', 'd', 'space', 'x', 'enter', 'f5', 'r', 'f']

def on_press(key):
    global last_time, stop_program, first_key_logged

    # Überprüfen, ob ESC gedrückt wurde, um das Programm zu stoppen
    if key == keyboard.Key.delete:
        stop_program = True
        return False

    # Aktuelle Zeit in Millisekunden
    current_time = time.time() * 1000

    try:
        # Überprüfen Sie, ob die Taste ein normales Zeichen ist
        key_char = key.char
        if key_char:
            log = key_char
        else:
            log = str(key)
    except AttributeError:
        # Wenn es sich um eine spezielle Taste handelt, holen Sie den Namen aus der Zuordnung
        log = key_mappings.get(key, str(key))

    if log not in relevant_inputs: return

    with lock:
        # Speichern Sie den Tastenanschlag in der Datei
        with open(log_file, "a") as f:
            f.write(log + '\n')
            print(f"{log} with ", end="")

        # Berechnen Sie den zeitlichen Abstand und speichern Sie ihn in der Zeitdatei
        if not first_key_logged:
            with open(time_log_file, "a") as f:
                f.write("0\n")
                print("0ms delay")
            first_key_logged = True
        else:
            time_difference = current_time - last_time
            with open(time_log_file, "a") as f:
                f.write(f"{int(time_difference)}\n")
                print(f"{int(time_difference)}ms delay")

        # Aktualisieren Sie die Zeit des letzten Tastendrucks
        last_time = current_time

def start_listener():
    # Listener starten
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def clear_log_file(file_path):
    with open(file_path, 'w') as file:
        # Nichts in die Datei schreiben, wodurch der Inhalt gelöscht wird
        pass

def record_new_log_file(key_log, time_log):
    clear_log_file(log_file)
    clear_log_file(time_log_file)
    start_listener()

def execute_log_file(key_log, time_log):
    global stop_program
    print("Executing logfile...")
    time.sleep(5)

    print("Started Execution")
    with open(key_log, "r") as keystroke_file:
        with open(time_log, "r") as timestamp_file:
            for timestamp, keystroke in zip(timestamp_file, keystroke_file):
                if stop_program:
                    break
                time.sleep((int(timestamp)/1000)+SAFETY_SLEEP) 
                keystroke = keystroke.strip()  # Entferne unnötige Leerzeichen und Zeilenumbrüche
                print(f"Pressed {keystroke} with {timestamp.strip()}ms delay")
                press(keystroke)

    print("Execution complete!")

def main():
    global stop_program

    mode = int(input("Record: 1, Execute: 2\n"))
    match(mode):
        case 1: 
            record_new_log_file(log_file, time_log_file)
        case 2: 
            # Zum Ausführen
            execute_thread = threading.Thread(target=execute_log_file, args=(log_file, time_log_file))
            execute_thread.start()

            # Warte, bis der Ausführungsthread beendet ist
            execute_thread.join()

if __name__ == "__main__":
    main()
