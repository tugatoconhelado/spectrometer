import numpy as np
from PyQt5.QtCore import (QObject, pyqtSignal, QTimer)
from seatease.spectrometers import Spectrometer
from model.model import SpectrumData, SpectrumModel, SpectrumParameterData


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
        self.parameters = []
        self.index = 0 # current index
        self.time = 0 # current time
        self.counts_time = np.array([])
        self.wavelength = np.zeros(10)
        self.counts = np.array([])
        self.average = np.array([])
        self.spectrum = np.array([])


        # Timer to perform the measurements
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.get_spectrum)

    def start_acquisition(self):

        #self.parameters = self.checker.model.data.parameters
        self.timer.setInterval(self.parameters.integration_time)
        self.average = np.zeros(self.checker.length)
        print(f'Reading Spectrum')
        print(f'Current Parameters')
        print(f'------------------')
        print(f'Integration time: {self.parameters.integration_time}')
        print(f'Scans to average: {self.parameters.scans_average}')
        print(f'Electrical dark: {self.parameters.electrical_dark}')
        self.timer.start()

    def get_spectrum(self):

        print(f'Computing spectrum {self.index}')

        self.spectrum = self.checker.spectrometer.intensities(
                self.parameters.electrical_dark
                )
        self.wavelength = self.checker.spectrometer.wavelengths()

        # Add to current average
        self.average += self.spectrum

        # Now compute the counts
        self.time += self.parameters.integration_time / 1000
        self.counts_time = np.append(
                self.counts_time, self.time
                )
        self.counts = np.append(self.counts, np.sum(self.spectrum))
        
        self.checker.update_data()

        # Check if measurement is done
        if self.index >= self.parameters.scans_average - 1:
            # -1 because we count from 0
            self.stop_acquisition()
        else:
            self.index += 1

    def stop_acquisition(self):

        if self.timer.isActive():
            self.timer.stop()
        self.index = 0
        self.counts_time = np.array([])
        self.counts = np.array([])
        self.time = 0

class DataCheckerSpectrometer(QObject):

    initialise_status_signal = pyqtSignal(bool)

    def __init__(self, model, view):

        super().__init__()

        self.model = model
        self.view = view
        self.acquirer = SpectrumAcquiring(self)
        self.length = 10
        self.data = []

    def initialise_spectrometer(self):

        print('Loading Spectrometer')
        try:
            self.spectrometer = Spectrometer.from_first_available()
            self.wavelength = self.spectrometer.wavelengths()
            self.length = len(self.wavelength)
            limits = self.spectrometer.integration_time_micros_limits
            MAX_INTEGRATION_TIME = limits[1] / 1000
            MIN_INTEGRATION_TIME = limits[0] / 1000
            self.initialise_status_signal.emit(True)
            print('Loading Spectrometer succesful')
        except:
            print('Loading Spectrometer failed')
            self.initialise_status_signal.emit(False)

    def modify_parameters(self):

        integration_time = int(self.view.integration_time_edit.text())
        scans_average = int(self.view.scans_average_edit.text())
        electrical_dark = self.view.electrical_dark_checkbox.checkState()
        new_parameter_data = SpectrumParameterData(
            integration_time, scans_average, electrical_dark
        )
        self.model.set_data(new_parameter_data)

    def update_data(self):

        #self.checker.model.averaged_spectrum = (
        #        self.checker.wavelength, self.current_average / (i + 1)
        #        )
        new_spectrum_data = SpectrumData(
            parameters=self.acquirer.parameters,
            wavelength = self.acquirer.wavelength,
            time = self.acquirer.counts_time,
            spectrum = self.acquirer.spectrum,
            averaged_spectrum = self.acquirer.average / (self.acquirer.index + 1),
            spectrum_counts = self.acquirer.counts
        )
        self.model.set_data(new_spectrum_data)

    def update(self, new_data):

        if type(new_data) is SpectrumData:
            self.data = new_data
            self.acquirer.parameters = self.data.parameters
            integration_time = new_data.parameters.integration_time
        elif type(new_data) is SpectrumParameterData:
            self.acquirer.parameters = new_data
            integration_time = new_data.integration_time

        print(self.acquirer.parameters.scans_average)
        # Update acquirer and spectrometer integration time
        self.spectrometer.integration_time_micros(
                integration_time * 1000
                )
        self.acquirer.timer.setInterval(integration_time)



if __name__ == '__main__':

    pass

