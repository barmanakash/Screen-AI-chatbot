import pyautogui

# Standard safety failsafe: Shoving the mouse to any screen corner aborts script execution immediately
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

class ActionExecutor:
    @staticmethod
    def click(x: int, y: int):
        pyautogui.moveTo(x, y, duration=0.3)
        pyautogui.click()

    @staticmethod
    def type_text(text: str):
        pyautogui.write(text, interval=0.05)

    @staticmethod
    def press_key(key: str):
        pyautogui.press(key)