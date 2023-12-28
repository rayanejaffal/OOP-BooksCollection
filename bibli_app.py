#!/usr/bin/env python3

import argparse
from bibli import bibli
import configparser

def parse_config(config_fichier='bibli.conf'): #récupérer les path et le nbmax du fichier de configuration
    config = configparser.ConfigParser()
    config.read(config_fichier) 
    livres_path = config['Bibliotheque']['bibliotheque']
    rapports_path = config['Bibliotheque']['etats']
    nbmax = int(config['Bibliotheque']['nbmax'])
    return livres_path, rapports_path, nbmax

def main():
    print("Script is running...") #debugging
    parser = argparse.ArgumentParser(description='Bibli Application') #découper la ligne du commande
    parser.add_argument('-c', '--config', help='Specifier le fichier de configuration', default='bibli.conf') #préciser le fichier de configuration
    parser.add_argument('command', help='url pour collecter ou "rapports"') #soit directement un url, soit le mots 'rapports'
    parser.add_argument('depth', type=int, nargs='?', help='profondeur') #récupérer le profondeur
    args = parser.parse_args()

    livres_path, rapports_path, nbmax = parse_config(args.config) #récupérer les path et le nbmax du fichier de configuration précisé
    biblio_instance = bibli(livres_path, rapports_path) #crée un instance de la classe bibli

    if 'https://' in args.command: #si c'est un url
        biblio_instance.alimenter(args.command, args.depth, nbmax)
        
    elif args.command == 'rapports': #si c'est le mots "rapports"

        biblio_instance.rapport_livres("PDF", "livres_report")
        biblio_instance.rapport_auteurs("PDF", "auteurs_report")
        biblio_instance.rapport_livres("EPUB", "livres_report")
        biblio_instance.rapport_auteurs("EPUB", "auteurs_report")
        
    else:
        print("Commande pas valide.")
        
if __name__ == '__main__':
    main()