from src.porte import Porte


class PorteDeTest(Porte):
    def __init__(self):
        self.signal_ouverture_reçu = False

    def demander_ouverture(self):
        # Si la demande d'ouverture est reçue, on modifie le flag
        self.signal_ouverture_reçu = True