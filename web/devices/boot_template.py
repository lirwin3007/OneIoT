import network
wlan=network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("{{SSID}}", "{{PSK}}")
wlan.ifconfig(('{{IP_ADDRESS}}','255.255.255.0','192.168.4.1','8.8.8.8'))

import webrepl
webrepl.start()
