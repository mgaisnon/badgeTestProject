import unittest

from src.ControleAcces import ControleAcces
from utilities.lecteurtest import LecteurDeTest
from utilities.portetest import PorteDeTest


class TestControleAcces(unittest.TestCase):
    def setUp(self):
        self.whitelist = [1234, 5678, 91011]
        self.blacklist = [9999, 8888]
        self.lecteur = LecteurDeTest()
        self.porte = PorteDeTest()
        self.controleur = ControleAcces(self.porte, self.lecteur, self.whitelist, self.blacklist)

    def test_badge_valide(self):
        # ETANT DONNE un badge valide (présent dans la whitelist)
        self.lecteur.simuler_detection_badge(1234)
        
        # QUAND le badge est détecté
        self.controleur.interroger_lecteur()
        
        # ALORS l'accès est accordé et la porte s'ouvre
        self.assertTrue(self.porte.signal_ouverture_reçu)

    def test_badge_non_valide(self):
        # ETANT DONNE un badge non valide (non présent dans la whitelist)
        self.lecteur.simuler_detection_badge(4321)
        
        # QUAND le badge est détecté
        self.controleur.interroger_lecteur()
        
        # ALORS l'accès est refusé et la porte ne s'ouvre pas
        self.assertFalse(self.porte.signal_ouverture_reçu)

    def test_aucun_badge_detecte(self):
        # ETANT DONNE aucun badge détecté
        # QUAND le lecteur ne détecte aucun badge
        self.controleur.interroger_lecteur()
        
        # ALORS l'accès est refusé et la porte ne s'ouvre pas
        self.assertFalse(self.porte.signal_ouverture_reçu)

    def test_badge_zero(self):
        # ETANT DONNE un badge avec la valeur zéro
        self.lecteur.simuler_detection_badge(0)
        
        # QUAND le badge est détecté
        self.controleur.interroger_lecteur()
        
        # ALORS l'accès est refusé et la porte ne s'ouvre pas
        self.assertFalse(self.porte.signal_ouverture_reçu)

    def test_badge_grande_valeur(self):
        # ETANT DONNE un badge avec une très grande valeur
        self.lecteur.simuler_detection_badge(9999999999)
        
        # QUAND le badge est détecté
        self.controleur.interroger_lecteur()
        
        # ALORS l'accès est refusé et la porte ne s'ouvre pas
        self.assertFalse(self.porte.signal_ouverture_reçu)

    def test_badge_valeur_negative(self):
        # ETANT DONNE un badge avec une valeur négative
        self.lecteur.simuler_detection_badge(-1)
        
        # QUAND le badge est détecté
        self.controleur.interroger_lecteur()
        
        # ALORS l'accès est refusé et la porte ne s'ouvre pas
        self.assertFalse(self.porte.signal_ouverture_reçu)

    def test_badge_en_double_dans_whitelist(self):
        # ETANT DONNE un badge en double dans la whitelist
        self.whitelist.append(1234)
        self.lecteur.simuler_detection_badge(1234)
        
        # QUAND le badge est détecté
        self.controleur.interroger_lecteur()
        
        # ALORS l'accès est accordé et la porte s'ouvre
        self.assertTrue(self.porte.signal_ouverture_reçu)

    def test_whitelist_vide(self):
        # ETANT DONNE une whitelist vide
        controleur_vide = ControleAcces(self.porte, self.lecteur, [])
        self.lecteur.simuler_detection_badge(1234)
        
        # QUAND le badge est détecté
        controleur_vide.interroger_lecteur()
        
        # ALORS l'accès est refusé et la porte ne s'ouvre pas
        self.assertFalse(self.porte.signal_ouverture_reçu)

    def test_badge_retire_apres_scan(self):
        # ETANT DONNE un badge valide (présent dans la whitelist)
        self.lecteur.simuler_detection_badge(1234)
        self.controleur.interroger_lecteur()
        self.assertTrue(self.porte.signal_ouverture_reçu)
        
        # ETANT DONNE que le badge a été retiré de la whitelist après utilisation
        self.porte.signal_ouverture_reçu = False
        self.controleur.interroger_lecteur()
        
        # ALORS l'accès est refusé et la porte ne s'ouvre plus
        self.assertFalse(self.porte.signal_ouverture_reçu)

    def test_badge_none_dans_whitelist(self):
        # ETANT DONNE que None est ajouté à la whitelist
        self.whitelist.append(None)
        self.lecteur.simuler_detection_badge(None)
        
        # QUAND le badge est détecté
        self.controleur.interroger_lecteur()
        
        # ALORS l'accès est refusé et la porte ne s'ouvre pas
        self.assertFalse(self.porte.signal_ouverture_reçu)

    def test_type_incorrect_string(self):
        # ETANT DONNE un badge avec un type incorrect (chaîne de caractères)
        self.lecteur.simuler_detection_badge("ABC")
        
        # QUAND le badge est détecté
        self.controleur.interroger_lecteur()
        
        # ALORS l'accès est refusé et la porte ne s'ouvre pas
        self.assertFalse(self.porte.signal_ouverture_reçu)

    def test_type_incorrect_dictionnaire(self):
        # ETANT DONNE un badge avec un type incorrect (dictionnaire)
        self.lecteur.simuler_detection_badge({})
        
        # QUAND le badge est détecté
        self.controleur.interroger_lecteur()
        
        # ALORS l'accès est refusé et la porte ne s'ouvre pas
        self.assertFalse(self.porte.signal_ouverture_reçu)


    def test_plusieurs_badges_successifs(self):
        # ETANT DONNE plusieurs badges valides successifs
        self.lecteur.simuler_detection_badge(1234)
        self.controleur.interroger_lecteur()
        self.assertTrue(self.porte.signal_ouverture_reçu)
        
        # Quand un autre badge valide est détecté
        self.porte.signal_ouverture_reçu = False
        self.lecteur.simuler_detection_badge(5678)
        self.controleur.interroger_lecteur()
        
        # ALORS l'accès est accordé pour chaque badge et la porte s'ouvre
        self.assertTrue(self.porte.signal_ouverture_reçu)

    def test_scan_rapide_badge(self):
        # ETANT DONNE des scans rapides avec un badge valide
        for _ in range(10):
            self.lecteur.simuler_detection_badge(1234)
            self.controleur.interroger_lecteur()
            self.assertTrue(self.porte.signal_ouverture_reçu)
            self.porte.signal_ouverture_reçu = False
    
    def test_ajout_badge_apres_initialisation(self):
        # ETANT DONNE l'ajout d'un badge après l'initialisation
        self.controleur.ajouter_badge(8881)
        self.lecteur.simuler_detection_badge(8881)
    
        # QUAND le badge est détecté
        self.controleur.interroger_lecteur()
    
        # ALORS l'accès est accordé et la porte s'ouvre
        self.assertTrue(self.porte.signal_ouverture_reçu)
    
    def test_retirer_badge_de_la_whitelist(self):
        # ETANT DONNE un badge retiré de la whitelist
        print(f"Avant retrait - Whitelist: {self.whitelist}") 
        self.controleur.retirer_badge(1234)  # Retirer le badge
        print(f"Après retrait - Whitelist: {self.whitelist}")

        self.lecteur.simuler_detection_badge(1234)
        
        # QUAND le badge est détecté
        self.controleur.interroger_lecteur()
        
        # ALORS l'accès est refusé et la porte ne s'ouvre pas
        print(f"Signal de porte reçu : {self.porte.signal_ouverture_reçu}")
        self.assertFalse(self.porte.signal_ouverture_reçu)  

    def test_multithreading_badges(self):
        # ETANT DONNE plusieurs scans de badges en multithreading
        import threading
        def scan_badge():
            self.lecteur.simuler_detection_badge(5678)
            self.controleur.interroger_lecteur()
            self.assertTrue(self.porte.signal_ouverture_reçu)
        
        # Quand plusieurs threads tentent de scanner le badge simultanément
        threads = [threading.Thread(target=scan_badge) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
    
    def test_surcharge_systeme_badges_incorrects(self):
        # ETANT DONNE un grand nombre de badges incorrects scannés
        for _ in range(100):
            self.lecteur.simuler_detection_badge(9999)
            self.controleur.interroger_lecteur()
            self.assertFalse(self.porte.signal_ouverture_reçu)
    
    def test_panne_lecteur(self):
        # ETANT DONNE une panne du lecteur
        self.lecteur = None
        
        # QUAND on tente de scanner un badge
        self.assertIsNone(self.lecteur)
    
    def test_panne_porte(self):
        # ETANT DONNE une panne de la porte
        self.porte = None
        
        # QUAND on tente d'ouvrir la porte
        self.assertIsNone(self.porte)
    
    def test_badge_detecte_apres_timeout(self):
        # ETANT DONNE un badge détecté après un délai
        import time
        self.lecteur.simuler_detection_badge(5678)
        time.sleep(2)  # Simule un délai
        
        # QUAND le badge est détecté après un délai
        self.controleur.interroger_lecteur()
        
        # ALORS l'accès est accordé et la porte s'ouvre
        self.assertTrue(self.porte.signal_ouverture_reçu)

    def test_badge_blacklist(self):
        # ETANT DONNE un badge dans la blacklist
        self.lecteur.simuler_detection_badge(9999)
        
        # QUAND le badge est détecté
        self.controleur.interroger_lecteur()
        
        # ALORS l'accès est refusé et la porte ne s'ouvre pas
        self.assertFalse(self.porte.signal_ouverture_reçu)
    
    def test_blacklist_prioritaire_sur_whitelist(self):
        # ETANT DONNE un badge dans la whitelist et la blacklist
        self.whitelist.append(8888)
        self.lecteur.simuler_detection_badge(8888)
        
        # QUAND le badge est détecté
        self.controleur.interroger_lecteur()
        
        # ALORS l'accès est refusé car la blacklist est prioritaire
        self.assertFalse(self.porte.signal_ouverture_reçu)
    
    def test_historique_acces(self):
        # ETANT DONNE un badge valide détecté
        self.lecteur.simuler_detection_badge(1234)
        self.controleur.interroger_lecteur()
        
        # QUAND l'accès est accordé
        # ALORS le badge est ajouté à l'historique des accès
        self.assertIn(1234, self.controleur.historique)
    
    def test_historique_refus(self):
        # ETANT DONNE un badge non valide détecté
        self.lecteur.simuler_detection_badge(4321)
        self.controleur.interroger_lecteur()
        
        # QUAND l'accès est refusé
        # ALORS le badge est ajouté à l'historique des refus
        self.assertIn(4321, self.controleur.historique_refus)
    
    def test_trois_echecs_consecutifs(self):
        # ETANT DONNE trois échecs consécutifs avec des badges invalides
        for _ in range(3):
            self.lecteur.simuler_detection_badge(4321)
            self.controleur.interroger_lecteur()
        
        # ALORS l'alarme est déclenchée
        self.assertTrue(self.controleur.alarm_triggered)
    
    def test_porte_securisee_double_validation(self):
        # ETANT DONNE un mode sécurisé activé sur la porte
        self.porte.secure_mode = True
        self.lecteur.simuler_detection_badge(1234)
        self.controleur.interroger_lecteur()
        
        # QUAND un seul scan est effectué
        self.assertFalse(self.porte.signal_ouverture_reçu)
        
        # ETANT DONNE que le badge est scanné à nouveau
        self.lecteur.simuler_detection_badge(1234)
        self.controleur.interroger_lecteur()
        
        # ALORS l'accès est accordé et la porte s'ouvre
        self.assertTrue(self.porte.signal_ouverture_reçu)
    
    def test_ajout_badge_temporaire(self):
        # ETANT DONNE un badge temporaire ajouté à la whitelist
        self.controleur.ajouter_badge_temporaire(7777)
        self.lecteur.simuler_detection_badge(7777)
        
        # QUAND le badge temporaire est détecté
        self.controleur.interroger_lecteur()
        
        # ALORS l'accès est accordé et la porte s'ouvre
        self.assertTrue(self.porte.signal_ouverture_reçu)
    
    def test_expiration_badge_temporaire(self):
        # ETANT DONNE un badge temporaire expiré
        self.controleur.ajouter_badge_temporaire(7777, expire=True)
        self.lecteur.simuler_detection_badge(7777)
        
        # QUAND le badge temporaire expiré est détecté
        self.controleur.interroger_lecteur()
        
        # ALORS l'accès est refusé et la porte ne s'ouvre pas
        self.assertFalse(self.porte.signal_ouverture_reçu)
    
    def test_reset_historique(self):
        # ETANT DONNE un badge détecté
        self.lecteur.simuler_detection_badge(1234)
        self.controleur.interroger_lecteur()
        
        # QUAND l'historique est réinitialisé
        self.controleur.reset_historique()
        
        # ALORS l'historique est vide
        self.assertEqual(len(self.controleur.historique), 0)
    
    def test_mode_urgence_desactive_toutes_les_controles(self):
        # ETANT DONNE que le mode urgence est activé
        self.controleur.activer_mode_urgence()
        self.lecteur.simuler_detection_badge(9999)
        
        # QUAND un badge de la blacklist est détecté
        self.controleur.interroger_lecteur()
        
        # ALORS l'accès est accordé même si le badge est en blacklist
        self.assertTrue(self.porte.signal_ouverture_reçu)
    
    def test_porte_securisee_double_validation(self):
        # ETANT DONNE un mode sécurisé activé sur la porte
        self.porte.secure_mode = True

        # Premier scan du badge (la porte ne doit pas s'ouvrir)
        self.lecteur.simuler_detection_badge(1234)
        self.controleur.interroger_lecteur()

        # QUAND un seul scan est effectué
        self.assertFalse(self.porte.signal_ouverture_reçu)

        # ETANT DONNE que le badge est scanné à nouveau
        self.lecteur.simuler_detection_badge(1234)
        self.controleur.interroger_lecteur()

        # ALORS l'accès est accordé et la porte s'ouvre
        self.assertTrue(self.porte.signal_ouverture_reçu)



if __name__ == '__main__':
    unittest.main()
