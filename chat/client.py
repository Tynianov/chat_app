from tkinter import *
from tkinter import messagebox
from socket import AF_INET,socket,SOCK_STREAM,gethostbyname,gethostname
from threading import Thread
import winsound
import re

CLASSIC_FONT = ("Arial", "10",'bold')

class ClientFrame(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.IP_ADDR = ''
        self.PORT = None
        self.username = ''
        self.BUFFER_SIZE = 2048
        self.client_side = socket(AF_INET,SOCK_STREAM)
        self.geometry('400x400')
        self.resizable(width=False, height=False)
        self.title('Client')
        self.iconbitmap('media/chat_icon.ico')

        self.init_first_frame()

    def init_first_frame(self):
        self.first_frame = Frame(self, width=400, height=400,bg='white')
        self.first_frame.grid(row=0, column=0)

        self.ip_label = Label(self.first_frame,text='Enter IP address:',font=CLASSIC_FONT,bg='white')
        self.ip_label.place(x=100,y=50)
        self.ip_filed = Entry(self.first_frame,width=29,highlightbackground='black',bd=2,font=CLASSIC_FONT)
        self.ip_filed.place(x=100,y=80)
        self.port_label = Label(self.first_frame,text='Enter port:',font=CLASSIC_FONT,bg='white')
        self.port_label.place(x=100,y=130)
        self.port_field = Entry(self.first_frame,width=29,highlightbackground='black',bd=2,font=CLASSIC_FONT)
        self.port_field.place(x=100,y=160)
        self.name_label = Label(self.first_frame,text='Enter username:',font=CLASSIC_FONT,bg='white')
        self.name_label.place(x=100,y=220)
        self.name_filed = Entry(self.first_frame,width=29,highlightbackground='black',bd=2,font=CLASSIC_FONT)
        self.name_filed.place(x=100,y=240)
        self.join_chat_button = Button(self.first_frame,text='Join chat',width=13,height=2,highlightbackground='black',bd=2,relief=GROOVE,
                                       bg='white',font=CLASSIC_FONT)
        self.join_chat_button.place(x=150,y=320)
        self.join_chat_button.bind('<Button-1>',self.connect_to_server)

    def init_second_frame(self):
        self.second_frame = Frame(self, width=400, height=400,bg='white')

        self.message_list = Listbox(self.second_frame,width=60,height=19)
        self.message_list.place(x=15,y=10)
        self.message_scrollbar = Scrollbar(orient=VERTICAL,command=self.message_list.yview)
        self.message_scrollbar.place(x=380,y=10, height=300)
        self.enter_field = Entry(self.second_frame,width=60)
        self.enter_field.place(x=15,y=330)
        self.send_button = Button(self.second_frame,text='Send',width=9,height=1,bg='#5b92ea')
        self.send_button.place(x=305,y=360)
        self.send_button.bind('<Button-1>',self.send_message)
        self.close_connection_button = Button(self.second_frame,text=u'\u2715',bg='#d13e43')
        self.close_connection_button.place(x=15,y=360)
        self.close_connection_button.bind('<Button-1>',self.close_connection)


    def connect_to_server(self,event):
        try:

            if self.check_input():
                self.init_second_frame()
                self.client_side.connect((self.IP_ADDR,self.PORT))
                self.client_side.send(bytes(self.username,'utf8'))
                self.second_frame.grid(row=0, column=0)
                self.first_frame.grid_forget()
            else:
                messagebox.showwarning('Wrong input', 'Enter valid data')

        except OSError:
            messagebox.showerror('Error','Error occurred while connecting to server!')

    def receive_message(self):
        while True:
            try:
                message = self.client_side.recv(self.BUFFER_SIZE).decode('utf8')

                self.message_list.insert(END,str(message))
                winsound.PlaySound('receive',winsound.SND_FILENAME)
            except OSError as e:
                pass

    def send_message(self,event):
        message = self.enter_field.get()
        self.client_side.send(bytes(message, 'utf8'))
        self.enter_field.delete(0,END)

    def close_connection(self,event):
        self.client_side.close()
        self.destroy()
        self.quit()

    def check_input(self):
        try:
            self.IP_ADDR = self.ip_filed.get()
            self.PORT = int(self.port_field.get())
            self.username = self.name_filed.get()

            valid_ip = re.findall('[0-9]+[.][0-9]+[.][0-9]+[.][0-9]+', self.IP_ADDR)

            if not valid_ip or not self.PORT:
               return False
            else:
                return True
        except ValueError:
            return False

client = ClientFrame()
thread = Thread(target=client.receive_message)
thread.start()
client.mainloop()