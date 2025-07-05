# Sonos Volume Control Script

This project is a Raspberry Pi-based remote control for a Sonos speaker system. It uses a rotary encoder and a button to control volume and mute/unmute, with additional features such as overlaying a button sound on the speakers and shutting down the device with a long button press.

---

## Features

1. **Volume Control**:
   - Adjust the speaker volume using a rotary encoder.

2. **Mute/Unmute**:
   - Press the button to toggle mute/unmute with a fade effect.

3. **Button Sound**:
   - Play a sound over the Sonos speakers when the button is shut down.

4. **Shutdown**:
   - Hold the button for 3 seconds to safely shut down the Raspberry Pi.

5. **Dynamic IP Detection**:
   - Automatically detects the Raspberry Pi's local IP address to interact with the Sonos HTTP API.

6. **Sonos HTTP API Server runs on the PI**:
   - Uses Systemd Service to run the python script and the Sonos HTTP API.

---

## Requirements

### Hardware
- **Raspberry Pi Zero W**
- **Rotary Encoder** with push-button functionality

### Software
- **Raspberry Pi OS (Lite recommended)**
- Python 3
- Required Python libraries:
  - `gpiozero`
  - `requests`

---

## Setup

### 1. Hardware Connection
- Connect the rotary encoder to the Raspberry Pi's GPIO pins:
  - `CLK` to GPIO 17
  - `DT` to GPIO 27
  - `SW` (button) to GPIO 22
  - `GND` to a ground pin
- Ensure the Raspberry Pi is powered and connected to Wi-Fi.

### 2. Install Dependencies
Run the following commands on the Raspberry Pi:
```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install gpiozero requests
```

### 3. Set Up the Sonos HTTP API
1. Clone the Sonos HTTP API repository:
   ```bash
   git clone https://github.com/jishi/node-sonos-http-api.git
   ```
2. Navigate to the directory:
   ```bash
   cd node-sonos-http-api
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Start the API:
   ```bash
   npm start
   ```

### 4. Configure the Python Script
1. Place the `button_press.mp3` sound file in your web server directory (e.g., `/var/www/html/`).
2. Update the script with the correct file paths and Sonos room name.

---

## Running the Script

### 1. Manual Run
To test the script manually, run:
```bash
python3 /path/to/your/script.py
```

### 2. Automatic Startup
To ensure the script and API run on startup:
- Use `crontab`:
  ```bash
  crontab -e
  ```
  Add the following lines:
  ```bash
  @reboot cd /path/to/node-sonos-http-api && npm start &
  @reboot python3 /path/to/your/script.py &
  ```
- Save and reboot:
  ```bash
  sudo reboot
  ```

---

## Usage

1. **Adjust Volume**:
   - Rotate the encoder clockwise to increase volume.
   - Rotate counterclockwise to decrease volume.

2. **Mute/Unmute**:
   - Press the button to toggle mute/unmute with a fade effect.

3. **Play Button Sound**:
   - A sound is played on the Sonos speakers when the button is pressed.

4. **Shutdown**:
   - Hold the button for 3 seconds to safely shut down the Raspberry Pi.

---

## Troubleshooting

- **Sonos API Not Responding**:
  - Ensure the API is running by checking:
    ```bash
    curl http://<pi-ip>:5005/zones
    ```

- **No Sound When Pressing the Button**:
  - Verify the `button_press.mp3` file is accessible at:
    ```bash
    http://<pi-ip>/button_press.mp3
    ```

- **Script Not Running on Startup**:
  - Check `crontab` entries and logs for errors.
  - Ensure all dependencies are installed.

---

## License
This project is open-source and licensed under the MIT License.

---

## Acknowledgments
- [Jishi's Node-Sonos-HTTP-API](https://github.com/jishi/node-sonos-http-api) for providing the Sonos API integration.

