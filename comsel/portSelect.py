from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIntValidator, QIcon
from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
)
import serial.tools.list_ports
import sys, re
from importlib.resources import files


class PortSelectionWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.selected_port = None
        self.selected_baudrate = None
        self.setWindowTitle("Выбор COM порта и скорости передачи данных")

        # Устанавливаем иконку окна
        icon_path = files("comsel.icons").joinpath("icon.ico")
        self.setWindowIcon(QIcon(str(icon_path)))

        # Применяем стиль
        self.setStyleSheet("""
            QDialog {
                background-color: #E6F7FF; /* Голубой фон */
            }
            QLabel {
                color: #003366; /* Темно-синий текст */
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit, QComboBox {
                background-color: #FFFFFF; /* Белый фон */
                color: #003366; /* Темно-синий текст */
                border: 1px solid #99CCFF; /* Голубая рамка */
                border-radius: 4px;
                padding: 4px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #99CCFF; /* Светло-голубой */
                color: #FFFFFF; /* Белый текст */
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #66B2FF; /* Темнее при наведении */
            }
            QPushButton:pressed {
                background-color: #3399FF; /* Еще темнее при нажатии */
            }
        """)

        # Настройка размеров окна
        self.setFixedSize(500, 300)

        # Основной вертикальный layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Горизонтальный layout для COM-порта и baudrate
        horizontal_layout = QHBoxLayout()

        # Выбор COM-порта
        port_layout = QVBoxLayout()
        port_label = QLabel("Список доступных COM портов:")
        self.ports_combo = QComboBox()
        self.populate_combo_box()

        self.port_input_label = QLabel("Или введите COM порт вручную:")
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Введите COM порт")

        port_layout.addWidget(port_label)
        port_layout.addWidget(self.ports_combo)
        port_layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        port_layout.addWidget(self.port_input_label)
        port_layout.addWidget(self.port_input)

        horizontal_layout.addLayout(port_layout)

        # Выбор Baudrate
        baudrate_layout = QVBoxLayout()
        baudrate_label = QLabel("Список доступных Baudrate:")
        self.baudrate_combo = QComboBox()
        self.populate_baudrate_combo()

        self.baudrate_input_label = QLabel("Или введите Baudrate вручную:")
        self.baudrate_input = QLineEdit()
        self.baudrate_input.setPlaceholderText("Введите Baudrate")
        self.baudrate_input.setValidator(QIntValidator(1, 1000000, self))

        baudrate_layout.addWidget(baudrate_label)
        baudrate_layout.addWidget(self.baudrate_combo)
        baudrate_layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        baudrate_layout.addWidget(self.baudrate_input_label)
        baudrate_layout.addWidget(self.baudrate_input)

        horizontal_layout.addLayout(baudrate_layout)

        # Добавляем горизонтальный layout в основной
        main_layout.addLayout(horizontal_layout)

        # Кнопка подтверждения
        self.confirm_button = QPushButton("&Подтвердить")
        self.confirm_button.clicked.connect(self.confirm_selection)
        main_layout.addWidget(self.confirm_button)

        # Таймер для обновления COM портов
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_com_ports)
        self.timer.start(1000)

    def populate_combo_box(self):
        ports = list(serial.tools.list_ports.comports())
        self.ports_combo.clear()
        if ports:
            for port in ports:
                self.ports_combo.addItem(port.device)
        else:
            self.ports_combo.addItem("Нет доступных COM портов")

    def update_com_ports(self):
        """Обновляет список COM портов."""
        current_ports = [self.ports_combo.itemText(i) for i in range(self.ports_combo.count())]
        new_ports = [port.device for port in serial.tools.list_ports.comports()]
        if current_ports != new_ports:
            self.populate_combo_box()

    def populate_baudrate_combo(self):
        default_baudrates = [115200, 9600, 19200, 38400, 57600, 250000]
        self.baudrate_combo.addItems(map(str, default_baudrates))
        self.baudrate_combo.setCurrentText("115200")

    def confirm_selection(self):
        selected_port = self.ports_combo.currentText()
        if self.port_input.text():
            selected_port = self.port_input.text()

        if not self.is_valid_port(selected_port):
            self.port_input_label.setText("Ошибка: Неверный формат COM порта")
            return

        selected_baudrate = self.baudrate_combo.currentText()
        if self.baudrate_input.text():
            selected_baudrate = self.baudrate_input.text()

        if not selected_baudrate.isdigit() or int(selected_baudrate) <= 0:
            self.baudrate_input_label.setText("Ошибка: Baudrate должен быть положительным числом")
            return

        self.selected_port = selected_port
        self.selected_baudrate = int(selected_baudrate)
        self.accept()

    def is_valid_port(self, port):
        pattern = r'^COM\d+$'
        return re.match(pattern, port) is not None

    def open_and_get_selection(self):
        """Открывает окно и возвращает результат."""
        if self.exec():
            return self.selected_port, self.selected_baudrate
        return None, None


# Пример использования
if __name__ == "__main__":
    app = QApplication(sys.argv)
    port_window = PortSelectionWindow()
    port, baudrate = port_window.open_and_get_selection()

    if port and baudrate:
        print(f"Выбран порт: {port}, скорость: {baudrate}")
    else:
        print("Порт или скорость не были выбраны.")
