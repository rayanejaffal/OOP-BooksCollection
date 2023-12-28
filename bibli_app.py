#!/usr/bin/env python3

import argparse
from bibli import bibli
import configparser

def parse_config(config_file='bibli.conf'):
    config = configparser.ConfigParser()
    config.read(config_file)
    livres_path = config['Bibliotheque']['bibliotheque']
    rapports_path = config['Bibliotheque']['etats']
    nbmax = int(config['Bibliotheque']['nbmax'])
    return livres_path, rapports_path, nbmax

def main():
    print("Script is running...")
    parser = argparse.ArgumentParser(description='Bibli Application')
    parser.add_argument('-c', '--config', help='Specify configuration file', default='biblio.conf')
    parser.add_argument('command', choices=['collect', 'reports'], help='Command to execute')
    parser.add_argument('url', nargs='?', help='URL for collection (required for collect command)')
    parser.add_argument('depth', type=int, nargs='?', help='Depth for collection (required for collect command)')
    args = parser.parse_args()

    livres_path, rapports_path, nbmax = parse_config(args.config)
    biblio_instance = bibli(livres_path, rapports_path)

    if args.command == 'collect':
        # Example usage: ./main.py -c biblio.conf collect https://math.univ-angers.fr/~jaclin/biblio/livres 1
        biblio_instance.alimenter(args.url, args.depth, nbmax)
    elif args.command == 'reports':

        biblio_instance.rapport_livres("PDF", "livres_report")
        biblio_instance.rapport_auteurs("PDF", "auteurs_report")
        biblio_instance.rapport_livres("EPUB", "livres_report")
        biblio_instance.rapport_auteurs("EPUB", "auteurs_report")

if __name__ == '__main__':
    main()