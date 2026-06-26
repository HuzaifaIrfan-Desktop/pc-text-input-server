

# pyperclip, pynput in __init__.py Works on Linux and windows this not needed

# import platform

# system = platform.system()

# if system == "Windows":
#     from input.windows import paste_text, backspace

# elif system == "Linux":
#     from input.linux import paste_text, backspace

# elif system == "Darwin":
#     from input.macos import paste_text, backspace

# else:
#     raise RuntimeError(f"Unsupported OS: {system}")


from pynput.keyboard import Controller, Key
import pyperclip
import time

# create controller instance
kb = Controller()

# ---------- helpers ----------

def paste_utf8_text(text: str):
    pyperclip.copy(text)
    time.sleep(0.05)

    with kb.pressed(Key.ctrl):
        kb.press('v')
        kb.release('v')


def type_utf8_text(text: str):
    kb.type(text)


def press_backspace(n: int = 1):
    for _ in range(n):
        kb.press(Key.backspace)
        kb.release(Key.backspace)


def paste_text(text: str):
    print("paste_text:", text)
    paste_utf8_text(text)



def backspace(count: int = 1):
    print("backspace:")
    press_backspace(count)


