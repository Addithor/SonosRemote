import time
import requests
import os
import socket
import board
from adafruit_seesaw import digitalio, rotaryio, seesaw
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()
SONOS_ROOM = os.getenv("SONSO_ROOM", "Living Room")
SONOS_API_PORT = os.getenv("SONOS_API_PORT", "5005")
BUTTON_SOUND_URL = os.getenv("BUTTON_SOUND_URL", "")


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
print(local_ip)

# Sonos API URL
SONOS_API = f"http://{local_ip}:{SONOS_API_PORT}/{SONOS_ROOM.replace(' ', '%20')}"

# URL of the button press sound (hosted in the web server directory)
BUTTON_SOUND_URL = f"http://{local_ip}/button_press.wav"

# Global variables to track mute state, volume, and button hold time
is_muted = False
current_volume = 30  # Initialize with a default value
previous_volume = 30  # To store volume before muting
button_hold_time = 0  # Track how long the button is pressed

i2c = board.I2C()  # uses board.SCL and board.SDA
seesaw = seesaw.Seesaw(i2c, addr=0x36)  # Default I2C address for the rotary encoder

seesaw_product = (seesaw.get_version() >> 16) & 0xFFFF
print(f"Found product {seesaw_product}")
if seesaw_product != 4991:
    print("Wrong firmware loaded?  Expected 4991")

# Configure seesaw pin used to read knob button presses
seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
button = digitalio.DigitalIO(seesaw, 24)

button_held = False

encoder = rotaryio.IncrementalEncoder(seesaw)
last_position = -encoder.position  # Fix: Initialize properly


# Function to play a sound on Sonos speakers without interrupting playback
def play_button_sound():
    try:
        requests.get(f"{SONOS_API}/clip/{BUTTON_SOUND_URL}/volume/50", timeout=2)
    except:
        pass


# Function to gradually change volume
def fade_volume(start, end, step=1, delay=0.1):
    global current_volume
    if start < end:
        for volume in range(start, end + 1, step):
            try:
                requests.get(f"{SONOS_API}/volume/{volume}", timeout=2)
                current_volume = volume
                time.sleep(delay)
            except:
                break
    else:
        for volume in range(start, end - 1, -step):
            try:
                requests.get(f"{SONOS_API}/volume/{volume}", timeout=2)
                current_volume = volume
                time.sleep(delay)
            except:
                break


# Function to handle button press for mute/unmute with fade
def toggle_mute():
    global is_muted, current_volume, previous_volume
    if not is_muted:
        previous_volume = current_volume
        fade_volume(current_volume, 0, step=2, delay=0.05)
        is_muted = True
    else:
        fade_volume(0, previous_volume, step=2, delay=0.05)
        is_muted = False


# Function to fetch initial volume from Sonos API
def fetch_current_volume():
    global current_volume
    try:
        response = requests.get(f"{SONOS_API}/state", timeout=5).json()
        current_volume = response.get("volume", 30)
    except:
        current_volume = 30


# Fetch the initial volume on startup
fetch_current_volume()

try:
    while True:
        # Read encoder position
        position = encoder.position
        if position != last_position:
            diff = position - last_position
            if diff > 0:
                new_volume = min(current_volume + 2, 100)
            else:
                new_volume = max(current_volume - 2, 0)

            try:
                requests.get(f"{SONOS_API}/volume/{new_volume}", timeout=2)
                current_volume = new_volume
                print(f"Volume: {current_volume}")
            except:
                print("Could not reach Sonos API")

            last_position = position

        # Check button state (polling approach)
        if not button.value and not button_held:
            button_hold_time = time.time()
            button_held = True

        if button.value and button_held:
            press_duration = time.time() - button_hold_time
            if press_duration >= 3:
                print("Long press detected. Shutting down...")
                play_button_sound()
                os.system("sudo shutdown -h now")
            else:
                print("Short press detected. Toggling mute.")
                play_button_sound()
                toggle_mute()
            button_held = False

        time.sleep(0.1)

except KeyboardInterrupt:
    pass
