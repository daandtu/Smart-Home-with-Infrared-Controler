# -*- coding: utf-8 -*-
import socket
import ssl
import threading
import atexit

class Cli:
    count = 0
    def __init__(self, con_s, addr):
        Cli.count += 1
        print("New connection:",addr[0],addr[1],"In total",Cli.count,"connections")
        self.con_s = con_s
        self.addr = addr
        self.topics = ""
        self.auth = False
    def recv(self, byt=1024):
        return self.con_s.recv(byt).decode()
    def exit(self):
        self.con_s.close()
        Cli.count -= 1
        print(self.addr[0], self.addr[1], "disconnected")
    def send(self, data):
        print(self.addr[1], "Send", data)
        self.con_s.send(data.encode())
    def subs(self, data):
        print(self.addr[1], "Subs", data)
        self.topics += data
    def unsubs(self, data):
        self.topics.replace(data, '')
        print(self.addr[1], 'Unsubs', data)

def on_new_client(cs,addr):#
    global clientList
    cl = Cli(cs, addr)
    clientList.append(cl)
    while True:
        data = cl.recv()
        if len(data) < 1:
            pass
        elif cl.auth:
            if data == "q":
                cl.exit()
                clientList.remove(cl)
                return
            elif data[0] == "t":
                cl.subs(data[1:])
            elif data[0] == "s":
                zus = "\n" if data[1] is "u" else ""
                for i in clientList:
                    if data[1] in i.topics:
                        i.send('s' + data[2:] + zus)
            elif data[0] == "d":
                cl.unsubs(data[1:])
            elif data[0] == "c":
                cl.send('c' + str(Cli.count))
            else:
                print(str(data))
        elif data[0] == "a":
            if data[1:] == "PASSWORD":
                cl.auth = True
                print(addr[1],"authenticated")
        else:
            print(addr[1],"not authenticated")
            cl.exit()
            clientList.remove(cl)
            return

def exit_handler():
    global s, ssock
    for cl in clientList:
        cl.exit()
    s.close()
    ssock.close()
    print("Socket closed")

atexit.register(exit_handler)  # Register an exit handler for unsuspected exits like KeyboardInterrupt

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile='ssl/cert.pem', keyfile='ssl/pv.key')

PORT = 4444
MAXCON = 2  # Max connections

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print('Socket created')
s.bind((socket.gethostname(), PORT))
print('Socket connected')
s.listen(5)
ssock = context.wrap_socket(s, server_side=True)

run = True
clientList = []

while run:
    #accept connections from outside
    if Cli.count <= MAXCON:
        conn, address = ssock.accept()
        threading.Thread(target=on_new_client,args=(conn,address)).start()
s.close()
