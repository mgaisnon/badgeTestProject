from src.porte import Porte


class PorteDeTest(Porte):
    def __init__(self):
        self.secure_mode = False
        self.signal_ouverture_reçu = False 
    
    def demander_ouverture(self):
        if not self.signal_ouverture_reçu:
            self.signal_ouverture_reçu = True
            print("Demande d'ouverture de la porte reçue")
            return True
        return False 