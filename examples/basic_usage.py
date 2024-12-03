from comsel.portSelect import select_com_port_and_baudrate

# Вызов функции выбора порта и скорости
port, baudrate = select_com_port_and_baudrate()

# Вывод результата
if port and baudrate:
    print(f"Выбран порт: {port}, скорость: {baudrate}")
else:
    print("Порт или скорость не были выбраны.")
