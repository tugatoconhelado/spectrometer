import os
import sys
import numpy as np
from constants import *
from dataclasses import dataclass, field
from PySide6.QtCore import QObject, Signal
from seatease.spectrometers import Spectrometer

@dataclass
class SpectrumParameterData:

    _integration_time: int = 100
    _scans_average: int = 1
    electrical_dark: bool = False

    def __post_init__(self):

        self.scans_average = self._scans_average
        self.integration_time = self._integration_time

    @property
    def integration_time(self) -> int:
        return self._integration_time

    @integration_time.setter
    def integration_time(self, new_time) -> None:

        if type(new_time) is int:

            if new_time <= MAX_INTEGRATION_TIME and new_time >= MIN_INTEGRATION_TIME:
                self._integration_time = new_time
                print(f'Setting integration time to {new_time}')
            else:
                print(f'Integration time out of bonds')
        else:
            print('Integration time must be an integer (in ms)')

    @property
    def scans_average(self) -> int:
        return self._scans_average

    @scans_average.setter
    def scans_average(self, new_value) -> None:

        if type(new_value) is int:
            if new_value <= MAX_SCANS_AVERAGE and new_value >= MIN_SCANS_AVERAGE:
                self._scans_average = new_value
                print(f'Setting scans to average to {new_value}')
            else:
                self._scans_average = 1
                print('Number of scans to average out of bonds')
        else:
            print('Scans to average must be an integer')

@dataclass
class SpectrumData:

    parameters: SpectrumParameterData
    wavelength: np.ndarray
    time: np.ndarray
    spectrum: np.ndarray
    averaged_spectrum: np.ndarray
    spectrum_counts: np.ndarray

class SpectrumModel(QObject):


    parameters_changed = Signal(SpectrumParameterData)
    spectrum_changed = Signal(SpectrumData)
    initialise_status_signal = Signal(bool)
    get_spectrum_signal = Signal(Spectrometer, SpectrumParameterData)


    def __init__(self, data=0, view=0):

        super().__init__()

        self.data = data
        self.view = view
        self.spectrometer = None

    def set_parameters(self, integration_time, scans_average, electrical_dark):


        self.data.parameters = SpectrumParameterData(
            integration_time,
            scans_average,
            electrical_dark
        )
        self.spectrometer.integration_time_micros(integration_time * 1000)
        self.parameters_changed.emit(self.data.parameters)

    def set_spectrum(
            self, wavelength, time, spectrum, averaged_spectrum, spectrum_counts
    ):
        parameters = self.data.parameters
        self.data = SpectrumData(
            parameters,
            wavelength,
            time,
            spectrum,
            averaged_spectrum,
            spectrum_counts
        )
        self.spectrum_changed.emit(self.data)

    def initialise_spectrometer(self):

        print('Loading Spectrometer')
        try:
            self.spectrometer = Spectrometer.from_first_available()
            limits = self.spectrometer.integration_time_micros_limits
            print('Loading Spectrometer succesful')
            self.initialise_status_signal.emit(True)
        except:
            print('Loading Spectrometer failed')
            self.initialise_status_signal.emit(False)

    def update_data(self):

        #self.checker.model.averaged_spectrum = (
        #        self.checker.wavelength, self.current_average / (i + 1)
        #        )
        start = time.time()
        self.model.set_spectrum(
            parameters=self.acquirer.parameters,
            wavelength=self.acquirer.wavelength,
            time=self.acquirer.counts_time,
            spectrum=self.acquirer.spectrum,
            averaged_spectrum=self.acquirer.average / (self.acquirer.index + 1),
            spectrum_counts=self.acquirer.counts
        )
        end = time.time()
        print(f'Ellapsed time updating {(end - start) * 1000}')

    def request_spectrum(self):

        self.get_spectrum_signal.emit(self.spectrometer, self.data.parameters)







if __name__ == '__main__':

    from constants import *

    m_data = SpectrumParameterData()
    print(m_data.scans_average)
    data = SpectrumData(m_data, [], [], [], [], [])
    model = SpectrumModel(data=data)
