import os
import pyqtgraph as pg
import pandas as pd
from PySide6.QtWidgets import QFileDialog
from datetime import datetime

class SpectrumDataSaving:


    def __init__(self, view):

        self.view = view
        self.current_file = ''

    def save(self, directory='data'):
        """
        Saves current data being displayed.
        Note: It won't save the entire data, only the portion the user is
        currently viewing.

        The data will be saved in the specified directory, if it does not exists
        it will create it. If no directory is provided it will be saved in the
        'data' directory. Only the data in the current spectrum plot (upper
        left plot in the displayed window) will be saved.

        Parameters
        ----------
            folder (str): Directory in which to save the data.

        Returns
        -------
            status (bool): Indicates if the save was succesful
        """
        directory = 'data'
        if not os.path.exists(directory):
            print('creating data folder')
            os.mkdir('data')
            os.mkdir(os.path.join('data', 'png'))
        try:
            filename = 'SPR' + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            exporter = pg.exporters.ImageExporter(self.view.current_spectrum_plot.scene())
            csv_exporter = pg.exporters.CSVExporter(self.view.current_spectrum_plot.plotItem)
            savepath = os.path.join('data', filename)
            csv_exporter.export(savepath + '.csv')
            savepath = os.path.join('data', 'png', filename)
            exporter.export(savepath + '.png')
            return True
        except:
            return False

    def load(self, parent, directory='data'):
        """
        Generates a File Dialog to select file to load.

        The loading with begin from the 'data' folder unless a different
        directory is given.
        Parameters
        ----------
            directory : str, optional
            Directory in which to start the File Dialog

        Returns
        -------
            status : bool
            Indicates if the load was succesful

        """
        dialog = QFileDialog(parent)
        print('Opening')
        directory = os.path.join(os.getcwd(), directory)
        dialog.setDirectory(directory)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter('JSON Files (*.json);; Picle Files (*.pickle)')
        dialog.setViewMode(QFileDialog.ViewMode.Detail)
        if dialog.exec_():
            filename = dialog.selectedFiles()[0]
            return filename


    def load_iterate(self, position=1):
        """
        Loads a previous or next file with respect to the current file.

        It looks based on the value of position. The search is in the current
        save directory.

        Parameters
        ----------
        position : int, optional
            Indicates to move to next (position = 1) or previous file
            (position = -1). It can only take values 1 or -1.

        Returns
        -------
        status : bool
            Indicated wether the load was succesful or not.

        """

        if position == 1 or position == -1:
            directory = os.path.join(os.getcwd(), 'data')
            files = [os.path.join(directory, file) for file in os.listdir(directory)]
            if self.current_file in files:
                new_file = files.index(self.current_file) + position
                print(new_file)
                new_file = files[new_file]
                print(new_file)
        else:
            print('Load iteration value invalid (different from +-1)')
            return False



