import socket
import struct
import threading
import tkinter
import tkinter.scrolledtext

bind_addr = '0.0.0.0'
mcast_dir = '224.0.0.0'
puerto = 6000

enlace = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
member = socket.inet_aton(mcast_dir) + socket.inet_aton(bind_addr)
enlace.setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP,member)
enlace.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

enlace.bind((bind_addr,puerto))

def limpio():
    todoTexto.config(state = "normal")
    todoTexto.delete("2.0",tkinter.END)
    todoTexto.insert(tkinter.INSERT,"\n\n")
    todoTexto.config(state = "disabled")

def recibir():
    while True:
        mensaje = enlace.recvfrom(50)[0]
        todoTexto.config(state = "normal")
        todoTexto.insert(tkinter.INSERT,mensaje.decode(),"CB")
        todoTexto.insert(tkinter.INSERT," ¡ALERTA!\n","CR")
        todoTexto.config(state = "disabled")

mainW = tkinter.Tk()
mainW.configure(background = "blue")
mainW.title("RECEPTOR 1")
mainW.geometry("400x287")

todoTexto = tkinter.scrolledtext.ScrolledText(mainW,height = 15,state = "normal",width = 46)
todoTexto.insert(tkinter.INSERT,"WORKING...\n\n")
todoTexto.config(state = "disabled")
todoTexto.place(x = 5,y = 5)
todoTexto.tag_config("CB",foreground = 'black')
todoTexto.tag_config("CR",foreground = 'red')

boton2 = tkinter.Button(mainW,command = limpio,text = "CLEAR",width = 8)
boton2.place(x = 168,y = 256)

t = threading.Thread(target = recibir)
t.start()
mainW.mainloop()