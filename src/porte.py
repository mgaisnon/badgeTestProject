import abc

class Porte(abc.ABC):
    @abc.abstractmethod
    def demander_ouverture(self):
        pass