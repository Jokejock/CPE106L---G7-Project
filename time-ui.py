import tkinter as tk

class SliderCountdownTimer:
    def __init__(self, master):
        self.master = master
        self.master.title("Countdown Timer")

        # Label for minutes
        self.label_minutes = tk.Label(master, text="Set Minutes (0-59):")
        self.label_minutes.pack()

        # Slider for selecting minutes
        self.slider_minutes = tk.Scale(master, from_=0, to=59, orient='horizontal', length=300)
        self.slider_minutes.pack()

        # Label for seconds
        self.label_seconds = tk.Label(master, text="Set Seconds (0-59):")
        self.label_seconds.pack()

        # Slider for selecting seconds
        self.slider_seconds = tk.Scale(master, from_=0, to=59, orient='horizontal', length=300)
        self.slider_seconds.pack()

        self.start_button = tk.Button(master, text="Start", command=self.start_timer)
        self.start_button.pack()

        self.timer_label = tk.Label(master, text="", font=("Helvetica", 48))
        self.timer_label.pack()

        self.is_running = False

    def start_timer(self):
        if self.is_running:
            return  # Prevent starting multiple timers

        # Get the values from the sliders
        minutes = self.slider_minutes.get()
        seconds = self.slider_seconds.get()
        total_seconds = minutes * 60 + seconds

        if total_seconds < 0:
            self.timer_label.config(text="Negative time not allowed.")
            return

        self.is_running = True
        self.countdown(total_seconds)

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
    countdown_timer = SliderCountdownTimer(root)
    root.mainloop()