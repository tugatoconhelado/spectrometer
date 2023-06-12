# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'spectrometerKydvBf.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from pyqtgraph import PlotWidget

class Ui_spectrometer_widget(object):
    def setupUi(self, spectrometer_widget):
        if not spectrometer_widget.objectName():
            spectrometer_widget.setObjectName(u"spectrometer_widget")
        spectrometer_widget.resize(1279, 642)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(spectrometer_widget.sizePolicy().hasHeightForWidth())
        spectrometer_widget.setSizePolicy(sizePolicy)
        self.horizontalLayoutWidget = QWidget(spectrometer_widget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 0, 1051, 621))
        self.main_layout = QHBoxLayout(self.horizontalLayoutWidget)
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setSizeConstraint(QLayout.SetMinimumSize)
        self.main_layout.setContentsMargins(2, 2, 2, 2)
        self.control_frame = QFrame(self.horizontalLayoutWidget)
        self.control_frame.setObjectName(u"control_frame")
        self.control_frame.setMaximumSize(QSize(350, 600))
        self.control_frame.setFrameShape(QFrame.Box)
        self.control_frame.setFrameShadow(QFrame.Raised)
        self.control_layout = QVBoxLayout(self.control_frame)
        self.control_layout.setSpacing(2)
        self.control_layout.setObjectName(u"control_layout")
        self.control_layout.setSizeConstraint(QLayout.SetMaximumSize)
        self.initialise_layout = QHBoxLayout()
        self.initialise_layout.setObjectName(u"initialise_layout")
        self.initialise_button = QPushButton(self.control_frame)
        self.initialise_button.setObjectName(u"initialise_button")

        self.initialise_layout.addWidget(self.initialise_button)

        self.initialise_label = QLabel(self.control_frame)
        self.initialise_label.setObjectName(u"initialise_label")
        self.initialise_label.setTextFormat(Qt.AutoText)

        self.initialise_layout.addWidget(self.initialise_label)


        self.control_layout.addLayout(self.initialise_layout)

        self.integration_time_layout = QHBoxLayout()
        self.integration_time_layout.setObjectName(u"integration_time_layout")
        self.integration_time_label = QLabel(self.control_frame)
        self.integration_time_label.setObjectName(u"integration_time_label")

        self.integration_time_layout.addWidget(self.integration_time_label)

        self.integration_time_edit = QLineEdit(self.control_frame)
        self.integration_time_edit.setObjectName(u"integration_time_edit")
        self.integration_time_edit.setEnabled(False)
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.integration_time_edit.sizePolicy().hasHeightForWidth())
        self.integration_time_edit.setSizePolicy(sizePolicy1)
        self.integration_time_edit.setMaximumSize(QSize(100, 100))
        self.integration_time_edit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.integration_time_layout.addWidget(self.integration_time_edit)


        self.control_layout.addLayout(self.integration_time_layout)

        self.scans_average_layout = QHBoxLayout()
        self.scans_average_layout.setObjectName(u"scans_average_layout")
        self.scans_average_label = QLabel(self.control_frame)
        self.scans_average_label.setObjectName(u"scans_average_label")

        self.scans_average_layout.addWidget(self.scans_average_label)

        self.scans_average_edit = QLineEdit(self.control_frame)
        self.scans_average_edit.setObjectName(u"scans_average_edit")
        self.scans_average_edit.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.scans_average_edit.sizePolicy().hasHeightForWidth())
        self.scans_average_edit.setSizePolicy(sizePolicy1)
        self.scans_average_edit.setMaximumSize(QSize(100, 100))
        self.scans_average_edit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.scans_average_layout.addWidget(self.scans_average_edit)


        self.control_layout.addLayout(self.scans_average_layout)

        self.filter_layout = QHBoxLayout()
        self.filter_layout.setObjectName(u"filter_layout")
        self.filter_checkbox = QCheckBox(self.control_frame)
        self.filter_checkbox.setObjectName(u"filter_checkbox")
        self.filter_checkbox.setEnabled(False)

        self.filter_layout.addWidget(self.filter_checkbox)

        self.filter_lower_limit_edit = QLineEdit(self.control_frame)
        self.filter_lower_limit_edit.setObjectName(u"filter_lower_limit_edit")
        self.filter_lower_limit_edit.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.filter_lower_limit_edit.sizePolicy().hasHeightForWidth())
        self.filter_lower_limit_edit.setSizePolicy(sizePolicy1)
        self.filter_lower_limit_edit.setMaximumSize(QSize(70, 100))
        self.filter_lower_limit_edit.setLayoutDirection(Qt.RightToLeft)
        self.filter_lower_limit_edit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.filter_layout.addWidget(self.filter_lower_limit_edit)

        self.to_label = QLabel(self.control_frame)
        self.to_label.setObjectName(u"to_label")

        self.filter_layout.addWidget(self.to_label)

        self.filter_upper_limit_edit = QLineEdit(self.control_frame)
        self.filter_upper_limit_edit.setObjectName(u"filter_upper_limit_edit")
        self.filter_upper_limit_edit.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.filter_upper_limit_edit.sizePolicy().hasHeightForWidth())
        self.filter_upper_limit_edit.setSizePolicy(sizePolicy1)
        self.filter_upper_limit_edit.setMaximumSize(QSize(70, 100))
        self.filter_upper_limit_edit.setLayoutDirection(Qt.LeftToRight)
        self.filter_upper_limit_edit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.filter_layout.addWidget(self.filter_upper_limit_edit)


        self.control_layout.addLayout(self.filter_layout)

        self.electrical_dark_layout = QHBoxLayout()
        self.electrical_dark_layout.setObjectName(u"electrical_dark_layout")
        self.electrical_dark_checkbox = QCheckBox(self.control_frame)
        self.electrical_dark_checkbox.setObjectName(u"electrical_dark_checkbox")
        self.electrical_dark_checkbox.setEnabled(False)

        self.electrical_dark_layout.addWidget(self.electrical_dark_checkbox)


        self.control_layout.addLayout(self.electrical_dark_layout)

        self.substract_background_layout = QHBoxLayout()
        self.substract_background_layout.setObjectName(u"substract_background_layout")
        self.substract_background_checkbox = QCheckBox(self.control_frame)
        self.substract_background_checkbox.setObjectName(u"substract_background_checkbox")
        self.substract_background_checkbox.setEnabled(False)

        self.substract_background_layout.addWidget(self.substract_background_checkbox)


        self.control_layout.addLayout(self.substract_background_layout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.control_layout.addItem(self.verticalSpacer)

        self.measure_layout = QVBoxLayout()
        self.measure_layout.setObjectName(u"measure_layout")
        self.single_spectrum_button = QPushButton(self.control_frame)
        self.single_spectrum_button.setObjectName(u"single_spectrum_button")
        self.single_spectrum_button.setEnabled(False)
        self.single_spectrum_button.setCheckable(False)
        self.single_spectrum_button.setChecked(False)
        self.single_spectrum_button.setAutoRepeat(False)
        self.single_spectrum_button.setAutoRepeatDelay(300)
        self.single_spectrum_button.setAutoDefault(False)
        self.single_spectrum_button.setFlat(False)

        self.measure_layout.addWidget(self.single_spectrum_button)

        self.play_stop_layout = QHBoxLayout()
        self.play_stop_layout.setObjectName(u"play_stop_layout")
        self.play_button = QPushButton(self.control_frame)
        self.play_button.setObjectName(u"play_button")
        self.play_button.setEnabled(False)

        self.play_stop_layout.addWidget(self.play_button)

        self.stop_button = QPushButton(self.control_frame)
        self.stop_button.setObjectName(u"stop_button")

        self.play_stop_layout.addWidget(self.stop_button)


        self.measure_layout.addLayout(self.play_stop_layout)


        self.control_layout.addLayout(self.measure_layout)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.control_layout.addItem(self.verticalSpacer_2)

        self.store_background_button = QPushButton(self.control_frame)
        self.store_background_button.setObjectName(u"store_background_button")
        self.store_background_button.setEnabled(False)

        self.control_layout.addWidget(self.store_background_button)

        self.load_background_button = QPushButton(self.control_frame)
        self.load_background_button.setObjectName(u"load_background_button")
        self.load_background_button.setEnabled(False)

        self.control_layout.addWidget(self.load_background_button)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.control_layout.addItem(self.verticalSpacer_3)

        self.save_button = QPushButton(self.control_frame)
        self.save_button.setObjectName(u"save_button")
        self.save_button.setEnabled(False)

        self.control_layout.addWidget(self.save_button)

        self.load_layout = QHBoxLayout()
        self.load_layout.setObjectName(u"load_layout")
        self.load_button = QPushButton(self.control_frame)
        self.load_button.setObjectName(u"load_button")

        self.load_layout.addWidget(self.load_button)

        self.previous_button = QPushButton(self.control_frame)
        self.previous_button.setObjectName(u"previous_button")

        self.load_layout.addWidget(self.previous_button)

        self.next_button = QPushButton(self.control_frame)
        self.next_button.setObjectName(u"next_button")

        self.load_layout.addWidget(self.next_button)


        self.control_layout.addLayout(self.load_layout)


        self.main_layout.addWidget(self.control_frame)

        self.plots_layout = QGridLayout()
        self.plots_layout.setObjectName(u"plots_layout")
        self.plots_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.current_spectrum_plot = PlotWidget(self.horizontalLayoutWidget)
        self.current_spectrum_plot.setObjectName(u"current_spectrum_plot")

        self.plots_layout.addWidget(self.current_spectrum_plot, 0, 0, 1, 1)

        self.average_spectrum_plot = PlotWidget(self.horizontalLayoutWidget)
        self.average_spectrum_plot.setObjectName(u"average_spectrum_plot")

        self.plots_layout.addWidget(self.average_spectrum_plot, 1, 0, 1, 1)

        self.spectrometer_counts_plot = PlotWidget(self.horizontalLayoutWidget)
        self.spectrometer_counts_plot.setObjectName(u"spectrometer_counts_plot")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.spectrometer_counts_plot.sizePolicy().hasHeightForWidth())
        self.spectrometer_counts_plot.setSizePolicy(sizePolicy2)
        self.spectrometer_counts_plot.setMinimumSize(QSize(100, 100))
        self.spectrometer_counts_plot.setMaximumSize(QSize(100000, 100000))

        self.plots_layout.addWidget(self.spectrometer_counts_plot, 0, 1, 1, 1)

        self.spectrometer_counts_plot_2 = PlotWidget(self.horizontalLayoutWidget)
        self.spectrometer_counts_plot_2.setObjectName(u"spectrometer_counts_plot_2")
        sizePolicy2.setHeightForWidth(self.spectrometer_counts_plot_2.sizePolicy().hasHeightForWidth())
        self.spectrometer_counts_plot_2.setSizePolicy(sizePolicy2)
        self.spectrometer_counts_plot_2.setMinimumSize(QSize(100, 100))
        self.spectrometer_counts_plot_2.setMaximumSize(QSize(100000, 100000))

        self.plots_layout.addWidget(self.spectrometer_counts_plot_2, 1, 1, 1, 1)

        self.plots_layout.setRowStretch(0, 1)
        self.plots_layout.setRowStretch(1, 1)
        self.plots_layout.setColumnStretch(0, 3)
        self.plots_layout.setColumnStretch(1, 2)

        self.main_layout.addLayout(self.plots_layout)

        self.main_layout.setStretch(0, 1)
        self.main_layout.setStretch(1, 4)

        self.retranslateUi(spectrometer_widget)

        self.single_spectrum_button.setDefault(False)


        QMetaObject.connectSlotsByName(spectrometer_widget)
    # setupUi

    def retranslateUi(self, spectrometer_widget):
        spectrometer_widget.setWindowTitle(QCoreApplication.translate("spectrometer_widget", u"Spectrometer", None))
        self.initialise_button.setText(QCoreApplication.translate("spectrometer_widget", u"Initialise", None))
        self.initialise_label.setText(QCoreApplication.translate("spectrometer_widget", u"Status: not connected", None))
        self.integration_time_label.setText(QCoreApplication.translate("spectrometer_widget", u"Integration time (ms)", None))
        self.integration_time_edit.setText(QCoreApplication.translate("spectrometer_widget", u"100", None))
        self.scans_average_label.setText(QCoreApplication.translate("spectrometer_widget", u"Scans to average", None))
        self.scans_average_edit.setText(QCoreApplication.translate("spectrometer_widget", u"1", None))
        self.filter_checkbox.setText(QCoreApplication.translate("spectrometer_widget", u"Filter from (nm)", None))
        self.filter_lower_limit_edit.setText(QCoreApplication.translate("spectrometer_widget", u"400", None))
        self.to_label.setText(QCoreApplication.translate("spectrometer_widget", u"to", None))
        self.filter_upper_limit_edit.setText(QCoreApplication.translate("spectrometer_widget", u"1100", None))
        self.electrical_dark_checkbox.setText(QCoreApplication.translate("spectrometer_widget", u"Correct for electrical dark", None))
        self.substract_background_checkbox.setText(QCoreApplication.translate("spectrometer_widget", u"Substract background", None))
        self.single_spectrum_button.setText(QCoreApplication.translate("spectrometer_widget", u"Get Single Spectrum", None))
        self.play_button.setText(QCoreApplication.translate("spectrometer_widget", u"Play", None))
        self.stop_button.setText(QCoreApplication.translate("spectrometer_widget", u"Stop", None))
        self.store_background_button.setText(QCoreApplication.translate("spectrometer_widget", u"Store spectrum as background", None))
        self.load_background_button.setText(QCoreApplication.translate("spectrometer_widget", u"Load spectrum as background", None))
        self.save_button.setText(QCoreApplication.translate("spectrometer_widget", u"Save", None))
        self.load_button.setText(QCoreApplication.translate("spectrometer_widget", u"Load", None))
        self.previous_button.setText(QCoreApplication.translate("spectrometer_widget", u"Previous", None))
        self.next_button.setText(QCoreApplication.translate("spectrometer_widget", u"Next", None))
    # retranslateUi

