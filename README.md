# Installation Process

This instruction will allow you to configure your environment and install all the dependencies for this project.

Neither [Server Setup](#server-setup) nor [Client Setup](#client-setup) includes Python and Python Virtual Environment installation step.

## Server Setup

Assumptions:
- Server has python3 installed
- Server has python3-virtualenv installed

### Configuring Environment

1. Install the Osmium tool

**Linux**
```
sudo apt-get install osmium-tool
```

**macOS**
```
sudo brew osmium-tool
```

2. Take a note of the IP address

```
ifconfig
```

3. Download the OSM data

```
wget https://download.geofabrik.de/europe/ukraine-latest.osm.pbf
```

### Installing the Server

1. Download the Server

**GitHub**
```
git clone https://github.com/KrutaRyba/DiplomaProject.git
cd DiplomaProject/Server
```

2. Create venv

```
python3 -m venv .venv
```

3. Activate venv
```
source .venv/bin/activate
```

4. Install the dependencies

```
pip install -r requirements.txt
```

5. Edit ServerConfig.json

```
"osm_file":"[path_to_the_osm_file]"
```

6. Start the Server

```
python3 Server.py
```

## Client Setup

Assumptions:
- Client has python3 installed
- Client has python3-virtualenv installed
- Client is running on Raspberry Pi
- Client is (correctly) connected to the Waveshare 7.3-inch e-Paper HAT (F) display

### Configuring Raspberry Pi

Based on the [official Waveshare tutorial](https://www.waveshare.com/wiki/7.3inch_e-Paper_HAT_(F)_Manual)

1. Enable SPI Interface

```
sudo raspi-config
Choose Interfacing Options -> SPI -> Yes Enable SPI interface
```

2. Reboot

```
sudo reboot
```

3. Install the function library

```
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo pip3 install spidev
```

4. Install the gpiozero library (should be installed by default)

```
sudo apt-get update
sudo apt install python3-gpiozero
```

### Installing the E-Paper Library

1. Download the demo

**GitHub**
```
git clone https://github.com/waveshare/e-Paper.git
```

**wget**
```
wget https://files.waveshare.com/upload/7/71/E-Paper_code.zip
unzip E-Paper_code.zip -d e-Paper
```

2. Add folder \<path_to_your_folder\>/e-Paper/RaspberryPi_JetsonNano/python/lib/ to the PATH variable

```
sudoedit /etc/environment
```

3. Apply change

```
source /etc/environment
```

### Installing the Client

1. Download the Client (skip if already done so in the [Server Setup](#server-setup))

**GitHub**
```
git clone https://github.com/KrutaRyba/DiplomaProject.git
cd DiplomaProject/Client
```

2. Create venv

```
python3 -m venv .venv --system-site-packages
```

3. Activate venv
```
source .venv/bin/activate
```

4. Install the dependencies

```
pip install -r requirements.txt
```

5. Edit ClientConfig.json

```
"server_ip":"[server_ip]",
```

6. Start the Client

```
python3 Client.py

```
