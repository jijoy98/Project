import tkinter as tk
from tkinter import messagebox
import threading
import time

class CountdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⏳ Countdown Timer")

        self.running = False
        self.paused = False
        self.time_left = 0

        # UI Layout
        self.create_widgets()

    def create_widgets(self):
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Minutes:").grid(row=0, column=0)
        self.minutes_entry = tk.Entry(input_frame, width=5)
        self.minutes_entry.insert(0, "1")
        self.minutes_entry.grid(row=0, column=1)

        tk.Label(input_frame, text="Seconds:").grid(row=0, column=2)
        self.seconds_entry = tk.Entry(input_frame, width=5)
        self.seconds_entry.insert(0, "0")
        self.seconds_entry.grid(row=0, column=3)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        self.start_btn = tk.Button(button_frame, text="Start", command=self.start_timer)
        self.start_btn.grid(row=0, column=0, padx=5)

        self.pause_btn = tk.Button(button_frame, text="Pause", command=self.pause_timer, state='disabled')
        self.pause_btn.grid(row=0, column=1, padx=5)

        self.reset_btn = tk.Button(button_frame, text="Reset", command=self.reset_timer, state='disabled')
        self.reset_btn.grid(row=0, column=2, padx=5)

        self.timer_label = tk.Label(self.root, text="00:00", font=("Helvetica", 40))
        self.timer_label.pack(pady=20)

    def start_timer(self):
        try:
            minutes = int(self.minutes_entry.get())
            seconds = int(self.seconds_entry.get())
            self.time_left = minutes * 60 + seconds
            if self.time_left <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter valid numbers for minutes and seconds.")
            return

        self.running = True
        self.paused = False
        self.update_buttons(start=False, pause=True, reset=True)
        self.minutes_entry.config(state='disabled')
        self.seconds_entry.config(state='disabled')
        threading.Thread(target=self.countdown, daemon=True).start()

    def countdown(self):
        while self.time_left > 0 and self.running:
            if not self.paused:
                mins, secs = divmod(self.time_left, 60)
                self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
                time.sleep(1)
                self.time_left -= 1
        if self.time_left == 0 and self.running:
            self.timer_label.config(text="⏰ Time's Up!")
            threading.Thread(target=self.play_sound, daemon=True).start()
            self.update_buttons(start=True, pause=False, reset=True)

    def play_sound(self):
        try:
            playsound("alarm.mp3")  # Put an 'alarm.mp3' file in the same folder
        except:
            print("Sound failed. Check 'alarm.mp3' is available.")

    def pause_timer(self):
        self.paused = not self.paused
        self.pause_btn.config(text="Resume" if self.paused else "Pause")

    def reset_timer(self):
        self.running = False
        self.paused = False
        self.time_left = 0
        self.timer_label.config(text="00:00")
        self.minutes_entry.config(state='normal')
        self.seconds_entry.config(state='normal')
        self.update_buttons(start=True, pause=False, reset=False)

    def update_buttons(self, start, pause, reset):
        self.start_btn.config(state='normal' if start else 'disabled')
        self.pause_btn.config(state='normal' if pause else 'disabled', text="Pause")
        self.reset_btn.config(state='normal' if reset else 'disabled')


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownApp(root)
    root.mainloop()
