import datetime
import serial
import socket
import struct
import threading
import time
import tkinter
import tkinter.scrolledtext

mcast_dir = '224.0.0.0'
puerto = 6000

arduino = serial.Serial('COM4',9600,timeout = 3)
limite = 30.0
time.sleep(5)

enlace = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
time2live = struct.pack('b',1)
enlace.setsockopt(socket.IPPROTO_IP,socket.IP_MULTICAST_TTL,time2live)

def cambiar():
    global limite
    limite = float(cajaTexto.get())
    cajaTexto.delete(0,tkinter.END)
    todoTexto.config(state = 'normal')
    realTime = datetime.datetime.now()
    todoTexto.insert(tkinter.INSERT,realTime.strftime("%d-%m-%Y %H:%M:%S --> "),"CB")
    todoTexto.insert(tkinter.INSERT,"%05.2f °C" % limite,"CB")
    todoTexto.insert(tkinter.INSERT," ¡LIMITE!\n","CA")
    todoTexto.config(state = "disabled")

def limpio():
    todoTexto.config(state = "normal")
    todoTexto.delete("2.0",tkinter.END)
    todoTexto.insert(tkinter.INSERT,"\n\n")
    todoTexto.config(state = "disabled")

def sensar():
    while True:
        arduino.write(b'A')
        temperatura = arduino.readline(5)
        realTime = datetime.datetime.now()
        mensaje = realTime.strftime("%d-%m-%Y %H:%M:%S --> ") + temperatura.decode() + " °C"
        
        if float(temperatura.decode())>limite:
            todoTexto.config(state = "normal")
            todoTexto.insert(tkinter.INSERT,mensaje,"CB")
            todoTexto.insert(tkinter.INSERT," ¡ALERTA!\n","CR")
            todoTexto.config(state = "disabled")
            enlace.sendto(mensaje.encode(),(mcast_dir,puerto))
        else:
            realTime = datetime.datetime.now()
            todoTexto.config(state = "normal")
            todoTexto.insert(tkinter.INSERT,(mensaje + "\n"),"CB")
            todoTexto.config(state = "disabled")
        
        time.sleep(10)

mainW = tkinter.Tk()
mainW.configure(background = "purple")
mainW.title("Interfaz-Servidor (TCP)")
mainW.geometry("400x287")

todoTexto = tkinter.scrolledtext.ScrolledText(mainW,height = 15,state = "normal",width = 46)
todoTexto.insert(tkinter.INSERT,"WORKING...\n\n")
realTime = datetime.datetime.now()
todoTexto.insert(tkinter.INSERT,realTime.strftime("%d-%m-%Y %H:%M:%S --> "),"CB")
todoTexto.insert(tkinter.INSERT,"%05.2f °C" % limite,"CB")
todoTexto.insert(tkinter.INSERT," ¡LIMITE!\n","CA")
todoTexto.config(state = "disabled")
todoTexto.place(x = 5,y = 5)
todoTexto.tag_config("CB",foreground = 'black')
todoTexto.tag_config("CA",foreground = 'blue')
todoTexto.tag_config("CR",foreground = 'red')

cajaTexto = tkinter.Entry(mainW,width = 39)
cajaTexto.place(x = 5,y = 260)

boton1 = tkinter.Button(mainW,command = cambiar,text = "SET",width = 8)
boton1.place(x = 327,y = 256)

boton2 = tkinter.Button(mainW,command = limpio,text = "CLEAR",width = 8)
boton2.place(x = 255,y = 256)

t = threading.Thread(target = sensar)
t.start()
mainW.mainloop()