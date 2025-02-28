import time

def countdown_timer(minutes, seconds):
    total_seconds = minutes * 60 + seconds
    while total_seconds:
        mins, secs = divmod(total_seconds, 60)
        timer = f'{mins:02d}:{secs:02d}'
        print(timer, end='\r')  # Print the timer on the same line
        time.sleep(1)  # Wait for 1 second
        total_seconds -= 1

    print("Time's up!")

def main():
    print("Welcome to the Countdown Timer!")
    
    # Get user input for minutes and seconds
    try:
        minutes = int(input("Enter the number of minutes: "))
        seconds = int(input("Enter the number of seconds: "))
        
        if minutes < 0 or seconds < 0:
            print("Please enter non-negative values.")
            return
        
        countdown_timer(minutes, seconds)
    
    except ValueError:
        print("Invalid input. Please enter integers for minutes and seconds.")

if __name__ == "__main__":
    main()