from gpiozero import RotaryEncoder, Button
import requests
import time
import os
import socket


# Function to get the Pi's local IP address
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


# Get the local IP dynamically
local_ip = get_local_ip()

# Sonos API URL
SONOS_API = f"http://{local_ip}:5005/Living%20Room"

# URL of the button press sound (hosted in the web server directory)
BUTTON_SOUND_URL = f"http://{local_ip}/button_press.mp3"

# Global variables to track mute state, volume, and button hold time
is_muted = False
current_volume = 50  # Initialize with a default value
previous_volume = 50  # To store volume before muting
button_hold_time = 0  # Track how long the button is pressed


# Function to play a sound on Sonos speakers without interrupting playback
def play_button_sound():
    # Use the `clip` feature of the Sonos API to play a sound overlay
    requests.get(
        f"{SONOS_API}/clip/{BUTTON_SOUND_URL}/volume/30"
    )  # Adjust volume as needed


# Function to gradually change volume
def fade_volume(start, end, step=1, delay=0.1):
    global current_volume
    if start < end:
        for volume in range(start, end + 1, step):
            requests.get(f"{SONOS_API}/volume/{volume}")
            current_volume = volume  # Update global volume
            time.sleep(delay)
    else:
        for volume in range(start, end - 1, -step):
            requests.get(f"{SONOS_API}/volume/{volume}")
            current_volume = volume  # Update global volume
            time.sleep(delay)


# Function to handle button press for mute/unmute with fade
def toggle_mute():
    global is_muted, current_volume, previous_volume
    if not is_muted:
        # Store the current volume and fade to mute
        previous_volume = current_volume
        fade_volume(current_volume, 0, step=5, delay=0.05)
        is_muted = True
    else:
        # Fade back to the previous volume
        fade_volume(0, previous_volume, step=5, delay=0.05)
        is_muted = False


# Function to adjust volume via rotary encoder
def adjust_volume():
    global is_muted, current_volume, previous_volume
    if is_muted and encoder.steps > 0:
        # Unmute if volume is being increased
        is_muted = False
    if encoder.steps > 0:
        # Increase volume
        new_volume = current_volume + 5
        if new_volume <= 100:  # Ensure volume does not exceed 100
            requests.get(f"{SONOS_API}/volume/{new_volume}")
            current_volume = new_volume
    elif encoder.steps < 0:
        # Decrease volume
        new_volume = current_volume - 5
        if new_volume >= 0:  # Ensure volume does not go below 0
            requests.get(f"{SONOS_API}/volume/{new_volume}")
            current_volume = new_volume


# Function to handle long press for shutdown
def handle_button_hold():
    global button_hold_time
    button_hold_time = time.time()  # Record the time when button is pressed


def handle_button_release():
    global button_hold_time
    press_duration = time.time() - button_hold_time
    if press_duration >= 3:  # Check if button was held for 3 seconds or more
        print("Long press detected. Shutting down...")
        play_button_sound()  # Play sound when button is pressed
        os.system("sudo shutdown -h now")
    else:
        # Handle short press for mute/unmute
        toggle_mute()


# Function to fetch initial volume from Sonos API
def fetch_current_volume():
    global current_volume
    response = requests.get(f"{SONOS_API}/state").json()
    current_volume = response.get("volume", 50)  # Default to 50 if not found


# Set up GPIO
encoder = RotaryEncoder(17, 27)  # CLK, DT pins
button = Button(22)  # SW pin

# Fetch the initial volume on startup
fetch_current_volume()

# Bind events
encoder.when_rotated = adjust_volume
button.when_pressed = handle_button_hold
button.when_released = handle_button_release

# Keep the script running
while True:
    pass
