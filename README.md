# Pokerouge Candyfarmer

A small Python tool for automating repetitive inputs in PokeRogue, a browser-based Pokémon roguelike. It records your keystrokes with their timing, then replays them on demand. A separate experimental script automates the starter selection menu.

> **Status:** early work in progress. The recorder and replayer work. `navigator.py` is an unfinished experiment and is not connected to the GUI.

## Features

- **Tkinter GUI** with Start/Stop Recording and Start/Stop Execution buttons
- **Key recorder** that logs each key press together with the delay since the previous one
- **Replay** of a recording with the original timing, after a 5 second countdown so you can switch to the game window
- **Selectable key sets**:
  - *PokeRogue*: `W A S D`, `Space`, `X`, `Enter`, `R`, `F`, `F5`
  - *Letters Only*: `A` to `Z`
  - *Whole Keyboard*: every supported key, including modifiers and function keys
- **Clear on Record** option to overwrite the previous recording or append to it
- Recordings are stored as plain CSV (`key,delay_ms`) in `key_log.csv`
- **Experimental menu navigator** (`navigator.py`) that scripts the starter selection screen with `pyautogui`

## Installation

Requires Python 3.9 or newer with Tkinter.

```bash
git clone https://github.com/YSehbaoui/Pokerouge-Candyfarmer.git
cd Pokerouge-Candyfarmer
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install pynput pyautogui
```

Tkinter ships with the Windows and macOS installers of Python. On Arch / CachyOS install it separately:

```bash
sudo pacman -S tk
```

### Platform notes

Global key capture and key injection work on Windows, macOS and X11. Wayland compositors generally block both, so on a Wayland desktop run the game and this tool in an X11 session or through XWayland, and expect limitations.

## Usage

```bash
python main.py
```

1. Choose the keys to record in the dropdown.
2. Click **Start Recording**, play your sequence in the game, then click **Stop Recording**.
3. Click **Start Execution** and switch to the game window within 5 seconds. The recording is replayed with its original timing.
4. Click **Stop Execution** to abort a replay.

## Privacy

The recorder listens to keystrokes system-wide while it is running. Only keys from the selected set are written to `key_log.csv`, but the *Letters Only* and *Whole Keyboard* modes also capture whatever you type with those keys in any window, including passwords. Stop the recording before typing anything sensitive, and delete the log when you are done. `*.csv` is in `.gitignore`, so recordings are not committed.

## Disclaimer

This is a fan project and is not affiliated with PokeRogue, Nintendo, Game Freak or The Pokémon Company. Automating inputs may be against the rules of a game or service. Use it at your own risk.
