# install.sh
#!/usr/bin/env bash
set -euo pipefail

# System deps (document these clearly)
sudo apt update
sudo apt install -y python3-venv python3-pip python3-full \
                    python3-smbus i2c-tools git \
                    tmux

# Enable I2C if needed (user can run manually)
# sudo raspi-config nonint do_i2c 0

# Project venv
python3 -m venv .venv
. .venv/bin/activate

# Python deps
pip install --upgrade pip
pip install -r requirements.txt
echo "Install complete."

# SONOS API
git clone https://github.com/jishi/node-sonos-http-api.git
cd node-sonos-http-api
npm install