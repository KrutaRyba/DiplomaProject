# Installation Process

This instruction will allow you to configure your environment and install all the dependencies for this project.

Neither [Server Setup](#server-setup) nor [Client Setup](#client-setup) includes Python and Python Virtual Environment installation step.

## Server Setup

Assumptions:
- Server has python3 installed
- Server has python3-virtualenv installed

### Installing the Server

1. Download the Server

**GitHub**
```
git clone https://github.com/KrutaRyba/DiplomaProject.git
cd DiplomaProject/Server
```

2. Run the setup script

```
chmod +x Setup.sh
./Setup.sh
```

3. Reboot

```
sudo reboot
```

4. Activate venv
```
source .venv/bin/activate
```

5. Start the Server

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

### Installing the Client

1. Download the Client (skip if already done so in the [Server Setup](#server-setup))

**GitHub**
```
git clone https://github.com/KrutaRyba/DiplomaProject.git
cd DiplomaProject/Client
```

2. Edit ClientConfig.json

```
"server_ip":"[server_ip]",
```

3. Start the Client

```
python3 Client.py
```

### Installing the E-Paper Library (optional since it is already included in the repository)

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

2. Add e-Paper library to the Client files

```
cp <path_to_epaper_folder>/RaspberryPi_JetsonNano/python/lib/waveshare_epd <path_to_client_folder>
```