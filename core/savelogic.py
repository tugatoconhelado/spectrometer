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

        if not os.path.isabs(self.data_dir):
            self.data_dir = os.path.abspath(self.data_dir)

        directory = os.path.join(self.data_dir, experiment_name)
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

    def __init__(self, data_dir: str = 'data', experiment_name: str = 'generic', data=None) -> None:

        self.data_dir = data_dir
        self.save_dir = self.get_path_for_experiment(experiment_name)
        self.current_file = ''
        self.data = data

    def save(self, parent, add_timestamp: bool = True):

        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        if add_timestamp:
            file_path = os.path.join(self.save_dir, 'SPR' + current_time + '.json')

        data_dict = self.data.to_dict()
        # Saves to json file
        with open(file_path, 'w') as file:
            json.dump(data_dict, file, indent=2)

        self.current_file = file_path
        print(f'Saved to {file_path}')
        return file_path

    def load(self, parent=None, iterate=0):
        """
        Generates a File Dialog to select file to load.

        The loading with begin from the 'data' folder unless a different
        directory is given.
        Parameters
        ----------
        parent : QWidget
            QWidget that will be the parent for the QFileDialog
        iterate : int, optional
            Indicates if the load should be iteratively, i.e., if the previous
            or next file with respect with the current file should be loaded.

        Returns
        -------
        filename : str
            Indicates the name of the loaded file

        """

        if iterate != 0:
            return self.load_iteratively(iterate=iterate)
        dialog = QFileDialog(parent)
        print('Opening')
        directory = self.save_dir
        dialog.setDirectory(directory)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter('JSON Files (*.json);; Pickle Files (*.pickle)')
        dialog.setViewMode(QFileDialog.ViewMode.Detail)
        if dialog.exec_():
            file_path = dialog.selectedFiles()[0]
            file_type = dialog.selectedNameFilter()
        else:
            return ''

        if file_type == 'Pickle Files (*.pickle)':
            self.load_pickle(file_path)
        elif file_type == 'JSON Files (*.json)':
            self.load_json(file_path)

        self.current_file = file_path
        return file_path

    def load_json(self, filename):

        print(f'Loading file {filename}')
        with open(filename, 'r') as file:
            loaded_data = json.load(file)

        return self.data.from_dict(loaded_data['Experiment_Data'])

    def load_pickle(self, filename):

        print(f'Loading file {filename}')
        with open(filename, 'rb') as file:
            loaded_data = pickle.load(file)

        return self.data.from_dict(loaded_data['Experiment_Data'])

    def load_iteratively(self, iterate=1) -> str:
        """
        Loads a previous or next file with respect to the current file.

        It looks based on the value of position. The search is in the current
        save directory. If the current file is '' it loads the last file in 
        the folder.

        Parameters
        ----------
        iterate : int, optional
            Indicates to move to next (position = 1) or previous file
            (position = -1). It can only take values 1 or -1.

        Returns
        -------
        filename : str
            Name of the file loaded or None if no file was found.

        """
        directory = self.save_dir
        files = [os.path.join(directory, file) for file in os.listdir(directory)]
        if len(files) == 0:
            print(f'No files found in {directory}')
            return ''

        # If no file has been saved or loaded the current file is the
        # last in the directory (the latest saved file)
        if self.current_file == '':
            self.current_file = files[-1]
            iterate = 0

        if self.current_file in files:
            # Gets the cycling over the files (4%4=0, 5%4=1, ...)
            new_file_index = (files.index(self.current_file) + iterate ) % len(files)
            file_path = files[new_file_index]
            self.current_file = file_path
            self.load_json(file_path)
            return file_path
        else:
            print('No previous or next file found')
            return ''


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    widget = QWidget()
    widget.show()
    saver = SaveLogic()
    dir = saver.get_path_for_experiment('spectra')
    saver.load(None, None, dir, iterate=0)
    sys.exit(app.exec_())
