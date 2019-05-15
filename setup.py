import os, sys, subprocess
import datetime

def print_message(status, message, include_time = False):
	print('[' + status + ']\t' + message + ('\t' + str(datetime.datetime.now().strftime('%M:%S.%f')) if include_time else ''))
	
def install_package(name):
	print_message('INFO', 'Installing ' + name)
	result = subprocess.call([sys.executable, '-m', 'pip', 'install', name])
	if result != 0:
		print_message('FATAL', 'Package install "' + name + '" failed with code ' + result + '. Try running "sudo apt-get update && apt-get upgrade" and try again')
		exit()
	print_message('INFO', 'Succesfully installed ' + name)

if not __name__ == '__main__':
	print_message('FATAL', 'Not executing as top level code')
	exit()

if not os.getcwd() == os.path.expanduser('~') + '/OneIoT':
	print_message('FATAL', 'Not executing in ' + os.path.expanduser('~') + '/OneIoT')
	exit()

#Set up microphone and speaker
set_up = False
while not set_up:
	print()
	subprocess.call(['arecord', '-l'])
	print()
	mic_card = input('Enter the card number of your microphone')
	mic_device = input('Enter the device number of your microphone')

	print()
	subprocess.call(['aplay', '-l'])
	print()
	spk_card = input('Enter the card number of your speaker')
	spk_device = input('Enter the device number of your speaker')

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

print()
input("Installing required packages. press [Enter] to continue")

#Installing packagages
print_message('INFO', 'Installing required python packages')
install_package('google-assistant-library==1.0.1')
install_package('google-assistant-sdk[samples]==0.5.1')

