import network
wlan=network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("OneIoT", "OneIoTPass")
wlan.ifconfig(('192.168.4.7','255.255.255.0','192.168.4.1','8.8.8.8'))

import webrepl
webrepl.start()
