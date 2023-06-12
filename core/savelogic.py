import dataclasses
import json
import pickle
import os
import datetime
from PySide6.QtWidgets import QFileDialog, QApplication, QWidget

class SaveLogic:

    def __init__(self, savedir: str = 'data') -> None:
        
        self.savedir = savedir

    def save_json(self, data, filepath, addtimestamp: bool = True):

        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        if addtimestamp:
            filepath = os.path.join(filepath, 'SPR' + current_time + '.json')

        data_dict = data.to_dict()
        # Saves to json file
        with open(filepath, 'w') as file:
            json.dump(data_dict, file, indent=2)
        
        return filepath
    
    def save_pickle(self, data, filepath, addtimestamp: bool = True):

        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        if addtimestamp:
            filepath = os.path.join(filepath, 'SPR' + current_time + '.pickle')

        data_dict = data.to_dict()
        with open(filepath, 'wb') as file:
            pickle.dump(data_dict, file)

        return filepath
    
    def get_path_for_experiment(self, experiment_name):

        directory = os.path.join(self.savedir, experiment_name)
        if not os.path.exists(directory):
            os.mkdir(directory)
        return directory
    
    def load(self, parent=None, data=None, directory='data'):
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
        dialog = QFileDialog(parent=parent)
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


    
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    widget = QWidget()
    widget.show()
    saver = SaveLogic()
    print(saver.load(widget))
    sys.exit(app.exec())