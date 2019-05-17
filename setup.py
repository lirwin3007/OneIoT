import os, sys, subprocess
import datetime

def print_message(status, message, include_time = False):
	print('[' + status + ']\t' + message + ('\t' + str(datetime.datetime.now().strftime('%M:%S.%f')) if include_time else ''))

def install_package(name):
	print_message('INFO', 'Installing ' + name)
	result = subprocess.call([sys.executable, '-m', 'pip', 'install', name])
	if result != 0:
		print_message('ERROR', 'Package install "' + name + '" failed with code ' + str(result) + '. Try running "sudo apt-get update && apt-get upgrade" and try again')
	else:
		print_message('INFO', 'Succesfully installed ' + name)

if not __name__ == '__main__':
	print_message('FATAL', 'Not executing as top level code')
	exit()

if not os.getcwd() == os.path.expanduser('~') + '/OneIoT':
	print_message('FATAL', 'Not executing in ' + os.path.expanduser('~') + '/OneIoT')
	exit()

os.system("clear")
print("OneIoT setup")
print()
print("Please ensure that you are connected to the internet")
print("Plug in a microphone and speaker and press [ENTER] to continue")
input()

os.system("clear")
#Set up microphone and speaker
set_up = False
while not set_up:
	print()
	subprocess.call(['arecord', '-l'])
	print()
	mic_card = input('Enter the card number of your microphone: ')
	mic_device = input('Enter the device number of your microphone: ')

	print()
	subprocess.call(['aplay', '-l'])
	print()
	spk_card = input('Enter the card number of your speaker: ')
	spk_device = input('Enter the device number of your speaker: ')

	audioFile = open(os.path.expanduser('~') + '/.asoundrc', 'w+')
	audioFile.write('pcm.!default {\n\ttype asym\n\tcapture.pcm "mic"\n\tplayback.pcm "speaker"\n}\n')
	audioFile.write('pcm.mic {\n\ttype plug\n\tslave {\n\t\tpcm "hw:' + mic_card + ',' + mic_device + '"\n\t}\n}\n')
	audioFile.write('pcm.speaker {\n\ttype plug\n\tslave {\n\t\tpcm "hw:' + spk_card + ',' + spk_device + '"\n\t}\n}')
	audioFile.close()

	print("Testing audio")
	subprocess.call(['speaker-test', '-t', 'wav', '-l', '3'])
	set_up = input("Was sound audible? (y/n)") == 'y'

	if set_up:
		print("Testing microphone. Please make noise")
		subprocess.call(['arecord', '--format=S16_LE', '--duration=5', '--rate=16000', '--file-type=raw', 'out.raw'])
		subprocess.call(['aplay', '--format=S16_LE', '--rate=16000', 'out.raw'])
		set_up = input("Was recording audible? (y/n)") == 'y'

os.system("clear")
print("Follow these instructions to set up a google assistant project:")
print()
print("1 - Press [ENTER] to open the google actions console")
print("2 - Click 'Add/import project'")
print("3 - Give the project a name and click 'CREATE PROJECT'")
print("4 - Type the name that you gave the project into this console and press [ENTER]")
print("5 - Click 'Device registration'. This will be a box in the bottom row on your screen. Leave this page open, it'll be important in a bit.")
print("6 - In this console, press [ENTER] to open the assistant API page. Then click 'Enable'")
print("7 - In this console, press [ENTER] to configure the OAuth consent screen. Most fields on this page are optional.")
print()
print("All tabs except 'Actions on google' can be closed. Press [ENTER] to continue")
print()

input()
os.system("chromium-browser https://console.actions.google.com &")
project_id = input("Waiting for project name: ")
input()
os.system("chromium-browser https://console.developers.google.com/apis/api/embeddedassistant.googleapis.com/overview &")
input()
os.system("chromium-browser https://console.developers.google.com/apis/credentials/consent &")
input()

os.system("clear")
print("Follow these instructions to register this raspberry pi as an assistant enabled device:")
print()
print("1 - Return to the 'Device registration' tab and click 'REGISTER MODEL'")
print("2 - Fill out the details, set the Device type to 'Speaker'. When finished, click 'REGISTER MODEL'")
print("3 - Download the OAth 2.0 credentials, and store it in the location /home/pi/assistant-credentials.json")
print("4 - Click 'NEXT' and then 'SKIP'")
print("5 - Click on the new entry in the table that you just made, and copy the Model Id into this console. Press [ENTER] once complete")
print()
print("Press [ENTER] to continue with installing required packages")
print()

model_id = input("Waiting for Model Id: ")
input()

os.system("clear")
print("Installing required packages")

#Installing packagages
print_message('INFO', 'Installing required python packages')
install_package('google-assistant-library==1.0.1')
install_package('google-assistant-sdk[samples]==0.5.1')
install_package('google-auth-oauthlib[tool]')

os.system("clear")
os.system("google-oauthlib-tool --scope https://www.googleapis.com/auth/assistant-sdk-prototype --scope https://www.googleapis.com/auth/gcm --save --headless --client-secrets /home/pi/assistant-credentials.json")

os.system("clear")
print("Device setup complete! Assistant should be running now - say 'okay Google' to test it out. Once finished, press CTRL + C to exit")
os.system("googlesamples-assistant-hotword --project-id " + project_id + " --device-model-id " + model_id)
