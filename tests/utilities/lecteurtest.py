from src.lecteur import Lecteur


class LecteurDeTest(Lecteur):
    def __init__(self):
        self.__numero_badge_detecte = None

    def poll(self) -> int | None:
        # Retourne le badge détecté, puis réinitialise la valeur
        numero_detecte = self.__numero_badge_detecte
        self.__numero_badge_detecte = None
        return numero_detecte

    def simuler_detection_badge(self, numero_badge: int):
        # Simule la détection d'un badge
        self.__numero_badge_detecte = numero_badge