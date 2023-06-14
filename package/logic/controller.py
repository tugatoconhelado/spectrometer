import numpy as np
import core.savelogic
from seabreeze.spectrometers import Spectrometer
# from seatease.spectrometers import Spectrometer # Emulate the spectrometer
from PySide2.QtCore import (QObject, Signal, QTimer)
from package.model.datamodel import SpectrumData, SpectrumParameterData


class SpectrumExperiment(QObject):
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
    spectrum: np.ndarray
        Current spectrum measured.
    average: np.ndarray
        Averaded spectrum.
    """
    spectrum_data_signal = Signal(SpectrumData)
    parameters_data_signal = Signal(SpectrumParameterData)
    experiment_status_signal = Signal(bool)


    def __init__(self, data_storage):

        super().__init__()

        self.__length = 1000
        self.index = 0 # current index
        self.time_sum = 0 # current time
        self.data = data_storage
        self.spectra = np.zeros((10, 10))
        self.single_measurement = False
        self.save_backend = core.savelogic.JSONSaver('data', 'spectra', self.data)


        # Timer to perform the measurements
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.get_spectrum)

    def start_acquisition(self, single_measurement: bool = False) -> None:
        """
        Starts the spectrum acquisition.

        For this, it sets the timer interval to the integration time,
        then creates the arrays that will contain the counts, the
        count_time and the spectra to average. Finally, it starts the
        experiment, contained in get_spectrum, which performs the acquisition.

        Parameters
        ----------
        single_measurement: bool
            Indicates wether to calculate a single measurement until the
            number of averaged spectra is equal to the number of scans to
            average, or read until the user stops the experiment.

        Returns
        -------
        None

        """
        self.single_measurement = single_measurement
        self.spectra = np.zeros((self.data.parameters.scans_average, self.__length))
        self.data.average = np.zeros(self.__length)
        self.data.counts_time = np.array([])
        self.data.counts = np.array([])
        self.timer.setInterval(self.data.parameters.integration_time)
        print(f'Starting Acquisition')
        print(f'Current Parameters')
        print(f'------------------')
        print(f'Integration time: {self.data.parameters.integration_time}')
        print(f'Scans to average: {self.data.parameters.scans_average}')
        print(f'Electrical dark: {self.data.parameters.electrical_dark}')
        self.experiment_status_signal.emit(False)
        self.timer.start()

    def get_spectrum(self) -> None:
        """
        Handles the data acquiring. It esentially performs the experiment

        Records the spectrum and wavelengths from the spectrometer object.
        Each measured spectrum is averaged and the counts are computed as
        the sum of all the intensities recorded. Finally, it emits a
        spectrum_data_signal containing all the info stracted:
        """

        self.data.spectrum = self.spectrometer.intensities(
                self.data.parameters.electrical_dark
                )
        if self.data.parameters.substract_background:
            self.data.spectrum -= self.data.background
        self.data.wavelength = self.spectrometer.wavelengths()

        # Add to current average
        self.spectra = np.roll(self.spectra, 1, axis=0)
        self.spectra[-1, :] = self.data.spectrum
        self.data.average = np.sum(self.spectra, axis=0) / (self.data.parameters.scans_average)

        # Now compute the counts
        self.time_sum += self.data.parameters.integration_time / 1000 # In seconds
        self.data.counts_time = np.append(
                self.data.counts_time, self.time_sum
                )
        self.data.counts = np.append(self.data.counts, np.sum(self.data.spectrum))

        self.spectrum_data_signal.emit(self.data)

        self.save_backend.save(None)
        # Check if measurement is done
        if (
            self.single_measurement and
            (self.index >= self.data.parameters.scans_average - 1)
        ):
            # -1 because we count from 0
            self.stop_acquisition()
        else:
            self.index += 1

    def stop_acquisition(self) -> None:
        """
        Stops the timer if it is still running.

        Resets all the index counters and partial sums
        Emits a signal with the status of the experiment.
        True for experiment done and False for experiment running
        """

        if self.timer.isActive():
            self.timer.stop()
        self.index = 0
        self.time_sum = 0
        self.experiment_status_signal.emit(True)
        print('Measurement stopped')

    def set_parameters(
            self,
            integration_time : int = 100,
            scans_average : int = 10,
            electrical_dark : bool = False,
            susbstract_background : bool = False
            ) -> None:
        """
        Sets the measurement parameters to the data containing object

        Parameters
        ----------
        integration_time : int
            Integration time for the measurement
        scans_average: int
            Number of scans to average
        electrical_dark: bool
            Indicates if the hardware built in electrical dark counts correction
            should be used in the measurement.
        substract_background: bool
            Indicates if the currently stores background should be substracted
            from the currently measured spectrum.

        Returns
        -------
        None
        """

        self.data.parameters.integration_time = integration_time
        self.data.parameters.scans_average = scans_average
        self.data.parameters.electrical_dark = electrical_dark
        self.data.parameters.substract_background = susbstract_background

        self.timer.setInterval(self.data.parameters.integration_time)
        self.spectrometer.integration_time_micros(
            self.data.parameters.integration_time * 1000 # In microseconds
        )
        self.parameters_data_signal.emit(self.data.parameters)

    def set_background(self):
        """
        Stores the current spectrum as the background
        """

        self.data.background = self.data.average
        self.spectrum_data_signal.emit(self.data)

    def initialise_spectrometer(self) -> None:
        """
        Creates an instance of the spectrometer object.
        Stores the length of the data recorded. To do this, it stracts the
        wavelengths from the spectrometer, and calculates its length.
        Emits a signal to enable gui
        """

        print('Loading Spectrometer')
        try:
            self.spectrometer = Spectrometer.from_first_available()
            limits = self.spectrometer.integration_time_micros_limits
            print('Loading Spectrometer succesful')
            self.__length = len(self.spectrometer.wavelengths())
            self.data.background = np.zeros(self.__length)
            self.experiment_status_signal.emit(True)
        except:
            print('Loading Spectrometer failed')
            self.experiment_status_signal.emit(False)

    def load_data(self) -> str:
        """
        Calls the data saving backend to load prompt a File Dialog and load the
        data.
        It passes the directory for the experiment type ('spectra') as a
        variable to start the File Dialog in this folder

        Parameters
        ----------
        iterate : int = 0, optional
            Indicates in which direction from the last saved file to iterate.
            If iterate = 0 the save_backend will prompt a File Dialog
            It is passed to the saved logic

        Returns
        -------
        loaded_data : str
            Path of the loaded data

        """
        self.spectrum_data_signal.emit(self.data)
        self.parameters_data_signal.emit(self.data.parameters)


if __name__ == '__main__':

    experiment = SpectrumExperiment()

