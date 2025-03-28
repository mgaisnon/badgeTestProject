import unittest
from src.lecteur import Lecteur
from utilities.lecteurtest import LecteurDeTest

class TestLecteurDeTest(unittest.TestCase):
    def setUp(self):
        self.lecteur_test = LecteurDeTest()

    def test_detection_badge_valide(self):
        self.lecteur_test.simuler_detection_badge(1234)

        self.assertEqual(self.lecteur_test.poll(), 1234)

    def test_detection_badge_multiple(self):
        self.lecteur_test.simuler_detection_badge(1234)
        self.assertEqual(self.lecteur_test.poll(), 1234)

        self.lecteur_test.simuler_detection_badge(5678)
        self.assertEqual(self.lecteur_test.poll(), 5678)

    def test_aucun_badge_detecte(self):
        self.lecteur_test.simuler_badge_invalide()

        self.assertIsNone(self.lecteur_test.poll())

    def test_simulation_badge_invalide(self):
        self.lecteur_test.simuler_detection_badge(1234)

        self.assertEqual(self.lecteur_test.poll(), 1234)

        self.lecteur_test.simuler_badge_invalide()

        self.assertIsNone(self.lecteur_test.poll())

    def test_detection_multiple_badges(self):
        self.lecteur_test.simuler_detection_badge(1234)
        self.assertEqual(self.lecteur_test.poll(), 1234)

        self.lecteur_test.simuler_detection_badge(5678)
        self.assertEqual(self.lecteur_test.poll(), 5678)

        self.lecteur_test.simuler_detection_badge(91011)
        self.assertEqual(self.lecteur_test.poll(), 91011)

    def test_consommation_badge(self):
        self.lecteur_test.simuler_detection_badge(1234)

        self.assertEqual(self.lecteur_test.poll(), 1234)

        self.assertIsNone(self.lecteur_test.poll())

if __name__ == '__main__':
    unittest.main()
