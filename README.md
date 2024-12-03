---

```markdown
# COM Port Selection Tool

This is a PyQt6-based GUI library for selecting COM ports and setting the baud rate. It is designed for ease of use
in Python projects that require serial communication. The library allows dynamic detection of available COM ports, error
handling for invalid input, and a clean modern interface.

![Screenshot](./docs/app_screenshot.png)

---

## Features

- **Dynamic COM Port Detection:** Automatically updates the list of available COM ports every second.
- **Custom Input:** Allows manual entry of COM port and baud rate.
- **Error Handling:** Validates user input for both COM port and baud rate.
- **Professional Interface:** Includes a white-blue modern design with an application icon.

---

## Requirements

- Python 3.9 or higher
- PyQt6
- pyserial

---

## Installation

Install the library directly from GitHub using `pip`:

```bash
pip install git+https://github.com/Molisc/ComSelectApp.git
```

Alternatively, you can add it to your `requirements.txt`:

```text
git+https://github.com/Molisc/ComSelectApp.git
```

---

## Usage

After installing, you can use the `PortSelectionWindow` class to integrate the COM Port Selection Tool into your Python application.

### Example 1: Basic Usage

This script demonstrates the simplest way to use the library. It selects a COM port and baud rate and prints the results to the console.

```python
from comsel.portSelect import PortSelectionWindow

port, baudrate = PortSelectionWindow.get_port_and_baudrate()
if port and baudrate:
    print(f"Selected COM port: {port}, Baud rate: {baudrate}")
else:
    print("No selection made.")
```

Run this script:

```bash
python basic_usage.py
```

---

### Example 2: GUI Output

This script displays the selected COM port and baud rate in a graphical message box.

```python
from PyQt6.QtWidgets import QApplication, QMessageBox
from comsel.portSelect import PortSelectionWindow
import sys

app = QApplication(sys.argv)

port, baudrate = PortSelectionWindow.get_port_and_baudrate()
if port and baudrate:
    QMessageBox.information(None, "Selection Complete", f"COM Port: {port}\nBaud Rate: {baudrate}")
else:
    QMessageBox.warning(None, "No Selection", "No COM port or baud rate was selected.")
```

Run this script:

```bash
python gui_output.py
```

---

### Example 3: Read Data from COM Port

This script connects to the selected COM port and continuously reads data, printing it to the console.

```python
import serial
from comsel.portSelect import PortSelectionWindow

def connect_and_read(port, baudrate):
    try:
        with serial.Serial(port, baudrate, timeout=1) as ser:
            print(f"Connected to {port} at {baudrate} baud.")

            while True:
                data = ser.readline().decode('utf-8').strip()
                if data:
                    print(f"Received: {data}")
    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nDisconnected from port.")

if __name__ == "__main__":
    port, baudrate = PortSelectionWindow.get_port_and_baudrate()
    if port and baudrate:
        connect_and_read(port, baudrate)
    else:
        print("No COM port or baud rate selected.")
```

Run this script:

```bash
python read_from_port.py
```

---

## File Structure

```
com-port-selection-tool/
├── comsel/
│   ├── __init__.py
│   ├── portSelect.py           # Main library file
│   └── icons/
│       └── icon.ico            # Application icon
├── docs/
│   └── app_screenshot.png      # Screenshot of the application
├── examples/
│   ├── basic_usage.py          # Example 1: Basic usage
│   ├── gui_output.py           # Example 2: GUI output
│   └── read_from_port.py       # Example 3: Reading data from COM port
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
├── setup.py                    # Installation script
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing

Feel free to submit issues or pull requests if you find any bugs or want to add features.
```

---

### Основные изменения:
1. **Упрощена установка**: Описана установка через `pip` и GitHub.
2. **Актуализированы пути импортов**: Используется `comsel.portSelect` для импорта.
3. **Примеры адаптированы**: Подчёркнута возможность интеграции библиотеки в Python-проекты.

Этот `README.md` подходит для использования вашей библиотеки через `pip install` из GitHub.