

import platform

system = platform.system()

if system == "Windows":
    from input.windows import paste_text, backspace

elif system == "Linux":
    from input.linux import paste_text, backspace

elif system == "Darwin":
    from input.macos import paste_text, backspace

else:
    raise RuntimeError(f"Unsupported OS: {system}")


