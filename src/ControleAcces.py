from .lecteur import Lecteur
from .porte import Porte

class ControleAcces:
    def __init__(self, porte: Porte, lecteur: Lecteur, whitelist: list):
        self.__lecteur = lecteur
        self.__porte = porte
        self.__whitelist = whitelist

    def interroger_lecteur(self):
        badge_detecte = self.__lecteur.poll()  
        if badge_detecte is not None:
            if badge_detecte in self.__whitelist:  
                self.__porte.demander_ouverture()
                print("Accès autorisé")  
            else:
                print("Accès refusé : Badge non autorisé")
        else:
            print("Aucun badge détecté")