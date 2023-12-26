import base_livre
import shutil
import os
import pandas as pd
from ebooklib import epub
from weasyprint import HTML


""""  Afin de créer une instance de la classe base_bibli il faudra lui passer en argument le chemin vers 
        le répertoire qui vous servira de bibliothèque"""


class base_bibli:
    def __init__(self,path):
        """ path désigne le répertoire contenant les livres de cette bibliothèque """
        self.path = path

    def ajouter(self,livre): 
        """Ajoute le livre à la bibliothèque """
        if livre.endswith(".pdf") or livre.endswith(".epub"):
            destination_path = os.path.join(self.path, os.path.basename(livre))

            # on copie le livre dans la bibliothèque
            shutil.copy(livre, destination_path)
            print(f" {livre} a été ajouté à la bibliothèque.")
        else:
            print(f"Format non pris en charge pour le livre {livre}.")

                   
    def rapport_livres(self, format, fichier):
        # Contenu HTML du rapport
        df = self.donnees()
    
        # Convertir le DataFrame en une table HTML
        html_table = df.to_html(index=False)

        # Générer le contenu HTML complet
        html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Rapport des livres</title>
            </head>
            <body>
                <h1>État des livres</h1>
                {html_table}
            </body>
            </html>
        """

        # Générer le rapport au format spécifié
        return self.genere_rapport(format, fichier, html_content)
        
    
        
    def rapport_auteurs(self, format, fichier):
        # Construire le contenu HTML du rapport
        grouped_df = self.donnees().groupby('auteur').agg({
                'titre': lambda x: ', '.join(x),
                'type': lambda x: ', '.join(x),
                'nom du fichier': lambda x: ', '.join(x)
                }).reset_index()

        html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Rapport des Auteurs</title>
            </head>
            <body>
                <h1>État des livres classés par auteurs</h1>
        """

        for index, row in grouped_df.iterrows():
            html_content += f"<h4>{row['auteur']}</h4>"
            html_content += "<ul>"
            for titre, type, nom_fichier in zip(row['titre'], row['type'], row['nom du fichier']):
                html_content += f"""
                    <li>
                        <p>Titre : {titre} </p>
                    </li>
                """

            html_content += "</ul>"

        html_content += """
                </body>
            </html>
        """
        return self.genere_rapport(format, fichier, html_content)


    def donnees(self):
        try:
            file_data_list = []
            for file_name in os.listdir(self.path): # pour parcourir les éléments du répertoire 
                file_path = os.path.join(self.path, file_name)#concatène le chemin du répertoire a celui de l'element pour déterminer le chemin du livre
                book = base_livre(file_path)
                
                file_data= {
                    'titre': book.titre(),
                    'auteur': book.auteur(),
                    'type': book.type().__name__,
                    'nom du fichier': book.ressource[len(self.path)+1:-4]
                }
                file_data_list.append(file_data)
            df = pd.DataFrame(file_data_list, columns=['titre','auteur','type','nom du fichier'])
            return df    
        except:
            print(" Données non accessibles!")
            
            
    def genere_rapport(self,format,fichier,html_content):
        try:
            if format == "PDF":
                #on transforme le texte html directement en fichier pdf
                HTML(string=html_content).write_pdf(fichier)
                
                return f"Rapport généré au format {format}, nom du fichier : {fichier}"

            elif format == "EPUB":
                book = epub.EpubBook() # crée l'objet  de type EPUB
                # on crée une section pour le rapport
                section = epub.EpubHtml(title="Rapport Livres", file_name="rapport.html", lang="fr")
                section.content = html_content #  on defini le contenu de la section
                # On ajoute la section au rapport
                book.add_item(section)
                # On rajoute la section au rapport comme contenu
                book.spine = [section]
                #on ajoute nos diférentes sections au fichier EPUB
                epub.write_epub(fichier, book, {})
                return f"Rapport généré au format {format}, nom du fichier : {fichier}"
        except:
            raise NotImplementedError(" format non pris en charge ")
            
