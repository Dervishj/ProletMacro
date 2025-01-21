import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import time
import threading
import keyboard
import random

import sys
import ctypes

if sys.platform == 'win32':
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# PyAutoGUI optimizations
pyautogui.PAUSE = 0.001
pyautogui.FAILSAFE = False

class ProletMacro:
    def __init__(self, root):
        self.root = root
        self.root.title("ProletMacro v1.0")
        self.root.geometry("500x450")
        
        # Variables
        self.hold_button = tk.StringVar(value="left")
        self.turbo1_button = tk.StringVar(value="left")
        self.turbo2_button = tk.StringVar(value="right")
        self.turbo1_min = tk.IntVar(value=0)
        self.turbo1_max = tk.IntVar(value=0)
        self.turbo2_min = tk.IntVar(value=0)
        self.turbo2_max = tk.IntVar(value=0)
        
        self.holding = False
        self.turbo1_active = False
        self.turbo2_active = False

        # Interface
        self.create_interface()
        
        # Hotkeys
        keyboard.add_hotkey("ctrl", self.toggle_hold)
        keyboard.add_hotkey("shift+1", self.toggle_turbo1)
        keyboard.add_hotkey("shift+2", self.toggle_turbo2)

    def create_interface(self):
        notebook = ttk.Notebook(self.root)
        
        # Hold Mode Tab
        hold_frame = ttk.Frame(notebook)
        ttk.Label(hold_frame, text="Hold Mode Settings", font=('Helvetica', 12, 'bold')).pack(pady=10)
        
        ttk.Label(hold_frame, text="Mouse Button:").pack()
        ttk.Combobox(hold_frame, textvariable=self.hold_button, 
                    values=["left", "right", "middle"], state="readonly").pack()
        
        notebook.add(hold_frame, text="⏺ Hold")
        
        # Turbo 1 Tab
        turbo1_frame = ttk.Frame(notebook)
        ttk.Label(turbo1_frame, text="Turbo Click 1 Settings", font=('Helvetica', 12, 'bold')).pack(pady=10)
        
        ttk.Label(turbo1_frame, text="Mouse Button:").pack()
        ttk.Combobox(turbo1_frame, textvariable=self.turbo1_button,
                    values=["left", "right", "middle"], state="readonly").pack()
        
        ttk.Label(turbo1_frame, text="Min Delay (ms):").pack()
        ttk.Entry(turbo1_frame, textvariable=self.turbo1_min).pack()
        
        ttk.Label(turbo1_frame, text="Max Delay (ms):").pack()
        ttk.Entry(turbo1_frame, textvariable=self.turbo1_max).pack()
        
        notebook.add(turbo1_frame, text="⚡ Turbo 1")
        
        # Turbo 2 Tab
        turbo2_frame = ttk.Frame(notebook)
        ttk.Label(turbo2_frame, text="Turbo Click 2 Settings", font=('Helvetica', 12, 'bold')).pack(pady=10)
        
        ttk.Label(turbo2_frame, text="Mouse Button:").pack()
        ttk.Combobox(turbo2_frame, textvariable=self.turbo2_button,
                    values=["left", "right", "middle"], state="readonly").pack()
        
        ttk.Label(turbo2_frame, text="Min Delay (ms):").pack()
        ttk.Entry(turbo2_frame, textvariable=self.turbo2_min).pack()
        
        ttk.Label(turbo2_frame, text="Max Delay (ms):").pack()
        ttk.Entry(turbo2_frame, textvariable=self.turbo2_max).pack()
        
        notebook.add(turbo2_frame, text="🔥 Turbo 2")
        
        notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Help Button
        help_btn = ttk.Button(self.root, text="❓ Help", command=self.show_help)
        help_btn.place(relx=0.95, rely=0.95, anchor="se")

    def show_help(self):
        help_text = """🚀 ProletMacro - Help Center 🚀

► BASIC USAGE:
- ⏺ Hold Mode: CTRL key (Continuous hold)
- ⚡ Turbo 1: SHIFT+1 (200+ CPS)
- 🔥 Turbo 2: SHIFT+2 (200+ CPS)

⚙️ PERFORMANCE SETTINGS:
• CPS Calculation:
  CPS = 1000 / (Delay in ms)
  Example: 5ms delay → 200 CPS

• Optimal Delay Values:
  - Min Delay: 0-2ms (Maximum speed)
  - Max Delay: 1-5ms (Stable performance)

🔧 HOW TO FIND BEST SETTINGS?
1. Start with Min=0, Max=0
2. Measure CPS (3rd party tools)
3. Increase Max Delay by 1ms if instability
4. Test until hardware limits

⚠️ WARNINGS:
- Hardware limitations under 5ms
- Anti-cheat systems may detect low delays
- Continuous max speed may damage hardware"""

        messagebox.showinfo("Help Center - ProletMacro", help_text)

    def toggle_hold(self):
        if not self.holding:
            self.holding = True
            threading.Thread(target=self.hold_action, daemon=True).start()
        else:
            self.holding = False

    def hold_action(self):
        pyautogui.mouseDown(button=self.hold_button.get())
        while self.holding:
            time.sleep(0.01)
        pyautogui.mouseUp(button=self.hold_button.get())

    def toggle_turbo1(self):
        self.turbo1_active = not self.turbo1_active
        if self.turbo1_active:
            threading.Thread(target=self.turbo_action, args=(1,), daemon=True).start()

    def toggle_turbo2(self):
        self.turbo2_active = not self.turbo2_active
        if self.turbo2_active:
            threading.Thread(target=self.turbo_action, args=(2,), daemon=True).start()

    def turbo_action(self, mode):
        button = self.turbo1_button.get() if mode == 1 else self.turbo2_button.get()
        min_d = self.turbo1_min.get() if mode == 1 else self.turbo2_min.get()
        max_d = self.turbo1_max.get() if mode == 1 else self.turbo2_max.get()
        
        while getattr(self, f"turbo{mode}_active"):
            start = time.perf_counter()
            pyautogui.click(button=button, _pause=False)
            delay = random.randint(min_d, max_d)/1000
            elapsed = time.perf_counter() - start
            time.sleep(max(0.0001, delay - elapsed))

if __name__ == "__main__":
    root = tk.Tk()
    app = ProletMacro(root)
    root.mainloop()