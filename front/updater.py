from PyQt5.QtCore import QThread, pyqtSignal

class UpdaterSpectrometer(QThread):


    def __init__(self, view=None):

        super().__init__()
        self.view = view

    def run(self):

        self.exec_()

    def update_parameter_display(self, data):

        self.view.integration_time_edit.setText(str(data.integration_time))
        self.view.scans_average_edit.setText(str(data.scans_average))
        self.view.electrical_dark_checkbox.setCheckState(data.electrical_dark)

    def update_spectrum_plot(self, data):

        self.view.spectrometer_counts_dataline.setData(data.time, data.spectrum_counts, pen='b')
        self.view.current_spectrum_dataline.setData(data.wavelength, data.spectrum, pen='yellow')
        self.view.average_spectrum_dataline.setData(data.wavelength, data.averaged_spectrum, pen='yellow')

    def update_status_gui(self, status):
        """
        Enables components from the gui in the event of spectrometer
        intialisation.

        The components being activated when the spectrometer gets online are:
            - integration_time_edit : QLineEdit
            - scans_average_edit : QLineEdit
            - filter_checkbox : QCheckBox
            - filter_lower_limit_edit : QLineEdit
            - filter_upper_limit_edit : QLineEdit
            - electrical_dark_checkbox : QCheckBox
            - substract_background_checkbox: QCheckBox
            - single_spectrum_button : QPushButton
            - read_continuously_button : QPushButton
            - store_background_button : QPushButton
            - load_background_button : QPushButton
            - save_button : QPushButton
        """

        response = { # Just for display
            True: 'Enabling',
            False: 'Disabling'
        }
        print(f'Spectrometer status: {status}. {response[status]} Gui')
        self.view.integration_time_edit.setEnabled(status)
        self.view.scans_average_edit.setEnabled(status)
        self.view.filter_checkbox.setEnabled(status)
        self.view.filter_lower_limit_edit.setEnabled(status)
        self.view.filter_upper_limit_edit.setEnabled(status)
        self.view.electrical_dark_checkbox.setEnabled(status)
        self.view.substract_background_checkbox.setEnabled(status)
        self.view.single_spectrum_button.setEnabled(status)
        self.view.play_button.setEnabled(status)
        self.view.store_background_button.setEnabled(status)
        self.view.load_background_button.setEnabled(status)
        self.view.save_button.setEnabled(status)
        status_label = {
            True: 'connected',
            False: 'not connected'
        }

        self.view.initialise_label.setText(f'Status: {status_label[status]}')

    def update_filter_range(self):
        """
        Updates the filter range.

        It sets the range of the currently displayed data in both the current
        spectrum plot and the average spectrum plot.
        If the filter box is unchecked it returns the plot to their normal range
        """

        if self.view.filter_checkbox.isChecked():
            self.view.current_spectrum_plot.setRange(
                    xRange=[
                        float(self.view.filter_lower_limit_edit.text()),
                        float(self.view.filter_upper_limit_edit.text())
                        ]
                    )
        #elif not self.view.filter_checkbox.isChecked():
        #    self.view.current_spectrum_plot.setRange(
        #            xRange=[np.min(wavelength), np.max(wavelength)]
        #            )

