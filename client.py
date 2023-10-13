import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import socket
import threading
import pyaudio
import ssl

class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s = ssl.wrap_socket(self.s,
                                 certfile='ssl_certs_keys/client1_certificate.pem',
                                 keyfile='ssl_certs_keys/client1_key.pem')
        
        while 1:
            try:
                self.target_ip = '10.30.203.243'
                self.target_port = 9060
                self.s.connect((self.target_ip, self.target_port))
                break
            except:
                print("Couldn't connect to server")

        chunk_size = 1024 # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000
        self.kstop = threading.Event()

        # initialise microphone recording
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
        
        print("Connected to Server")

        # start threads
        receive_thread = threading.Thread(target=self.receive_server_data)
        receive_thread.daemon = True
        receive_thread.start()
        
        send_thread = threading.Thread(target=self.send_data_to_server)
        send_thread.daemon = True
        send_thread.start()

    def stop(self):
        self.kstop.set()

    def receive_server_data(self):
        while not self.kstop.is_set():
            try:
                data = self.s.recv(1024)
                self.playing_stream.write(data)
            except:
                pass


    def send_data_to_server(self):
        while not self.kstop.is_set():
            try:
                data = self.recording_stream.read(1024)
                self.s.sendall(data)
            except:
                pass

class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('300x200')
        self.title('Caller Window')
        self.configure(bg='#cddfff')

        style = ttk.Style()
        style.theme_use('default')
        style.configure('Sbutton.TButton', font=('Times', 18),foreground='black', background='#1CBF2F', borderwidth=3, bordercolor='black')
        style.configure('Cbutton.TButton', font=('Times', 18),foreground='black', background='#F70A32', borderwidth=3, bordercolor='black')
        style.map('Sbutton.TButton', background=[('active', 'black')],foreground=[('active', '#1CBF2F')])
        style.map('Cbutton.TButton', background=[('active', 'black')],foreground=[('active', '#F70A32')])
        ttk.Button(self,text='Talk',command = self.fnc, style='Sbutton.TButton').pack(expand=True)
        ttk.Button(self,text='Close',command = self.dest, style='Cbutton.TButton').pack(expand=True)
        self.talk = 0

    def fnc(self):
        if self.talk == 0:
            self.client = Client()
            self.talk = 1

    def dest(self):
        try:
            self.talk = 0
            self.client.stop()
            self.destroy()
        except:
            self.destroy()


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('600x600')
        self.title('Voice Over Internet Protocol')
        self.configure(bg='#cddfff')

        #displaying the names
        ttk.Label(self, text = "Press 'Start App' to start the app", font=('Times', 18),background='#cddfff').pack(expand=True)
        ttk.Label(self, text = "Press 'Talk' in the new window to connect to server" ,font=('Times', 18),background='#cddfff').pack(expand=True)
        ttk.Label(self, text = "Press 'Close' in the new window to end call :" ,font=('Times', 18),background='#cddfff').pack(expand=True)
        ttk.Label(self, text = "Press 'Close App' to close the app :" ,font=('Times', 18),background='#cddfff').pack(expand=True)

        # place a button on the root window
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Sbutton.TButton', font=('Times', 18),foreground='black', background='#1CBF2F', borderwidth=3, bordercolor='black')
        style.configure('Cbutton.TButton', font=('Times', 18),foreground='black', background='#F70A32', borderwidth=3, bordercolor='black')
        style.map('Sbutton.TButton', background=[('active', 'black')],foreground=[('active', '#1CBF2F')])
        style.map('Cbutton.TButton', background=[('active', 'black')],foreground=[('active', '#F70A32')])
        ttk.Button(self,text='Start App',command=self.open_window, style='Sbutton.TButton',padding=(10,5)).pack(expand=True)
        # place a button on the root window
        ttk.Button(self,text='Close App',command=self.destroy, style='Cbutton.TButton',padding=(10,5)).pack(expand=True)

    def open_window(self):
        window = Window(self)
        window.grab_set()

if __name__ == "__main__":
    app = App()
    app.mainloop()