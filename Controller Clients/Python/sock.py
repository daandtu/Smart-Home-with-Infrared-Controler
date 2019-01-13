import socket
import ssl
import threading
import atexit

ss = None

def send(ss):
	while True:
		text = input("")
		if text == "q":
			ss.send(text.encode())
			print("Exit")
			ss.close()
			break
		elif len(text) > 0:
			ss.send(text.encode())

def recv(ss):
	while True:
		data = ss.recv(1024).decode()
		print(data)

def exit_handler():
	ss.send("q".encode())
	ss.close()
	client_socket.close()
	print("Socket closed")

# host = "000.000.000.000"  # Set you IP here
port = 4444

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
context.load_verify_locations("cert.pem")
client_socket = socket.socket()  # instantiate
client_socket.connect((host, port))  # connect to the server
ss = context.wrap_socket(client_socket, server_hostname=host)
print("Connected")
# ss.send("aPASSWORD".encode())  # Set your password here
atexit.register(exit_handler)

threading.Thread(target=send, args=(ss,)).start()
threading.Thread(target=recv, args=(ss,)).start()