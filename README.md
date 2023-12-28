# Bienvenue à la Guide d'Utilisation! 
Réalisation du projet final de POO   
Rayane JAFFAL et Jennifer NGOUNA   
Prof. Jacquelin Charbonel   
Université d'Angers   
 
## Projet-POO : Collecte de livres  
L’objectif de ce projet est de concevoir une application pour constituer et suivre une bibliothèque de livres. L’idée est de pouvoir collecter des livres (au format _EPUB_ et _PDF_) sur le web (_web scraping_) pour constituer une bibliothèque,
et générer divers catalogues de cette bibliothèque.
Page d'accueil : [https://github.com/rayanejaffal/Collecte-de-livres.git](https://github.com/rayanejaffal/Collecte-de-livres.git)   

[](#Documentation_du_Module)Documentation du Module  
---------------------------------------------------   
Ce module se compose de quatre classes: la classe `base_livre` qui englobe les sous-classes `PDF` et `EPUB`, la classe `base_bibli`, la classe `bibli`, et enfin la classe `bibli_scrap`. 
 
[](##_librairies_python)Librairies Python 
----------------------------------------
Les principales librairies Python utilisées dans notre module:
- `pypdf` qui intéragit avec les fichiers au format PDF [description](https://pypi.org/project/pypdf/)
- `EbookLib` qui interagit avec les fichiers au format EPUB [description](https://pypi.org/project/EbookLib/) 
- `requests` qui envoie des demandes HTTP [description](https://pypi.org/project/requests/)
- `BeautifulSoup` qui scrape les informations des pages HTML [description](https://pypi.org/project/BeautifulSoup/)
- `pdfkit` qui aide à créer des documents PDF en transformant de simples pages HTML [description](https://pypi.org/project/pdfkit/)
- `shutil` est une bibliothèque standard qui offre un ensemble de fonctions haut niveau pour effectuer des opérations de manipulation de fichiers et de répertoires. Elle est particulièrement utile pour effectuer des opérations courantes telles
que la copie, le déplacement, la suppression et l'archivage de fichiers et de répertoires.
- `pandas` qui fournit des structures de données rapides et flexibles: DataFrame [description](https://pypi.org/project/pandas/)   
- `reportlab` qui génère des fichier pdf [description](https://pypi.org/project/reportlab/)   
 
[](##_les_méta-données)Les Méta-données 
--------------------------------------
La classe `base_livre` utilise principalement les librairies `pypdf` et `EbookLib` pour extraire les méta-données des livres au format PDF ou EPUD. Cela peut être effectué à partir d'un chemin local ou d'une URL. Tout d'abord, l'extension de la
ressource est vérifiée pour déterminer le type de fichier, puis en fonction de ce type, la sous-classe appropriée, soit `PDF`, soit `EPUB`, est appelée. 
Ensuite, la nature de la ressource est examinée, car les librairies utilisées ne peuvent lire les fichiers que depuis un chemin local. Ainsi, si la ressource est une URL, la librarie `tempfile` est utilisée pour ouvrir et stocker le livre dans
une fichier temporaire, permettant ainsi l'extraction des méta-données. 
les méthodes pour récupérer les méta-données de chaque librarie: 
```python
#EbookLib
#Pour les fichiers EPUB
from ebooklib import epub 
f = epub.read_epub(ressource)
f.get_metadata("DC","title") #DC pour Dublin Core metadata: les meta-données essentielles 
f.get_metadata("DC","creator")
f.get_metadata("DC","language")
f.get_metadata("DC","date")
#pypdf
#Pour les fichiers PDF
from pypdf import PdfReader
f = PdfReader(ressource)
f.metadata.title
f.metadata.author
f.metadata.subject
f.metadata.creation_date
````
Exemple d'utilisation de cette classe: 
````python
from base_livre import base_livre 
livre = base_livre("path or URL")
print("Type:", livre.type())
print("Titre:", livre.titre())
print("Auteur:", livre.auteur())
print("Langue:", livre.langue())
print("Sujet:", livre.sujet())
print("Date:", livre.date())
````
 
[](##_la_bibliothèque)La base de la bibliothèque 
-----------------------------------------------
La classe `base_bibli` qui prend en paramètre un `path`(lien vers la bibliothèque) permet de stocker et génère un états de tous les livres présents dans notre bibliothèque(dans un répertoire sur notre machine). 
Elle est dotée de cinq méthodes:
- `ajouter(ressource)`: qui ajoute un livre directement dans notre répertoire. `path` est la ressource du livre.
- `create_dataframe()`: qui récupère tous les métadatas des fichiers présents dans notre répertoire et les stock dans un dataframe.
- `rapport_livres(format, fichier)` : qui appelle la fonction `_generate_pdf_report(df, fichier)` ou la fonction `_generate_epub_report(df, fichier)` selon la format précisée. Parsuite une fichier (de format pdf ou epub) d'états des livres présents est crée où les livres sont regroupés par titre.  
- `rapport_auteurs(format, fichier)` : qui appelle la fonction `_generate_pdf_author_report(df, fichier)` ou la fonction `_generate_epub_author_report(df, fichier)` selon la format précisée. Parsuite une fichier(de format pdf ou epub) d'états des livres présentsest crée où les livres sont regroupés par auteur.   

Exemple d'utilisation de cette classe: 
````python
from base_bibli import base_bibli
ma_bibliotheque = base_bibli(livres_path, rapports_path)
ma_bibliotheque.ajouter(ressource)
ma_bibliotheque.rapport_livres("PDF", "Mon rapport") #ou EPUB
ma_bibliotheque.rapport_auteurs("PDF", "Mon rapport") #ou EPUB
````  

[](##_bibli)La Bibliothèque 
----------------------------- 
La classe `bibli` est la classe complète qui définit notre bibliothèque. Elle prend en argument `path` (lien vers la bibliothèque). Elle hérite de la `base_bibli`, elle est donc capable de faire appel à la méthode `ajouter()` (de `base_bibli`)
si le livre est déja présent dans notre machine locale. De plus elle est capable d'appeler la méthode `scrap()` (de `bibli_scrap`) si `path` est une `url` afin d'ajouter des livres à notre bibliothèque.
Exemple d'utilisation de cette classe:
````python
from bibli import bibli
ma_bibliotheque = bibli(livres_path, rapports_path) #path est la bibliothèque où sauvegarder les fichiers
ma_bibliotheque.alimenter("https://math.univ-angers.fr/~jaclin/biblio/livres/",100)
````
 
[](##web_scraping)Web Scraping 
-------------------------------
La classe `bibli_scrap` est responsable de réaliser le web scraping destiné à alimenter la bibliothèque. Elle est dotée d'une méthode nommée `scrap` qui prends trois paramètres : `url`, `profondeur` et `nbmax`. Cette méthode récupère la page
web référencée par url, puis télécharge tous les fichiers PDF et EPUB qui y sont référencés. Ensuite, elle extrait tous les liens vers d’autres pages web de cette page, répetant le processus sur chacune d’entre elles. Ce cycle se répète jusqu’à
ce que l’un des critères d’arrêt soit satisfait. 
Le paramètre `url` représente l’URL de départ pour le scraping, `profondeur` détermine le nombre maximal de sites à explorer, et `nbmax` indique le nombre maximal de documents à télécharger. 
Cette classe utilise principalement la librairie `BeautifulSoup`. En particulier, la méthode `find_all` pour rechercher les liens dans la page qui appartiennent aux fichiers PDF et EPUB. 
Ensuite, les fichiers sont téléchargés: 
 
````python
#téléchargement
with open(filename, mode="wb") as file: #télechargement
 file.write(reponse.content)
````
Exemple d'utilisation de cette classe: 
````python
path = bibli_scrap(livres_path, rapports_path) #le directoire où sauvegarder les fichiers
path.scrap("https://math.univ-angers.fr/~jaclin/biblio/livres/", 1, 100) #récupérer de cette page web
````
Ensuite, cette classe explore la même page à la recherche des liens qui ne renvoient pas vers des livres, puis elle applique la méthode `scrap` sur ces lien de manière récursive jusqu'à ce que la profendeur souhaitée est atteinte.     

[](#Documentation_de_l'Application)Documentation de l'Application 
-----------------------------------------------------------------   
Cette application `bibli_app` utilise le module ci-dessus et s'execute comme:   
````console
$ ./bibli_app.py -c bibli.conf https://math.univ-angers.fr/~jaclin/biblio/livres/ 1
````   
pour lancer une collecte de profondeur 1 visant à compléter la bibliothèque, et :   
````console
$ ./bibli_app.py -c bibli.conf rapports
````   
pour générer les 2x2 rapports au format EPUB et PDF.  

[](##Fichier_de_Configuration)Fichier de Configuration  
------------------------------------------------------   
L’application utilise un fichier de configuration `bibli.conf` contenant :   
- le nom du répertoire destiné à recevoir les livres récoltés,
- le nom du répertoire destiné à recevoir les rapports,
- le nombre max de livres à rapatrier à chaque collecte.

-------------------------------------------------------------- 
Test possible des classes avec l’URL [bibliothèque](https://math.univ-angers.fr/~jaclin/biblio/livres/)
