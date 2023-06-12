import json
import pickle
import numpy as np
import package.model.constants as config
import dataclasses

@dataclasses.dataclass
class SpectrumParameterData:


    _integration_time: int = 100
    _scans_average: int = 1
    electrical_dark: bool = False
    substract_background: bool = False

    def __post_init__(self):

        self.scans_average = self._scans_average
        self.integration_time = self._integration_time

    @property
    def integration_time(self) -> int:
        return self._integration_time

    @integration_time.setter
    def integration_time(self, new_time) -> None:

        if type(new_time) is int:

            if new_time <= config.MAX_INTEGRATION_TIME and new_time >= config.MIN_INTEGRATION_TIME:
                self._integration_time = new_time
                print(f'Setting integration time to {new_time}')
            else:
                print(f'Integration time out of bonds')
                self._integration_time = config.DEFAULT_INTEGRATION_TIME
        else:
            print('Integration time must be an integer (in ms)')

    @property
    def scans_average(self) -> int:
        return self._scans_average

    @scans_average.setter
    def scans_average(self, new_value) -> None:

        if type(new_value) is int:
            if new_value <= config.MAX_SCANS_AVERAGE and new_value >= config.MIN_SCANS_AVERAGE:
                self._scans_average = new_value
                print(f'Setting scans to average to {new_value}')
            else:
                self._scans_average = config.DEFAULT_SCANS_AVERAGE
                print('Number of scans to average out of bonds')
        else:
            print('Scans to average must be an integer')

@dataclasses.dataclass
class SpectrumData:


    parameters: SpectrumParameterData = None
    wavelength: np.ndarray = None
    counts_time: np.ndarray = None
    background: np.ndarray = None
    spectrum: np.ndarray = None
    average: np.ndarray = None
    counts: np.ndarray = None


    def to_dict(self):

        # Store data in dict
        dict_data = dataclasses.asdict(self)

        # Converts numpy arrays to list (json does not store arrays)
        dict_data = {key: value.tolist() if isinstance(value, np.ndarray) else value for key, value in dict_data.items()}

        # Converts parameters from dict to entries in the dict_data
        full_data = dict_data.pop('parameters')
        full_data.update(dict_data)

        full_data = {
            'Experiment_Data': full_data
        }

        return full_data

    def from_dict(self, dict_data):

        self.parameters.integration_time = dict_data['_integration_time']
        self.parameters.scans_average = dict_data['_scans_average']
        self.parameters.electrical_dark = dict_data['electrical_dark']
        self.parameters.substract_background = dict_data['substract_background']
        self.wavelength = dict_data['wavelength']
        self.counts_time = dict_data['counts_time']
        self.background = dict_data['background']
        self.spectrum = dict_data['spectrum']
        self.average = dict_data['average']
        self.counts = dict_data['counts']

        return self





if __name__ == '__main__':

    sdata = SpectrumData()