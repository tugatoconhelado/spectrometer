import sys
import os
from datetime import datetime
import numpy as np
import pyqtgraph as pg
import pandas as pd
import pyqtgraph.exporters
from spectrometerui import Ui_spectrometer_widget
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog)

# Cargamos el formulario usando uic
#window_name, base_class = uic.loadUiType("spectrometer.ui")


class UiSpectrometer(QWidget, Ui_spectrometer_widget):

    read_continuously_signal = pyqtSignal(int)
    integration_time_signal = pyqtSignal(int)
    scans_average_signal = pyqtSignal(int)

    def __init__(self, options=None):

        super().__init__()

        self.current_file = None
        self.x_counts = list()
        self.y_counts = list()
        print(self.current_file)

        if options is None:
            options = {
                    'foreground': 'black',
                    'background': 'transparent'
                    }

        pg.setConfigOptions(**options)
        self.init_gui(self)

    def init_gui(self, mainWindow):

        print('Loading Ui')
        super().setupUi(mainWindow)
        self.setLayout(self.main_layout)
        self.configure_plots()

        self.read_continuously_button.clicked.connect(
                lambda x: self.read_continuously_signal.emit(
                    int(self.read_continously_edit.text())
                    )
                )

        self.integration_time_edit.editingFinished.connect(
                self.update_integration_time
                )
        self.scans_average_edit.editingFinished.connect(
                self.update_scans_average
                )
        self.save_button.clicked.connect(self.save)
        self.load_button.clicked.connect(self.load)
        self.previous_button.clicked.connect(self.load_iterate)
        self.filter_checkbox.stateChanged.connect(self.update_filter_range)

        path = os.path.join(os.getcwd(), 'data')
        if (os.path.exists('data')) and (
                any(os.path.splitext(f)[1] == '.csv' for f in os.listdir(path))
                ):
            self.current_file = os.path.join(path, os.listdir(path)[-1])
        print(self.current_file, type(self.current_file))
        print(path)

    def configure_plots(self):

        self.current_spectrum_plot.setLabel('left', 'Intensity (counts)')
        self.current_spectrum_plot.setLabel('bottom', 'Wavelength (nm)')
        self.average_spectrum_plot.setLabel('left', 'Intensity (counts)')
        self.average_spectrum_plot.setLabel('bottom', 'Wavelength (nm)')


    def save(self):

        if not os.path.exists('data'):
            print('creating data folder')
            os.mkdir('data')
            os.mkdir(os.path.join('data', 'png'))

        filename = 'SPR' + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        exporter = pg.exporters.ImageExporter(self.current_spectrum_plot.scene())
        csv_exporter = pg.exporters.CSVExporter(self.current_spectrum_plot.plotItem)
        savepath = os.path.join('data', filename)
        csv_exporter.export(savepath + '.csv')
        savepath = os.path.join('data', 'png', filename)
        exporter.export(savepath + '.png')

    def load(self):

        dialog = QFileDialog(self)
        dialog.setDirectory(os.getcwd())
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter('CSV Files (*.csv)')
        dialog.setViewMode(QFileDialog.ViewMode.Detail)
        if dialog.exec_():
            filename = dialog.selectedFiles()[0]
            print(filename)
            self.current_file = filename
            data = pd.read_csv(filename, delimiter=',')
            wavelength = data['x0000']
            spectrum = data['y0000']
            self.update_current_spectrum_plot((wavelength, spectrum))

    def load_iterate(self, position=1):

        position = -1
        directory = os.path.join(os.getcwd(), 'data')
        files = [os.path.join(directory, file) for file in os.listdir(directory)]
        if self.current_file in files:
            new_file = files.index(self.current_file) + position
            print(new_file)
            new_file = files[new_file]
            print(new_file)

    def update_filter_range(self):

        if self.filter_checkbox.isChecked():
            self.current_spectrum_plot.setRange(
                    xRange=[
                        float(self.filter_lower_limit_edit.text()),
                        float(self.filter_upper_limit_edit.text())
                        ]
                    )
        elif not self.filter_checkbox.isChecked():
            self.current_spectrum_plot.setRange(
                    xRange=[np.min(wavelength), np.max(wavelength)]
                    )



    def enable_gui(self, status):

        response = { # Just for display
            True: 'Enabling',
            False: 'Disabling'
        }
        print(f'Spectrometer status: {status}. {response[status]} Gui')
        self.integration_time_edit.setEnabled(status)
        self.scans_average_edit.setEnabled(status)
        self.filter_checkbox.setEnabled(status)
        self.filter_lower_limit_edit.setEnabled(status)
        self.filter_upper_limit_edit.setEnabled(status)
        self.electrical_dark_checkbox.setEnabled(status)
        self.substract_background_checkbox.setEnabled(status)
        self.single_spectrum_button.setEnabled(status)
        self.read_continuously_button.setEnabled(status)
        self.read_continously_edit.setEnabled(status)
        self.store_background_button.setEnabled(status)
        self.load_background_button.setEnabled(status)
        self.save_button.setEnabled(status)
        status_label = {
            True: 'connected',
            False: 'not connected'
        }

        self.initialise_label.setText(f'Status: {status_label[status]}')

    def update_integration_time(self):
        current_text = self.integration_time_edit.text()
        if current_text.isnumeric():
            current_text = int(current_text)
            self.integration_time_signal.emit(int(current_text))
        else:
            print('Integration time must be an integer')
            self.integration_time_edit.setText('100')

    def update_scans_average(self):
        current_text = self.scans_average_edit.text()
        if current_text.isnumeric():
            current_text = int(current_text)
            if current_text > 0:
                self.scans_average_signal.emit(int(current_text))
        else:
            print('Scans average must be an integer')
            self.scans_average_edit.setText('1')

    def update_spectrometer_counts_plot(self, data):

        self.y_counts.append(data)
        self.x_counts.append(self.y_counts.index(data))
        self.spectrometer_counts_plot.clear()
        self.spectrometer_counts_plot.plot(self.x_counts, self.y_counts, pen='b')

    def update_current_spectrum_plot(self, data):

        wavelength = data[0]
        spectrum = data[1]

        self.current_spectrum_plot.clear()
        self.current_spectrum_plot.plot(wavelength, spectrum, pen='blue')

    def update_average_spectrum_plot(self, data):

        wavelength = data[0]
        average = data[-1]

        self.average_spectrum_plot.clear()
        self.average_spectrum_plot.plot(wavelength, average, pen='blue')





if __name__ == '__main__':
    app = QApplication([])
    form = UiSpectrometer()
    form.show()
    sys.exit(app.exec_())
