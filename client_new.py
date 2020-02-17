import socket, threading
from time import sleep

# connect to server 
sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_port= ("18.195.107.195", 5378)
sock.connect(host_port)
print('Connected to server!')

try:
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

except OSError as errorMsg:
    print(errorMsg)

def rec():
    while True:
        #receive msg
        data = sock.recv(4096)
        # decode the msg
        myData = data.decode("utf-8")
        
        if myData.startswith("DELIVERY"):
            print("MSG from >>" + myData[8:])

        elif myData.startswith("SEND-OK"):
            print("MSG SENT!\n")

        elif myData.startswith("UNKNOWN"):
            print("destination user is not currently logged in.\n")

        elif myData.startswith("BUSY"):
            print("maximum number of clients has been reached.\n")
        
        # TODO!!!!!
        # those 2 not working properly
        elif myData.startswith("BAD-RQST-HDR"):
            print("an error in the header.\n")
        elif myData.startswith("BAD-RQST-BODY"):
            print("an error in the body.\n")
            
        else:
            print(myData)

def send():
    while True:
        # send msgs
        msg = input('You> ')
        # when user enter !who
        if msg == "!who":
            loggedInUsers = "WHO\n".encode("utf-8")
            sock.sendall(loggedInUsers)

        # quit client
        elif msg == "!quit":
            sock.close()
            exit()

        # slice the msg string
        elif msg.startswith("@"):
            user = msg[1:msg.index(' ')]
            myMsg = msg[msg.index(' '):]
            sendUser = user.encode("utf-8")
            sendMsg = myMsg.encode("utf-8")
            send = "SEND ".encode("utf-8")
            newLine = "\n".encode("utf-8")
            sock.sendall(send + sendUser + sendMsg + newLine)

        else:
            myMsg = msg.encode("utf-8")
            sock.sendall(myMsg)
        
        sleep(1)

if __name__ == "__main__":
    
    t1 = threading.Thread(target=send)
    t2 = threading.Thread(target=rec)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    