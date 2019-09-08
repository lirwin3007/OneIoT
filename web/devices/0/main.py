import user
import socket
import json

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

callables = {'set_state': ['redValue', 'greenValue', 'blueValue']}

running = True
while running:
    cl, addr = s.accept()
    print('client connected from', addr)

    headers = cl.recv(1024).decode("utf-8")
    if not headers: break
    data = cl.recv(1024).decode("utf-8")
    if not data: break

    args = {}
    if len(data) > 0:
        try:
            args = json.loads(data)
        except:
            args = {}

    if headers.find("POST") != -1:
        type = "POST"
        url = headers[headers.index("POST ") + 5:headers.index("HTTP")].strip()
    elif headers.find("GET") != -1:
        type = "GET"
        url = headers[headers.index("GET ") + 4:headers.index("HTTP")].strip()

    print("args = " + str(args))
    print("type = " + str(type))
    print("url = " + str(url))

    if url == "/kill_for_program_flash":
        running = False
        break

    valid = True
    if url[1:] in callables:
        arg_string = ""
        for needed_arg in callables[url[1:]]:
            if not needed_arg in args:
                valid = False
            if valid:
                if isinstance(args[needed_arg], bool):
                    arg_string += str(args[needed_arg]) + ","
                else:
                    arg_string += json.dumps(args[needed_arg]) + ","
        arg_string = arg_string[:-1]
    else:
        valid = False

    if valid:
        print("Valid arguments found")
        command = "result = user." + url[1:] + "(" + arg_string + ")"
        print("Executing " + command)
        try:
            exec(command)
        except Exception as e:
            result = None
            print("Error executing '" + command + "':\n" + str(e))
    else:
        result = "Invalid request"
        print("Invalid request")

    cl.send('HTTP/1.1 200 OK\n')
    cl.send('Content-Type: text/html\n')
    cl.send('Connection: close\n\n')
    cl.sendall(json.dumps(result))
    cl.close()
