import os
import shutil
import pandas as pd
from base_livre import base_livre
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from ebooklib import epub


class base_bibli:
    def __init__(self, livres_path, rapports_path):
        """
        livres_path: le path du répertoire destiné à recevoir les livres récoltés,
        reports_path: le path du répertoire destiné à recevoir les rapports,
        """
        self.livres_path = livres_path
        self.rapports_path = rapports_path
        self.books = []  # liste pour poursuivre les livres de la bibliothèque

        try:
            if not os.path.exists(livres_path):
                # Crée le dossier si celui-ci n'existe pas
                print(f"Le dossier {livres_path} n'existe pas.")
                print(f"Création du dossier {livres_path}.")
                os.makedirs(livres_path)
                
            else: 
                file_paths = [os.path.join(livres_path, f) for f in os.listdir(livres_path) if os.path.isfile(os.path.join(livres_path, f))]
                self.books.extend(file_paths) #ajouter les livres déja existants
        except Exception as e:
            print(f"Erreur lors de l'initialisation de la bibliothèque : {e}")
            
        try:
            if not os.path.exists(rapports_path):
                # Crée le dossier si celui-ci n'existe pas
                print(f"Le dossier {rapports_path} n'existe pas.")
                print(f"Création du dossier {rapports_path}.")
                os.makedirs(rapports_path)
        
        except Exception as e:
            print(f"Erreur lors de l'initialisation du répertoire destiné à recevoir les rapports : {e}")

    def ajouter(self, livre):
        """
        Ajoute le livre à la bibliothèque.
        """
        try:
            # Vérifie si le livre est déjà présent
            livre_name = os.path.basename(livre)
            if livre_name in [os.path.basename(book) for book in self.books]:
                print(f"Le livre {livre_name} est déjà présent.")   
            
            # Vérifie si le chemin existe
            if os.path.isfile(livre):
                # Si c'est un dossier local, copie le fichier dans le dossier
                shutil.copy(livre, self.livres_path)
                print(f"Le livre {livre_name} a été ajouté au dossier.")
                self.books.append(os.path.join(self.livres_path, livre_name)) #ajouter le livre
            else:
                print("Type de chemin non pris en charge.")
                


        except Exception as e:
            print(f"Erreur lors de l'ajout du livre à la bibliothèque : {e}")
    
    def create_dataframe(self): #pour faciliter la creation des rapports, soit par titre, soit par auteur
        """
        Crée un DataFrame contenant les livres et leurs métadonnées.
        """
        data = {
            "Titre": [],
            "Auteur": [],
            "Langue": [],
            "Sujet": [],
            "Date": [],
            "Type": [],
            "Fichier": []  
        }

        for book_path in self.books:
            book = base_livre(book_path).create_instance()
            data["Titre"].append(book.titre())
            data["Auteur"].append(book.auteur())
            data["Langue"].append(book.langue() if hasattr(book, "langue") else None)
            data["Sujet"].append(book.sujet() if hasattr(book, "sujet") else None)
            data["Date"].append(book.date() if hasattr(book, "date") else None)
            data["Type"].append(book.type())
            data["Fichier"].append(os.path.basename(book_path))
            
        df = pd.DataFrame(data)
        return df
    
    def rapport_livres(self, format, fichier):
        """
        Génère un état des livres de la bibliothèque.
        Il contient la liste des livres,
        et pour chacun d'eux
        son titre, son auteur, son type (PDF ou EPUB), et le nom du fichier correspondant.

        format: format du rapport (PDF ou EPUB)
        fichier: nom du fichier généré
        """
        df = self.create_dataframe()

        if format == "PDF":
            self._generate_pdf_report(df, fichier)
        elif format == "EPUB":
            self._generate_epub_report(df, fichier)
        else:
            print("Format non pris en charge!")

    def rapport_auteurs(self, format, fichier):
        """
        Génère un état des auteurs des livres de la bibliothèque.
        Il contient pour chaque auteur
        le titre de ses livres en bibliothèque et le nom du fichier correspondant au livre.
        le type (PDF ou EPUB),
        et le nom du fichier correspondant.

        format: format du rapport (PDF ou EPUB)
        fichier: nom du fichier généré
        """
        df = self.create_dataframe()

        if format == "PDF":
            self._generate_pdf_author_report(df, fichier)
        elif format == "EPUB":
            self._generate_epub_author_report(df, fichier)
        else:
            print("Format non pris en charge!")
            


    def _generate_pdf_report(self, df, fichier):
        """
        Génère un rapport PDF.
        """
        pdf_path = os.path.join(self.rapports_path, fichier + ".pdf")
        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.setFont("Helvetica", 10)
    
        c.drawString(100, 800, "Rapport des Livres de la Bibliothèque")
        
        Titles = df['Titre'].unique() 
    
        y_position = 780
        for title in Titles:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(100, y_position - 20, f"Titre: {title}")
            y_position -= 20
            c.setFont("Helvetica", 10)
            
            title_books = df[df['Titre'] == title]
            for index, row in title_books.iterrows():
                c.setFont("Helvetica", 10)
                y_position -= 20
                c.drawString(120, y_position, f"Auteur: {row['Auteur']}")
                y_position -= 20
                c.drawString(120, y_position, f"Langue: {row['Langue']}")
                y_position -= 20
                c.drawString(120, y_position, f"Sujet: {row['Sujet']}")
                y_position -= 20
                c.drawString(120, y_position, f"Date: {row['Date']}")
                y_position -= 20
                c.drawString(120, y_position, f"Type: {row['Type']}")
                y_position -= 20
                c.drawString(120, y_position, f"Fichier: {row['Fichier']}")
                y_position -= 20
                c.drawString(120, y_position, "_" * 50)
                
                if y_position <= 140: #sauter sur une nouvelle page, break
                        c.showPage()
                        y_position = 780
                
        c.save()


    def _generate_pdf_author_report(self, df, fichier):
        """
        Génère un rapport PDF des auteurs.
        """
        pdf_path = os.path.join(self.rapports_path, fichier + "_auteurs.pdf")
        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.setFont("Helvetica", 10)
    
        c.drawString(100, 800, "Rapport des Auteurs de la Bibliothèque")
    
        authors = df['Auteur'].unique() 
        
        y_position = 780
        for author in authors:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(100, y_position - 20, f"Auteur: {author}")
            y_position -= 20
            c.setFont("Helvetica", 10)
    
            author_books = df[df['Auteur'] == author]
            for index, row in author_books.iterrows():
                c.setFont("Helvetica", 10)
                y_position -= 20
                c.drawString(120, y_position, f"Titre: {row['Titre']}")
                y_position -= 20
                c.drawString(120, y_position, f"Langue: {row['Langue']}")
                y_position -= 20
                c.drawString(120, y_position, f"Sujet: {row['Sujet']}")
                y_position -= 20
                c.drawString(120, y_position, f"Date: {row['Date']}")
                y_position -= 20
                c.drawString(120, y_position, f"Type: {row['Type']}")
                y_position -= 20
                c.drawString(120, y_position, f"Fichier: {row['Fichier']}")
                y_position -= 20
                c.drawString(120, y_position, "_" * 50)
                
                if y_position <= 140: #sauter sur une nouvelle page, break
                    c.showPage()
                    y_position = 780
    
        c.save()
    

        

    def _generate_epub_report(self, df, fichier):
        """
        Génère un rapport EPUB.
        """
        epub_path = os.path.join(self.rapports_path, fichier + ".epub")
        book = epub.EpubBook()
        book.set_title("Rapport des Livres de la Bibliothèque")

        Titles = df['Titre'].unique()
        rapport_livres= ""

        for title in Titles:
            title_books = df[df['Titre'] == title]
            rapport_livres += f"<h2>{title}</h2>"
            
            for index, row in title_books.iterrows():
                rapport_livres += f"<p>Auteur: {row['Auteur']}</p>"
                rapport_livres += f"<p>Langue: {row['Langue']}</p>"
                rapport_livres += f"<p>Sujet: {row['Sujet']}</p>"
                rapport_livres += f"<p>Date: {row['Date']}</p>"
                rapport_livres += f"<p>Type: {row['Type']}</p>"
                rapport_livres += f"<p>Fichier: {row['Fichier']}</p>"
                rapport_livres += "<hr>"

        chapter = epub.EpubHtml(title="Rapport_livres", file_name="Rapport_livres.xhtml", lang='fr')
        chapter.content = rapport_livres
        book.add_item(chapter)
        epub.write_epub(epub_path, book)

    def _generate_epub_author_report(self, df, fichier):
        """
        Génère un rapport EPUB des auteurs.
        """
        epub_path = os.path.join(self.rapports_path, fichier + "_auteurs.epub")
        book = epub.EpubBook()
        book.set_title("Rapport des Auteurs de la Bibliothèque")

        authors = df['Auteur'].unique()
        rapport_auteurs= ""

        for author in authors:
            author_books = df[df['Auteur'] == author]
            rapport_auteurs += f"<h2>{author}</h2>"
            

            for index, row in author_books.iterrows():
                rapport_auteurs += f"<p>Titre: {row['Titre']}</p>"
                rapport_auteurs += f"<p>Langue: {row['Langue']}</p>"
                rapport_auteurs += f"<p>Sujet: {row['Sujet']}</p>"
                rapport_auteurs += f"<p>Date: {row['Date']}</p>"
                rapport_auteurs += f"<p>Type: {row['Type']}</p>"
                rapport_auteurs += f"<p>Fichier: {row['Fichier']}</p>"
                rapport_auteurs += "<hr>"
           
        chapter = epub.EpubHtml(title="Rapport_auteurs", file_name="Rapport_auteurs.xhtml", lang='fr')
        chapter.content = rapport_auteurs
        book.add_item(chapter)
        epub.write_epub(epub_path, book)