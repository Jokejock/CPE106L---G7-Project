import tkinter as tk
import pygame

class SliderCountdownTimer:
    def __init__(self, master):
        self.master = master
        self.master.title("STEADYPACE")

        # Initialize Pygame mixer for alarm
        pygame.mixer.init()
        self.alarm_sound = "overthehorizon.mp3"  # Replace with your sound file
        pygame.mixer.music.load(self.alarm_sound)

        # Label for hours
        self.label_hours = tk.Label(master, text="Set Hours (0-23):")
        self.label_hours.pack()

        # Slider for selecting hours
        self.slider_hours = tk.Scale(master, from_=0, to=23, orient='horizontal', length=300, command=self.update_time_display)
        self.slider_hours.pack()

        # Label for minutes
        self.label_minutes = tk.Label(master, text="Set Minutes (0-59):")
        self.label_minutes.pack()

        # Slider for selecting minutes
        self.slider_minutes = tk.Scale(master, from_=0, to=59, orient='horizontal', length=300, command=self.update_time_display)
        self.slider_minutes.pack()

        # Label for seconds
        self.label_seconds = tk.Label(master, text="Set Seconds (0-59):")
        self.label_seconds.pack()

        # Slider for selecting seconds
        self.slider_seconds = tk.Scale(master, from_=0, to=59, orient='horizontal', length=300, command=self.update_time_display)
        self.slider_seconds.pack()

        # Label to display selected time
        self.selected_time_label = tk.Label(master, text="", font=("Helvetica", 24))
        self.selected_time_label.pack()

        #Frame for buttons
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)  # Add some vertical padding

        self.start_button = tk.Button(master, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(master, text="Pause", command=self.pause_timer)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.resume_button = tk.Button(master, text="Resume", command=self.resume_timer)
        self.resume_button.pack(side=tk.RIGHT, padx=5)

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_timer)
        self.stop_button.pack(side=tk.RIGHT, padx=5)

        self.timer_label = tk.Label(master, text="", font=("Helvetica", 48))
        self.timer_label.pack()

        self.is_running = False
        self.is_paused = False
        self.remaining_time = 0
        self.should_play_alarm = True  # Flag to control alarm playback

        # Update the time display initially
        self.update_time_display()

    def update_time_display(self, event=None):
        hours = self.slider_hours.get()
        minutes = self.slider_minutes.get()
        seconds = self.slider_seconds.get()
        self.selected_time_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")

    def start_timer(self):
        if self.is_running:
            return  # Prevent starting multiple timers

        # Get the values from the sliders
        hours = self.slider_hours.get()
        minutes = self.slider_minutes.get()
        seconds = self.slider_seconds.get()
        self.remaining_time = hours * 3600 + minutes * 60 + seconds  # Convert to total seconds

        if self.remaining_time < 0:
            self.timer_label.config(text="NEGATIVE TIME NOT ALLOWED")
            return

        self.is_running = True
        self.is_paused = False
        self.should_play_alarm = True  # Reset the alarm flag when starting
        self.countdown()

    def countdown(self):
        if self.remaining_time >= 0 and not self.is_paused:
            mins, secs = divmod(self.remaining_time, 60)
            hours, mins = divmod(mins, 60)
            timer = f'{hours:02d}:{mins:02d}:{secs:02d}'
            self.timer_label.config(text=timer)
            self.remaining_time -= 1
            self.master.after(1000, self.countdown)  # Call countdown every second
        elif self.remaining_time < 0:
            self.timer_label.config(text="TIME'S UP!")
            self.is_running = False
            if self.should_play_alarm:  # Check if the alarm should play
                self.play_alarm()

    def pause_timer(self):
        if self.is_running and not self.is_paused:
            self.is_paused = True

    def resume_timer(self):
        if self.is_running and self.is_paused:
            self.is_paused = False
            self.countdown()  # Resume countdown

    def stop_timer(self):
        self.is_running = False
        self.is_paused = False
        self.remaining_time = 0
        self.timer_label.config(text="")
        self.should_play_alarm = False  # Prevent the alarm from playing
        self.stop_alarm()  # Ensure the alarm is stopped if it was playing

    def play_alarm(self):
        pygame.mixer.music.play()  # Play the alarm sound
        self.master.after(30000, self.stop_alarm)  # Stop the alarm after 30 seconds

    def stop_alarm(self):
        pygame.mixer.music.stop()  # Stop the alarm sound


if __name__ == "__main__":
    root = tk.Tk()
    countdown_timer = SliderCountdownTimer(root)
    root.mainloop()