import sys
from PySide6.QtWidgets import QApplication
from front.spectrometer import ViewSpectrometer
from controller.controller import SpectrumAcquiring
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
        self.acquirer = SpectrumAcquiring()

        self.connect_signals_slots()
        self.view.show()

    def connect_signals_slots(self):
        
        self.model.initialise_status_signal.connect(
                self.updater.update_status_gui
                )

        # Connect view signals to data checker
        self.view.initialise_button.clicked.connect(
                self.model.initialise_spectrometer
                )

        self.view.integration_time_edit.editingFinished.connect(
                self.view.send_parameter_data
                )
        self.view.scans_average_edit.editingFinished.connect(
                self.view.send_parameter_data
                )
        self.view.electrical_dark_checkbox.stateChanged.connect(
                self.view.send_parameter_data
                )

        self.view.parameter_data_signal.connect(self.model.set_parameters)
        self.acquirer.spectrum_data_signal.connect(self.model.set_spectrum)

        # What to do after parameters have changed
        self.model.parameters_changed.connect(self.acquirer.update_parameters)
        self.model.parameters_changed.connect(self.updater.update_parameter_display)

        # What to do after spectrum have changed
        self.model.spectrum_changed.connect(self.updater.update_spectrum_plot)

        self.view.single_spectrum_button.clicked.connect(
                self.model.request_spectrum
                )
        self.model.get_spectrum_signal.connect(self.acquirer.start_acquisition)
        self.view.stop_button.clicked.connect(self.acquirer.stop_acquisition)

        self.updater.start()


if __name__ == '__main__':

    app = App(sys.argv)
    sys.exit(app.exec_())


