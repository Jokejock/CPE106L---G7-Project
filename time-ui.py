import time
import tkinter as tk

class CountdownTimer:
    def __init__(self, master):
        self.master = master
        self.master.title("Countdown Timer")

        self.label = tk.Label(master, text="Enter time (MM:SS):")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.start_button = tk.Button(master, text="Start", command=self.start_timer)
        self.start_button.pack()

        self.timer_label = tk.Label(master, text="", font=("Helvetica", 48))
        self.timer_label.pack()

        self.is_running = False

    def start_timer(self):
        if self.is_running:
            return  # Prevent starting multiple timers

        time_input = self.entry.get()
        try:
            minutes, seconds = map(int, time_input.split(':'))
            total_seconds = minutes * 60 + seconds

            if total_seconds < 0:
                raise ValueError("Negative time not allowed.")

            self.is_running = True
            self.countdown(total_seconds)
        except ValueError:
            self.timer_label.config(text="Invalid input. Use MM:SS format.")

    def countdown(self, total_seconds):
        if total_seconds >= 0:
            mins, secs = divmod(total_seconds, 60)
            timer = f'{mins:02d}:{secs:02d}'
            self.timer_label.config(text=timer)
            self.master.after(1000, self.countdown, total_seconds - 1)  # Call countdown every second
        else:
            self.timer_label.config(text="Time's up!")
            self.is_running = False

if __name__ == "__main__":
    root = tk.Tk()
    countdown_timer = CountdownTimer(root)
    root.mainloop()