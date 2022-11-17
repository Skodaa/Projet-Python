"""!

    Ce premier fichier contient les classes permettant le traitement des informations et des fichiers ics et vcf

    @author VOLQUARDSEN Alex
    @since 13/11/2022
    @version 1.0.2


"""

### IMPORTS ###

import sys
import os
from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime
from pathlib import Path
import pytz



### DEBUT ###

## CONSTANTES ##

ARG_LEN = len(sys.argv)

## VARIABLES GLOBAL ##

etage_actuel:bool = True

## CLASSE ##


##
# Classe contenant les opérations à effectuer sur les fichiers ics
#
# @version 1.0.1
# @since 13/11/2022
class items:

    ##
    # Constructeur de la classe ics
    # @param file_path : le chemin du fichier que l'on va traiter
    def __init__(self, file_path):
        self.path = file_path

    ##
    # Fonction permettant d'afficher l'aide et les fonctionnalités du programme
    def help(self)->None:
        print(f"Vous avez différentes commande possibles pour utliser ce programme,\n essayer donc l'une d'entre elles :")
        print(f"\t 'python3 cl.py -d [repertoire] :'")
        print(f"\n\t\t Cette commande vous permet de lister l'ensemble des fichiers .vcf ou .ics depuis le répertoire choisi.")
        print(f"\n\t 'python3 cli.py -i [fichier .ics ou .vcf]'")
        print(f"\n\t\t Cette commande vous permet d'afficher le contenu d'un fichier .vcf ou .ics")
        print(f"\n\t 'python3 cli.py -i [fichier .ics ou .vcf] -h [Nom d'un fichier .html]'")
        print(f"\n\t\t Cette commande vous permet de créer un fragment de code html \n\t\tcontenant les informations de votre fichier .vcf ou .ics ")
        print(f"\n\t 'python3 cli.py -i [fichier .ics ou .vcf] -c [Nom d'un fichier .csv]'")
        print(f"\n\t\t Cette commande vous permet d'ajouter/créer dans un fichier csv \n\t\tles informations de votre fichier .vcf ou .ics ")
        print(f"\n\t 'python3 cli.py -i [fichier .ics ou .vcf] -p [Nom d'un fichier .html]'")
        print(f"\n\t\t Cette commande vous permet de créer un squelette de page html \n\t\tcontenant les information de votre fichier .vcf ou .ics \n")

    ##
    # Fonction permettant d'afficher l'ensemble des fichier .vcf et .ics dans un répertoire et les répertoires en son sein
    # @param directory : le répertoire que l'on veut fouiller
    # @param etage : l'étage auquel on est (nombre de répertoire dans lequel on est rentré)
    def list_files(self,directory:str,etage:int)->None:
        global etage_actuel

        # Affiche le répertoire initial 
        if(etage == 0):
            tab:str = " " * etage
            print(f"\u001b[37m {tab}{directory}")
            print(f"{tab}|")
            print(f"{tab}->")

        # on traverse l'ensemble des éléments du répertoire courant
        for file in os.listdir(directory):

            f = file

            # si l'élément courant est un fichier 
            if("." in f):

                # et que ce fichier est de l'extension voulu
                if((".vcf" in f ) or (".ics" in f)):

                    # affiche le répertoire courant du fichier
                    if(etage_actuel == False):
                        tab:str = " " * etage
                        print(f"\u001b[37m {tab}{directory}")
                        print(f"{tab}|")
                        print(f"{tab}->")
                        etage_actuel = True
                    tab_file = " " * (etage+1)
                    # affiche le fichier actuel
                    print(f"\u001b[31m {tab_file}|- {f}\u001b[37m \n")
            # Si l'élément ne possède pas de "." c'est forcément un répertoire, dans ce cas
            elif(not(f.startswith(".")) or not(f.startswith("__"))):
                temp_dir:str = directory + f"\{f}"
                # appel récursivement la fonction pour traverser ce répertoire à la recherche de fichier
                etage_actuel = False
                self.list_files(temp_dir,etage+1)
                continue


    ##
    # Fonction permettant d'afficher le contenue du fichier ics
    # @param summary : le titre de l'evenement
    # @param start : le début de l'evenement
    # @param end : la fin de l'evenement
    # @param location : l'endroit ou se passe l'évenement
    # @param description : la description de l'evenement
    def affiche_ics(self,summary:str, start:str, end:str, location:str, description:str)->None:

        line:str = "-" * 50
        line = line + "\n"

        print(line)
        if(summary != None):
            sum_line = f"|  Titre : {summary}  |"
            print(sum_line)
        else:
            pass
        if(start != None):

            start_line:str = f"|  start time : {start}  |"
            print(start_line)
        else:
            pass
        if(end != None):

            end_line:str = f"|  end time : {end}   |"
            print(end_line)
        else:
            pass
        if(location != None):
            location_line = f"|  location : {location}  |"
            print(location_line)
        else:
            pass
        if(description != None):
            description_line = f"|  description : {description}  |"
            print(description_line)
            """if(len(description_line) >= 100):
                split_ind:int = len(description_line)/2
                first:str = description_line[::split_ind]
                last:str = description_line[split_ind::]
                print(f"{first}\n{last}")
            else:
                print(description_line)
                pass"""
        else:
            pass
        print(line)
        


    ##
    # Fonction permettant de lire le contenu un fichier .ics
    # @param path : le fichier que l'on souhaite afficher
    def read_ics(self,path:str)->None:

        if(path == None):
            path = self.path

        print(f"reading {path}\n")
        opened:bool = False

        with open(path, 'rb') as cal:
            ecal = Calendar.from_ical(cal.read())
            for component in ecal.walk():

                event:str = component.name

                if( (event == "VEVENT") and (opened == False)):
                    opened = True
                    summary:str = component.get("SUMMARY")
                    start:str = component.decoded("DTSTART")
                    end:str = component.decoded("DTEND")
                    location:str = component.get("LOCATION")
                    descritpion:str = component.get("DESCRIPTION")

                is_ended:str = component.name

                if((is_ended == "VEVENT") and (opened == True)):
                    opened = False
                    self.affiche_ics(summary,start,end,location,descritpion)
                    
                else:
                    print("\u001b[31m Erreur ! Votre fichier contient surement une erreur \u001b[37m")
                    exit

