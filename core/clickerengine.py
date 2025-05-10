import tkinter as tk
import threading

from pynput import keyboard, mouse
from time import sleep as sl

from core import config, utils


class AutoClickerEngine:
    def __init__(self):
        self.mouse_controller = mouse.Controller()
        self.is_clicking = False
        self.click_thread = None
        self.setup_global_hotkeys()

    def start_clicking(
        self,
        button,
        click_count,
        interval,
        repeat=1,
    ):
        if self.is_clicking:
            return

        self.is_clicking = True
        total_interval = interval

        match button.lower():
            case "left":
                btn = mouse.Button.left
            case "right":
                btn = mouse.Button.right
            case "middle":
                btn = mouse.Button.middle

        match click_count.lower():
            case "single":
                clickcount = 1
            case "double":
                clickcount = 2
            case "triple":
                clickcount = 3

        def click_loop():
            count = 0

            while self.is_clicking and (repeat is None or count < repeat):
                self.mouse_controller.click(btn, clickcount)
                count += 1
                if total_interval > 0:
                    sl(interval)

            self.is_clicking = False
            utils.on_f8_press(config.startbutton)

        self.click_thread = threading.Thread(target=click_loop, daemon=True)
        self.click_thread.start()

    def stop_clicking(self):
        self.is_clicking = False

        if self.click_thread and self.click_thread.is_alive():
            self.click_thread.join(timeout=0.1)

    def setup_global_hotkeys(self):
        if hasattr(self, "listener") and self.listener is not None:
            self.listener.stop()
            self.listener = None

        self.listener = keyboard.GlobalHotKeys(
            {
                config.start_hotkey: lambda: self.on_hotkey_press(True),
                config.stop_hotkey: lambda: self.on_hotkey_press(False),
            }
        )

        self.listener.start()

    def on_hotkey_press(self, start):
        if config.binding_mode:
            return

        if start:
            button = config.buttonclick.get().lower()
            clickcount = config.clicktype.get().lower()

            hours = int(config.entrynames["hourstoclick"].get() or 0)
            mins = int(config.entrynames["minstoclick"].get() or 0)
            secs = int(config.entrynames["sectoclick"].get() or 0)
            msecs = int(config.entrynames["msectoclick"].get() or 10)
            total_interval = hours * 3600 + mins * 60 + secs + msecs / 1000

            repeat = (
                None
                if config.untilstoppedvar.get()
                else int(config.timestorepeat.get() or 1)
            )

            # updating entries text
            intervalslist = (hours, mins, secs, msecs)
            for entry, interval in zip(config.entrynames.values(), intervalslist):
                entry.delete(0, tk.END)
                entry.insert(0, str(interval))

            # updating timestorepeat (entry) text
            if config.untilstoppedvar.get():
                # if untilstopped == true then check if timestorepeat entry == ""
                if config.timestorepeat.get() == "":
                    config.timestorepeat.delete(0, tk.END)
                    config.timestorepeat.insert(0, "1")
            else:
                config.timestorepeat.delete(0, tk.END)
                config.timestorepeat.insert(0, str(repeat))

            self.start_clicking(button, clickcount, total_interval, repeat)
            utils.on_f6_press(config.startbutton)
        else:
            self.stop_clicking()
            utils.on_f8_press(config.startbutton)
