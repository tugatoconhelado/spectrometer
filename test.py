import sys
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton


class WorkerThread(QThread):
    signal_received = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()

    def run(self):
        # Wait for the signal to be emitted
        self.signal_received.wait()

        # Perform the action
        self.print_numbers()

    def print_numbers(self):
        print("Printing numbers...")
        num1, num2 = self.signal_received.mapped()
        print(f"Number 1: {num1}")
        print(f"Number 2: {num2}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.worker_thread = WorkerThread()
        self.worker_thread.signal_received.connect(self.on_signal_received)

        self.button = QPushButton("Send Signal", self)
        self.button.clicked.connect(self.send_signal)

    def on_signal_received(self, num1, num2):
        print("Signal received in main window!")
        print(f"Received numbers: {num1}, {num2}")

    def send_signal(self):
        num1 = 10
        num2 = 20
        self.worker_thread.signal_received.emit(num1, num2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())