import json
import tkinter as tk
from tkinter import ttk

from pynput import keyboard

from core import config

# ------------------------------------------- Functions for save / load config -------------------------------------------


def save_config():
    config_data = {
        "hours": config.entrynames["hourstoclick"].get() or "0",
        "minutes": config.entrynames["minstoclick"].get() or "0",
        "seconds": config.entrynames["sectoclick"].get() or "0",
        "milliseconds": config.entrynames["msectoclick"].get() or "10",
        "button": config.buttonclick.get(),
        "click_type": config.clicktype.get(),
        "repeat_times": config.timestorepeat.get() or "1",
        "until_stopped": config.untilstoppedvar.get(),
        "start_hotkey": config.start_hotkey,
        "stop_hotkey": config.stop_hotkey,
    }

    with open(config.configfile, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=4, ensure_ascii=False)


def load_config():
    try:
        with open(config.configfile, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except FileNotFoundError:
        return

    for field, configkey, defaultvalue in (
        ("hourstoclick", "hours", "0"),
        ("minstoclick", "minutes", "0"),
        ("sectoclick", "seconds", "0"),
        ("msectoclick", "milliseconds", "10"),
    ):
        # if interval entries are exists and if intervals are exists
        if field in config.entrynames and config.entrynames[field] is not None:
            config.entrynames[field].delete(0, tk.END)
            config.entrynames[field].insert(
                0, str(config_data.get(configkey, defaultvalue))
            )

    if config.buttonclick is not None:
        config.buttonclick.set(config_data.get("button", "Left"))

    if config.clicktype is not None:
        config.clicktype.set(config_data.get("click_type", "Single"))

    if config.timestorepeat is not None:
        config.timestorepeat.delete(0, tk.END)
        config.timestorepeat.insert(0, config_data.get("repeat_times", "1"))

    if config.untilstoppedvar is not None:
        config.untilstoppedvar.set(config_data.get("until_stopped", False))

    config.start_hotkey = config_data.get("start_hotkey", "<F6>")
    if config.startbutton is not None:
        on_f8_press(config.startbutton)

    config.stop_hotkey = config_data.get("stop_hotkey", "<F8>")


# --------------------------------------------------- Functions for UI ---------------------------------------------------


def draw_rectangle(canvas, x, y, w, h):
    canvas.create_line(x, y, x + w, y, fill="gray", width=1.5, stipple="gray25")
    canvas.create_line(x, y + h, x + w, y + h, fill="gray", width=1.5, stipple="gray25")
    canvas.create_line(x, y, x, y + h, fill="gray", width=1.5, stipple="gray25")
    canvas.create_line(x + w, y, x + w, y + h, fill="gray", width=1.5, stipple="gray25")


def draw_entry(root, entryvar, labeltext, labelplace, entryplace):
    validate_key = get_validate_key(root)
    entry = ttk.Entry(
        root,
        font=config.fontparameter2,
        justify="right",
        validate="key",
        validatecommand=(validate_key, "%P"),
    )
    entry.place(
        x=entryplace[0], y=entryplace[1], width=entryplace[2], height=entryplace[3]
    )
    entry.delete(0, tk.END)
    entry.insert(0, "0")
    ttk.Label(root, text=labeltext, font=config.fontparameter).place(
        x=labelplace[0], y=labelplace[1]
    )

    config.entrynames[entryvar] = entry


def draw_combobox(root, boxvalues, boxstate, boxplace, boxset, labeltext, labelplace):
    combobox = ttk.Combobox(root, values=boxvalues, state=boxstate)
    combobox.place(x=boxplace[0], y=boxplace[1], width=boxplace[2], height=boxplace[3])
    combobox.set(boxset)
    ttk.Label(root, text=labeltext, font=config.fontparameter).place(
        x=labelplace[0], y=labelplace[1]
    )

    return combobox


def draw_spinbox(root, boxplace, labeltext, labelplace):
    validate_key = get_validate_key(root)
    spinbox = ttk.Spinbox(
        root,
        from_=1,
        to=1e100,
        increment=1,
        font=config.fontparameter2,
        justify="center",
        validate="key",
        validatecommand=(validate_key, "%P"),
    )
    spinbox.place(x=boxplace[0], y=boxplace[1], width=boxplace[2], height=boxplace[3])
    spinbox.set(1)
    ttk.Label(root, text=labeltext, font=config.fontparameter).place(
        x=labelplace[0], y=labelplace[1]
    )

    return spinbox


def draw_checkbutton(root, btntext, btnvar, btnplace, labeltext, labelplace):
    checkbutton = ttk.Checkbutton(root, text=btntext, variable=btnvar)
    checkbutton.place(
        x=btnplace[0], y=btnplace[1], width=btnplace[2], height=btnplace[3]
    )
    ttk.Label(root, text=labeltext, font=config.fontparameter).place(
        x=labelplace[0], y=labelplace[1]
    )

    return checkbutton


def draw_button(root, btntext, btnplace, command=""):
    button = ttk.Button(
        root,
        text=btntext,
        command=command,
    )
    button.place(x=btnplace[0], y=btnplace[1], width=btnplace[2], height=btnplace[3])

    return button


def draw_label(root, txt, fontparam, pos):
    ttk.Label(root, text=txt, font=fontparam).place(x=pos[0], y=pos[1])


def on_f6_press(button):
    button.config(text=f"Stop (Bind = {config.stop_hotkey.strip('<>').capitalize()})")


def on_f8_press(button):
    button.config(text=f"Start (Bind = {config.start_hotkey.strip('<>').capitalize()})")


# ------------------------------------ Validate input + get key to validate functions ------------------------------------


def validate_input(text):
    return text.isdigit() or text == ""


def get_validate_key(root):
    validatekey = root.register(validate_input)
    return validatekey


# ---------------------------------------- Hotkey listener + set hotkey functions ----------------------------------------


def on_key_press(key, hotkey_form_tobind, listener):
    if hasattr(key, "char") and key.char:
        key_name = key.char.lower()
        formatted_key = f"{key_name}"
    else:
        key_name = key.name
        formatted_key = f"<{key_name}>"

    if formatted_key in config.forbidden_keys:
        return

    if hotkey_form_tobind == "start":
        if formatted_key != config.stop_hotkey:
            config.start_hotkey = formatted_key

            config.change_hotkeys_call()

            if config.starthotkeyentry is not None:
                config.starthotkeyentry.config(state="normal")
                config.starthotkeyentry.delete(0, tk.END)
                config.starthotkeyentry.insert(
                    0, f"{formatted_key.strip('<>').capitalize()}"
                )
                config.starthotkeyentry.config(state="readonly")
    if hotkey_form_tobind == "stop":
        if formatted_key != config.start_hotkey:
            config.stop_hotkey = formatted_key
            config.change_hotkeys_call()

            if config.stophotkeyentry is not None:
                config.stophotkeyentry.config(state="normal")
                config.stophotkeyentry.delete(0, tk.END)
                config.stophotkeyentry.insert(
                    0, f"{formatted_key.strip('<>').capitalize()}"
                )
                config.stophotkeyentry.config(state="readonly")

    if config.startbutton is not None:
        config.startbutton.config(
            text=f"Start (Bind: {config.start_hotkey.strip('<>').capitalize()})"
        )

    if listener:
        listener.stop()


def start_listener(hotkey_form):
    if hotkey_form == "start":
        listener = keyboard.Listener(
            on_press=lambda key: on_key_press(key, "start", listener)
        )
    elif hotkey_form == "stop":
        listener = keyboard.Listener(
            on_press=lambda key: on_key_press(key, "stop", listener)
        )

    listener.start()


def on_hotkeys_change(callback):
    config.change_hotkeys_call = callback
