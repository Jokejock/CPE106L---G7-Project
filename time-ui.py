import tkinter as tk
import pygame

class SliderCountdownTimer:
    def __init__(self, master):
        self.master = master
        self.master.title("Countdown Timer")

        # Initialize Pygame mixer for alarm
        pygame.mixer.init()
        self.alarm_sound = "overthehorizon.mp3"  # Replace with your sound file
        pygame.mixer.music.load(self.alarm_sound)

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

        self.pause_button = tk.Button(master, text="Pause", command=self.pause_timer)
        self.pause_button.pack()

        self.resume_button = tk.Button(master, text="Resume", command=self.resume_timer)
        self.resume_button.pack()

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_timer)
        self.stop_button.pack()

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
            self.play_alarm()
    
    def pause_timer(self):
        if self.is_running and not self.is_paused:
            self.is_paused = True
    
    def resume_timer(self):
        if self.is_running and self.is_paused:
            self.is_paused = False
            self.countdown() #Resume Countdown
    
    def stop_timer(self):
        self.is_running = False
        self.is_paused = False
        self.remaining_time = 0
        self.timer_label.config(text="")

    def play_alarm(self):
        pygame.mixer.music.play()  # Play the alarm sound
        self.master.after(30000, self.stop_alarm)  # Stop the alarm after 5 seconds

    def stop_alarm(self):
        pygame.mixer.music.stop()  # Stop the alarm sound

if __name__ == "__main__":
    root = tk.Tk()
    countdown_timer = SliderCountdownTimer(root)
    root.mainloop()