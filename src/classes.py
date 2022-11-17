"""!

    Ce premier fichier contient les classes permettant le traitement des informations et des fichiers ics et vcf

    @author VOLQUARDSEN Alex
    @since 13/11/2022
    @version 1.0.3


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
LINE = 70

## VARIABLES GLOBAL ##

etage_actuel:bool = True

## CLASSE ##


##
# Classe contenant les opérations à effectuer sur les fichiers ics
#
# @version 1.0.2
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
    def affiche_ics(self,liste:list)->None:

        line:str = "-" * LINE

        for elements in liste:
            print(line)

            for items in elements :
                print(items)   

            print(line)
        

    ##
    # Fonction récuperant le contenue des évenements d'un icalendar
    # @param path : le fichier que l'on souhaite afficher
    def get_content_ics(self,path:str)->list:

        element:list = []
        res:list = []

        print(f"reading {path}\n")
        opened:bool = False

        with open(path, 'rb') as cal:
            ecal = Calendar.from_ical(cal.read())
            for component in ecal.walk():

                event:str = component.name

                if( (event == "VEVENT") and (opened == False)):
                    opened = True
                    summary:str = "|  Event : " + component.get("SUMMARY")
                    start:str = component.decoded("DTSTART")
                    if("+" in str(start)):
                        list_s = str(start).split("+")
                        start = list_s[0]                        
                    start = f"\n|  start on : {start}"
                    end:str = component.decoded("DTEND")
                    if("+" in str(end)):
                        list_e = str(end).split("+")
                        end = list_e[0]  
                    end = f"|  ending on : {end}\n"
                    if(component.get("LOCATION") != ""):
                        location:str = "|  location : "+component.get("LOCATION") + "\n"
                    else:
                        location:str = "|  location : Not specified"
                    if(component.get("DESCRIPTION") != ""):
                        descritpion:str = "|  description : "+component.get("DESCRIPTION")
                    else:
                        descritpion:str = "|  description : No description specified"

                is_ended:str = component.name
                if((is_ended == "VEVENT") and (opened == True)):
                    opened = False 
                    element = [summary,start,end,location,descritpion]
                    res.append(element)

                elif(is_ended != "VEVENT"):
                    pass 
                else:
                    print("\u001b[31m Erreur ! Votre fichier contient surement une erreur \u001b[37m")
                    exit

        return res
