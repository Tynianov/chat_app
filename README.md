# Chat application
### Simple chat application (socket + tkinter)

Program consists of 2 files:
- server.py
- client.py

For building application TCP sockets have been used.

## Server
After server has been started, ***accept_connection*** method continuously listens to connections. 
When user connected to server, program store some of users's data such as nickname and IP address in dictionaries and starts new thread for this user.
***handle_client_connection*** is a target function for thread. When thread is created, ***handle_client_connection***  starts executing.
Function sends welcoming message to client. When client sends message, method receives it and call ***send_message*** function to brodcast message to other users. 

## Client
After running *client.py* file, user will see window with 3 inputs fields, for IP address, port and username respectively. User need to fill all fileds and press the button to connect to the server. When connection is successfully established, ***receive_message*** starts waiting for incomming messages. If messages was received, it will be shown in the listbox.
To send message client need to enter some text into message field at the bottom of the window and press *Send* button. ***Send message*** method will send it to server.
When it's time to close connection, user can press red button and leave the chat. ***close_connection*** function will be called.

GUI created with help of tkinter library.  

## To start the chat:

1) Run server.py on your computer. You will see following window.

![](images/server.png)


2) Run client.py


3) Enter IP address, port and username as shown below.

![](images/client.png)



4) Now you see welcoming message

![](images/welcome.png)


5) Run client.py on another PC and try to send message.
