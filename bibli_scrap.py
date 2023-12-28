from bs4 import BeautifulSoup #Python library for pulling data out of HTML 
import requests
import os
from base_bibli import base_bibli

class bibli_scrap(base_bibli):

    def __init__(self, livres_path, rapports_path):
        base_bibli.__init__(self, livres_path, rapports_path) #hérite le lien du répertoire où télecharger les livres de la classe base_bibli 
        
    def scrap(self, url, profondeur, nbmax):
        if profondeur == 0 or nbmax == 0: #si les arguments sont nuls on sort
            return #ça return None automatiquement
        
        directory = self.livres_path #je détermine le répertoire 
        
        if not os.path.exists(directory): #si le répertoire n'existe pas on le crée
            os.makedirs(directory)
        
        try:
            html_page = requests.get(url, verify=False).content
            soup = BeautifulSoup(html_page, "html.parser")

            for l in soup.find_all("a"): #ici on cherche les liens
                lien = l.get('href', []) #on extract les liens
                if lien.endswith('.pdf') or lien.endswith('.epub'): 
                    try:
                        if 'https://' not in lien:
                            lien = url + lien #ajouter le nom du server au lien incomplet
                        reponse = requests.get(lien, verify =False)
                        
                        filename = os.path.join(directory, os.path.basename(lien)) #nommer le fichier de chaque livre selon le nom de base du lien
                        
                        with open(filename, mode="wb") as file: #télechargement
                            file.write(reponse.content)
                        nbmax -= 1
                        if nbmax <= 0: #on a dépasser le nombre max des fichier à télécharger
                            break
                        
                    except requests.exceptions.RequestException as e:
                        print(f"Erreur du téléchargement {lien}: {e}")
                        
            for l in soup.find_all("a"): #ici on cherche les liens pour passer à des autres pages web
                    next_lien = l.get('href',[]) #on extract les liens
                    if next_lien.endswith('.pdf') or next_lien.endswith('.epub'): 
                        continue   #on continue car on cherche pas des liens des livres ici
                    try:
                        if 'https://' not in next_lien:
                            next_lien = url + next_lien  #ajouter le nom du server au lien incomplet
                        if nbmax > 0 and profondeur > 1: #j'ai mis 1 pour le prof. car déja le code fait le scraping dans un site
                            self.scrap(next_lien, profondeur, nbmax) #recursion
                            profondeur -= 1
                        
                    except requests.exceptions.RequestException as e:
                        print(f"Erreur traitement {next_lien}: {e}")
        
        except requests.exceptions.RequestException as e:
            print(f"Un erreur inattendu: {e}")
            
