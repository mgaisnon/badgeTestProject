class ControleAcces:
    def __init__(self, porte, lecteur, whitelist=None, blacklist=None):
        self.__lecteur = lecteur
        self.__porte = porte
        self.__whitelist = set(whitelist) if whitelist else set()
        self.__blacklist = set(blacklist) if blacklist else set()
        self.historique = []
        self.historique_refus = []
        self.echecs_consecutifs = {}
        self.alarm_triggered = False
        self.badges_temporaires = set()
        self.mode_urgence = False
        self.double_validation = {}

    def interroger_lecteur(self):
        """Gère l'interrogation du lecteur pour déterminer si l'accès est autorisé."""
        
        if self.alarm_triggered:
            print("Accès refusé : alarme activée, toute tentative est bloquée.")
            self.__porte.signal_ouverture_reçu = False
            return
        
        badge_detecte = self.__lecteur.poll()  # Simuler la détection du badge
        if badge_detecte is None:
            print("Aucun badge détecté")
            return

        if self.mode_urgence:
            self._mode_urgence()
            return
        
        if self._verifier_badge_incorrect(badge_detecte):
            return
        
        if self._verifier_blacklist(badge_detecte):
            return
        
        if self._verifier_whitelist(badge_detecte):
            return
        
        self._refuser_acces(badge_detecte)

    def _mode_urgence(self):
        """Gère le mode urgence."""
        print("Mode urgence activé. La porte s'ouvre automatiquement.")
        self.__porte.signal_ouverture_reçu = True  # La porte s'ouvre automatiquement
        self.__porte.demander_ouverture()

    def _verifier_badge_incorrect(self, badge_detecte):
        """Vérifie si le badge est un dictionnaire (type incorrect)."""
        if isinstance(badge_detecte, dict):
            print(f"Accès refusé : Type de badge incorrect (dictionnaire) - {badge_detecte}")
            return True
        return False

    def _verifier_blacklist(self, badge_detecte):
        """Vérifie si le badge est sur la blacklist."""
        if badge_detecte in self.__blacklist:
            self.historique_refus.append(badge_detecte)
            print(f"Accès refusé : Badge {badge_detecte} sur liste noire")
            self.__porte.signal_ouverture_reçu = False
            return True
        return False

    def _verifier_whitelist(self, badge_detecte):
        """Vérifie si le badge est dans la whitelist ou badges temporaires."""
        print(f"Vérification badge {badge_detecte} dans whitelist: {badge_detecte in self.__whitelist}")
        
        if badge_detecte in self.__whitelist:
            print(f"Le badge {badge_detecte} est dans la whitelist.")
            
            if self.__porte.secure_mode:
                if badge_detecte in self.double_validation:
                    self.__porte.signal_ouverture_reçu = True
                    self.__porte.demander_ouverture()
                    del self.double_validation[badge_detecte]
                    print("Accès autorisé après double validation")
                else:
                    self.double_validation[badge_detecte] = True
                    print("Première validation effectuée, veuillez repasser le badge")
            else:
                self.__porte.signal_ouverture_reçu = True
                self.__porte.demander_ouverture()
                print("Accès autorisé")
            
            self.historique.append(badge_detecte)
            self.echecs_consecutifs[badge_detecte] = 0
            return True
        
        if badge_detecte in self.badges_temporaires:
            print(f"Le badge {badge_detecte} est temporaire et valide.")
            self.__porte.signal_ouverture_reçu = True
            self.__porte.demander_ouverture()
            
            self.historique.append(badge_detecte)
            self.echecs_consecutifs[badge_detecte] = 0
            return True
        
        self.__porte.signal_ouverture_reçu = False
        return False

    def _refuser_acces(self, badge_detecte):
        """Gère le refus d'accès."""
        self.historique_refus.append(badge_detecte)
        self.echecs_consecutifs[badge_detecte] = self.echecs_consecutifs.get(badge_detecte, 0) + 1
        self.__porte.signal_ouverture_reçu = False  # Refus d'accès, porte ne s'ouvre pas
        print(f"Accès refusé : Badge {badge_detecte} non autorisé.")
        
        if self.echecs_consecutifs[badge_detecte] >= 3:
            self.alarm_triggered = True
            print("ALERTE : Trois échecs consécutifs détectés.")

    def ajouter_badge_temporaire(self, badge, expire=False):
        """Ajoute un badge temporaire à la liste des badges temporaires."""
        if expire:
            print(f"Le badge {badge} a expiré et ne peut plus être ajouté.")
            if badge in self.badges_temporaires:
                self.badges_temporaires.remove(badge)
                print(f"Badge {badge} retiré des badges temporaires.")
            return
        self.badges_temporaires.add(badge)
        print(f"Badge {badge} ajouté temporairement")

    def retirer_badge_temporaire(self, badge):
        """Retire un badge de la liste des badges temporaires."""
        if badge in self.badges_temporaires:
            self.badges_temporaires.remove(badge)
            print(f"Badge {badge} retiré des badges temporaires.")
        else:
            print(f"Badge {badge} n'est pas dans les badges temporaires.")
    
    def activer_mode_urgence(self):
        """Active le mode urgence qui permet d'ouvrir automatiquement la porte."""
        self.mode_urgence = True
        print("Mode urgence activé : Toutes les portes s'ouvrent automatiquement.")
    
    def desactiver_mode_urgence(self):
        """Désactive le mode urgence."""
        self.mode_urgence = False
        print("Mode urgence désactivé.")
    
    def reset_historique(self):
        """Réinitialise l'historique des accès et des refus."""
        self.historique.clear()
        self.historique_refus.clear()
        print("Historique réinitialisé.")

    def ajouter_badge(self, badge):
        """Ajoute un badge à la whitelist."""
        if badge in self.__whitelist:
            print(f"Le badge {badge} est déjà dans la whitelist.")
        else:
            self.__whitelist.add(badge)
            print(f"Badge {badge} ajouté à la whitelist.")

    def retirer_badge(self, badge):
        """Retire un badge de la whitelist."""
        if badge in self.__whitelist:
            self.__whitelist.remove(badge)
            print(f"Badge {badge} retiré de la whitelist.")
        else:
            print(f"Badge {badge} n'est pas dans la whitelist.")

    def afficher_whitelist(self):
        """Affiche le contenu de la whitelist."""
        print(f"Whitelist actuelle : {self.__whitelist}")