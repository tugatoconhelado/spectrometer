import sys
from PySide2.QtWidgets import QApplication
from package.ui.spectrometergui import SpectrometerGui
from package.logic.controller import SpectrumExperiment
from package.model.datamodel import SpectrumParameterData, SpectrumData
import numpy as np


class SpectrometerApp:

    def __init__(self) -> None:
        
        self.gui = SpectrometerGui()
        pdata = SpectrumParameterData(100, 1, False, False)
        self.data = SpectrumData(pdata, np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([]))
        self.experiment = SpectrumExperiment(self.data)
        self.connect_gui_experiment()
        self.gui.show()

    def connect_gui_experiment(self):

        self.gui.initialise_button.clicked.connect(
            self.experiment.initialise_spectrometer
        )
        self.gui.parameter_data_signal.connect(self.experiment.set_parameters)
        self.gui.request_single_spectrum_experiment.connect(
            self.experiment.start_acquisition
        )
        self.gui.stop_button.clicked.connect(self.experiment.stop_acquisition)
        self.experiment.experiment_status_signal.connect(self.gui.update_status_gui)

        self.experiment.parameters_data_signal.connect(
            self.gui.update_parameter_display
        )
        self.experiment.spectrum_data_signal.connect(
            self.gui.update_spectrum_plot
        )
        self.gui.store_background_button.clicked.connect(
            self.experiment.set_background
        )
        self.gui.save_button.clicked.connect(
            lambda: self.experiment.save_backend.save(self.gui, True)
        )
        self.gui.load_button.clicked.connect(
            lambda: self.experiment.save_backend.load(self.gui, iterate=0)
        )
        self.gui.previous_button.clicked.connect(
            lambda: self.experiment.save_backend.load(self.gui, iterate=-1)
        )
        self.gui.next_button.clicked.connect(
            lambda: self.experiment.save_backend.load(self.gui, iterate=1)
        )
        self.gui.load_button.clicked.connect(self.experiment.load_data)
        self.gui.previous_button.clicked.connect(self.experiment.load_data)
        self.gui.next_button.clicked.connect(self.experiment.load_data)
        self.gui.previous_button.clicked.emit()


def main():

    app = QApplication(sys.argv)
    form = SpectrometerApp()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
