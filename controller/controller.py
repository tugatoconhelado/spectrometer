import os
import sys
import numpy as np
from time import sleep
from PyQt5 import QtTest
from PyQt5.QtCore import (QObject, pyqtSignal, QTimer)
from seabreeze.spectrometers import Spectrometer


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

    def __init__(self, checker):

        super().__init__()

        self.checker = checker
        self.current_index = 0
        self.current_time = 0
        self.counts_time = np.array([])
        self.counts = np.array([])
        self.current_average = np.array([])



        # Timer to perform the measurements
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.get_spectrum)

    def start_acquisition(self):

        self.timer.setInterval(self.checker.model.integration_time)
        self.current_average = np.zeros(self.checker.length)
        print(f'Reading Spectrum')
        print(f'Current Parameters')
        print(f'------------------')
        print(f'Integration time: {self.checker.model.integration_time}')
        print(f'Scans to average: {self.checker.model.scans_average}')
        print(f'Electrical dark: {self.checker.model.electrical_dark}')
        self.timer.start()

    def get_spectrum(self):

        i = self.current_index

        print(f'Computing spectrum {i}')
        current_spectrum = self.checker.spectrometer.intensities(
                self.checker.model.electrical_dark
                )


        self.checker.model.spectrum= (self.checker.wavelength, current_spectrum)

        # Add to current average
        self.current_average += current_spectrum

        # Update the value in the model
        self.checker.model.averaged_spectrum = (
                self.checker.wavelength, self.current_average / (i + 1)
                )

        # Now compute the counts
        self.current_time += self.checker.model.integration_time
        self.counts_time = np.append(
                self.counts_time, self.current_time
                )
        self.counts = np.append(self.counts, np.sum(current_spectrum))
        self.checker.model.spectrum_counts = (
                self.counts_time / 1000,
                self.counts
                )

        # Check if measurement is done
        if self.current_index >= self.checker.model.scans_average - 1:
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
        self.current_time = 0

class DataCheckerSpectrometer(QObject):

    initialise_status_signal = pyqtSignal(bool)
    def __init__(self, model):

        super().__init__()

        self.model = model
        self.acquirer = SpectrumAcquiring(self)
        self.integration_time_limits = (10, 1000)
        self.wavelength = np.array([])
        self.length = 10

    def initialise_spectrometer(self):

        print('Loading Spectrometer')
        try:
            self.spectrometer = Spectrometer.from_first_available()
            self.wavelength = self.spectrometer.wavelengths()
            self.length = len(self.wavelength)
            limits = self.spectrometer.integration_time_micros_limits
            ms_limits = (limits[0] / 1000, limits[1] / 1000) # Convert to ms
            self.integration_time_limits = ms_limits
            self.initialise_status_signal.emit(True)
            print('Loading Spectrometer succesful')
        except:
            print('Loading Spectrometer failed')
            self.initialise_status_signal.emit(False)

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
            # Integration time must be in us for spectrometer
            self.spectrometer.integration_time_micros(current_text * 1000)
            self.acquirer.timer.setInterval(current_text)
        else:
            print(f'Integration time out of \
            bonds {self.integration_time_limits}')
            self.model.integration_time = 100
            self.spectrometer.integration_time_micros(100 * 1000)
            self.acquirer.setInterval(100)

    def check_scans_average(self):

        scans_average_edit = self.sender()
        current_text = scans_average_edit.text()
        if current_text.isnumeric():
            print('Updating scans average')
            current_text = int(current_text)
            self.model.scans_average = current_text

if __name__ == '__main__':

    pass
