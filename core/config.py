import sys
import os
import tkinter as tk
from tkinter import ttk


def get_config_path():
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    return os.path.join(data_dir, "userconfig.json")


configfile = get_config_path()

start_hotkey = "<F6>"
stop_hotkey = "<F8>"

fontparameter = ("Times New Roman", 12)
fontparameter2 = ("Times New Roman", 8)
fontparameter3 = ("Times New Roman", 10)

buttonstoclick = ("Left", "Right", "Middle")
clicktypes = ("Single", "Double", "Triple")

hourstoclick: ttk.Entry = None
minstoclick: ttk.Entry = None
sectoclick: ttk.Entry = None
msectoclick: ttk.Entry = None
timestorepeat: ttk.Entry = None
untilstopped: ttk.Checkbutton = None
untilstoppedvar: tk.BooleanVar = None
buttonclick: ttk.Combobox = None
clicktype: ttk.Combobox = None
startbutton: ttk.Button = None
helpbutton: ttk.Button = None
hotkeysbutton: ttk.Button = None
starthotkeyentry: ttk.Entry = None
stophotkeyentry: ttk.Entry = None

entrynames: dict[str, ttk.Entry] = {}
entryargs = (
    ("hourstoclick", "Hours", (90, 39), (15, 40, 65, 22)),
    ("minstoclick", "Minutes", (246, 39), (177, 40, 65, 22)),
    ("sectoclick", "Seconds", (405, 39), (330, 40, 65, 22)),
    ("msectoclick", "Milliseconds", (235, 73), (160, 74, 65, 22)),
)

forbidden_keys = {
    "<esc>",
    "<tab>",
    "<caps_lock>",
    "<shift>",
    "<shift_r>",
    "<ctrl>",
    "<ctrl_r>",
    "<alt>",
    "<alt_r>",
    "<cmd>",
    "<cmd_r>",
    "<windows>",
    "<fn>",
    "<fn_r>",
    "<space>",
    "<backspace>",
    "<enter>",
    "<insert>",
    "<delete>",
    "<home>",
    "<end>",
    "<page_up>",
    "<page_down>",
    "<up>",
    "<down>",
    "<left>",
    "<right>",
}

change_hotkeys_call: callable = None

binding_mode = False
