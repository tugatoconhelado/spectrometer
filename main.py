import sys
from PyQt5.QtWidgets import QApplication
from spectrometer import ViewSpectrometer
from controller import (
        DataCheckerSpectrometer,
        UpdaterSpectrometer,
        SpectrumAcquiring
        )
from model import SpectraData


class App(QApplication):


    def __init__(self, sys_argv):

        super(App, self).__init__(sys_argv)
        self.model = SpectraData()
        self.view = ViewSpectrometer()
        self.updater = UpdaterSpectrometer(self.view)
        self.checker = DataCheckerSpectrometer(self.model)

        self.connect_signals_slots()
        self.view.show()

    def connect_signals_slots(self):


        # Model communitacion to updater
        self.model.averaged_spectrum_signal.connect(
                self.updater.update_average_spectrum_plot
                )
        self.model.spectrum_signal.connect(
                self.updater.update_current_spectrum_plot
                )
        self.model.scans_average_signal.connect(
                self.updater.update_scans_average
                )
        self.model.integration_time_signal.connect(
                self.updater.update_integration_time
                )
        self.model.spectrum_counts_signal.connect(
                self.updater.update_spectrometer_counts_plot
                )

        self.checker.initialise_status_signal.connect(
                self.updater.update_status_gui
                )

        # Connect view signals to data checker
        self.view.initialise_button.clicked.connect(
                self.checker.initialise_spectrometer
                )
        self.view.integration_time_edit.editingFinished.connect(
                self.checker.check_integration_time
                )
        self.view.scans_average_edit.editingFinished.connect(
                self.checker.check_scans_average
                )
        self.view.electrical_dark_checkbox.stateChanged.connect(
                self.checker.check_electrical_dark
                )
        self.view.single_spectrum_button.clicked.connect(
                self.checker.acquirer.start_acquisition
                )


if __name__ == '__main__':

    app = App(sys.argv)
    sys.exit(app.exec_())


