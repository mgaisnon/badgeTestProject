import unittest
from src.porte import Porte
from utilities.portetest import PorteDeTest

class TestPorteDeTest(unittest.TestCase):
    def setUp(self):
        self.porte_test = PorteDeTest()

    def test_ouverture_porte(self):
        result = self.porte_test.demander_ouverture()

        self.assertTrue(result)
        self.assertTrue(self.porte_test.signal_ouverture_reçu)

    def test_ouverture_porte_une_seule_fois(self):
        self.porte_test.demander_ouverture()

        result = self.porte_test.demander_ouverture()

        self.assertFalse(result)
        self.assertTrue(self.porte_test.signal_ouverture_reçu)

    def test_mode_securise(self):
        self.porte_test.secure_mode = True

        result = self.porte_test.demander_ouverture()

        self.assertTrue(result)
        self.assertTrue(self.porte_test.signal_ouverture_reçu)

    def test_pas_de_ouverture_si_porte_ouverte(self):
        self.porte_test.demander_ouverture()

        result = self.porte_test.demander_ouverture()

        self.assertFalse(result)
        self.assertTrue(self.porte_test.signal_ouverture_reçu)

    def test_initialisation_porte(self):
        self.assertFalse(self.porte_test.secure_mode)

        self.assertFalse(self.porte_test.signal_ouverture_reçu)

if __name__ == '__main__':
    unittest.main()
