import socket
import select
import pickle

IP = '127.0.0.1'
PORT = 1234

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

server_socket.bind((IP,PORT))
server_socket.listen()
print(f"connection started at {IP} {PORT}")
socket_list = [server_socket,]
clients = {}

def recieveMessages(client_socket):
    try:
        message = pickle.loads(client_socket.recv(1024))
        if not len(message):
            return False
        return message
    except:
        return False

while True:
    readers,_,errors = select.select(socket_list,[],socket_list)
    for notified_socket in readers:
        if notified_socket == server_socket:
            client_socket,client_address = server_socket.accept()
            userinfo = recieveMessages(client_socket)
            if userinfo is False:
                continue
            socket_list.append(client_socket)
            clients[client_socket] = userinfo
            print(clients)
            print(f"accepted connection from {userinfo[0]} at {client_address}")
        else:
            message = recieveMessages(notified_socket)
            if message is False:
                print(f"disconnected from {clients[notified_socket][0]}")
                socket_list.remove(notified_socket)
                del clients[notified_socket]
            else:
                if type(message) == str:
                    print(f"user request for {message}")
                    for client in clients:
                        flag = False
                        if clients[client][0] == message:
                            notified_socket.send(pickle.dumps(clients[client][1]))
                            print(f"sent public key {clients[client][1]}" )
                            flag = True
                            break
                    if flag == False:
                        notified_socket.send(pickle.dumps("NaN"))
                else:
                    reciever = message[0]
                    send_message = message[1]
                    for client in clients:
                        if reciever == clients[client][0]:
                            client.send(pickle.dumps(send_message))
    for notified_socket in errors:
        print(f"something is wrong with {clients[notified_socket][0]}")
        socket_list.remove(notified_socket)
        del clients[notified_socket]
