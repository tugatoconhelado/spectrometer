import dataclasses
import abc
import json
import pickle
import os
import datetime
from PySide2.QtWidgets import QFileDialog, QApplication, QWidget


class LoadLogic(abc.ABC):

    def load(self):
        pass

class SaveLogic(abc.ABC):


    def get_path_for_experiment(self, experiment_name) -> str:

        if not os.path.isabs(self.savedir):
            self.savedir = os.path.abspath(self.savedir)

        directory = os.path.join(self.savedir, experiment_name)
        if not os.path.exists(directory):
            os.mkdir(directory)
        return directory

    @abc.abstractmethod
    def save(self, data):
        pass

class PickleSaver(SaveLogic):

    def __init__(self, savedir: str = 'data') -> None:

        self.savedir = savedir
        self.current_file = ''

    def save(self, data, filepath, addtimestamp: bool = True):

        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        if addtimestamp:
            filepath = os.path.join(filepath, 'SPR' + current_time + '.pickle')

        data_dict = data.to_dict()
        with open(filepath, 'wb') as file:
            pickle.dump(data_dict, file)

        self.current_file = filepath
        return filepath

class JSONSaver(SaveLogic):

    def __init__(self, savedir: str = 'data') -> None:

        self.savedir = savedir
        self.current_file = ''

    def save(self, data, filepath, addtimestamp: bool = True):

        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        if addtimestamp:
            filepath = os.path.join(filepath, 'SPR' + current_time + '.json')

        data_dict = data.to_dict()
        # Saves to json file
        with open(filepath, 'w') as file:
            json.dump(data_dict, file, indent=2)

        self.current_file = filepath
        return filepath

    def load(self, parent=None, data=None, directory='data', iterate=0):
        """
        Generates a File Dialog to select file to load.

        The loading with begin from the 'data' folder unless a different
        directory is given.
        Parameters
        ----------
        data : ExperimentData
            Instance of an object containing the data to be saved
        directory : str, optional
            Directory in which to start the File Dialog
        iterate : int, optional
            Indicates if the load should be iteratively, i.e., if the previous
            or next file with respect with the current file should be loaded.

        Returns
        -------
        filename : str
            Indicates the name of the loaded file

        """

        if iterate != 0:
            return self.load_iteratively(data=data, directory=directory, iterate=iterate)
        dialog = QFileDialog(parent)
        print('Opening')
        directory = os.path.join(os.getcwd(), directory)
        dialog.setDirectory(directory)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter('JSON Files (*.json);; Pickle Files (*.pickle)')
        dialog.setViewMode(QFileDialog.ViewMode.Detail)
        if dialog.exec_():
            filename = dialog.selectedFiles()[0]
            filter = dialog.selectedNameFilter()

        if filter == 'Pickle Files (*.pickle)':
            self.load_pickle(data, filename)
        elif filter == 'JSON Files (*.json)':
            self.load_json(data, filename)

        self.current_file = filename
        return filename

    def load_json(self, data, filename):

        print(f'Loading file {filename}')
        with open(filename, 'r') as file:
            loaded_data = json.load(file)

        return data.from_dict(loaded_data['Experiment_Data'])

    def load_pickle(self, data, filename):

        print(f'Loading file {filename}')
        with open(filename, 'rb') as file:
            loaded_data = pickle.load(file)

        return data.from_dict(loaded_data['Experiment_Data'])

    def load_iteratively(self, data=None, directory='data', iterate=1) -> str:
        """
        Loads a previous or next file with respect to the current file.

        It looks based on the value of position. The search is in the current
        save directory. If the current file is '' it loads the last file in 
        the folder.

        Parameters
        ----------
        data : ExperimentData
            Contains the data to be saved
        directory : str
            Directory in which to look for files
        position : int, optional
            Indicates to move to next (position = 1) or previous file
            (position = -1). It can only take values 1 or -1.

        Returns
        -------
        filename : str
            Name of the file loaded or None if no file was found.

        """

        files = [os.path.join(directory, file) for file in os.listdir(directory)]
        if self.current_file == '':
            self.current_file = files[-1]
            iterate = 0
        if self.current_file in files:
            # Gets the cycling over the files (4%4=0, 5%4=1, ...)
            new_file_index = (files.index(self.current_file) + iterate ) % len(files)
            filename = files[new_file_index]
            self.current_file = filename
            self.load_json(data, filename)
            return filename
        else:
            print('No previous or next file found')
            return None









if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    widget = QWidget()
    widget.show()
    saver = SaveLogic()
    dir = saver.get_path_for_experiment('spectra')
    saver.load(None, None, dir, iterate=0)
    sys.exit(app.exec_())
