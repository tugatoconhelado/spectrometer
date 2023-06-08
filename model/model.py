import os
import sys
import numpy as np
from constants import *
from dataclasses import dataclass, field

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
            self._integration_time = new_time
            print(f'Setting integration time to {new_time}')

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


class DataModel:


    def __init__(self, data=[], observers: list = []):

        self.data = data
        self.observers = observers

    def set_data(self, new_data):

        self.data = new_data
        self.notify_observers(self.data)

    def register_observer(self, new_observer):

        self.observers.append(new_observer)

    def notify_observers(self, new_data):

        for observer in self.observers:
            observer.update(new_data)


class SpectrumModel(DataModel):

    def __init__(self, data=[], observers: list = []):

        super().__init__(data, observers)

    def set_data(self, new_data):

        if type(new_data) is SpectrumParameterData:
            self.data.measurement_info = new_data
        elif type(new_data) is SpectrumData:
            self.data = new_data
        self.notify_observers(new_data)


if __name__ == '__main__':

    from constants import *

    m_data = SpectrumParameterData()
    print(m_data.scans_average)
    data = SpectrumData(m_data, [], [], [], [], [])
    model = SpectrumModel(data=data)
    model = DataModel(data=data)
