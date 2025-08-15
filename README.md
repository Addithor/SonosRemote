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
   - Uses cron service to run the python script and the Sonos HTTP API.

---

## Requirements

### Hardware
- **Raspberry Pi Zero W**
- **Rotary Encoder** with push-button functionality
   - Adafruit I2C Stemma QT Rotary Encoder Breakout with Encoder - STEMMA QT / Qwiic
- **STEMMA QT / Qwiic breakout** 
   - SparkFun Qwiic or Stemma QT SHIM for Raspberry Pi / SBC

### Software
- **Raspberry Pi OS (Lite recommended)**
- Python 3
- requirements.txt for python libraries
- install.sh for system dependancies

---

## Setup

### 1. Hardware Connection
- Connect the rotary encoder to the Raspberry Pi via the STEMMA QT / Qwiic interface.

### 2. Run the installer
- Run install.sh
- Make the installer executable if needed: chmod +x ./install.sh

### 4. Configure the Python Script
- Update .env.sonos with the appropriate room name, port for the Sonos API and path to the button sound

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
  @reboot /path/to/your/script/startup_sonos.sh >> /path/to/your/script/startup.log 2>&1
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
   - A sound is played on the Sonos speakers after long press.

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
  - The button sound file (`button_press.wav` or `.mp3`) should be placed in:
`/var/www/html/` this is the default public folder for the Apache web server on Raspberry Pi OS.

- **Script Not Running on Startup**:
  - Check `crontab` entries and logs for errors.
  - Ensure all dependencies are installed.

---

## License
This project is open-source and licensed under the MIT License.

---

## Acknowledgments
- [Jishi's Node-Sonos-HTTP-API](https://github.com/jishi/node-sonos-http-api) for providing the Sonos API integration.

