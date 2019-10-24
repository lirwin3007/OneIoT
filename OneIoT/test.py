import DeviceManager, time

manager = DeviceManager.DeviceManager()

test_device = manager.get_device("test")
#test_device.disconnect()
#test_device.connect()

#print(test_device.connected)

#test_device.connect()

#print(test_device.connected)

#test_device.disconnect()

#print(test_device.connected)

#test_device.upload("/home/pi/.oneIot/devices/test/user.py", "user.py")

#print(test_device.test_routine())

while True:
    time.sleep(1)
    test_device.led_state(0)
    time.sleep(1)
    test_device.led_state(1)
