import os
import sys
import numpy as np
from time import sleep
from PyQt5 import QtTest
from PyQt5.QtCore import (QObject, pyqtSignal, QTimer)
from seatease.spectrometers import Spectrometer


class SpectrumAcquiring(QObject):
    """
    Reads the spectrum from the spectrometer object

    It reads continously. This means that when the signals is to be averaged,
    it emits signals for every measurement performed in order to average

    Parameters
    ----------
    spectrometer : Spectrometer
        The Spectrometer object from which to read the data.
    integration_time: int
        Integration time of the measurement.
    scans_average : int
        Number of scans to be averaged.
    """

    initialise_status_signal = pyqtSignal(bool)

    def __init__(self, model, spectrometer=None):

        super().__init__()

        self.model = model
        self.spectrometer = spectrometer
        self.electrical_dark = False
        self.substract_background = False
        self.length = 10
        self.current_index = 0
        self.counts_time = np.array([])
        self.counts = np.array([])

        # Timer to perform the measurements
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.get_spectrum)

    def start_acquisition(self):

        # Query measurement info
        self.integration_time = self.model.integration_time
        self.scans_average = self.model.scans_average
        self.electrical_dark = self.model.electrical_dark

        self.timer.setInterval(self.integration_time)
        print(f'Reading Spectrum')
        print(f'Parameters')
        print(f'----------')
        print(f'Integration time: {self.integration_time}')
        print(f'Scans to average: {self.scans_average}')
        print(f'Electrical dark: {self.electrical_dark}')
        self.timer.start()

    def get_spectrum(self):

        spectra = np.zeros((self.scans_average, self.length)) # Stores measurements
        i = self.current_index
        print(f'Computing spectrum {i}')
        current_spectrum = self.spectrometer.intensities(
                self.electrical_dark
                )
        spectra[i, :] = current_spectrum
        self.model.spectrum = (self.wavelength, current_spectrum)
        self.model.averaged_spectrum = (
                self.wavelength, np.sum(spectra, axis=0) / (i + 1)
                )
        self.counts_time = np.append(self.counts_time, i * self.integration_time)
        self.counts = np.append(self.counts, np.sum(current_spectrum))
        self.model.spectrum_counts = (
                self.counts_time / 1000,
                self.counts
                )
        if self.current_index >= self.scans_average - 1:
            # -1 because we count from 0
            self.stop_acquisition()
        else:
            self.current_index += 1

    def stop_acquisition(self):

        if self.timer.isActive():
            self.timer.stop()
        self.current_index = 0
        self.counts_time = np.array([])
        self.counts = np.array([])

    def initialise(self):

        print('Loading Spectrometer')
        try:
            self.spectrometer = Spectrometer.from_first_available()
            self.wavelength = self.spectrometer.wavelengths()
            self.length = len(self.wavelength)
            self.model.initialise_status_signal.emit(True)
        except:
            print('Loading Spectrometer failed')
            self.model.initialise_status_signal.emit(False)

class DataCheckerSpectrometer(QObject):


    def __init__(self, model):

        super().__init__()

        self.model = model
        self.acquirer = SpectrumAcquiring(self.model)
        self.integration_time_limits = (10, 1000)

    def initialise_spectrometer(self):

        print('Loading Spectrometer')
        try:
            self.spectrometer = Spectrometer.from_first_available()
            self.wavelength = self.spectrometer.wavelengths()
            self.length = len(self.wavelength)
            self.model.initialise_status_signal.emit(True)
            limits = self.spectrometer.integration_time_micros_limits
            ms_limits = (limits[0] / 1000, limits[1] / 1000) # Convert to ms
            self.integration_time_limits = ms_limits
            self.acquirer.spectrometer = self.spectrometer
            self.acquirer.length = len(self.wavelength)
            self.acquirer.wavelength = self.wavelength
            print(self.integration_time_limits)
        except:
            print('Loading Spectrometer failed')
            self.model.initialise_status_signal.emit(False)

    def check_electrical_dark(self):

        electrical_dark_checkbox = self.sender()
        self.model.electrical_dark = electrical_dark_checkbox.checkState()

    def check_integration_time(self):

        integration_time_edit = self.sender()
        current_text = int(integration_time_edit.text())
        if (current_text >= self.integration_time_limits[0]) and \
        (current_text <= self.integration_time_limits[1]):
            print(f'Setting integration time to {current_text}')
            self.model.integration_time = current_text
            # Integration time must be in us
            self.spectrometer.integration_time_micros(current_text * 1000)
        else:
            print(f'Integration time out of \
            bonds {self.integration_time_limits}')
            self.model.integration_time = 100
            self.spectrometer.integration_time_micros(100 * 1000)

    def check_scans_average(self):

        scans_average_edit = self.sender()
        current_text = scans_average_edit.text()
        if current_text.isnumeric():
            print('Updating scans average')
            current_text = int(current_text)
            self.model.scans_average = current_text

class UpdaterSpectrometer:

    def __init__(self, view=None):

        self.view = view

    def update_integration_time(self, new_time):

        self.view.integration_time_edit.setText(str(new_time))

    def update_scans_average(self, new_scans):

        self.view.scans_average_edit.setText(str(new_scans))

    def update_spectrometer_counts_plot(self, data):

        time = data[0]
        counts = data[1]

        self.view.spectrometer_counts_plot.clear()
        self.view.spectrometer_counts_plot.plot(time, counts, pen='b')

    def update_current_spectrum_plot(self, data):

        wavelength = data[0]
        spectrum = data[1]

        self.view.current_spectrum_plot.clear()
        self.view.current_spectrum_plot.plot(wavelength, spectrum, pen='blue')

    def update_average_spectrum_plot(self, data):

        wavelength = data[0]
        average = data[-1]

        self.view.average_spectrum_plot.clear()
        self.view.average_spectrum_plot.plot(wavelength, average, pen='blue')


if __name__ == '__main__':

    pass
