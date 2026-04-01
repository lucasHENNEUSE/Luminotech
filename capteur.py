import os
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from langchain.tools import tool

# --- PARTIE 1 : GESTION DES ALIMENTS ---

class Aliment:
    def __init__(self, nom, jours_avant_alerte=1):
        self.nom = nom
        # Pour le test, on simule que l'aliment a été ajouté il y a 6 jours
        self.date_ajout = datetime.now() - timedelta(days=6)
        self.alerte_dlc = self.date_ajout + timedelta(days=jours_avant_alerte)
        self.consomme = False

    def est_urgent(self):
        return datetime.now() >= self.alerte_dlc and not self.consomme

class Refrigerateur:
    def __init__(self):
        self.contenu = []

    def ajouter_aliment(self, nom):
        nouvel_aliment = Aliment(nom)
        self.contenu.append(nouvel_aliment)
        print(f"Capteur : {nom} détecté et ajouté au frigo.")

    def scanner_peremption(self):
        for item in self.contenu:
            if item.est_urgent():
                self.envoyer_alerte_email(item.nom)
                item.consomme = True

    def envoyer_alerte_email(self, nom_aliment):

        load_dotenv()
        mot_de_passe = os.getenv("GMAIL_APP_PASSWORD")

        message = MIMEMultipart()
        message["From"] = expediteur
        message["To"] = destinataire
        message["Subject"] = f"ALERTE FRIGO : Consommer {nom_aliment}"
        corps = f"Bonjour, l'aliment '{nom_aliment}' a atteint sa limite. Consommez-le !"
        message.attach(MIMEText(corps, "plain"))

        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(expediteur, mot_de_passe)
            server.send_message(message)
            server.quit()
            print(f"Mail envoyé pour : {nom_aliment}")
        except Exception as e:
            print(f"Erreur email : {e}")

# --- PARTIE 2 : INITIALISATION DU FRIGO ---

# On crée l'instance qui sera lue par l'IA
mon_frigo = Refrigerateur()

# Simulation de détection capteur
mon_frigo.ajouter_aliment("Lait")
mon_frigo.ajouter_aliment("Yaourt")
mon_frigo.ajouter_aliment("Pomme")
mon_frigo.ajouter_aliment("Fromage")
mon_frigo.ajouter_aliment("Jus d'orange")
mon_frigo.ajouter_aliment("Œufs")
mon_frigo.ajouter_aliment("Beurre")
mon_frigo.ajouter_aliment("Salade")


# --- PARTIE 3 : L'OUTIL POUR AGENT IA ---

@tool
def consulter_inventaire_frigo() -> str:
    """Consulte la liste des aliments actuellement présents dans le réfrigérateur pour proposer des recettes."""
    # On récupère les noms des aliments qui ne sont pas marqués comme consommés
    aliments_presents = [item.nom for item in mon_frigo.contenu if not item.consomme]
    
    if not aliments_presents:
        return "Le réfrigérateur est actuellement vide selon les capteurs."
    
    return f"Le capteur détecte les ingrédients suivants : {', '.join(aliments_presents)}."

# --- TEST DU SCAN  ---
if __name__ == "__main__":
    print("--- DÉBUT DU TEST : Vérification des dates et envoi d'emails ---")
    mon_frigo.scanner_peremption()
