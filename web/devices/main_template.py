import user
import socket

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

callables = {{CALLABLES}}

running = True
while running:
    cl, addr = s.accept()
    print()
    print('client connected from', addr)
    request = cl.recv(1024)
    request = str(request)

    args = {}
    temp_args = request.split("\\r\\n\\r\\n")
    if len(temp_args) > 1:
        if temp_args[1] != "'":
            temp_args = temp_args[1][:-1].split("&")
            args = {arg.split("=")[0]:arg.split("=")[1] for arg in temp_args}
    if request.find("POST") != -1:
        type = "POST"
        url = request[request.index("POST ") + 5:request.index("HTTP")].strip()
    elif request.find("GET") != -1:
        type = "GET"
        url = request[request.index("GET ") + 4:request.index("HTTP")].strip()

    print("args = " + str(args))
    print("type = " + str(type))
    print("url = " + str(url))

    if url == "/kill_for_program_flash":
        running = False

    valid = True
    if url[1:] in callables:
        arg_string = ""
        for needed_arg in callables[url[1:]]:
            if not needed_arg in args:
                valid = False
            if valid:
                arg_string += args[needed_arg] + ","
        arg_string = arg_string[:-1]
    else:
        valid = False

    if valid:
        print("Valid arguments found")
        command = "user." + url[1:] + "(" + arg_string + ")"
        print("Executing " + command)
        try:
            exec(command)
        except Exception as e:
            print("Error executing '" + command + "':\n" + str(e))
    else:
        print("Invalid request")

    cl.send('HTTP/1.1 200 OK\n')
    cl.send('Content-Type: text/html\n')
    cl.send('Connection: close\n\n')
    cl.sendall("OK")
    cl.close()
