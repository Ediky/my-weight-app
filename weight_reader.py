import serial
import serial.tools.list_ports
import time
import logging

# Настройка записи в файл
logging.basicConfig(
    filename='weight_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def find_weight_port():
    """Ищет порт, который реально шлет данные"""
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        try:
            # Пробуем основные скорости: 1200 (для табло) и 9600 (стандарт)
            for baud in [1200, 9600]:
                with serial.Serial(p.device, baud, timeout=1) as ser:
                    time.sleep(1) # Ждем немного
                    if ser.in_waiting > 0:
                        return p.device, baud
        except:
            continue
    return None, None

def main():
    print("🔍 Ищу весы...")
    port, baud = find_weight_port()
    
    if not port:
        logging.error("Весы не найдены. Проверьте кабель.")
        return

    logging.info(f"Подключено к {port} на скорости {baud}")
    
    try:
        with serial.Serial(port, baud, timeout=1) as ser:
            while True:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('ascii', errors='ignore').strip()
                    if line:
                        logging.info(f"Вес: {line}")
                time.sleep(0.1)
    except KeyboardInterrupt:
        logging.info("Программа остановлена пользователем.")

if __name__ == "__main__":
    main()
