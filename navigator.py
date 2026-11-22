from pyautogui import press
import time

NUMBER_OF_GENS = 9
SAFETY_SLEEP = 0.1

def pressKey(key: str):
    press(key)
    time.sleep(SAFETY_SLEEP)

def startGame():
    def getToStarters():
        for _ in range(5): pressKey("s")
        for _ in range(3): pressKey("w")
        pressKey("space")
        pressKey("space")

    def resetPick(x: int, y: int) -> tuple[int, int]:
        for _ in range(x): pressKey("a")
        for _ in range(y+NUMBER_OF_GENS): pressKey("w")
        return 0,0

    def pickPokemon(gen: int, x: int, y: int) -> tuple[int, int]:
        for _ in range(gen-1): pressKey("s")
        for _ in range(x): pressKey("d")
        for _ in range(y-1): pressKey("s")
        pressKey('space') # choce
        pressKey('space') # pick
        return x,y

    def lockInPicks():
        for _ in range(NUMBER_OF_GENS): pressKey("s")
        pressKey("space")
        time.sleep(SAFETY_SLEEP)
        pressKey("space")

    def pickYourStartes(pokemon: list):
        curx, cury = resetPick(0, 0) # safety

        for i, pkm in enumerate(pokemon):
            if i>5: break
            curx, cury = pickPokemon(pkm[0], pkm[1], pkm[2])
            curx, cury = resetPick(curx, cury)
        
        lockInPicks()

    def choseSafe(freeSafe: int):
        pressKey("space")
        time.sleep(3)
        pressKey("space")


    getToStarters()

    pickYourStartes([
        (9, 9, 6)
        ]
    )

    choseSafe()

    print("game started")

def attack():
    for _ in range(2): pressKey("space")

def gimmeCandy():
    time.sleep(5)

    startGame()

    attack()


