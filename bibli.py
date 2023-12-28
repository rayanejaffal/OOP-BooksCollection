from base_bibli import base_bibli
import os
  

# La classe bibli sert à alimenter notre bibliothèque à l'aide du web scraping. 
# Pour se faire, elle hérite des méthodes de "base_bibli" pour la génération des rapports
# et de "bibli_scrap" pour récupérer les documents depuis l'url directement 

class bibli(base_bibli):
    
    def __init__(self, livres_path, rapports_path):
        """ Vous devez lui passer en arguments le chemin vers le répertoire
            qui vous servira de bibliothèque"""
        super().__init__(livres_path, rapports_path)
        from bibli_scrap import bibli_scrap
        self.scrap_instance = bibli_scrap(livres_path, rapports_path)

    def alimenter(self, url, profondeur, nbmax):
        if os.path.exists(url): #si le fichier  est sur notre machine, le programme appelle 'ajouter()'
            return self.ajouter(url)
        else:  #sinon c'est une url,  le programme appelle 'scrap()'
            return self.scrap_instance.scrap(url, profondeur, nbmax)        
