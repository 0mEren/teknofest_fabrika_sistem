import tkinter as tk
import time
import serial
import serial.tools.list_ports
import threading
import queue
import json

SERIAL_CONNECTION = None
json_yolu = "/home/modus/fabrika_ws/gorev2_arayuz_step/konumlar.json"


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MOTOR KONTROL ARAYUZU")
        
        self.motorkonumu = 0
        self.motordurumu_var = tk.StringVar(value=f"MOTOR DURUMU: DURUYOR")
        self.motor_konum_var = tk.StringVar(value=f"MOTOR KONUMU: 0.0")
        self.veri_sirasi = queue.Queue()
        self.dur_event = threading.Event()
        self.baslangic = 0
        self.hedef = 0
        self.json_yukle()
        self.setup_butonlar()

        self.sira_kontrol()

        self.root.protocol("WM_DELETE_WINDOW", self.kapat)

    def setup_butonlar(self):
        

        motor_durumu = tk.Label(self.root, textvariable=self.motordurumu_var)
        motor_konumu = tk.Label(self.root, textvariable=self.motor_konum_var)



        buton_bas_kaydet = tk.Button(self.root, text = "BAŞLANGICI KAYDET", activebackground="blue", activeforeground="white", command=lambda: self.json_kaydet(0))

        buton_basla = tk.Button(self.root, text = "BAŞLA", activebackground="blue", activeforeground="white", command=lambda: self.serial_yolla("BASLA"))

        buton_dur = tk.Button(self.root, text = "DUR", activebackground="blue", activeforeground="white", command=lambda: self.serial_yolla("DUR"))
  
        buton_konumu_kaydet = tk.Button(self.root, text = "KONUMU KAYDET", activebackground="blue", activeforeground="white", command=lambda: self.json_kaydet(1))
  
        buton_bas_git = tk.Button(self.root, text = "BAŞLANGICA GİT", activebackground="blue", activeforeground="white", command=lambda: self.serial_yolla("GIT " + str(self.baslangic)))

        buton_kayitli_git = tk.Button(self.root, text = "KAYITLI KONUMA GİT", activebackground="blue", activeforeground="white", command=lambda: self.serial_yolla("GIT " + str(self.hedef)))





        motor_durumu.grid(row = 4, column = 0)
        motor_konumu.grid(row = 4, column = 2)
        buton_bas_kaydet.grid(row=0, column = 0, )
        buton_basla.grid(row=0, column = 1, )
        buton_dur.grid(row=0, column = 2, )
        buton_konumu_kaydet.grid(row=1, column = 0, )
        buton_bas_git.grid(row=1, column = 1, )
        buton_kayitli_git.grid(row=1, column = 2, )

    def json_kaydet(self, mode):
        
        if mode:
            try:
                with open(json_yolu, "r", encoding="utf-8") as dosya:
                    veri = json.load(dosya)
                veri["kayitli"] = self.motorkonumu
                self.hedef = self.motorkonumu
            except:
                veri = {"baslangic": 0, "kayitli": 0}
            with open(json_yolu, "w", encoding="utf-8") as dosya:
                json.dump(veri, dosya, indent = 4)
            
        else:
            try:
                with open(json_yolu, "r", encoding="utf-8") as dosya:
                    veri = json.load(dosya)
                veri["baslangic"] = self.motorkonumu
                self.baslangic = self.motorkonumu
            except:
                veri = {"baslangic": 0, "kayitli": 0}
            with open(json_yolu, "w", encoding="utf-8") as dosya:
                json.dump(veri, dosya, indent = 4)
            self.serial_yolla("KONUM " + str(self.motorkonumu))

    def json_yukle(self):
        try:
            with open(json_yolu, "r", encoding="utf-8") as dosya:
                veri = json.load(dosya)
            self.hedef = veri["kayitli"]
            self.baslangic = veri["baslangic"]
        except:
            self.baslangic = 0
            self.hedef = 0
    def serial_baslat(self):
        if SERIAL_CONNECTION and SERIAL_CONNECTION.is_open:
            self.thread = threading.Thread(
                target=self.serial_yakala,
                daemon=True
            )
            self.thread.start()

    def serial_yolla(self, mesaj):
        if SERIAL_CONNECTION and SERIAL_CONNECTION.is_open:
            try:
                SERIAL_CONNECTION.write((mesaj + "\n").encode('utf-8'))
            except Exception as e:
                print(f"{e}")


    def sira_kontrol(self):
        while not self.veri_sirasi.empty():
            durum,konum = self.veri_sirasi.get_nowait()
            if durum != None:
                self.motordurumu_var.set(f"MOTOR DURUMU: {durum}")
            if konum != None:
                self.motor_konum_var.set(f"MOTOR KONUMU: {konum}")
                self.motorkonumu = int(konum)

        self.root.after(50, self.sira_kontrol)

    
    def serial_yakala(self):
        while not self.dur_event.is_set():
            if SERIAL_CONNECTION and SERIAL_CONNECTION.in_waiting > 0:
                try:
                    seri = SERIAL_CONNECTION.readline()
                    veri = seri.decode('utf-8', errors='ignore').strip()

                    if not veri:
                        continue

                    konum_str = ""
                    durum_str = "DURUYOR"

                    konum_idx = veri.find("KONUM")
                    durum_idx = veri.find("DURUM")

                    if konum_idx != -1:
                        try:
                            konum_str = veri.split(":", 1)[1].strip()
                        except IndexError:
                            pass
                    elif konum_idx == -1:
                        konum_str = None
                    if durum_idx != -1:
                        sub = veri[durum_idx + 5:]
                        if "A" in sub:
                            durum_str = "AKTIF"
                    elif durum_idx == -1:
                        durum_str = None

                    if konum_str or durum_idx != -1:
                        self.veri_sirasi.put((durum_str, konum_str))

                except Exception as e:
                    print(f"{e}")
            time.sleep(0.01)
        
        
    def kapat(self):
        self.dur_event.set()
        if SERIAL_CONNECTION and SERIAL_CONNECTION.is_open:
            SERIAL_CONNECTION.close()
        self.root.destroy()

    def run_loop(self):
        self.serial_baslat()
        self.root.mainloop()





def arduino_ara():
    
    ports = serial.tools.list_ports.comports()

    for port in ports:
        if "Arduino" in port.description or "ttyACM" in port.device or "ttyUSB" in port.device:
            return port.device

    return None






def program():
    global SERIAL_CONNECTION
    cihaz = arduino_ara()
    if cihaz:
        try:
            SERIAL_CONNECTION = serial.Serial(cihaz, baudrate = 115200, timeout=1)
            time.sleep(2)
        except serial.SerialException as e:
            print(f"{e}")
    
    app = App()
    app.run_loop()



if __name__ == '__main__':
    program()





