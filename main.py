import sys
from PyQt5.QtWidgets import QApplication
from spectrometer import UiSpectrometer
from controller import ControlSpectrometer


if __name__ == '__main__':

    app = QApplication([])
    ui_spectrometer = UiSpectrometer()

    qepro = ControlSpectrometer()

    # Connect ui call signals
    ui_spectrometer.initialise_button.clicked.connect(qepro.initialise)
    ui_spectrometer.single_spectrum_button.clicked.connect(
            qepro.get_single_spectrum
            )
    ui_spectrometer.read_continuously_signal.connect(qepro.read_continuously)
    ui_spectrometer.integration_time_signal.connect(
            lambda _: setattr(qepro, 'integration_time', _)
            )
    ui_spectrometer.scans_average_signal.connect(
            lambda _: setattr(qepro, 'scans_average', _)
            )
    ui_spectrometer.electrical_dark_checkbox.stateChanged.connect(
            lambda _ : setattr(
                qepro,
                'electrical_dark',
                ui_spectrometer.electrical_dark_checkbox.isChecked()
                )
            )
    ui_spectrometer.substract_background_checkbox.stateChanged.connect(
            lambda _: setattr(
                qepro,
                'substract_background',
                ui_spectrometer.substract_background_checkbox.isChecked()
                )
            )

    # Connect controller response signals
    qepro.spectrum_signal.connect(ui_spectrometer.update_current_spectrum_plot)
    qepro.averaged_spectrum_signal.connect(
            ui_spectrometer.update_average_spectrum_plot
            )
    qepro.initialise_status_signal.connect(ui_spectrometer.enable_gui)
    qepro.spectrometer_counts_signal.connect(ui_spectrometer.update_spectrometer_counts_plot)



    ui_spectrometer.show()
    sys.exit(app.exec_())


