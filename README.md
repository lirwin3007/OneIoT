# OneIoT
An open source platform for IoT development  
*Maintained by Louis Irwin*

OneIoT is a platform to create an interconnected network of devices. The center of this network is a Raspberry Pi 3, which runs the Google assistant and can connect to a number of ESP32 based development boards running Micropython.

### Installation
##### Requirements
 - Raspberry Pi 3 running Raspbian (or Noobs)
 - Internet connection

##### Setup
Install dependancies
```bash
sudo apt-get update
sudo apt-get install python3-dev
sudo apt-get install portaudio19-dev libffi-dev libssl-dev libmpg123-dev
```
Get the source
```bash
cd ~
git clone https://github.com/lirwin3007/OneIoT.git
```
Run the setup
```bash
cd OneIoT
python3 setup.py
```
