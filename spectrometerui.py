# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spectrometer.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_spectrometer_widget(object):
    def setupUi(self, spectrometer_widget):
        spectrometer_widget.setObjectName("spectrometer_widget")
        spectrometer_widget.resize(1279, 642)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(spectrometer_widget.sizePolicy().hasHeightForWidth())
        spectrometer_widget.setSizePolicy(sizePolicy)
        self.horizontalLayoutWidget = QtWidgets.QWidget(spectrometer_widget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1051, 621))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.main_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.main_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.main_layout.setContentsMargins(2, 2, 2, 2)
        self.main_layout.setObjectName("main_layout")
        self.control_frame = QtWidgets.QFrame(self.horizontalLayoutWidget)
        self.control_frame.setMaximumSize(QtCore.QSize(350, 600))
        self.control_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.control_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.control_frame.setObjectName("control_frame")
        self.control_layout = QtWidgets.QVBoxLayout(self.control_frame)
        self.control_layout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.control_layout.setSpacing(2)
        self.control_layout.setObjectName("control_layout")
        self.initialise_layout = QtWidgets.QHBoxLayout()
        self.initialise_layout.setObjectName("initialise_layout")
        self.initialise_button = QtWidgets.QPushButton(self.control_frame)
        self.initialise_button.setObjectName("initialise_button")
        self.initialise_layout.addWidget(self.initialise_button)
        self.initialise_label = QtWidgets.QLabel(self.control_frame)
        self.initialise_label.setTextFormat(QtCore.Qt.AutoText)
        self.initialise_label.setObjectName("initialise_label")
        self.initialise_layout.addWidget(self.initialise_label)
        self.control_layout.addLayout(self.initialise_layout)
        self.integration_time_layout = QtWidgets.QHBoxLayout()
        self.integration_time_layout.setObjectName("integration_time_layout")
        self.integration_time_label = QtWidgets.QLabel(self.control_frame)
        self.integration_time_label.setObjectName("integration_time_label")
        self.integration_time_layout.addWidget(self.integration_time_label)
        self.integration_time_edit = QtWidgets.QLineEdit(self.control_frame)
        self.integration_time_edit.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.integration_time_edit.sizePolicy().hasHeightForWidth())
        self.integration_time_edit.setSizePolicy(sizePolicy)
        self.integration_time_edit.setMaximumSize(QtCore.QSize(100, 100))
        self.integration_time_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.integration_time_edit.setObjectName("integration_time_edit")
        self.integration_time_layout.addWidget(self.integration_time_edit)
        self.control_layout.addLayout(self.integration_time_layout)
        self.scans_average_layout = QtWidgets.QHBoxLayout()
        self.scans_average_layout.setObjectName("scans_average_layout")
        self.scans_average_label = QtWidgets.QLabel(self.control_frame)
        self.scans_average_label.setObjectName("scans_average_label")
        self.scans_average_layout.addWidget(self.scans_average_label)
        self.scans_average_edit = QtWidgets.QLineEdit(self.control_frame)
        self.scans_average_edit.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scans_average_edit.sizePolicy().hasHeightForWidth())
        self.scans_average_edit.setSizePolicy(sizePolicy)
        self.scans_average_edit.setMaximumSize(QtCore.QSize(100, 100))
        self.scans_average_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.scans_average_edit.setObjectName("scans_average_edit")
        self.scans_average_layout.addWidget(self.scans_average_edit)
        self.control_layout.addLayout(self.scans_average_layout)
        self.filter_layout = QtWidgets.QHBoxLayout()
        self.filter_layout.setObjectName("filter_layout")
        self.filter_checkbox = QtWidgets.QCheckBox(self.control_frame)
        self.filter_checkbox.setEnabled(False)
        self.filter_checkbox.setObjectName("filter_checkbox")
        self.filter_layout.addWidget(self.filter_checkbox)
        self.filter_lower_limit_edit = QtWidgets.QLineEdit(self.control_frame)
        self.filter_lower_limit_edit.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filter_lower_limit_edit.sizePolicy().hasHeightForWidth())
        self.filter_lower_limit_edit.setSizePolicy(sizePolicy)
        self.filter_lower_limit_edit.setMaximumSize(QtCore.QSize(70, 100))
        self.filter_lower_limit_edit.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.filter_lower_limit_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.filter_lower_limit_edit.setObjectName("filter_lower_limit_edit")
        self.filter_layout.addWidget(self.filter_lower_limit_edit)
        self.to_label = QtWidgets.QLabel(self.control_frame)
        self.to_label.setObjectName("to_label")
        self.filter_layout.addWidget(self.to_label)
        self.filter_upper_limit_edit = QtWidgets.QLineEdit(self.control_frame)
        self.filter_upper_limit_edit.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filter_upper_limit_edit.sizePolicy().hasHeightForWidth())
        self.filter_upper_limit_edit.setSizePolicy(sizePolicy)
        self.filter_upper_limit_edit.setMaximumSize(QtCore.QSize(70, 100))
        self.filter_upper_limit_edit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.filter_upper_limit_edit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.filter_upper_limit_edit.setObjectName("filter_upper_limit_edit")
        self.filter_layout.addWidget(self.filter_upper_limit_edit)
        self.control_layout.addLayout(self.filter_layout)
        self.electrical_dark_layout = QtWidgets.QHBoxLayout()
        self.electrical_dark_layout.setObjectName("electrical_dark_layout")
        self.electrical_dark_checkbox = QtWidgets.QCheckBox(self.control_frame)
        self.electrical_dark_checkbox.setEnabled(False)
        self.electrical_dark_checkbox.setObjectName("electrical_dark_checkbox")
        self.electrical_dark_layout.addWidget(self.electrical_dark_checkbox)
        self.control_layout.addLayout(self.electrical_dark_layout)
        self.substract_background_layout = QtWidgets.QHBoxLayout()
        self.substract_background_layout.setObjectName("substract_background_layout")
        self.substract_background_checkbox = QtWidgets.QCheckBox(self.control_frame)
        self.substract_background_checkbox.setEnabled(False)
        self.substract_background_checkbox.setObjectName("substract_background_checkbox")
        self.substract_background_layout.addWidget(self.substract_background_checkbox)
        self.control_layout.addLayout(self.substract_background_layout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.control_layout.addItem(spacerItem)
        self.measure_layout = QtWidgets.QVBoxLayout()
        self.measure_layout.setObjectName("measure_layout")
        self.single_spectrum_button = QtWidgets.QPushButton(self.control_frame)
        self.single_spectrum_button.setEnabled(False)
        self.single_spectrum_button.setCheckable(False)
        self.single_spectrum_button.setChecked(False)
        self.single_spectrum_button.setAutoRepeat(False)
        self.single_spectrum_button.setAutoRepeatDelay(300)
        self.single_spectrum_button.setAutoDefault(False)
        self.single_spectrum_button.setDefault(False)
        self.single_spectrum_button.setFlat(False)
        self.single_spectrum_button.setObjectName("single_spectrum_button")
        self.measure_layout.addWidget(self.single_spectrum_button)
        self.play_stop_layout = QtWidgets.QHBoxLayout()
        self.play_stop_layout.setObjectName("play_stop_layout")
        self.play_button = QtWidgets.QPushButton(self.control_frame)
        self.play_button.setEnabled(False)
        self.play_button.setObjectName("play_button")
        self.play_stop_layout.addWidget(self.play_button)
        self.stop_button = QtWidgets.QPushButton(self.control_frame)
        self.stop_button.setObjectName("stop_button")
        self.play_stop_layout.addWidget(self.stop_button)
        self.measure_layout.addLayout(self.play_stop_layout)
        self.control_layout.addLayout(self.measure_layout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.control_layout.addItem(spacerItem1)
        self.store_background_button = QtWidgets.QPushButton(self.control_frame)
        self.store_background_button.setEnabled(False)
        self.store_background_button.setObjectName("store_background_button")
        self.control_layout.addWidget(self.store_background_button)
        self.load_background_button = QtWidgets.QPushButton(self.control_frame)
        self.load_background_button.setEnabled(False)
        self.load_background_button.setObjectName("load_background_button")
        self.control_layout.addWidget(self.load_background_button)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.control_layout.addItem(spacerItem2)
        self.save_button = QtWidgets.QPushButton(self.control_frame)
        self.save_button.setEnabled(False)
        self.save_button.setObjectName("save_button")
        self.control_layout.addWidget(self.save_button)
        self.load_layout = QtWidgets.QHBoxLayout()
        self.load_layout.setObjectName("load_layout")
        self.load_button = QtWidgets.QPushButton(self.control_frame)
        self.load_button.setObjectName("load_button")
        self.load_layout.addWidget(self.load_button)
        self.previous_button = QtWidgets.QPushButton(self.control_frame)
        self.previous_button.setObjectName("previous_button")
        self.load_layout.addWidget(self.previous_button)
        self.next_button = QtWidgets.QPushButton(self.control_frame)
        self.next_button.setObjectName("next_button")
        self.load_layout.addWidget(self.next_button)
        self.control_layout.addLayout(self.load_layout)
        self.main_layout.addWidget(self.control_frame)
        self.plots_layout = QtWidgets.QGridLayout()
        self.plots_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.plots_layout.setObjectName("plots_layout")
        self.current_spectrum_plot = PlotWidget(self.horizontalLayoutWidget)
        self.current_spectrum_plot.setObjectName("current_spectrum_plot")
        self.plots_layout.addWidget(self.current_spectrum_plot, 0, 0, 1, 1)
        self.average_spectrum_plot = PlotWidget(self.horizontalLayoutWidget)
        self.average_spectrum_plot.setObjectName("average_spectrum_plot")
        self.plots_layout.addWidget(self.average_spectrum_plot, 1, 0, 1, 1)
        self.spectrometer_counts_plot = PlotWidget(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spectrometer_counts_plot.sizePolicy().hasHeightForWidth())
        self.spectrometer_counts_plot.setSizePolicy(sizePolicy)
        self.spectrometer_counts_plot.setMinimumSize(QtCore.QSize(100, 100))
        self.spectrometer_counts_plot.setMaximumSize(QtCore.QSize(100000, 100000))
        self.spectrometer_counts_plot.setObjectName("spectrometer_counts_plot")
        self.plots_layout.addWidget(self.spectrometer_counts_plot, 0, 1, 1, 1)
        self.spectrometer_counts_plot_2 = PlotWidget(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spectrometer_counts_plot_2.sizePolicy().hasHeightForWidth())
        self.spectrometer_counts_plot_2.setSizePolicy(sizePolicy)
        self.spectrometer_counts_plot_2.setMinimumSize(QtCore.QSize(100, 100))
        self.spectrometer_counts_plot_2.setMaximumSize(QtCore.QSize(100000, 100000))
        self.spectrometer_counts_plot_2.setObjectName("spectrometer_counts_plot_2")
        self.plots_layout.addWidget(self.spectrometer_counts_plot_2, 1, 1, 1, 1)
        self.plots_layout.setColumnStretch(0, 3)
        self.plots_layout.setColumnStretch(1, 2)
        self.plots_layout.setRowStretch(0, 1)
        self.plots_layout.setRowStretch(1, 1)
        self.main_layout.addLayout(self.plots_layout)
        self.main_layout.setStretch(0, 1)
        self.main_layout.setStretch(1, 4)

        self.retranslateUi(spectrometer_widget)
        QtCore.QMetaObject.connectSlotsByName(spectrometer_widget)

    def retranslateUi(self, spectrometer_widget):
        _translate = QtCore.QCoreApplication.translate
        spectrometer_widget.setWindowTitle(_translate("spectrometer_widget", "Spectrometer"))
        self.initialise_button.setText(_translate("spectrometer_widget", "Initialise"))
        self.initialise_label.setText(_translate("spectrometer_widget", "Status: not connected"))
        self.integration_time_label.setText(_translate("spectrometer_widget", "Integration time (ms)"))
        self.integration_time_edit.setText(_translate("spectrometer_widget", "100"))
        self.scans_average_label.setText(_translate("spectrometer_widget", "Scans to average"))
        self.scans_average_edit.setText(_translate("spectrometer_widget", "1"))
        self.filter_checkbox.setText(_translate("spectrometer_widget", "Filter from (nm)"))
        self.filter_lower_limit_edit.setText(_translate("spectrometer_widget", "400"))
        self.to_label.setText(_translate("spectrometer_widget", "to"))
        self.filter_upper_limit_edit.setText(_translate("spectrometer_widget", "1100"))
        self.electrical_dark_checkbox.setText(_translate("spectrometer_widget", "Correct for electrical dark"))
        self.substract_background_checkbox.setText(_translate("spectrometer_widget", "Substract background"))
        self.single_spectrum_button.setText(_translate("spectrometer_widget", "Get Single Spectrum"))
        self.play_button.setText(_translate("spectrometer_widget", "Play"))
        self.stop_button.setText(_translate("spectrometer_widget", "Stop"))
        self.store_background_button.setText(_translate("spectrometer_widget", "Store spectrum as background"))
        self.load_background_button.setText(_translate("spectrometer_widget", "Load spectrum as background"))
        self.save_button.setText(_translate("spectrometer_widget", "Save"))
        self.load_button.setText(_translate("spectrometer_widget", "Load"))
        self.previous_button.setText(_translate("spectrometer_widget", "Previous"))
        self.next_button.setText(_translate("spectrometer_widget", "Next"))
from pyqtgraph import PlotWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    spectrometer_widget = QtWidgets.QWidget()
    ui = Ui_spectrometer_widget()
    ui.setupUi(spectrometer_widget)
    spectrometer_widget.show()
    sys.exit(app.exec_())
