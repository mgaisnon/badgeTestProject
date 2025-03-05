import unittest
from datetime import datetime

from src.ControleAcces import ControleAcces
from utilities.lecteurtest import LecteurDeTest
from utilities.portetest import PorteDeTest


class TestControleAcces(unittest.TestCase):        
    def test_badge_valide(self):
        # ETANT DONNE un badge valide
        whitelist = [1234, 5678, 91011]  # Liste des badges autorisés
        lecteur = LecteurDeTest()
        porte = PorteDeTest()
        controleur = ControleAcces(porte, lecteur, whitelist)

        lecteur.simuler_detection_badge(1234)  # Badge valide (présent dans la whitelist)
        
        # QUAND le badge est détecté
        controleur.interroger_lecteur()
        
        # ALORS l'accès est accordé et la porte s'ouvre
        self.assertTrue(porte.signal_ouverture_reçu)  # La porte doit s'ouvrir

    def test_badge_non_valide(self):
        # ETANT DONNE un badge non valide
        whitelist = [1234, 5678, 91011]  # Liste des badges autorisés
        lecteur = LecteurDeTest()
        porte = PorteDeTest()
        controleur = ControleAcces(porte, lecteur, whitelist)

        lecteur.simuler_detection_badge(4321)  # Badge non valide (non présent dans la whitelist)
        
        # QUAND le badge est détecté
        controleur.interroger_lecteur()
        
        # ALORS l'accès est refusé et la porte ne doit pas s'ouvrir
        self.assertFalse(porte.signal_ouverture_reçu)  # La porte ne doit pas s'ouvrir


if __name__ == '__main__':
    unittest.main()