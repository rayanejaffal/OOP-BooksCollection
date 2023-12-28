#classe base_livre
#sous classes: PDF, EPUB 
import os
import requests
import tempfile
from ebooklib import epub  #librairie pour traiter les documents de type "epub" #pip install EbookLib #EbookLib 0.18
from pypdf import PdfReader #librairie pour traiter les documents de type "pdf" #pip install pypdf #pypdf 3.17.1

class base_livre:
    def __init__(self,ressource):
        self.ressource = ressource
        
    def create_instance(self): #si le lien ou le path termine par les extentions souhaitées on excute soit la class PDF soit EPUB
        if self.ressource.endswith(".pdf"):
            return PDF(self.ressource)
        elif self.ressource.endswith(".epub"):
            return EPUB(self.ressource)
        else:
            raise NotImplementedError("Format non pris en charge!")
            return None
        
    def type(self): 
        return self.create_instance().type()
    
    def titre(self):
        return self.create_instance().titre()

    def auteur(self):
        return self.create_instance().auteur()

    def langue(self):
        return self.create_instance().langue()

    def sujet(self):
        return self.create_instance().sujet()

    def date(self):
        return self.create_instance().date()

class PDF(base_livre):

    def __init__(self, ressource):
        super().__init__(ressource) #on hérite soit la ressource de la classe base_livre
        if "://" in self.ressource: #on voit si la ressource est un URL
            response = requests.get(self.ressource, verify=False) #on ouvert le URL
            if response.status_code == 200: #succès 
                 with tempfile.NamedTemporaryFile(delete=False) as temp_fichier: # Télecharger le contenu dans un fichier temporaire
                    temp_fichier.write(response.content)
                    temp_nom = temp_fichier.name

                 self.ressource = PdfReader(temp_nom) # Lire le PDF du fichier temporaire
            else:
                raise FileNotFoundError("ressource inaccessible") 
        else:
            if not os.path.exists(self.ressource): #si ce path n'existe pas sur la machine
                raise FileNotFoundError(f"File '{self.ressource}' does not exist.")
            self.ressource = PdfReader(self.ressource) #si c'est un path d'une fichier locale on peut le lire directement
    
    def type(self):
        return "pdf"

    def titre(self):
        return self.ressource.metadata.title  

    def auteur(self):
        return self.ressource.metadata.author

    def langue(self):
        return NotImplementedError(None)  #selon le documentation y a pas de méthode metadata pour la langue 
        
    def sujet(self):
        return self.ressource.metadata.subject

    def date(self):
        return self.ressource.metadata.creation_date

class EPUB(base_livre):
    
    def __init__(self,ressource):
        super().__init__(ressource) #on hérite soit la ressource de la classe base_livre
        if "://" in self.ressource: #on voit si la ressource est un URL
            response = requests.get(self.ressource,verify=False)  #on ouvert le URL
            if response.status_code == 200: #succès 
                with tempfile.NamedTemporaryFile(delete=False) as temp_fichier: # Télecharger le contenu dans un fichier temporaire
                    temp_fichier.write(response.content)
                    temp_nom = temp_fichier.name

                self.ressource = epub.read_epub(temp_nom) # Lire le EPUB du fichier temporaire
            else:
                raise FileNotFoundError("ressource inaccessible")

        # Check if the resource is a file path
        else:
            if not os.path.exists(self.ressource): #si ce path n'existe pas sur la machine
                raise FileNotFoundError(f"File '{self.ressource}' does not exist.")
            self.ressource = epub.read_epub(self.ressource) #si c'est un path d'une fichier locale on peut le lire directement
            
    def type(self):
        return "epub"

    def titre(self):
        metadata = self.ressource.get_metadata("DC", "title")
        if metadata:
            return metadata[0][0]
        else:
            return None

    def auteur(self):
        metadata = self.ressource.get_metadata("DC", "creator")
        if metadata:
            return metadata[0][0]
        else:
            return None

    def langue(self):
        metadata = self.ressource.get_metadata("DC", "language")
        if metadata:
            return metadata[0][0]
        else:
            return None
    
    def sujet(self):
        return NotImplementedError(None) #selon le documentation y a pas de méthode metadata pour le sujet

    def date(self):
        metadata = self.ressource.get_metadata("DC", "date")
        if metadata:
            return metadata[0][0]
        else:
            return None
