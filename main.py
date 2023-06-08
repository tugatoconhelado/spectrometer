import sys
from PyQt5.QtCore import QSignalMapper
from PyQt5.QtWidgets import QApplication
from front.spectrometer import ViewSpectrometer
from controller.controller import (
        DataCheckerSpectrometer
)
from front.updater import UpdaterSpectrometer
import numpy as np
from constants import *
from model.model import SpectrumData, SpectrumModel, SpectrumParameterData


class App(QApplication):


    def __init__(self, sys_argv):

        super(App, self).__init__(sys_argv)
        parameters = SpectrumParameterData()
        data = SpectrumData(
            parameters=parameters,
            wavelength=np.array([]),
            time=np.array([]),
            spectrum=np.array([]),
            averaged_spectrum=np.array([]),
            spectrum_counts=np.array([])
        )
        self.model = SpectrumModel(data=data)
        self.view = ViewSpectrometer()
        self.updater = UpdaterSpectrometer(self.view)
        self.checker = DataCheckerSpectrometer(self.model, self.view)
        self.model.register_observer(self.updater)
        self.model.register_observer(self.checker)

        self.connect_signals_slots()
        self.view.show()

    def connect_signals_slots(self):
        
        self.checker.initialise_status_signal.connect(
                self.updater.update_status_gui
                )

        # Connect view signals to data checker
        self.view.initialise_button.clicked.connect(
                self.checker.initialise_spectrometer
                )

        self.view.integration_time_edit.editingFinished.connect(
                self.checker.modify_parameters
                )
        self.view.scans_average_edit.editingFinished.connect(
                self.checker.modify_parameters
                )
        self.view.electrical_dark_checkbox.stateChanged.connect(
                self.checker.modify_parameters
                )

        self.view.single_spectrum_button.clicked.connect(
                self.checker.acquirer.start_acquisition
                )
        #self.view.play_button.clicked.connect(
        #    self.checker.measure
        #)


if __name__ == '__main__':

    app = App(sys.argv)
    sys.exit(app.exec_())


