import abc


class ExperimentLogic(abc.ABC):

    @abc.abstractmethod
    def run_experiment(self):

        pass

    @abc.abstractmethod
    def save_data(self):

        pass

