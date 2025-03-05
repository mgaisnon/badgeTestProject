import unittest
from src.ControleAcces import ControleAcces

class TestControleAcces(unittest.TestCase):

    def setUp(self):
        self.systeme_controle = ControleAcces()

    def test_badge_valide(self):
        resultat = self.systeme_controle.verifier_acces("12345")
        self.assertEqual(resultat, "Ouvrir")

    def test_badge_invalide(self):
        resultat = self.systeme_controle.verifier_acces("99999")
        self.assertEqual(resultat, "Accès refusé")


if __name__ == "__main__":
    unittest.main()
