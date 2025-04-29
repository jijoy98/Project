import tkinter as tk

def start_timer():
    time_left = int(entry.get())

    def countdown():
        nonlocal time_left
        if time_left > 0:
            mins, secs = divmod(time_left, 60)
            timer_label.config(text=f"{mins:02d}:{secs:02d}")
            time_left -= 1
            window.after(1000, countdown)
        else:
            timer_label.config(text="⏰ Time's Up!")

    countdown()

# GUI setup
window = tk.Tk()
window.title("Countdown Timer")

entry = tk.Entry(window, width=10)
entry.insert(0, "60")
entry.pack(pady=10)

start_button = tk.Button(window, text="Start Timer", command=start_timer)
start_button.pack()

timer_label = tk.Label(window, text="00:00", font=("Helvetica", 32))
timer_label.pack(pady=20)

window.mainloop()

