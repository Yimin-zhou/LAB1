import socket, select, threading

# connect to server 
sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_port= ("18.195.107.195", 5378)
sock.connect(host_port)
print('Connected to server!')

# first hand shake
userName = input('Enter your username to start: ')
name = userName.encode("utf-8")
newLine = "\n".encode("utf-8")
firstHandShake = "HELLO-FROM ".encode("utf-8")
# sendall calls send repeatedly until all bytes are sent.
sock.sendall(firstHandShake + name + newLine)

# second handshake
secondHandShake = sock.recv(4096)
print (secondHandShake.decode("utf-8"))

# a loop
while True:
    # send msgs
    msg = input('You> ')
    # when user enter !who
    if msg == "!who":
        loggedInUsers = "WHO\n".encode("utf-8")
        sock.sendall(loggedInUsers)

    # quit client
    elif msg == "!quit":
        exit()

    # slice the msg string
    # need to FIX !!!!!!!!
    elif msg.startswith("@"):
        user = msg[1:msg.index(' ')]
        myMsg = msg[msg.index(' ') + 1:]
        sendUser = user.encode("utf-8")
        sendMsg = myMsg.encode("utf-8")
        send = "SEND".encode("utf-8")
        newLine = "\n".encode("utf-8")
        sock.sendall(send + sendMsg + newLine)

    else:
        newLine = "\n".encode("utf-8")
        myMsg = msg.encode("utf-8")
        sock.sendall(myMsg + newLine)
    
    #receive msg
    data = sock.recv(4096)

    # decode the msg
    myData = data.decode("utf-8")

    # need to FIX !!!!!!!!
    if myData == "IN-USE\n":
        print('Name has been taken, start over again')
        exit()

    else:
        print(myData)

sock.close()
