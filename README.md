# Spectrometer
---
## Dependencies
---

The dependencies needed for the program to run are:

- `PyQt5`: For graphical user interface.
- `pyqtgraph`: Python graphics for data displaying.
- `seabreeze`: Connection with ocean optics spectrometer. More info [here](https://python-seabreeze.readthedocs.io/en/latest/).
- `numpy`: Data manipulation and storage.


## Logic

In a normal run what will happen is:

User changes integration time -> *controller* will check if the change is valid -> if it is it will update the value on the data class (the model)

When a value in the model changes, it will let the view and the controller know that they must update their data.

This way, when a measurement is being performed and you alter the values, a new instance of the data class will be created and stored in the model.
