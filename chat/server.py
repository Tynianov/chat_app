from tkinter import *
from socket import AF_INET,socket,SOCK_STREAM,gethostbyname,gethostname
from threading import Thread
import select

LARGE_FONT = ("Times", "27", "bold")
SMALL_FONT = ("Arial", "12", "bold")
COLORED_FONT = ("Arial", "10",'bold')


class ServerWindow(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.addresses = {}
        self.clients = {}
        self.PORT = 1234
        self.IP_ADDR = gethostbyname(gethostname())
        self.BUFSIZE = 2048
        self.server = socket(AF_INET,SOCK_STREAM)
        self.server.bind((self.IP_ADDR, self.PORT))
        self.server.listen()
        self.title('Chat')
        self.accepting_connection = True
        self.geometry('400x400')
        self.resizable(width=False,height=False)
        self.protocol('WM_DELETE_WINDOW',self.quit_server)
        self.init_window()


    def init_window(self):
        self.first_frame = Frame(self,width=400,height=400,bg='WHITE')
        self.first_frame.grid(row=0, column=0)

        self.logs = Listbox(self.first_frame,width=50,height=21,highlightbackground='#2d4366',fg='#1b3256',font=COLORED_FONT)
        self.logs.place(x=22,y=15)
        self.logs.insert(END,'Server has been stared on {}:{}'.format(self.IP_ADDR,self.PORT))
        self.logs.insert(END, 'Waiting for connections...')


    def accept_connection(self):

        while self.accepting_connection:
            try:
                client,client_ip_address = self.server.accept()
                self.logs.insert(END,'{} joined chat!'.format(client_ip_address))
                client.send(bytes('Welcome to chat!','utf-8'))
                self.addresses[client] = client_ip_address
                new_user_thread =  Thread(target=self.handle_client_connection, args=(client,),daemon=True)
                new_user_thread.start()

            except SystemExit:
                self.quit_server()

            except OSError:
               self.quit_server()

    def handle_client_connection(self,client):

        name = client.recv(self.BUFSIZE).decode('utf8')
        client.send(bytes('Hello, {}'.format(name),'utf8'))
        self.send_message(bytes('{} joined chat'.format(name),'utf8'))
        self.clients[client] = name

        while True:
            try:
                message = client.recv(self.BUFSIZE)

                self.send_message(message, name+':')

            except ConnectionError:
                self.logs.insert(END, '{} has left the chat'.format(self.addresses[client]))
                del self.clients[client]
                self.send_message(bytes('{} has left the chat'.format(name), 'utf8'))
                break


    def send_message(self,message,name=''):

        for client in self.clients:
            client.send(bytes(name, "utf8") + message)

    def quit_server(self):

        self.accepting_connection = False
        for client in self.clients:
            client.close()

        self.server.close()
        self.destroy()


if __name__ == '__main__':
    server_side = ServerWindow()

    thread = Thread(target=server_side.accept_connection,daemon=True)
    thread.start()
    server_side.mainloop()
    server_side.server.close()
