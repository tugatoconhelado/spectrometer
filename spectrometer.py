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
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog)

# Cargamos el formulario usando uic
#window_name, base_class = uic.loadUiType("spectrometer.ui")


class ViewSpectrometer(QWidget, Ui_spectrometer_widget):

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

        #pg.setConfigOptions(**options)
        self.init_gui(self)

    def init_gui(self, mainWindow):
        """
        Initializes the gui of the widget.

        It calls on the setupUI from the .ui or .py file containing the GUI.
        Calls the configure_plots method to setup axis labels on the plots.
        Sets validators on the Line Edits corresponding to integration time and
        number of scans to average.
        Connects button clicked events to their respective functions.
        """

        print('Loading Ui')
        super().setupUi(mainWindow)
        self.setLayout(self.main_layout)
        self.configure_plots()

        # Set validator to only accept positive integers
        validator = QIntValidator(bottom=0)
        self.integration_time_edit.setValidator(validator)
        self.scans_average_edit.setValidator(validator)

        # Connect Button clicked events with slots
        self.read_continuously_button.clicked.connect(
                lambda x: self.read_continuously_signal.emit(
                    int(self.read_continously_edit.text())
                    )
                )
        self.save_button.clicked.connect(self.save)
        self.load_button.clicked.connect(self.load)
        self.previous_button.clicked.connect(self.load_iterate)
        self.filter_checkbox.stateChanged.connect(self.update_filter_range)

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

    def update_filter_range(self):
        """
        Updates the filter range.

        It sets the range of the currently displayed data in both the current
        spectrum plot and the average spectrum plot.
        If the filter box is unchecked it returns the plot to their normal range
        """

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
        """
        Enables components from the gui in the event of spectrometer
        intialisation.

        The components being activated when the spectrometer gets online are:
            - integration_time_edit : QLineEdit
            - scans_average_edit : QLineEdit
            - filter_checkbox : QCheckBox
            - filter_lower_limit_edit : QLineEdit
            - filter_upper_limit_edit : QLineEdit
            - electrical_dark_checkbox : QCheckBox
            - substract_background_checkbox: QCheckBox
            - single_spectrum_button : QPushButton
            - read_continuously_button : QPushButton
            - store_background_button : QPushButton
            - load_background_button : QPushButton
            - save_button : QPushButton
        """

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






if __name__ == '__main__':
    app = QApplication([])
    form = ViewSpectrometer()
    form.show()
    sys.exit(app.exec_())
