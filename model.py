import os
import sys
import numpy as np
from PyQt5 import QtTest
from PyQt5.QtCore import (QObject, pyqtSignal)
from seabreeze.spectrometers import Spectrometer


class SpectraData(QObject):


    spectrum_signal = pyqtSignal(tuple)
    averaged_spectrum_signal = pyqtSignal(tuple)
    spectrum_counts_signal = pyqtSignal(tuple)
    scans_average_signal = pyqtSignal(int)
    initialise_status_signal = pyqtSignal(bool)
    integration_time_signal = pyqtSignal(int)


    def __init__(self):

        super().__init__()

        self.__spectrum_counts = np.array([])
        self.__spectrum = np.array([])
        self.__averaged_spectrum = np.array([])
        self.__scans_average = 1
        self.__integration_time = 100
        self.electrical_dark = False

    @property
    def averaged_spectrum(self):
        return self.__averaged_spectrum

    @averaged_spectrum.setter
    def averaged_spectrum(self, new_average):
        self.__averaged_spectrum = new_average
        self.averaged_spectrum_signal.emit(new_average)

    @property
    def spectrometer_counts(self):
        return self.__spectrum_counts

    @spectrometer_counts.setter
    def spectrum_counts(self, new_counts):
        self.__spectrum_counts = new_counts
        self.spectrum_counts_signal.emit(self.spectrum_counts)

    @property
    def integration_time(self):
        return self.__integration_time

    @integration_time.setter
    def integration_time(self, new_time):

        self.__integration_time = new_time
        self.integration_time_signal.emit(self.integration_time)

    @property
    def spectrum(self):
        return self.__spectrum

    @spectrum.setter
    def spectrum(self, spectrum):

        self.__spectrum = spectrum
        self.spectrum_signal.emit(
                self.spectrum
                )

    @property
    def scans_average(self):
        return self.__scans_average

    @scans_average.setter
    def scans_average(self, new_avg):

        self.__scans_average = new_avg
        self.scans_average_signal.emit(self.scans_average)




if __name__ == '__main__':

    model = SpectraData()
