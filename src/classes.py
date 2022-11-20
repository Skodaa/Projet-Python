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
import csv



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
    # Constructeur de la classe items (nom random parce que je ne savais pas comment la nommer)
    # @param file_path : le chemin du fichier que l'on va traiter
    def __init__(self, file_path):
        self.path = file_path
        
    """
                    *********************************
                    ********* TRONC COMMUN **********
                    *********************************
    """

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
    # Fonction permettant d'afficher le contenue d'un fichier à l'aide de la liste obtenue dans la fonction get_content
    # @param liste : la liste des elements à afficher
    def afficher(self,liste:list)->None:

        line:str = "-" * LINE

        for elements in liste:
            print(line)

            for items in elements :
                print(items)   

            print(line)
        



    """
                    *********************************
                    ********** PARTIE ICS ***********
                    *********************************    
    """


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
                    end = f"\n|  ending on : {end}"
                    if(component.get("LOCATION") != ""):
                        location:str = "\n|  location : "+component.get("LOCATION")
                    else:
                        location:str = "|  location : Not specified"
                    if(component.get("DESCRIPTION") != ""):
                        descritpion:str = "\n|  description : "+component.get("DESCRIPTION")
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

    ##
    # Fonction permettant de créer un fragment HTML contenant les VEVENT d'un fichier ics et les écrit dans un fichier
    # @param liste : l'ensemble des éléments des VEVENT
    # @param file : le fichier dans lequel on écrit le fragment
    def fragment_ics(self,liste:list,file:str)->None:
        """
        Format d'un fragment VEVENT utilisé :

        <div class="vevent">
        <div class="summary">Summary</div>
        <abbr class="dtstart" title="20070824">date</abbr> - 
        <abbr class="dtend" title="20070827">date</abbr>
        <div class="location">adresse</div>
        <div class="description">description</div>
        </div>
        """
        
        with open(file, 'a+', encoding='utf-8') as frag:
            
            i:int = 0
            trait:str = "-" * 40

            for elements in liste:
                
                for items in elements :
                    
                    match i :
                        case 0:
                            line:str = f"<p>{trait}<p>"
                            line = f"{line}\n<div class=\"vevent\">\n<div class=\"summary\">{items}</div>\n"
                            frag.write(line)
                            i += 1
                        case 1:
                            line = f"\t<abbr class=\"dtstart\"> {items} </abbr>\n"
                            frag.write(line)
                            i += 1
                        case 2:
                            line = f"\t<abbr class=\"dtend\"> {items} </abbr>\n"
                            frag.write(line)
                            i += 1
                        case 3 :
                            line = f"\t<div class=\"location\">{items}</div>\n"
                            frag.write(line)
                            i += 1
                        case 4:
                            line = f"\t<div class=\"description\">{items}</div>\n</div>\n"
                            frag.write(line)
                            i = 0

    ##
    # Fonction permettant d'écrire les evenements dans un fichier csv
    # @param liste : la liste des évenements à rentrer dans le csv
    # @param file : le csv que l'on veut remplir
    def csv_ics(self,liste:list,file:str)->None:

        """
        Format du csv :

        summary,start,end,location,description
        """

        file_exist:bool = os.path.exists(file)

        with open(file, 'a+', encoding='UTF-8', newline='') as file:

            writer = csv.writer(file)

            if file_exist == False :
                header:list = ["summary","start","end","location","description"]
                print(header)
                writer.writerow(header)

            for elements in liste:

                row:list = []

                for items in elements:
                    splitter:str = items.split(" : ")
                    obj = splitter[1]
                    print(obj)
                    row.append(obj)
                writer.writerow(row)


    ##
    # Fonction qui va créer un squelette de page html contenant les fragments html des évenements
    # @param liste : liste des éléments contenue dans les évenements
    # @param file : la page qui sera créer
    def page_ics(self,liste:list,file:str)->None:

        heading:str = "<!DOCTYPE html>\n<html lang=\"fr\">\n<head>\n\t<meta charset=\"utf-8\">\n\t<title>évenements de votre calendrier</title>\n</head>\n<body>"
        ending:str = "</body>\n</html>"

        with open(file, 'a+', encoding='UTF-8') as page:

            page.write(heading)
        
        self.fragment_ics(liste,file)

        with open(file, 'a', encoding='UTF-8') as page:
            page.write(ending)

    """
                    *********************************
                    ********** PARTIE VCF ***********
                    *********************************    
    """


    ##
    # Fonction permettant de récuperer les informations dans un fichier vcf
    # @param path : le fichier que l'on veut ouvrir
    def get_content_vcf(self,path:str)->list:

        """
        Format de vcard que l'on veut récupérer : 

        N: name 
        FN : fullname
        ORG : organisation he/she works for
        TITLE : job he/she's doing 
        NICKNAME : nickname of the sb
        GENDER : the gender
        BDAY : birthday date
        EMAIL : personal email
        EMAIL : work email
        TEL : cellphone of the sb
        TEL : work phone
        ADR : home adress
        ADR : work adress       
        """

        element:list = []
        res:list = []

        is_opened:bool = False

        print(f" reading : {path}\n")

        with open(path, 'rb') as file:
            
            for lines in file:

                decoded = lines.decode('utf-8')
                ini_split = decoded.split("\r")
                proper_line = ini_split[0]
                
                if('BEGIN:VCARD' in proper_line):
                    is_opened = True
                    nom:str = "nom : non renseigner"
                    prenom:str = "prenom : non renseigner"
                    second_prenom:str = "second prenom : non renseigner"
                    gender:str = "genre : sac wallmart"
                    nickname:str = "surnom : non renseigner"
                    organisation:str = "entreprise : non renseigner"
                    title:str = "emploi : non renseigner"
                    birthday:str = "date de naissance : non renseigner"
                    email_home:str = "email privee : non renseigner"
                    email_work:str = "email pro : non renseigner"
                    work_phone:str = "numéro pro : non renseigner"
                    personal_phone:str = "numéro privé : non renseigner"
                    adr_home:str = "adresse : non renseigner"
                    adr_work:str = "lieu de travail : non renseinger"

                elif((is_opened == True)and not("END:VCARD" in proper_line)):
                    splitter:list = proper_line.split(":")
                    line = splitter[0]
                    if((line.startswith("N;"))or(line.startswith("N:"))):
                        line = splitter[1]
                        if(";" in line):
                            resplitter:list = line.split(";")
                        else:
                            resplitter:list = line.split(" ")
                        nom = f"\nnom : {resplitter[0]}"
                        prenom = f"\nprenom : {resplitter[1]}"
                        if(len(resplitter)>3):
                            second_prenom = f"\nsecond prenom : {resplitter[2]}"
                            gender = f"\ngender : {resplitter[3]}"
                        else:
                            gender = f"\ngender : {resplitter[2]}"
                    elif("NICKNAME" in line):
                        nickname = f"\nnickname : {splitter[1]}"
                    elif("GENDER" in line):
                        gender = f"\ngender : {splitter[1]}"
                    elif("ORG" in line):
                        organisation = f"\nentreprise : {splitter[1]}"
                    elif("TITLE" in line):
                        title = f"\nemploi : {splitter[1]}"
                    elif("BDAY" in line):
                        birthday = f"\ndate de naissance : {splitter[1]}"
                    elif("EMAIL" in line):
                        if("HOME" in line):
                            email_home = f"\nemail perso : {splitter[1]}"
                        elif("WORK" in line):
                            email_work = f"\nemail pro : {splitter[1]}"
                    elif("TEL" in line):
                        if("WORK" in line):
                            work_phone = f"\ntelephone pro : {splitter[1]}"
                        elif(("HOME" in line )or ("CELL" in line)):
                            personal_phone = f"\ntelephone privee : {splitter[1]}"
                    elif("ADR" in line):
                        adr = splitter[1]
                        adr = adr.replace(";" , " ")
                        if("HOME" in line):
                            adr_home = f"\nadresse : {adr}"
                        elif("WORK" in line):
                            adr_work = f"\nlieu de travail : {adr}"
                
                elif("END:VCARD" in proper_line):
                    is_opened = False
                    element = [nom,prenom,second_prenom,gender,nickname,organisation,title,birthday,email_home,email_work,work_phone,personal_phone,adr_home,adr_work]
                    res.append(element)
                else:
                    pass
        return res


    ##
    # Fonction permettant de créer un fragment HTML contenant les Vcard d'un fichier vcf et les écrit dans un fichier donné en argument
    # @param liste : l'ensemble des éléments des vcard
    # @param file : le fichier dans lequel on écrit le fragment
    def fragment_vcf(self,liste:list,file:str)->None:
        """
        Format d'un fragment vcard utilisé :

        <div class="vcard">
            <div class="fn">Full name</div>
            <div class="gender"> gender </div>
            <div class="nickname">nickname</div>
            <div class="org">organisation</div>
            <div class="title">title</div>
            <div class="bday">date</div>
            <div class="email_pro">email</div>
            <div class="email_private">email</div>
            <div class="phone_pro">phone</div>
            <div class="phone_private>phone</div>
            <div class="adr_pro">adresse</div>
            <div class="adr_private>adresse</div>
        </div>
        """
        
        with open(file, 'a+', encoding='utf-8') as frag:
            
            trait:str = "-" * 40


            for elements in liste:

                i:int = 0
                size:int = len(elements)
                temp_list:list = []
                
                while(i < size):
                    temp:list = elements[i].split(" : ")
                    item:str = temp[1]
                    temp_list.append(item)
                    i += 1


                line:str = f"<p>{trait}</p>\n<div class=\"vcard\">\n\t<div class=\"fn\">{temp_list[0]} {temp_list[1]} {temp_list[2]}"
                line = f"{line}</div>\n\t<div class=\"gender\">{temp_list[3]}</div>\n\t<div class=\"nickname\">{temp_list[4]}</div>"
                line = f"{line}\n\t<div class=\"org\">{temp_list[5]}</div>\n\t<div class=\"title\">{temp_list[6]}</div>"
                line = f"{line}\n\t<div class=\"bday\">{temp_list[7]}</div>\n\t<div class=\"email_pro\">{temp_list[8]}</div>"
                line = f"{line}\n\t<div class=\"email_private\">{temp_list[9]}</div>\n\t<div class=\"phone_pro\">{temp_list[10]}</div>"
                line = f"{line}\n\t<div class=\"phone_private\">{temp_list[11]}</div>\n\t<div class=\"adr_pro\">{temp_list[12]}</div>"
                line = f"{line}\n\t<div class=\"adr_private\">{temp_list[13]}</div>\n</div>"
                
                frag.write(line)
            

    ##
    # Fonction permettant d'écrire les evenements dans un fichier csv
    # @param liste : la liste des évenements à rentrer dans le csv
    # @param file : le csv que l'on veut remplir
    def csv_vcf(self,liste:list,file:str)->None:

        """
        Format du csv :

        nom,prenom,second_prenom,gender,nickname,organisation,title,birthday,email_home,email_work,work_phone,personal_phone,adr_home,adr_work
        """

        file_exist:bool = os.path.exists(file)

        with open(file, 'a+', encoding='UTF-8', newline='') as file:

            writer = csv.writer(file)

            if file_exist == False :
                header:list = ["nom,prenom,second_prenom,gender,nickname,organisation,title,birthday,email_home,email_work,work_phone,personal_phone,adr_home,adr_work"]
                print(header)
                writer.writerow(header)

            for elements in liste:

                row:list = []

                for items in elements:
                    splitter:str = items.split(" : ")
                    obj = splitter[1]
                    print(obj)
                    row.append(obj)
                writer.writerow(row)


    ##
    # Fonction qui va créer un squelette de page html contenant les fragments html des évenements
    # @param liste : liste des éléments contenue dans les évenements
    # @param file : la page qui sera créer
    def page_vcf(self,liste:list,file:str)->None:

        heading:str = "<!DOCTYPE html>\n<html lang=\"fr\">\n<head>\n\t<meta charset=\"utf-8\">\n\t<title>évenements de votre calendrier</title>\n</head>\n<body>"
        ending:str = "</body>\n</html>"

        with open(file, 'a+', encoding='UTF-8') as page:

            page.write(heading)
        
        self.fragment_vcf(liste,file)

        with open(file, 'a', encoding='UTF-8') as page:
            page.write(ending)
                