import tkinter as tk
from tkinter import messagebox
import serial
import serial.tools.list_ports
import threading
import time

class WeightApp:
    def __init__(self, master):
        self.master = master
        master.title("Весовой Терминал")
        master.geometry("400x250")

        self.label_title = tk.Label(master, text="Текущий вес:", font=("Arial", 14))
        self.label_title.pack(pady=10)

        # Поле для вывода веса
        self.weight_var = tk.StringVar(value="0.00")
        self.label_weight = tk.Label(master, textvariable=self.weight_var, font=("Arial", 40, "bold"), fg="green")
        self.label_weight.pack(pady=10)

        self.status_var = tk.StringVar(value="Поиск весов...")
        self.label_status = tk.Label(master, textvariable=self.status_var, font=("Arial", 10), fg="gray")
        self.label_status.pack(side="bottom", fill="x")

        self.running = True
        self.thread = threading.Thread(target=self.read_serial, daemon=True)
        self.thread.start()

    def find_port(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            # На Mac порты выглядят как /dev/cu.usb..., на Windows как COM...
            for baud in [1200, 9600]:
                try:
                    with serial.Serial(p.device, baud, timeout=0.5) as ser:
                        time.sleep(0.5)
                        if ser.in_waiting > 0:
                            return p.device, baud
                except:
                    continue
        return None, None

    def read_serial(self):
        while self.running:
            port, baud = self.find_port()
            if port:
                self.status_var.set(f"Подключено: {port} ({baud} bps)")
                try:
                    with serial.Serial(port, baud, timeout=1) as ser:
                        while self.running:
                            if ser.in_waiting > 0:
                                line = ser.readline().decode('ascii', errors='ignore').strip()
                                if line:
                                    # Очищаем строку от лишних символов
                                    clean_weight = "".join(c for c in line if c.isdigit() or c in ".-")
                                    self.weight_var.set(clean_weight)
                            time.sleep(0.1)
                except:
                    self.status_var.set("Связь потеряна. Переподключение...")
            else:
                self.status_var.set("Весы не найдены. Проверьте кабель.")
            time.sleep(2)

if __name__ == "__main__":
    root = tk.Tk()
    app = WeightApp(root)
    root.mainloop()
