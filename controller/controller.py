import numpy as np
import time
from PyQt5.QtCore import (QObject, pyqtSignal, QTimer)


class SpectrumAcquiring(QObject):
    """
    Reads the spectrum from the spectrometer object

    It reads continously. This means that when the signals is to be averaged,
    it emits signals for every measurement performed in order to average

    Attributes
    ----------
    spectrometer : Spectrometer
        The Spectrometer object from which to read the data.
    parameters: SpectrumParameterData
        SpectrumParameter Data object containing measurements parameters.
    length : int
        length of the data to be acquiared.
    index: int
        Number of current measurement.
    time: int
        Elapsed time. Computed from index times integration time.
    counts_time: np.ndarray
        Array containing values of time for count register.
    wavelength: np.ndarray
        Wavelength of current measurement.

    """

    spectrum_data_signal = pyqtSignal(
        np.ndarray,
        np.ndarray,
        np.ndarray,
        np.ndarray,
        np.ndarray
    )

    def __init__(self):

        super().__init__()

        self.parameters = []
        self.length = 1000
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

    def start_acquisition(self, spectrometer, parameters):

        self.parameters = parameters
        self.spectrometer = spectrometer
        self.length = len(self.spectrometer.wavelengths())
        self.average = np.zeros(self.length)
        self.timer.setInterval(self.parameters.integration_time)
        print(f'Reading Spectrum')
        print(f'Current Parameters')
        print(f'------------------')
        print(f'Integration time: {self.parameters.integration_time}')
        print(f'Scans to average: {self.parameters.scans_average}')
        print(f'Electrical dark: {self.parameters.electrical_dark}')
        self.timer.start()

    def get_spectrum(self):

        start = time.time()
        print(f'Computing spectrum {self.index}')

        self.spectrum = self.spectrometer.intensities(
                self.parameters.electrical_dark
                )
        self.wavelength = self.spectrometer.wavelengths()

        # Add to current average
        self.average += self.spectrum

        # Now compute the counts
        self.time += self.parameters.integration_time / 1000
        self.counts_time = np.append(
                self.counts_time, self.time
                )
        self.counts = np.append(self.counts, np.sum(self.spectrum))

        finish = time.time()
        print(f'Time ellapsed: {(finish - start) * 1000}')
        
        self.spectrum_data_signal.emit(
            self.wavelength,
            self.counts_time,
            self.spectrum,
            self.average / (self.index + 1),
            self.counts
        )

        # Check if measurement is done
        if self.index >= self.parameters.scans_average - 1:
            # -1 because we count from 0
            self.stop_acquisition()
        else:
            self.index += 1

    def stop_acquisition(self):

        if self.timer.isActive():
            self.timer.stop()
        print("Stopping acquisition")
        self.index = 0
        self.counts_time = np.array([])
        self.counts = np.array([])
        self.time = 0

    def update_parameters(self, parameters):
        self.parameters = parameters
        self.timer.setInterval(self.parameters.integration_time)


if __name__ == '__main__':

    pass

