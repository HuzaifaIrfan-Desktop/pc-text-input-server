

# pyperclip, pynput in __init__.py Works on Linux this not needed

import shutil
import subprocess



if shutil.which("xdotool") is None:
    raise RuntimeError("xdotool is not installed.")

if shutil.which("xclip") is None:
    raise RuntimeError("xclip is not installed.")


def paste_text(text: str):

    print("paste_text Linux:", text)


    # Type Using only xdotool
    # 
    # subprocess.run(
    #     [
    #         "xdotool",
    #         "type",
    #         "--clearmodifiers",
    #         "--delay",
    #         "0",
    #         text,
    #     ],
    #     check=True,
    # )


    # Copy UTF-8 text to clipboard using xclip
    subprocess.run(
        ["xclip", "-selection", "clipboard"],
        input=text.encode("utf-8"),
        check=True,
    )

    # Paste using xdotool
    subprocess.run(
        [
            "xdotool",
            "key",
            "--clearmodifiers",
            "ctrl+v",
        ],
        check=True,
    )



def backspace(count: int = 1):

    print("backspace Linux:", count)

    for _ in range(count):
        subprocess.run(
            [
                "xdotool",
                "key",
                "--clearmodifiers",
                "BackSpace",
            ],
            check=True,
        )




