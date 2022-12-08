"""!

    Ce programme contient 

    @author VOLQUARDSEN Alex
    @since 13/11/2022
    @version 1.0.3


"""

### IMPORTS ###

import sys
import os
import csv



### DEBUT ###

## CONSTANTES ##

# Taille pour effectuer des lignes dans les affichages terminale
LINE = 70

## VARIABLES GLOBAL ##

# variable utiliser pour déterminer l'étage initiale lors de la recherche dans des répertoire
etage_actuel:bool = True

## CLASSES ##

##
# Classe contenant les opérations de base à effectuer sur les fichiers
#
# @version 1.2.1
# @since 13/11/2022
class items:

    ##
    # Constructeur de la classe items (nom random parce que je ne savais pas comment la nommer)
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
            # on augmente la "tabulation" lorsque l'on rentre dans un nouveau répertoire et inversement
            tab:str = " " * etage
            # on affiche le nom du répertoire et on met en forme la recherche
            print(f"\u001b[37m {tab}{directory}")
            print(f"{tab}|")
            print(f"{tab}->")

        # on traverse l'ensemble des éléments du répertoire courant
        for file in os.listdir(directory):

            f = file # le fichier courament tester dans la boucle

            # si l'élément courant est un fichier 
            if("." in f):
                # et que ce fichier est de l'extension voulu
                if((".vcf" in f ) or (".ics" in f)):
                    # affiche le répertoire courant du fichier
                    if(etage_actuel == False):
                        # on met en forme l'affichage
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
                temp_dir:str = directory + f"/{f}"
                # appel récursivement la fonction pour traverser ce répertoire à la recherche de fichier
                etage_actuel = False
                # on appel la fonction récursivement pour continuer le listage des fichiers
                self.list_files(temp_dir,etage+1)
                continue

    ##
    # Fonction permettant d'afficher le contenue d'un fichier à l'aide de la liste obtenue dans la fonction get_content
    # @param liste : la liste des elements à afficher
    def afficher(self,liste:list)->None:

        # on créer une ligne pour rendre l'affichage plus lisible
        line:str = "-" * LINE

        # si la taille de la liste est 5, c'est que nous avons un fichier ics
        if(len(liste[0]) == 5):
            # on affiche les élements contenue dans la liste
            for elements in liste:
                print(line)

                print(f"|  Event : {elements[0]}")
                print(f"|  start on : {elements[1]}")
                print(f"|  ending on : {elements[2]}")
                print(f"|  location : {elements[3]}")
                print(f"|  description : {elements[4]}")

                print(line)

        # si la liste est de taille 13, nous avons donc un fichier vcf a afficher
        elif(len(liste[0]) == 13):

            # encore une fois nous affichons les données de façon structuré
            for elements in liste:

                print(line)

                print(f"| nom : {elements[0]}")
                print(f"| prenom : {elements[1]}")
                print(f"| second_prenom : {elements[2]}")
                print(f"| nickname : {elements[3]}")
                print(f"| organisation : {elements[4]}")
                print(f"| title : {elements[5]}")
                print(f"| birthday : {elements[6]}")
                print(f"| personnal email : {elements[7]}")
                print(f"| work email : {elements[8]}")
                print(f"| work phone : {elements[9]}")
                print(f"| personnal phone : {elements[10]}")
                print(f"| home address : {elements[11]}")
                print(f"| work address : {elements[12]}")

                print(line)

        


    """
                    *********************************
                    ********** PARTIE ICS ***********
                    *********************************    
    """
##
# Classe contenant les opérations à effectuer sur les fichiers ics
#
# @version 1.1.9
# @since 13/11/2022
class ics(items):

    ##
    # fonction d'initialisation de la classe ics
    def __init__(self, file_path):
        super().__init__(file_path)

        ##
    # Fonction récuperant le contenue des évenements d'un icalendar
    # @param path : le fichier que l'on souhaite afficher
    def get_content_ics(self,path:str)->list:

        # liste des élements d'un évenement 
        element:list = []
        # liste contenant les listes des autres éléments
        res:list = []

        # on affiche un message pour montrer que l'on traite le fichier
        print(f"reading {path}\n")
        # on regarde si on entre dans un evenement
        is_opened:bool = False
        # Comme dans un calendar on peut tomber plusieurs fois sur le terme "BEGIN" on s'assure que c'est bien au bon endroit que l'on cherche
        danger:bool = False
        with open(path, 'rb') as file:
            # on inspecte chaque ligne du fichier
            for lines in file:

                # on décode chaque lignes en utf-8
                decoded = lines.decode('utf-8')
                ini_split = decoded.split("\r")
                proper_line = ini_split[0]

                # Lorsque l'on trouve un début d'evenement
                if('BEGIN:VEVENT' in proper_line):
                    # on considere que l'on rentre dans l'évenement
                    is_opened = True
                    # on initialise les valeurs pour s'assurer qu'aucunes d'entre elle ne soit null
                    summary:str = "Non renseigner"
                    start:str = "Non renseigner"
                    end:str = "Non renseigner"
                    location:str = "Non renseigner"
                    descritpion:str = "Non renseigner"

                # si nous somme considéré dans l'évenement mais que nous trouvons un autre BEGIN
                elif((is_opened == True) and("BEGIN" in proper_line)):
                    # nous passons danger à vrai
                    danger = True
                # si danger est vrai et que nous trouvons un END 
                elif((danger == True) and ("END" in proper_line)):
                    # nous repassons danger à faux
                    danger = False

                # si nous somme dans l'évenement et que la ligne n'est pas une fin d'évenement et que danger est faux
                elif((is_opened == True)and not("END:VEVENT" in proper_line) and (danger == False)):
                    # on sépare la ligne en deux via le charactère ":" forcément présent
                    splitter:list = proper_line.split(":")
                    # on récupère la première partie de la ligne
                    line = splitter[0]
                    
                    # Si la ligne contient "DTSTART"
                    if("DTSTART" in line):
                        # on sépare la chaine de charactere si elle peut l'être
                        resplitter = splitter[1].split("T")
                        start = ""
                        # on met en forme la date de début de l'evenement
                        for i in range(len(resplitter[0])):
                            if(i == 4 or i == 6):
                                start = start + "/" + resplitter[0][i]
                            else:
                                start = start + resplitter[0][i]
                    # si la ligne contient "DTEND"
                    elif("DTEND" in line):
                        resplitter = splitter[1].split("T")
                        end = ""
                        # on met en forme la date de fin de l'evenement
                        for i in range(len(resplitter[0])):
                            if(i == 4 or i == 6):
                                end = end + "/" + resplitter[0][i]
                            else:
                                end = end + resplitter[0][i]
                    # on associe les valeurs aux variables corrrespondantes
                    elif("SUMMARY" in line):
                        summary = splitter[1]
                    elif("DESCRIPTION" in line):
                        descritpion = splitter[1]
                    elif("LOCATION" in line):
                        location = splitter[1]
                    
                # si nous reperons la fin de l'evenement, nous ajoutons les valeurs dans une liste et nous "fermons" l'evenement
                elif("END:VEVENT" in proper_line):
                    is_opened = False
                    element = [summary,start,end,location,descritpion]
                    res.append(element)
                else:
                    pass
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
        
        # nous ouvrons le fichier de sorte à ajouter des éléments au fichier existant ou créant un fichier s'il n'existe pas
        with open(file, 'a+', encoding='utf-8') as frag:
            
            i:int = 0
            trait:str = "-" * 40

            # nous traversons la liste des listes d'éléments
            for elements in liste:
                # nous traversons la liste d'éléments courantes
                for items in elements :
                    # nous écrivons dans ce fichier le fragment html
                    match i :
                        case 0:
                            line:str = f"<p class=\"separator\">{trait}<p>"
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

        # nous verifions si le fichier existe
        file_exist:bool = os.path.exists(file)

        # nous ouvrons le fichier 
        with open(file, 'a+', encoding='UTF-8', newline='') as file:

            # on créer un objet pour écrire dans un fichier csv
            writer = csv.writer(file)

            # si le fichier n'existe pas à la base, nous écrivons une en-tête au fichier CSV
            if file_exist == False :
                header:list = ["summary","start","end","location","description"]
                writer.writerow(header)
            # nous ajoutons les éléments dans le CSV
            for elements in liste:

                row:list = []

                for items in elements:
                    obj = items
                    row.append(obj)
                writer.writerow(row)


    ##
    # Fonction qui va créer un squelette de page html contenant les fragments html des évenements
    # @param liste : liste des éléments contenue dans les évenements
    # @param file : la page qui sera créer
    def page_ics(self,liste:list,file:str)->None:

        # en-tête et pied-de-page du squelette de page html
        heading:str = "<!DOCTYPE html>\n<html lang=\"fr\">\n<head>\n\t<meta charset=\"utf-8\">\n\t<title>évenements de votre calendrier</title>\n</head>\n<body>"
        ending:str = "</body>\n</html>"

        # nous ouvrons le fichier et nous ajoutons en-tête, bas de page et les fragments html 
        with open(file, 'a+', encoding='UTF-8') as page:

            page.write(heading)
        
        self.fragment_ics(liste,file)

        with open(file, 'a', encoding='UTF-8') as page:
            page.write(ending)


    ##
    # Fonction permettant de modifier le contenue d'un fichier ics
    # @param liste : liste contenant les éléments avant modification
    # @param liste_replace : liste contenant les éléments modifiés par l'utilisateur
    # @param file : le fichier dans lequel on va enregistrer les modifications 
    # @param index : l'index de l'évenement à modifié pour ne pas modifié inutilement d'autres éléments
    def modify_ics(self,liste:list,liste_replace:list,file:str,index:int)->None:
        
        # on récupere la taille de la liste
        size:int = len(liste)
        i:int = 0
        opened:bool = False

        # on traverse l'ensemble des élements de la liste
        for i in range(size):
            # on récupère l'élément courant de chaque liste
            initial:str = liste[i]
            after:str = liste_replace[i]
            place:int = 0
            # si les éléments des deux listes sont les même on ne  change rien
            if(initial != after):

                # sinon on ouvre le fichier en mode lecture
                with open(file, 'r',encoding='UTF-8') as file_r:
                    # on va récupérer sous forme de liste l'ensembe des lignes du fichier
                    data = file_r.readlines()
                    # on récupère les informations qui nous intéresse 
                    split:list = initial.split(":")
                    temoi:str = split[0]
                    init_word:str = split[1]
                    split_end:list = after.split(":")
                    temoi_end:str = split_end[0]
                    end:str = split_end[1]
                                                
                    y:int = 0
                    # on traverse les élements de la liste
                    for y in range(len(data)):
                        elements = data[y]
                        # on va vérifier les élements et modifier en fonction de l'élément courant de la liste
                        if(elements.startswith("BEGIN:VEVENT")):
                            place += 1
                            opened = True
                        if(elements.startswith("END:VEVENT")):
                            opened = False
                        if((place == index)and(opened == True)):
                            if(init_word != end):
                                 # on annule la mise ne forme de la date précedemment effectuer
                                if("DTSTART" in temoi):
                                    if(elements.startswith("DTSTART")):
                                        split = end.split("/")
                                        end1 = split[0]
                                        end2 = split[1]
                                        end3 = split[2]
                                        data[y] = f"{temoi_end}:{end1}{end2}{end3}\n"
                                if("DTEND" in temoi):
                                    if(elements.startswith("DTEND")):
                                        split = end.split("/")
                                        end1 = split[0]
                                        end2 = split[1]
                                        end3 = split[2]
                                        data[y] = f"{temoi_end}:{end1}{end2}{end3}\n"
                                elif(elements.startswith(temoi)):
                                    if(init_word == "Not specified"):
                                        data[y] = f"{temoi_end}:{end}\n"
                                    else:
                                        data[y] = elements.replace(init_word,end)
                # on réouvre le fichier en mode ecriture pour prendre en compte les modifications
                with open(file, 'w', encoding='UTF-8') as file_w:

                    file_w.write("".join(str(item) for item in data))

    """
                    *********************************
                    ********** PARTIE VCF ***********
                    *********************************    
    """

##
# Classe contenant les opérations à effectuer sur les fichiers vcf
#
# @version 1.1.9
# @since 13/11/2022
class vcf(items):

    ##
    # fonction d'initialisation de la classe
    # @param file_path : le chemin du fichier
    def __init__(self, file_path):
        super().__init__(file_path)


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
        BDAY : birthday date
        EMAIL : personal email
        EMAIL : work email
        TEL : cellphone of the sb
        TEL : work phone
        ADR : home adress
        ADR : work adress       
        """

        # on créer une liste qui contiendras des éléments et une liste qui contiendras cest listes
        element:list = []
        res:list = []

        is_opened:bool = False
        # on affiche un message pour informer que l'on traite le fichier
        print(f" reading : {path}\n")

        # on ouvre le fichier pour le lire
        with open(path, 'rb') as file:
            # on regarde les lignes du fichier une par une
            for lines in file:
                # on decode ces lignes en utf-8
                decoded = lines.decode('utf-8')
                ini_split = decoded.split("\r")
                proper_line = ini_split[0]
                
                # si on remarque l'ouverture d'une carte, on initialise les variables
                if('BEGIN:VCARD' in proper_line):
                    is_opened = True
                    nom:str = "non renseigner"
                    prenom:str = "non renseigner"
                    second_prenom:str = "non renseigner"
                    nickname:str = "non renseigner"
                    organisation:str = "non renseigner"
                    title:str = "non renseigner"
                    birthday:str = "non renseigner"
                    email_home:str = "non renseigner"
                    email_work:str = "non renseigner"
                    work_phone:str = "non renseigner"
                    personal_phone:str = "non renseigner"
                    adr_home:str = "non renseigner"
                    adr_work:str = "non renseinger"

                # si on est dans la carte et que la ligne n'est pas la fin de la carte on traite les informations
                elif((is_opened == True)and not("END:VCARD" in proper_line)):
                    splitter:list = proper_line.split(":")
                    line = splitter[0]
                    # si jamais on tombe sur un N; ou un N: on sépare les informations de façon précise correspondant à la mise en forme du fichier
                    if((line.startswith("N;"))or(line == "N")):
                        line = splitter[1]
                        if(";" in line):
                            resplitter:list = line.split(";")
                        else:
                            resplitter:list = line.split(" ")
                        nom = resplitter[0]
                        prenom = resplitter[1]
                        if(len(resplitter)>3):
                            second_prenom = resplitter[2]
                    elif("NICKNAME" in line):
                        nickname = splitter[1]
                    elif("ORG" in line):
                        organisation = splitter[1]
                    elif("TITLE" in line):
                        title = splitter[1]
                    elif("BDAY" in line):
                        birthday = splitter[1]
                    elif("EMAIL" in line):
                        if("HOME" in line):
                            email_home = splitter[1]
                        elif("WORK" in line):
                            email_work = splitter[1]
                    elif("TEL" in line):
                        if("WORK" in line):
                            work_phone = splitter[1]
                        elif(("HOME" in line )or ("CELL" in line)):
                            personal_phone = splitter[1]
                    elif("ADR" in line):
                        adr = splitter[1]
                        adr = adr.replace(";" , " ")
                        if("HOME" in line):
                            adr_home = adr
                        elif("WORK" in line):
                            adr_work = adr
                        else:
                            adr_home = adr
                # si on repere la fin d'une carte ou met les informations dan une liste et on met cette liste dans une liste
                elif("END:VCARD" in proper_line):
                    is_opened = False
                    element = [nom,prenom,second_prenom,nickname,organisation,title,birthday,email_home,email_work,work_phone,personal_phone,adr_home,adr_work]
                    res.append(element)
                # si la ligne ne compte pas d'élément interessant, on passe à la prochaine
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
        # on ouvre le fichier ou on le créer
        with open(file, 'a+', encoding='utf-8') as frag:
            
            trait:str = "-" * 40

            # on traverse les éléments de la liste 
            for elements in liste:
                i:int = 0
                size:int = len(elements)
                temp_list:list = []
                # on ajoute les elements dans une liste
                while(i < size):
                    item:str = elements[i]
                    temp_list.append(item)
                    i += 1

                # on créer le fragment html puis on l'écrit dans le fichier
                line:str = f"<p class=\"separator\">{trait}</p>\n<div class=\"vcard\">\n\t<div class=\"fn\">{temp_list[0]} {temp_list[1]} {temp_list[2]}"
                line = f"{line}</div>\n\t<div class=\"nickname\">{temp_list[3]}</div>"
                line = f"{line}\n\t<div class=\"org\">{temp_list[4]}</div>\n\t<div class=\"title\">{temp_list[5]}</div>"
                line = f"{line}\n\t<div class=\"bday\">{temp_list[6]}</div>\n\t<div class=\"email_pro\">{temp_list[7]}</div>"
                line = f"{line}\n\t<div class=\"email_private\">{temp_list[8]}</div>\n\t<div class=\"phone_pro\">{temp_list[9]}</div>"
                line = f"{line}\n\t<div class=\"phone_private\">{temp_list[10]}</div>\n\t<div class=\"adr_pro\">{temp_list[11]}</div>"
                line = f"{line}\n\t<div class=\"adr_private\">{temp_list[12]}</div>\n</div>"
                
                frag.write(line)
            

    ##
    # Fonction permettant d'écrire les evenements dans un fichier csv
    # @param liste : la liste des évenements à rentrer dans le csv
    # @param file : le csv que l'on veut remplir
    def csv_vcf(self,liste:list,file:str)->None:

        """
        Format du csv :

        nom,prenom,second_prenom,nickname,organisation,title,birthday,email_home,email_work,work_phone,personal_phone,adr_home,adr_work
        """

        # on vérifie si le fichier existe déjà
        file_exist:bool = os.path.exists(file)

        # ouvre le fichier ou le créer si jamais il n'existe pas
        with open(file, 'a+', encoding='UTF-8', newline='') as file:

            writer = csv.writer(file)
            # si le fichier n'existais pas, nous ajoutons l'en-tête au fichier
            if file_exist == False :
                header:list = ["nom,prenom,second_prenom,nickname,organisation,title,birthday,email_home,email_work,work_phone,personal_phone,adr_home,adr_work"]
                writer.writerow(header)
            # on ajoute les elements de la liste au fichier
            for elements in liste:

                row:list = []

                for items in elements:
                    obj = items
                    row.append(obj)
                writer.writerow(row)


    ##
    # Fonction qui va créer un squelette de page html contenant les fragments html des évenements
    # @param liste : liste des éléments contenue dans les évenements
    # @param file : la page qui sera créer
    def page_vcf(self,liste:list,file:str)->None:

        heading:str = "<!DOCTYPE html>\n<html lang=\"fr\">\n<head>\n\t<meta charset=\"utf-8\">\n\t<title>évenements de votre calendrier</title>\n</head>\n<body>"
        ending:str = "</body>\n</html>"
        # même principe que pour les fichiers ics, nous créons un squelette de page html contenant les fragments de carte
        with open(file, 'a+', encoding='UTF-8') as page:

            page.write(heading)
        
        self.fragment_vcf(liste,file)

        with open(file, 'a', encoding='UTF-8') as page:
            page.write(ending)

    ##
    # Fonction permettant de modifier le contenue d'un fichier vcf
    # @param liste : liste des éléments à remplacer
    # @param liste_replace : liste des éléments de remplacement
    # @param file : le fichier dans lequel on applique les modifications
    def modify_vcf(self,liste:list,liste_replace:list,file:str)->None:
        
        size:int = len(liste)
        i:int = 0
        # on traverse les listes à la recherche des éléments à modifier
        for i in range(size):
            
            initial:str = liste[i]
            after:str = liste_replace[i]
            # si les éléments sont identique on ne fait rien sinon on agis sur la liste
            if(initial != after):
                # on ouvre le fichier en lecture
                with open(file, 'r',encoding='UTF-8') as file_r:
                    
                    # on récupère chaque ligne dans une liste 
                    data = file_r.readlines()

                    split:list = initial.split(":")
                    temoi:str = split[0]
                    init_word:str = split[1]
                    split_end:list = after.split(":")
                    temoi_end:str = split_end[0]
                    end:str = split_end[1]
                    # Comme certains éléments peuvent ne pas être présent dans une carte, on vérifie s'ils sont présent
                    nick_ = False
                    org_ = False
                    title_ = False
                    bday_ = False
                    pro_mail_ = False
                    pri_mail_ = False
                    pro_phone_ = False
                    pri_phone_ = False
                    pro_adr_ = False
                    pri_adr_ = False
                    for elements in data:
                        if(elements.startswith("NICKNAME")):
                            nick_ = True
                        if(elements.startswith("ORG")):
                            org_ = True
                        if(elements.startswith("TITLE")):
                            title_ = True
                        if(elements.startswith("BDAY")):
                            bday_ = True
                        if(elements.startswith("EMAIL")):
                            if("WORK" in elements):
                                pro_mail_ = True
                            if("HOME" in elements):
                                pri_mail_ = True
                        if(elements.startswith("TEL")):
                            if("WORK" in elements):
                                pro_phone_ = True
                            if("HOME" in elements or "CELL" in elements):
                                pri_phone_ = True
                        if(elements.startswith("ADR")):
                            if("WORK" in elements):
                                pro_adr_ = True
                            if("HOME" in elements):
                                pri_adr_ = True
        
                    # une fois la vérification faite, si l'élément existe, nous le modifions
                    y:int = 0
                    for y in range(len(data)):
                        elements = data[y]
                        if(init_word != end):
                            if(temoi == "FN"):
                                if((temoi in elements)or("N:" in elements)or("N;" in elements)):
                                    data[y] = elements.replace(init_word,end)
                            if(temoi == "NICKNAME"):
                                if(temoi in elements):
                                    data[y] = elements.replace(init_word,end)
                            if(temoi == "ORG"):
                                if(temoi in elements):
                                    data[y] = elements.replace(init_word,end)
                            if(temoi == "TITLE"):
                                if(temoi in elements):
                                    data[y] = elements.replace(init_word,end)
                            if(temoi == "BDAY"):
                                if(temoi in elements):
                                    data[y] = elements.replace(init_word,end)
                            if(temoi == "EMAIL"):
                                if(pri_mail_ == True):
                                    if(temoi in elements):
                                        if("HOME" in elements and "HOME" in temoi_end):
                                            print("home reperé")
                                            data[y] = elements.replace(init_word,end)          
                                if(pro_mail_ == True):
                                    if(temoi in elements):
                                        if("WORK" in elements and "WORK" in temoi_end):
                                            data[y] = elements.replace(init_word,end)
                                
                            if(temoi == "TEL"):
                                if(pro_phone_ == True):
                                    if(elements.startswith("TEL")):
                                        if("WORK" in elements and "WORK" in temoi_end):
                                            data[y] = elements.replace(init_word,end)
    
                                if(pri_phone_ == True):
                                    if(elements.startswith("TEL")):
                                        if("HOME" in elements or "CELL" in elements and "HOME" in temoi_end):
                                            data[y] = elements.replace(init_word,end)

                            if(temoi == "ADR"):
                                split = elements.split(":")
                                mod = split[1].replace(";"," ")
                                elements = f"{split[0]}:{mod}"
                                if(pri_adr_ == True):
                                    if(elements.startswith("ADR")):
                                        if("HOME" in elements and "HOME" in temoi_end):
                                            print(f"HOME {elements}")
                                            data[y] = elements.replace(init_word,end)

                                if(pro_adr_ == True):
                                    if(elements.startswith("ADR")):
                                        if(("WORK" in elements) and ("WORK" in temoi_end)):
                                            print(f"WORK {elements}")
                                            data[y] = elements.replace(init_word,end)
                        # si l'élément n'existe pas, on le créer 
                        if(nick_ != True):
                            if(temoi_end == "NICKNAME"):
                                temp:str = data[-1]
                                data[-1] = f"NICKNAME;CHARSET=UTF-8:{end}\n"
                                data.append(temp)
                                nick_ = True
                        if(org_ != True):
                            if(temoi_end == "ORG"):
                                temp = data[-1]
                                data[-1] = f"ORG;CHARSET=UTF-8:{end}\n"
                                data.append(temp)
                                org_ = True
                        if(title_ != True):
                            if(temoi_end == "TITLE"):
                                temp = data[-1]
                                data[-1] = f"TITLE;CHARSET=UTF-8:{end}\n"
                                data.append(temp)
                                title_ = True
                        if(bday_ != True):
                            if(temoi_end == "BDAY"):
                                temp = data[-1]
                                data[-1] = f"BDAY:{end}\n"
                                data.append(temp)
                                bday_ = True
                        if(pri_mail_ != True):
                            if("EMAIL;HOME" in temoi_end):
                                temp = data[-1]
                                data[-1] = f"EMAIL;CHARSET=UTF-8;type=HOME:{end}\n"
                                data.append(temp)
                                pri_mail_ = True
                        if(pro_mail_ != True):
                            if("EMAIL;WORK" in temoi_end):
                                temp = data[-1]
                                data[-1] = f"EMAIL;CHARSET=UTF-8;type=WORK:{end}\n"
                                data.append(temp)
                                pro_mail_ = True
                        if(pri_phone_ != True):
                            if("TEL;HOME" in temoi_end):
                                temp = data[-1]
                                data[-1] = f"TEL;TYPE=CELL:{end}\n"
                                data.append(temp)
                                pri_phone_ = True
                        if(pro_phone_ != True):
                            if("TEL;WORK" in temoi_end):
                                temp = data[-1]
                                data[-1] = f"TEL;TYPE=WORK:{end}\n"
                                data.append(temp)
                                pro_phone_ = True
                        if(pri_adr_ != True):
                            if("ADR;HOME" in temoi_end):
                                temp = data[-1]
                                data[-1] = f"ADR;CHARSET=UTF-8;TYPE=HOME:{end}\n"
                                data.append(temp)
                                pri_adr_ = True
                        if(pro_adr_ != True):
                            if("ADR;WORK" in temoi_end):
                                print(end)
                                print(temoi_end)
                                temp = data[-1]
                                data[-1] = f"ADR;CHARSET=UTF-8;TYPE=WORK:{end}\n"
                                data.append(temp)
                                pro_adr_ = True

                # on ouvre de nouveau le fichier pour écrire cette fois
                with open(file, 'w', encoding='UTF-8') as file_w:

                    file_w.write("".join(str(item) for item in data))
     