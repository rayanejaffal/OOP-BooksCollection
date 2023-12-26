from base_bibli import base_bibli
import os
  

# La classe bibli sert à alimenter notre bibliothèque à l'aide du web scraping. 
# Pour se faire, elle hérite des méthodes de "base_bibli" pour la génération des rapports
# et de "bibli_scrap" pour récupérer les documents depuis l'url directement 

class bibli(base_bibli):
    
    def __init__(self, path):
        """ Vous devez lui passer en arguments le chemin vers le répertoire
            qui vous servira de bibliothèque"""
        super().__init__(path)
        from bibli_scrap import bibli_scrap
        self.scrap_instance = bibli_scrap(path)

    def alimenter(self, url, nbmax):
        if os.path.exists(url): #si le fichier  est sur notre machine, le programme appelle 'ajouter()'
            return self.ajouter(url)
        else:  #sinon c'est une url,  le programme appelle 'scrap()'
            #selon le sujet elle ajoute tous les livres référencés dans la page web correspondant à l’URL
            profondeur = 1 #on a fixé la profondeur à pour que la méthode ne recupère que les fichiers de l'url passée en arguments et pas des lien adjacents
            return self.scrap_instance.scrap(url, profondeur, nbmax)        
