import tkinter as tk
import pygame

class SliderCountdownTimer:
    def __init__(self, master):
        self.master = master
        self.master.title("STEADYPACE")
        self.master.configure(bg="#f0f0f0")  # Set a light background color

        # Initialize Pygame mixer for alarm
        pygame.mixer.init()
        self.alarm_sound = "overthehorizon.mp3"  # Replace with your sound file
        pygame.mixer.music.load(self.alarm_sound)

        # Initialize presets dictionary
        self.presets = {}

        self.title_label = tk.Label(
            master, 
            text="STEADYPACE™", 
            font=("Helvetica", 36, "bold"),  # Large bold font
            bg="#f0f0f0",
            fg="blue"  # Blue text color
        )
        self.title_label.pack(side=tk.TOP, pady=10)

        # Create a frame for the timer display
        self.timer_frame = tk.Frame(master, bg="#ffffff", bd=5, relief=tk.RAISED)
        self.timer_frame.pack(side=tk.RIGHT, padx=20, pady=20)

        # Timer label positioned in the timer frame
        self.timer_label = tk.Label(self.timer_frame, text="", font=("Helvetica", 48), bg="#ffffff")
        self.timer_label.pack(padx=20, pady=20)  # Add padding inside the frame

        # Label for hours
        self.label_hours = tk.Label(master, text="Set Hours (0-23):", bg="#f0f0f0")
        self.label_hours.pack()

        # Slider for selecting hours
        self.slider_hours = tk.Scale(master, from_=0, to=23, orient='horizontal', length=300, command=self.update_time_display)
        self.slider_hours.pack()

        # Label for minutes
        self.label_minutes = tk.Label(master, text="Set Minutes (0-59):", bg="#f0f0f0")
        self.label_minutes.pack()

        # Slider for selecting minutes
        self.slider_minutes = tk.Scale(master, from_=0, to=59, orient='horizontal', length=300, command=self.update_time_display)
        self.slider_minutes.pack()

        # Label for seconds
        self.label_seconds = tk.Label(master, text="Set Seconds (0-59):", bg="#f0f0f0")
        self.label_seconds.pack()

        # Slider for selecting seconds
        self.slider_seconds = tk.Scale(master, from_=0, to=59, orient='horizontal', length=300, command=self.update_time_display)
        self.slider_seconds.pack()

        # Label to display selected time
        self.selected_time_label = tk.Label(master, text="", font=("Helvetica", 24), bg="#f0f0f0")
        self.selected_time_label.pack()

        # Frame for buttons
        self.button_frame = tk.Frame(master, bg="#f0f0f0")
        self.button_frame.pack(pady=10)  # Add some vertical padding

        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(self.button_frame, text="Pause", command=self.pause_timer)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.resume_button = tk.Button(self.button_frame, text="Resume", command=self.resume_timer)
        self.resume_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.button_frame, text="Stop", command=self.stop_timer)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Preset management
        self.preset_frame = tk.Frame(master, bg="#f0f0f0")
        self.preset_frame.pack(pady=10)

        self.preset_listbox = tk.Listbox(self.preset_frame, width=30)
        self.preset_listbox.pack(side=tk.BOTTOM)

        self.load_button = tk.Button(self.preset_frame, text="Load Preset", command=self.load_preset)
        self.load_button.pack(side=tk.TOP, padx=5)

        self.save_button = tk.Button(self.preset_frame, text="Save Preset", command=self.save_preset)
        self.save_button.pack(side=tk.TOP, padx=5)

        self.delete_button = tk.Button(self.preset_frame, text="Delete Preset", command=self.delete_preset)
        self.delete_button.pack(side=tk.TOP, padx=5)

        self.is_running = False
        self.is_paused = False
        self.remaining_time = 0
        self.should_play_alarm = True  # Flag to control alarm playback

        # Update the time display initially
        self.update_time_display()

        # Copyright label at the bottom
        self.copyright_label = tk.Label(
            master, 
            text="Copyright © Group 7 Studio LLC 2025, All rights reserved.", 
            font=("Helvetica", 10), 
            bg="#f0f0f0"
        )
        self.copyright_label.pack(side=tk.BOTTOM, pady=5)

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

    def save_preset(self):
        hours = self.slider_hours.get()
        minutes = self.slider_minutes.get()
        seconds = self.slider_seconds.get()
        preset_name = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        # Save the preset
        self.presets[preset_name] = (hours, minutes, seconds)
        self.update_preset_listbox()

    def load_preset(self):
        selected = self.preset_listbox.curselection()
        if selected:
            preset_name = self.preset_listbox.get(selected)
            hours, minutes, seconds = self.presets[preset_name]
            self.slider_hours.set(hours)
            self.slider_minutes.set(minutes)
            self.slider_seconds.set(seconds)
            self.update_time_display()

    def delete_preset(self):
        selected = self.preset_listbox.curselection()
        if selected:
            preset_name = self.preset_listbox.get(selected)
            del self.presets[preset_name]
            self.update_preset_listbox()

    def update_preset_listbox(self):
        self.preset_listbox.delete(0, tk.END)  # Clear the listbox
        for preset in self.presets.keys():
            self.preset_listbox.insert(tk.END, preset)  # Add presets to the listbox


if __name__ == "__main__":
    root = tk.Tk()
    countdown_timer = SliderCountdownTimer(root)
    root.mainloop()