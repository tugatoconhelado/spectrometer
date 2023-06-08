import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton


class DataClass:
    def __init__(self):
        self.data = "Initial Value"
        self.observers = []

    def set_data(self, new_data):
        self.data = new_data
        self.notify_observers()

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.data)


class GUI(QWidget):
    def __init__(self, data_class):
        super().__init__()
        self.data_class = data_class
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Data GUI")
        layout = QVBoxLayout()

        self.label = QLabel("Data: " + self.data_class.data)
        layout.addWidget(self.label)

        button = QPushButton("Change Data")
        button.clicked.connect(self.change_data)
        layout.addWidget(button)

        self.setLayout(layout)
        self.show()

    def update(self, new_data):
        self.label.setText("Data: " + new_data)

    def change_data(self):
        new_data = "New Value"
        self.data_class.set_data(new_data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    data = DataClass()

    # Create GUI and register data class as an observer
    gui = GUI(data)
    data.register_observer(gui)

    sys.exit(app.exec())
