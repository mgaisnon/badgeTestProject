class ControleAcces:
    def __init__(self):
        self.badges_valides = {"12345", "67890", "ABCDE"}

    def verifier_acces(self, badge_id):
        if badge_id in self.badges_valides:
            return self.envoyer_message_porte("Ouvrir")
        else:
            return self.envoyer_message_porte("Accès refusé")

    @staticmethod
    def envoyer_message_porte(message):
        return message
