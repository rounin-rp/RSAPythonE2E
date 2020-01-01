from tkinter import *
from threading import *
import socket
import pickle
from encryption import rsa
import sys

flag = False
quitFlagClient = False
USERNAME = ''
pubKey = ()
PRIKEY = ()
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
NaN_message = ''
recv_pub_key = ()
recievedMessage = {}
beText = ''
ED = 0
theMessageToSend = ""

recieverUserName = ''

def Exit():
    exit(0)

def enterMessage():
    global beText
    global inMessage
    print(beText)
    inMessage.delete('0.1',END)
    inMessage.insert(END,beText)

def connectToNetwork(host,port):
    global s
    try:
        s.connect((host,port))
        genKeys()
        if USERNAME != '' and len(pubKey) > 0:
            userinfo = (USERNAME,pubKey)
            s.send(pickle.dumps(userinfo))
    except:
        connectToNetwork(host,port+1)

def genKeys():
    global pubKey
    global PRIKEY
    pubKey,PRIKEY = rsa.keygen()


def recieverNotFound():
    global nanReciever
    nanReciever.config(text="reciever not found!")

def recieverFound():
    global nanReciever
    nanReciever.config(text="reciever found successfully!")

class Connect():
    def run(self):
        self.root = Tk()
        usernameLabel = Label(self.root,text = "username : ").place(x = 30, y = 50)
        self.usernameEntry = Entry(self.root)
        self.usernameEntry.place(x = 30, y = 70)
        B1 = Button(self.root,text="go",command = self.button1Application)
        B1.place(x = 50, y = 90)
        self.message = Label(self.root,text = '')
        self.message.place(x = 30, y = 110)
        self.root.mainloop()

    def button1Application(self):
        global flag
        global USERNAME
        username = self.usernameEntry.get()
        if username != '':
            USERNAME = username
            flag = True
            connectToNetwork('127.0.0.1',1234)
            flag = True
            self.message.config(text = "")
            self.root.destroy()
            obj3 = Client()
            obj3.run()
        else:
            self.message.config(text = "please enter a username ")

class Client():

    def decryptMessage(self):
        global recievedMessage
        global beText
        if len(recievedMessage) > 0:
            sender = recievedMessage['sender']
            cipher_text = recievedMessage['CT']
            cipher_block = recievedMessage['CB']
            beText = rsa.decrypt(cipher_block,PRIKEY)
            enterMessage()
            recievedMessage = {}

        else:
            pass

    def sendMessage(self):
        global theMessageToSend
        global recv_pub_key
        theMessageToSend = self.outMessage.get()
        if len(theMessageToSend) > 0:
            if type(recv_pub_key) == tuple:
                tosend = {}
                print(recv_pub_key)
                cipher_text,cipher_block = rsa.encrypt(theMessageToSend,recv_pub_key)
                tosend['sender'] = USERNAME
                tosend['CT'] = cipher_text
                tosend['CB'] = cipher_block
                send = [recieverUserName,tosend]
                s.send(pickle.dumps(send))
                theMessageToSend = ""
                self.outMessage.delete(0,END)



    def search(self):
        global recieverUserName
        global s
        global nanReciever
        recieverUserName = self.recieverEntry.get()
        print(recieverUserName)
        if recieverUserName == '':
            nanReciever.config(text="enter the name of the reciever")
        else:
            s.send(pickle.dumps(recieverUserName))


    def closeAsk(self):
        global quitFlagClient
        from tkinter import messagebox
        if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
            quitFlagClient = True
            self.root.destroy()

    def runClient(self):
        global USERNAME
        global inMessage
        global nanReciever
        self.root = Tk()
        title = "Welcome "+USERNAME+" !"
        self.root.title(title)
        self.root.protocol("WM_DELETE_WINDOW",self.closeAsk)
        self.root.geometry("640x480")
        self.recieverLabel = Label(self.root,text = "reciever's username : ")
        self.recieverLabel.place(x=10,y=10)
        self.recieverEntry = Entry(self.root)
        self.recieverEntry.place(x=200,y=10)
        nanReciever = Label(self.root,text = "")
        nanReciever.place(x=200,y=30)
        searchButton = Button(self.root,text="search",command = self.search)
        searchButton.place(x=350, y = 10)
        outMessageLabel = Label(self.root,text = "message : ")
        outMessageLabel.place(x=10,y=50)
        self.outMessage = Entry(self.root)
        self.outMessage.place(x=100,y=50,height=25,width=250)
        sendButton = Button(self.root,text = "send",command = self.sendMessage)
        sendButton.place(x=350,y=50)
        frame = Frame(self.root,width=150,height=150)
        inMessageLabel = Label(frame,text="recieved message : ")
        inMessageLabel.place(x=0,y=0)
        inMessage = Text(frame)
        inMessage.insert(END,beText)
        inMessage.place(x=0,y=20,height=150,width=150)
        frame.place(x = 10, y = 200)
        decryptButton = Button(self.root,text="decrypt",command = self.decryptMessage)
        decryptButton.place(x=200,y=275)
        self.root.mainloop()

    def run(self):
        global flag
        global quitFlagClient
        while True:
            if flag == True:
                self.runClient()
                break


class GetMessage(Thread):
    def run(self):
        global s
        global recv_pub_key
        global beText
        global recievedMessage
        global quitFlagClient
        while True:
            if quitFlagClient:
                print("trying to exit")
                Exit()
            if flag:
                mess = pickle.loads(s.recv(1024))
                if type(mess) == str:
                    if mess == "NaN":
                        recieverNotFound()
                elif type(mess) == dict:
                    recievedMessage = mess
                    beText = mess['CT']
                    enterMessage()
                elif type(mess) == tuple:
                    recv_pub_key = mess
                    print(recv_pub_key)
                    recieverFound()
                else:
                    pass


if __name__ == '__main__':
    obj1 = Connect()
    obj3 = GetMessage()
    obj3.start()
    obj1.run()
