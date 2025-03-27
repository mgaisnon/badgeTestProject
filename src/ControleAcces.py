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
        self.double_validation = {}  # Stocke la première tentative pour une porte sécurisée

    def interroger_lecteur(self):
        if self.mode_urgence:
            self.__porte.demander_ouverture()
            return

        badge_detecte = self.__lecteur.poll()
        if badge_detecte is not None:
            if badge_detecte in self.__blacklist:
                self.historique_refus.append(badge_detecte)
                print("Accès refusé : Badge sur liste noire")
                return
            
            if badge_detecte in self.__whitelist or badge_detecte in self.badges_temporaires:
                if getattr(self.__porte, "secure_mode", False):
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
                self.historique_refus.append(badge_detecte)
                self.echecs_consecutifs[badge_detecte] = self.echecs_consecutifs.get(badge_detecte, 0) + 1
                print("Accès refusé : Badge non autorisé")
                
                if self.echecs_consecutifs[badge_detecte] >= 3:
                    self.alarm_triggered = True
                    print("ALERTE : Trois échecs consécutifs détectés")
        else:
            print("Aucun badge détecté")

    def ajouter_badge_temporaire(self, badge, expire=False):
        if not expire:
            self.badges_temporaires.add(badge)
        print(f"Badge {badge} ajouté temporairement")
    
    def activer_mode_urgence(self):
        self.mode_urgence = True
        print("Mode urgence activé : Toutes les portes s'ouvrent automatiquement")
    
    def desactiver_mode_urgence(self):
        self.mode_urgence = False
        print("Mode urgence désactivé")
    
    def reset_historique(self):
        self.historique.clear()
        self.historique_refus.clear()
        print("Historique réinitialisé")
