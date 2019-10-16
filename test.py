import DeviceManager

manager = DeviceManager.DeviceManager()

test_device = manager.get_device("test")
test_device.disconnect()
#test_device.connect()

print(test_device.connected)

test_device.connect()

print(test_device.connected)

test_device.disconnect()

print(test_device.connected)

#test_device.upload("/home/pi/.oneIot/devices/test/user.py", "user.py")

#print(test_device.test_routine())
