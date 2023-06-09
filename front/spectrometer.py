import sys
import os
from datetime import datetime
import numpy as np
import pyqtgraph as pg
import pandas as pd
import pyqtgraph.exporters
from spectrometerui import Ui_spectrometer_widget
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIntValidator, QPalette, QColor
from PySide6.QtWidgets import (QApplication, QWidget, QFileDialog)

# Cargamos el formulario usando uic
#window_name, base_class = uic.loadUiType("spectrometer.ui")


class ViewSpectrometer(QWidget, Ui_spectrometer_widget):

    read_continuously_signal = Signal(int)
    parameter_data_signal = Signal(int, int, bool)

    def __init__(self, options=None):

        super().__init__()

        self.current_file = None

        if options is None:
            options = {
                    'foreground': 'black',
                    'background': 'transparent'
                    }

        #pg.setConfigOptions(**options)
        self.init_gui()

    def init_gui(self):
        """
        Initializes the gui of the widget.

        It calls on the setupUI from the .ui or .py file containing the GUI.
        Calls the configure_plots method to setup axis labels on the plots.
        Sets validators on the Line Edits corresponding to integration time and
        number of scans to average.
        Connects button clicked events to their respective functions.
        """

        print('Loading Ui')
        self.setupUi(self)
        self.setLayout(self.main_layout)
        self.configure_plots()

        # Set validator to only accept positive integers
        validator = QIntValidator(bottom=0)
        self.integration_time_edit.setValidator(validator)
        self.scans_average_edit.setValidator(validator)

        # Connect Button clicked events with slots
        #self.read_continuously_button.clicked.connect(
        #        lambda x: self.read_continuously_signal.emit(
        #            int(self.read_continously_edit.text())
        #            )
        #        )
        self.save_button.clicked.connect(self.save)
        self.load_button.clicked.connect(self.load)
        self.previous_button.clicked.connect(self.load_iterate)

        # Get the last file created
        path = os.path.join(os.getcwd(), 'data')
        if (os.path.exists('data')) and (
                any(os.path.splitext(f)[1] == '.csv' for f in os.listdir(path))
                ):
            self.current_file = os.path.join(path, os.listdir(path)[-1])

    def configure_plots(self):
        """
        Setups the axis labels for each PlotWidget
        """

        self.current_spectrum_plot.setLabel('left', 'Intensity (counts)')
        self.current_spectrum_plot.setLabel('bottom', 'Wavelength (nm)')
        self.average_spectrum_plot.setLabel('left', 'Intensity (counts)')
        self.average_spectrum_plot.setLabel('bottom', 'Wavelength (nm)')
        self.spectrometer_counts_plot.setLabel(
                'left', 'Intensity (counts)'
                )
        self.spectrometer_counts_plot.setLabel(
                'bottom', 'Time (s)'
                )

        self.current_spectrum_dataline = self.current_spectrum_plot.plot([], [], pen='yellow')
        self.average_spectrum_dataline = self.average_spectrum_plot.plot([], [], pen='yellow')
        self.spectrometer_counts_dataline = self.spectrometer_counts_plot.plot([], [], pen='blue')

    def send_parameter_data(self):

        self.parameter_data_signal.emit(
            int(self.integration_time_edit.text()),
            int(self.scans_average_edit.text()),
            self.electrical_dark_checkbox.checkState()
        )

    def save(self, directory='data'):
        """
        Saves current data being displayed.
        Note: It won't save the entire data, only the portion the user is
        currently viewing.

        The data will be saved in the specified directory, if it does not exists
        it will create it. If no directory is provided it will be saved in the
        'data' directory. Only the data in the current spectrum plot (upper
        left plot in the displayed window) will be saved.

        Parameters
        ----------
            folder (str): Directory in which to save the data.

        Returns
        -------
            status (bool): Indicates if the save was succesful
        """


        if not os.path.exists(directory):
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
        return True

    def load(self, directory='data'):
        """
        Generates a File Dialog to select file to load.

        The loading with begin from the 'data' folder unless a different
        directory is given.
        Parameters
        ----------
            directory : str, optional
            Directory in which to start the File Dialog

        Returns
        -------
            status : bool
            Indicates if the load was succesful

        """

        dialog = QFileDialog(self)
        directory = os.path.join(os.getcwd(), directory)
        dialog.setDirectory(directory)
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
        """
        Loads a previous or next file with respect to the current file.

        It looks based on the value of position. The search is in the current
        save directory.

        Parameters
        ----------
        position : int, optional
            Indicates to move to next (position = 1) or previous file
            (position = -1). It can only take values 1 or -1.

        Returns
        -------
        status : bool
            Indicated wether the load was succesful or not.

        """

        if position == 1 or position == -1:
            directory = os.path.join(os.getcwd(), 'data')
            files = [os.path.join(directory, file) for file in os.listdir(directory)]
            if self.current_file in files:
                new_file = files.index(self.current_file) + position
                print(new_file)
                new_file = files[new_file]
                print(new_file)
        else:
            print('Load iteration value invalid (different from +-1)')
            return False







if __name__ == '__main__':

    app = QApplication(sys.argv)
    form = ViewSpectrometer()
    form.show()
    sys.exit(app.exec())
