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
        if self.mode_urgence:
            print("Mode urgence activé. La porte s'ouvre automatiquement.")
            self.__porte.demander_ouverture()
            return

        badge_detecte = self.__lecteur.poll()
        if badge_detecte is not None:
            # Vérification du type de badge incorrect (dictionnaire)
            if isinstance(badge_detecte, dict):
                print(f"Accès refusé : Type de badge incorrect (dictionnaire) - {badge_detecte}")
                return

            print(f"Vérification badge {badge_detecte} dans whitelist: {badge_detecte in self.__whitelist}")

            # Si le badge est sur la blacklist, l'accès est refusé
            if badge_detecte in self.__blacklist:
                self.historique_refus.append(badge_detecte)
                print(f"Accès refusé : Badge {badge_detecte} sur liste noire")
                return
            
            # Si le badge est dans la whitelist ou badges temporaires, on accorde l'accès
            if badge_detecte in self.__whitelist or badge_detecte in self.badges_temporaires:
                if self.__porte.secure_mode:
                    # Si la porte est en mode sécurisé, vérifier la double validation
                    if badge_detecte in self.double_validation:
                        self.__porte.demander_ouverture()
                        del self.double_validation[badge_detecte]
                        print("Accès autorisé après double validation")
                    else:
                        self.double_validation[badge_detecte] = True
                        print("Première validation effectuée, veuillez repasser le badge")
                else:
                    self.__porte.demander_ouverture()
                    print("Accès autorisé")
                self.historique.append(badge_detecte)
                self.echecs_consecutifs[badge_detecte] = 0
            else:
                # Si le badge n'est pas dans la whitelist, l'accès est refusé
                self.historique_refus.append(badge_detecte)
                self.echecs_consecutifs[badge_detecte] = self.echecs_consecutifs.get(badge_detecte, 0) + 1
                print(f"Accès refusé : Badge {badge_detecte} non autorisé.")
                
                if self.echecs_consecutifs[badge_detecte] >= 3:
                    self.alarm_triggered = True
                    print("ALERTE : Trois échecs consécutifs détectés.")
        else:
            print("Aucun badge détecté")

    def ajouter_badge_temporaire(self, badge, expire=False):
        """Ajoute un badge temporaire à la liste des badges temporaires."""
        if expire:
            print(f"Le badge {badge} a expiré et ne peut plus être ajouté.")
            return
        self.badges_temporaires.add(badge)
        print(f"Badge {badge} ajouté temporairement")

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
