import os
import sys
import numpy as np
from PyQt5 import QtTest
from PyQt5.QtCore import (QObject, pyqtSignal)
from seabreeze.spectrometers import Spectrometer

class ControlSpectrometer(QObject):

    spectrum_signal = pyqtSignal(tuple)
    averaged_spectrum_signal = pyqtSignal(tuple)
    initialise_status_signal = pyqtSignal(bool)
    spectrometer_counts_signal = pyqtSignal(float)

    def __init__(self):

        super().__init__()

        self.length = 1000 # Length of the arrays
        self.__current_spectrum = np.zeros(self.length)
        self.__background = np.zeros(self.length)
        self.__spectrometer_counts = 0

        self.__integration_time = 100
        self.scans_average = 1
        self.electrical_dark = False

        self.substract_background = False

    @property
    def spectrometer_counts(self):
        return self.__spectrometer_counts

    @spectrometer_counts.setter
    def spectrometer_counts(self, new_counts):
        self.__spectrometer_counts = new_counts
        self.spectrometer_counts_signal.emit(self.spectrometer_counts)

    @property
    def integration_time(self):
        return self.__integration_time

    @integration_time.setter
    def integration_time(self, new_time):

        self.__integration_time = new_time
        self.spectrometer.integration_time_micros(self.integration_time * 1000)# In microseconds

    @property
    def current_spectrum(self):
        return self.__current_spectrum

    @current_spectrum.setter
    def current_spectrum(self, spectrum):
        if len(spectrum) == self.length:
            if self.substract_background is True:
                print('Substracting background')
                self.__current_spectrum = spectrum - self.background
            elif self.substract_background is False:
                self.__current_spectrum = spectrum
            self.spectrometer_counts = np.sum(spectrum)
            self.spectrum_signal.emit(
                    (self.wavelength, self.current_spectrum)
                    )

    @property
    def background(self):
        return self.__background

    @background.setter
    def background(self, bg):
        if len(bg) == self.length:
            self.__background = bg

    def initialise(self):

        print('Loading Spectrometer')
        self.spectrometer = Spectrometer.from_first_available()
        self.wavelength = self.spectrometer.wavelengths()
        self.length = len(self.wavelength)
        print(self.wavelength)
        self.initialise_status_signal.emit(True)
        self.background = np.ones(self.length)
        #self.spectrometer = Spectrometer.from_first_available()

    def get_single_spectrum(self):

        print(f'Reading Spectrum with {self.integration_time} ms \
                              integration time')
        spectrum = np.zeros(self.length)
        for i in range(self.scans_average):
            spectrum += self.spectrometer.intensities(self.electrical_dark)
            QtTest.QTest.qWait(self.integration_time)
        self.current_spectrum = spectrum / self.scans_average
        return self.current_spectrum

    def read_continuously(self, number_average=10):


        print(f'Measuring {number_average} spectra with integration time {self.integration_time} ms')
        spectra = np.zeros((number_average, self.length)) # Stores measurements

        for i in range(number_average):
            print(f'Computing spectrum {i}')
            self.current_spectrum = self.spectrometer.intensities(self.electrical_dark)
            spectra[i, :] = self.current_spectrum
            average_spectrum = np.sum(spectra, axis=0) / (i + 1)
            self.averaged_spectrum_signal.emit(
                    (self.wavelength, average_spectrum)
                    )
            QtTest.QTest.qWait(self.integration_time)

    def load_spectra(self, as_background=False):

        if as_background:
            pass
        pass

    def previous_spectra(self):
        pass

    def next_spectra(self):
        pass


if __name__ == '__main__':

    qepro = ControlSpectrometer()
