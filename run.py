from src.ControleAcces import ControleAcces

def main():
    systeme_controle = ControleAcces()

    badge_id = input("📛 Scannez votre badge : ")
    resultat = systeme_controle.verifier_acces(badge_id)
    print(f"🚪 {resultat}")

if __name__ == "__main__":
    main()
