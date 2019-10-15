import DeviceManager

manager = DeviceManager.DeviceManager()

test_device = manager.get_device("test")

#test_device.connect()

print(test_device.test_routine())
