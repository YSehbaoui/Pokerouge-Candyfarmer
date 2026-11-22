# config.py

_selected_option = "PokeRogue"
_clear_on_record = True

# Standard relevant inputs
_relevant_inputs = ['w', 'a', 's', 'd', 'space', 'x', 'enter', 'f5', 'r', 'f']

# Optionen
POKEROUGE_INPUTS = ['w', 'a', 's', 'd', 'space', 'x', 'enter', 'f5', 'r', 'f']
LETTERS_ONLY_INPUTS = list("abcdefghijklmnopqrstuvwxyz")
WHOLE_KEYBOARD_INPUTS = [
    'w', 'a', 's', 'd', 'space', 'x', 'enter', 'f5', 'r', 'f',
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
    'q', 'e', 't', 'y', 'u', 'i', 'o', 'p', 'z', 'g', 'h', 'j', 'k', 'l', 'm', 'b', 'n',
    'shift', 'ctrl_l', 'ctrl_r', 'alt_l', 'alt_r', 'tab', 'backspace', 'delete', 'home', 
    'end', 'page_down', 'page_up', 'left', 'right', 'up', 'down', 'print_screen', 'pause',
    'caps_lock', 'num_lock', 'scroll_lock', 'insert', 'f1', 'f2', 'f3', 'f4', 'f6', 'f7', 
    'f8', 'f9', 'f10', 'f11', 'f12'
]

def get_selected_option():
    return _selected_option

def set_selected_option(option):
    global _selected_option
    _selected_option = option

def get_clear_on_record():
    return _clear_on_record

def set_clear_on_record(state):
    global _clear_on_record
    _clear_on_record = state

def get_relevant_inputs():
    return _relevant_inputs

def set_relevant_inputs(inputs):
    global _relevant_inputs
    _relevant_inputs = inputs
