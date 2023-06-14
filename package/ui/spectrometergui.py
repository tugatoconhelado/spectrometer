import sys
import os
import core.gui
from package.ui.spectrometerui import Ui_spectrometer_widget
#from spectrometerui import Ui_spectrometer_widget
from PySide2.QtCore import Signal
from PySide2.QtGui import QIntValidator
from PySide2.QtWidgets import (QApplication, QWidget)


class SpectrometerGui(QWidget, Ui_spectrometer_widget, core.gui.ExperimentGui):

    request_single_spectrum_experiment = Signal(bool)
    single_spectrum_experiment_signal = Signal(bool)

    parameter_data_signal = Signal(int, int, bool, bool)

    def __init__(self, options=None):

        super().__init__()

        self.current_file = None
        #self.file_manager = filesaver.SpectrumDataSaving(self)

        if options is None:
            options = {
                    'foreground': 'black',
                    'background': 'transparent'
                    }

        #pg.setConfigOptions(**options)
        self.init_gui()

    def init_gui(self):
        """
        Initializes the gui of the widget.

        It calls on the setupUI from the .ui or .py file containing the GUI.
        Calls the configure_plots method to setup axis labels on the plots.
        Sets validators on the Line Edits corresponding to integration time and
        number of scans to average.
        Connects button clicked events to their respective functions.
        """

        print('Loading Ui')
        self.setupUi(self)
        self.setLayout(self.main_layout)
        self.configure_plots()
        self.setTheme()

        #self.load_button.clicked.connect(lambda _: self.file_manager.load(self))

        # Set validator to only accept positive integers
        validator = QIntValidator(bottom=0)
        self.integration_time_edit.setValidator(validator)
        self.scans_average_edit.setValidator(validator)

        # Connect parameter edit events to slots
        self.integration_time_edit.editingFinished.connect(
            self.send_parameter_data
        )
        self.scans_average_edit.editingFinished.connect(
            self.send_parameter_data
        )
        self.electrical_dark_checkbox.stateChanged.connect(
            self.send_parameter_data
        )
        self.substract_background_checkbox.stateChanged.connect(
            self.send_parameter_data
        )

        # Filter range events to slot
        self.filter_checkbox.stateChanged.connect(self.update_filter_range)
        self.filter_lower_limit_edit.editingFinished.connect(
            self.update_filter_range
        )
        self.filter_upper_limit_edit.editingFinished.connect(
            self.update_filter_range
        )

        # Connect experiment execution events (button press) to slots
        self.single_spectrum_button.clicked.connect(
            lambda _: self.request_single_spectrum_experiment.emit(True)
        )
        self.play_button.clicked.connect(
            lambda _: self.request_single_spectrum_experiment.emit(False)
        )

        # Get the last file created
        path = os.path.join(os.getcwd(), 'data')
        if (os.path.exists('data')) and (
                any(os.path.splitext(f)[1] == '.csv' for f in os.listdir(path))
                ):
            self.current_file = os.path.join(path, os.listdir(path)[-1])

    def configure_plots(self):
        """
        Setups the axis labels for each PlotWidget and creates their datalines
        """
        self.current_spectrum_plot.setLabel('left', 'Intensity (counts)')
        self.current_spectrum_plot.setLabel('bottom', 'Wavelength (nm)')
        self.average_spectrum_plot.setLabel('left', 'Intensity (counts)')
        self.average_spectrum_plot.setLabel('bottom', 'Wavelength (nm)')
        self.spectrometer_counts_plot.setLabel(
                'left', 'Intensity (counts)'
                )
        self.spectrometer_counts_plot.setLabel(
                'bottom', 'Time (s)'
                )

        self.current_spectrum_dataline = self.current_spectrum_plot.plot([], [], pen='yellow')
        self.average_spectrum_dataline = self.average_spectrum_plot.plot([], [], pen='yellow')
        self.spectrometer_counts_dataline = self.spectrometer_counts_plot.plot([], [], pen='blue')
        self.background_spectrum_dataline = self.background_spectrum_plot.plot([], [], pen='yellow')

    def send_parameter_data(self):

        self.parameter_data_signal.emit(
            int(self.integration_time_edit.text()),
            int(self.scans_average_edit.text()),
            self.electrical_dark_checkbox.isChecked(),
            self.substract_background_checkbox.isChecked()
        )

    def update_parameter_display(self, data):

        self.integration_time_edit.setText(str(data.integration_time))
        self.scans_average_edit.setText(str(data.scans_average))
        self.electrical_dark_checkbox.setChecked(data.electrical_dark)

    def update_spectrum_plot(self, data):

        self.spectrometer_counts_dataline.setData(data.counts_time, data.counts, pen='b')
        self.current_spectrum_dataline.setData(data.wavelength, data.spectrum, pen='yellow')
        self.average_spectrum_dataline.setData(data.wavelength, data.average, pen='yellow')
        self.background_spectrum_dataline.setData(data.wavelength, data.background, pen='yellow')

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
        self.integration_time_edit.setEnabled(status)
        self.scans_average_edit.setEnabled(status)
        self.filter_checkbox.setEnabled(status)
        self.filter_lower_limit_edit.setEnabled(status)
        self.filter_upper_limit_edit.setEnabled(status)
        self.electrical_dark_checkbox.setEnabled(status)
        self.substract_background_checkbox.setEnabled(status)
        self.single_spectrum_button.setEnabled(status)
        self.play_button.setEnabled(True)
        self.store_background_button.setEnabled(status)
        self.save_button.setEnabled(status)
        self.play_button.setEnabled(status)
        status_label = {
            True: 'connected',
            False: 'not connected'
        }

        self.initialise_label.setText(f'Status: {status_label[status]}')

    def update_filter_range(self):
        """
        Updates the filter range.

        It sets the range of the currently displayed data in both the current
        spectrum plot and the average spectrum plot.
        If the filter box is unchecked it returns the plot to their normal range
        """

        if (
            int(self.filter_lower_limit_edit.text())
            >= int(self.filter_upper_limit_edit.text())
        ):
            self.filter_lower_limit_edit.setText('300')
            self.filter_upper_limit_edit.setText('1000')
        if self.filter_checkbox.isChecked():
            self.current_spectrum_plot.setRange(
                    xRange=[
                        float(self.filter_lower_limit_edit.text()),
                        float(self.filter_upper_limit_edit.text())
                    ]
            )
            self.average_spectrum_plot.setRange(
                    xRange=[
                        float(self.filter_lower_limit_edit.text()),
                        float(self.filter_upper_limit_edit.text())
                    ]
            )
            self.background_spectrum_plot.setRange(
                xRange=[
                    float(self.filter_lower_limit_edit.text()),
                    float(self.filter_upper_limit_edit.text())
                ]
            )
        elif not self.filter_checkbox.isChecked():
            current_data = self.current_spectrum_dataline.getData()
            if current_data[0] is None:
                return 0
            self.current_spectrum_plot.setRange(
                    xRange=[
                        min(current_data[0]),
                        max(current_data[0])
                    ]
                    )
            self.average_spectrum_plot.setRange(
                xRange=[
                    min(current_data[0]),
                    max(current_data[0])
                ]
            )
            self.background_spectrum_plot.setRange(
                xRange=[
                    min(current_data[0]),
                    max(current_data[0])
                ]
            )


if __name__ == '__main__':

    app = QApplication(sys.argv)
    form = SpectrometerGui()
    form.show()
    form.update_status_gui(True)
    sys.exit(app.exec_())
