import tkinter as tk
import pygame

# Initialize Pygame
pygame.mixer.init()

# Load your sound file (make sure to have a .wav or .mp3 file in the same directory)
sound_file = "your_sound_file.wav"  # Replace with your sound file
pygame.mixer.music.load(sound_file)

def play_sound():
    pygame.mixer.music.play()

# Create the main window
root = tk.Tk()
root.title("Sound Player")

# Create a button to play the sound
play_button = tk.Button(root, text="Play Sound", command=play_sound)
play_button.pack(pady=20)
# Run the application
root.mainloop()