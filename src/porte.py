import abc

class Porte(abc.ABC):
    def __init__(self):
        self.secure_mode = False  # Mode sécurisé désactivé par défaut   
        self.signal_ouverture_reçu = False 

    @abc.abstractmethod
    def demander_ouverture(self):
        pass
