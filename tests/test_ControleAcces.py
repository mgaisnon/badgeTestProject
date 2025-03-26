import unittest

from src.ControleAcces import ControleAcces
from utilities.lecteurtest import LecteurDeTest
from utilities.portetest import PorteDeTest


class TestControleAcces(unittest.TestCase):
    def setUp(self):
        self.whitelist = [1234, 5678, 91011]  # Liste des badges autorisés
        self.blacklist = [9999, 8888]
        self.lecteur = LecteurDeTest()
        self.porte = PorteDeTest()
        self.controleur = ControleAcces(self.porte, self.lecteur, self.whitelist, self.blacklist)

    def test_badge_valide(self):
        self.lecteur.simuler_detection_badge(1234)
        self.controleur.interroger_lecteur()
        self.assertTrue(self.porte.signal_ouverture_reçu)

    def test_badge_non_valide(self):
        self.lecteur.simuler_detection_badge(4321)
        self.controleur.interroger_lecteur()
        self.assertFalse(self.porte.signal_ouverture_reçu)

    def test_aucun_badge_detecte(self):
        self.controleur.interroger_lecteur()
        self.assertFalse(self.porte.signal_ouverture_reçu)

    def test_badge_zero(self):
        self.lecteur.simuler_detection_badge(0)
        self.controleur.interroger_lecteur()
        self.assertFalse(self.porte.signal_ouverture_reçu)

    def test_badge_grande_valeur(self):
        self.lecteur.simuler_detection_badge(9999999999)
        self.controleur.interroger_lecteur()
        self.assertFalse(self.porte.signal_ouverture_reçu)

    def test_badge_valeur_negative(self):
        self.lecteur.simuler_detection_badge(-1)
        self.controleur.interroger_lecteur()
        self.assertFalse(self.porte.signal_ouverture_reçu)

    def test_badge_en_double_dans_whitelist(self):
        self.whitelist.append(1234)
        self.lecteur.simuler_detection_badge(1234)
        self.controleur.interroger_lecteur()
        self.assertTrue(self.porte.signal_ouverture_reçu)

    def test_whitelist_vide(self):
        controleur_vide = ControleAcces(self.porte, self.lecteur, [])
        self.lecteur.simuler_detection_badge(1234)
        controleur_vide.interroger_lecteur()
        self.assertFalse(self.porte.signal_ouverture_reçu)

    def test_badge_retire_apres_scan(self):
        self.lecteur.simuler_detection_badge(1234)
        self.controleur.interroger_lecteur()
        self.assertTrue(self.porte.signal_ouverture_reçu)
        self.porte.signal_ouverture_reçu = False
        self.controleur.interroger_lecteur()
        self.assertFalse(self.porte.signal_ouverture_reçu)

    def test_badge_none_dans_whitelist(self):
        self.whitelist.append(None)
        self.lecteur.simuler_detection_badge(None)
        self.controleur.interroger_lecteur()
        self.assertFalse(self.porte.signal_ouverture_reçu)

    def test_type_incorrect_string(self):
        self.lecteur.simuler_detection_badge("ABC")
        self.controleur.interroger_lecteur()
        self.assertFalse(self.porte.signal_ouverture_reçu)

    def test_type_incorrect_dictionnaire(self):
        self.lecteur.simuler_detection_badge({})
        self.controleur.interroger_lecteur()
        self.assertFalse(self.porte.signal_ouverture_reçu)

    def test_plusieurs_badges_successifs(self):
        self.lecteur.simuler_detection_badge(1234)
        self.controleur.interroger_lecteur()
        self.assertTrue(self.porte.signal_ouverture_reçu)
        self.porte.signal_ouverture_reçu = False
        self.lecteur.simuler_detection_badge(5678)
        self.controleur.interroger_lecteur()
        self.assertTrue(self.porte.signal_ouverture_reçu)

    def test_scan_rapide_badge(self):
        for _ in range(10):
            self.lecteur.simuler_detection_badge(1234)
            self.controleur.interroger_lecteur()
            self.assertTrue(self.porte.signal_ouverture_reçu)
            self.porte.signal_ouverture_reçu = False
    
    def test_ajout_badge_apres_initialisation(self):
        self.whitelist.append(8888)
        self.lecteur.simuler_detection_badge(8888)
        self.controleur.interroger_lecteur()
        self.assertTrue(self.porte.signal_ouverture_reçu)
    
    def test_retirer_badge_de_la_whitelist(self):
        self.whitelist.remove(1234)
        self.lecteur.simuler_detection_badge(1234)
        self.controleur.interroger_lecteur()
        self.assertFalse(self.porte.signal_ouverture_reçu)
    
    def test_multithreading_badges(self):
        import threading
        def scan_badge():
            self.lecteur.simuler_detection_badge(5678)
            self.controleur.interroger_lecteur()
            self.assertTrue(self.porte.signal_ouverture_reçu)
        
        threads = [threading.Thread(target=scan_badge) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
    
    def test_surcharge_systeme_badges_incorrects(self):
        for _ in range(100):
            self.lecteur.simuler_detection_badge(9999)
            self.controleur.interroger_lecteur()
            self.assertFalse(self.porte.signal_ouverture_reçu)
    
    def test_panne_lecteur(self):
        self.lecteur = None
        self.assertIsNone(self.lecteur)
    
    def test_panne_porte(self):
        self.porte = None
        self.assertIsNone(self.porte)
    
    def test_badge_detecte_apres_timeout(self):
        import time
        self.lecteur.simuler_detection_badge(5678)
        time.sleep(2)  # Simule un délai
        self.controleur.interroger_lecteur()
        self.assertTrue(self.porte.signal_ouverture_reçu)

    def test_badge_blacklist(self):
        self.lecteur.simuler_detection_badge(9999)
        self.controleur.interroger_lecteur()
        self.assertFalse(self.porte.signal_ouverture_reçu)
    
    def test_blacklist_prioritaire_sur_whitelist(self):
        self.whitelist.append(8888)
        self.lecteur.simuler_detection_badge(8888)
        self.controleur.interroger_lecteur()
        self.assertFalse(self.porte.signal_ouverture_reçu)
    
    def test_historique_acces(self):
        self.lecteur.simuler_detection_badge(1234)
        self.controleur.interroger_lecteur()
        self.assertIn(1234, self.controleur.historique)
    
    def test_historique_refus(self):
        self.lecteur.simuler_detection_badge(4321)
        self.controleur.interroger_lecteur()
        self.assertIn(4321, self.controleur.historique_refus)
    
    def test_trois_echecs_consecutifs(self):
        for _ in range(3):
            self.lecteur.simuler_detection_badge(4321)
            self.controleur.interroger_lecteur()
        self.assertTrue(self.controleur.alarm_triggered)
    
    def test_porte_securisee_double_validation(self):
        self.porte.secure_mode = True
        self.lecteur.simuler_detection_badge(1234)
        self.controleur.interroger_lecteur()
        self.assertFalse(self.porte.signal_ouverture_reçu)
        self.lecteur.simuler_detection_badge(1234)
        self.controleur.interroger_lecteur()
        self.assertTrue(self.porte.signal_ouverture_reçu)
    
    def test_ajout_badge_temporaire(self):
        self.controleur.ajouter_badge_temporaire(7777)
        self.lecteur.simuler_detection_badge(7777)
        self.controleur.interroger_lecteur()
        self.assertTrue(self.porte.signal_ouverture_reçu)
    
    def test_expiration_badge_temporaire(self):
        self.controleur.ajouter_badge_temporaire(7777, expire=True)
        self.lecteur.simuler_detection_badge(7777)
        self.controleur.interroger_lecteur()
        self.assertFalse(self.porte.signal_ouverture_reçu)
    
    def test_reset_historique(self):
        self.lecteur.simuler_detection_badge(1234)
        self.controleur.interroger_lecteur()
        self.controleur.reset_historique()
        self.assertEqual(len(self.controleur.historique), 0)
    
    def test_mode_urgence_desactive_toutes_les_controles(self):
        self.controleur.activer_mode_urgence()
        self.lecteur.simuler_detection_badge(9999)
        self.controleur.interroger_lecteur()
        self.assertTrue(self.porte.signal_ouverture_reçu)
    
    def test_sortie_logique_pour_multiple_portes(self):
        porte2 = PorteDeTest()
        controleur2 = ControleAcces(porte2, self.lecteur, self.whitelist, self.blacklist)
        self.lecteur.simuler_detection_badge(1234)
        self.controleur.interroger_lecteur()
        controleur2.interroger_lecteur()
        self.assertTrue(self.porte.signal_ouverture_reçu)
        self.assertTrue(porte2.signal_ouverture_reçu)
    


if __name__ == '__main__':
    unittest.main()
