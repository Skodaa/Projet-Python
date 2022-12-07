"""!
    Programme permettant de créer le la version graphique du logiciel de gestion de fichiers vcf et ics

    @author VOLQUARDSEN Alex
    @since 25/11/2022
    @verison 1.0.0
"""

import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog as fd
from classes import *


##--------------------------------------##
#           FENETRE PRINCIPALE           #
##--------------------------------------##

##
# Classe dérivée de Frame permettant de créer la fenêtre principale du programme 
#
# @version 1.2.0
# @since 20/11/2022
class main_window(tk.Frame):

    # Attribut de la classe initialiser à vide
    path = "" # le chemin du fichier
    frame = None; # la fenêtre principale
    main_label = None # le label principale
    select = None # le boutons selection
    file_label = None # le label contenant le nom du fichier
    show_button = None # le boutton d'affichage
    edit_button = None # le bouton d'edition
    quit_button = None # le bouton de fermeture

    ##
    # initialisation de la classe
    # @param root : la fenêtre dans laquel on créer le tout
    def __init__(self,root):
        super().__init__()

        self.root = root # La fenêtre de la classe devient par défaut c'elle donner à l'initialisation

        root.title("Vviewer") # nom de la fenêtre principale
        
        self.create_main() # appel de la méthode de création de la fenêtre principale

    ##
    # Fonction créant le contenue de la fenêtre principale
    def create_main(self):
        # Création de la fenêtre
        self.frame = ttk.Frame(self.root,padding=100)
        # on disposeras les éléments sous forme de grille
        self.frame.grid()
        # création du label principal
        self.main_label = ttk.Label(self.frame,padding=10, text="Vueillez choisir un fichier à visualiser :").grid(column=1,row=0)
        # création du boutton de sélection de fichier appelant la méthode selection au clic
        self.select = ttk.Button(self.frame, text="Choisir", command=self.selection).grid(column=1,row=1)
        # création du label contenant le nom du fichier (initialisé de sorte à afficher un message au lancement)
        self.file_label = ttk.Label(self.frame,padding=10, text="aucun fichier sélectionné")
        # on met ici la disposition après car si on le mettait comme au dessus, l'objet ne serais pas créer correctement et non modifiable
        self.file_label.grid(column=1,row=3)
        # création du boutton pour afficher le contenue ( de base non clicable) appelant la méthode show au clic
        self.show_button = ttk.Button(self.frame,text="Afficher contenue",padding=10, state=DISABLED ,command=self.show)
        self.show_button.grid(column=0,row=5)
        # création du boutton pour editer le contenue ( de base non clicable) appelant la méthode edit au clic
        self.edit_button = ttk.Button(self.frame,text="Modifier contenue",padding=10, state=DISABLED ,command=self.edit)
        self.edit_button.grid(column=2,row=5)
        # création du boutton pour quitter la fenêtre
        self.quit_button = ttk.Button(self.frame, text="Quitter",padding=10 ,command=self.root.destroy).grid(column=1,row=10)

    ##
    # Fonction permettant de chercher et sélectionné un fichier ics ou vcf 
    def selection(self)->None:
        
        # on utilise un élément de la bibliothèque pour ouvrir un explorateur de fichier n'affichant que les répertoires et les fichiers .ics et .vcf
        file = fd.askopenfilename(initialdir="/",title="choisissez un fichier",filetypes=(("iCalendar","*.ics"),("vCard","*.vcf")))
        
        # on modifie le label pour afficher le nom du dossier 
        self.file_label.configure(text=f"Fichier : {file}")
        # on passe comme valeur le fichier a l'attribut path de la classe
        self.path = file
        # on rend clicable les bouton d'affichage et d'édition
        if(".vcf" in file or ".ics" in file):
            self.show_button.configure(state=NORMAL)
            self.edit_button.configure(state=NORMAL)

    ##
    # Créer la fenêtre d'affichage des informations
    def show(self)->None:
        # on créer une nouvelle fenêtre
        show_root = tk.Tk()
        # on appel la fonction pour afficher la fenêtre d'affichage
        affiche = show_window(show_root,self.path)

    ##
    # Créer la fenêtre d'édition des informations
    def edit(self)->None:
        # on créer une nouvelle fenêtre
        edit_root = tk.Tk()
        # on appel la fonction pour afficher la fenêtre d'édition
        modify = edit_window(edit_root,self.path)


##--------------------------------------##
#           FENETRE AFFICHAGE            #
##--------------------------------------##

##
# Classe dérivé de Frame permettant d'afficher le contenue d'un fichier donné
#
# @version 1.2.0
# @since 20/11/2022
class show_window(tk.Frame):

    # compteur utiliser pour savoir quel évènement on regarde dans un fichier ics
    selected = 0

    ##
    # Initialisation de la classe
    # @param show_win : la fenêtre dans laquel on afficheras les élements
    # @param path : le chemin du fichier à afficher
    def __init__(self,show_win,path) -> None:
        super().__init__()

        # On initialise le path et la fenêtre de la classe avec les arguments donnés
        self.show_win = show_win
        self.path = path

        # Titre de la fenêtre d'affichage
        self.show_win.title("Informations du fichier")

        # on créer une frame on l'on placeras nos éléments en grille
        self.content_frame = ttk.Frame(self.show_win)
        self.content_frame.grid()
        
        # si le fichier est un ics on vient créer la fenêtre en conséquence
        if(self.path.endswith(".ics")):
            
            #création des différents label qui contiendrons les informations du fichier
            self.summ_lbl = ttk.Label(self.content_frame,padding=10)
            self.summ_lbl.grid(sticky=W,column=0,row=2)
            self.desc_lbl = ttk.Label(self.content_frame,padding=10)
            self.desc_lbl.grid(sticky=W,column=0,row=3)
            self.locat_lbl = ttk.Label(self.content_frame,padding=10)
            self.locat_lbl.grid(sticky=W,column=0,row=4)
            self.start_lbl = ttk.Label(self.content_frame,padding=10)
            self.start_lbl.grid(sticky=W,column=0, row=5)
            self.end_lbl = ttk.Label(self.content_frame,padding=10)
            self.end_lbl.grid(sticky=W,column=1,row=5)

            # création du bouton pour actualisé les inforation de la fenêtre
            self.see_button = ttk.Button(self.content_frame,padding=10,text="Actualiser", command=self.create_show).grid(columnspan=2,column=0,row=20)
        
        # si le fichier est un vcf on créer la fenêtre en conséquence 
        elif(path.endswith(".vcf")):

            # Création des différents label qui contiendrons les informations
            self.nom_lbl = ttk.Label(self.content_frame,padding=5)
            self.nom_lbl.grid(sticky=W,column=0,row=0,padx=10,pady=10)
            self.prenom_lbl = ttk.Label(self.content_frame,padding=5)
            self.prenom_lbl.grid(sticky=W,column=0,row=1,padx=10)
            self.second_lbl = ttk.Label(self.content_frame,padding=5)
            self.second_lbl.grid(sticky=W,column=0,row=2,padx=10)
            self.nick_lbl = ttk.Label(self.content_frame,padding=5)
            self.nick_lbl.grid(sticky=W,column=0,row=3,padx=10)
            self.org_lbl = ttk.Label(self.content_frame,padding=5)
            self.org_lbl.grid(sticky=W,column=0,row=4,padx=10)
            self.title_lbl = ttk.Label(self.content_frame,padding=5)
            self.title_lbl.grid(sticky=W,column=0,row=5,padx=10)
            self.bday_lbl = ttk.Label(self.content_frame,padding=5)
            self.bday_lbl.grid(sticky=W,column=0,row=6,padx=10)
            self.email_pro_lbl = ttk.Label(self.content_frame,padding=5)
            self.email_pro_lbl.grid(sticky=W,column=0,row=7,padx=10)
            self.email_pri_lbl = ttk.Label(self.content_frame,padding=5)
            self.email_pri_lbl.grid(sticky=W,column=0,row=8,padx=10)
            self.phone_pro_lbl = ttk.Label(self.content_frame,padding=5)
            self.phone_pro_lbl.grid(sticky=W,column=0,row=9,padx=10)
            self.phone_pri_lbl = ttk.Label(self.content_frame,padding=5)
            self.phone_pri_lbl.grid(sticky=W,column=0,row=10,padx=10)
            self.adr_pro_lbl = ttk.Label(self.content_frame,padding=5)
            self.adr_pro_lbl.grid(sticky=W,column=0,row=11,padx=10)
            self.adr_pri_lbl = ttk.Label(self.content_frame,padding=5)
            self.adr_pri_lbl.grid(sticky=W,column=0,row=12,padx=10)

        # création du bouton pour quitter la fenêtre ( présent quelque soit le type du fichier)
        self.quit_show = ttk.Button(self.content_frame, text="Retour",padding=10, command=self.show_win.destroy).grid(columnspan=2,column=0,row=21)

        # appel de la fonction de création de la fenêtre d'affichage
        self.create_show()
    ##
    # Fonction affichant le contenue du fichier choisi
    def create_show(self)->None:

        # on vérifie si le fichier est un ics (icalendar)
        if(self.path.endswith(".ics")):
            # si c'est le cas on créer un objet ics
            item = ics(self.path)

            # on récupère le contenue du fichier à l'aide d'une fonction de la classe ics
            content = item.get_content_ics(self.path)
            # on récupère la taille de ce contenue
            size = len(content)

            # on attribue aux éléments les informations de l'évenement sélectionné
            summary = content[self.selected][0]
            start = content[self.selected][1]
            end = content[self.selected][2]
            location = content[self.selected][3]
            description = content[self.selected][4]

            
            i:int = 0
            # on créer une liste contenant un indice numérique des évènements du fichier
            taille = []
            for i in range(size):
                taille.append(str(i))

            # nous créons une combobox contenant le tableaux précedement créer
            selec_combox = ttk.Combobox(self.content_frame, values=taille)
            selec_combox.grid(sticky=W,column=0, row=0,padx=10,pady=10)
            # la combobox ne peut pas être modifié par l'utilisateur
            selec_combox['state'] = 'readonly'
            # on initialise la combobox sur l'élement actuellement affiché
            selec_combox.current(self.selected)

            # on configure les label pour afficher le contenue de l'évenement sélectionner
            self.summ_lbl.configure(text=f"Evenement : {summary}")
            self.desc_lbl.configure(text=f"description : {description}")
            self.locat_lbl.configure(text=f"lieu : {location}")
            self.start_lbl.configure(text=f"commence le : {start}")
            self.end_lbl.configure(text=f"fini le : {end}")

            # lorsque l'utilisateur sélectionne un élément de la combobox, l'attribut selected est modifié
            selec_combox.bind('<<ComboboxSelected>>', lambda _: self.set_selected(selec_combox))
            
        # on vérifie si le fichier est un vcf
        elif(self.path.endswith(".vcf")):

            # on créer l'objet vcf
            item = vcf(self.path)

            # on récupère le contenue du fichier
            content = item.get_content_vcf(self.path)
            
            # on attribue les éléments du fichier a des variables
            for elements in content:

                nom = elements[0]
                prenom = elements[1]
                scond = elements[2]
                nickname = elements[3]
                orga = elements[4]
                title = elements[5]
                birth = elements[6]
                pro_mail = elements[8]
                pri_mail = elements[7]
                pro_phone = elements[9]
                pri_phone = elements[10]
                pri_adr = elements[11]
                pro_adr = elements[12]

            # on modifie le contenue des label pour afficher le contenue du fichier
            self.nom_lbl.configure(text=f"Nom : {nom}")
            self.prenom_lbl.configure(text=f"Prenom : {prenom}")
            self.second_lbl.configure(text=f"second prenom : {scond}")
            self.nick_lbl.configure(text=f"alias : {nickname}")
            self.org_lbl.configure(text=f"entreprise : {orga}")
            self.title_lbl.configure(text=f"emploi : {title}")
            self.bday_lbl.configure(text=f"date de naissance : {birth}")
            self.email_pro_lbl.configure(text=f"email pro : {pro_mail}")
            self.email_pri_lbl.configure(text=f"email privée : {pri_mail}")
            self.phone_pro_lbl.configure(text=f"numéro pro : {pro_phone}")
            self.phone_pri_lbl.configure(text=f"numéro privée : {pri_phone}")
            self.adr_pro_lbl.configure(text=f"lieu de travail : {pro_adr}")
            self.adr_pri_lbl.configure(text=f"lieu de résidence : {pri_adr}")

        # on actualise la fenêtre pour prendre en compte les modifications effectuer
        self.content_frame.update_idletasks()



    ##
    # Change la valeur de selection de la combobox
    def set_selected(self,combox)->None:

        # on modifie la valeur de l'attribut selected de la classe
        self.selected = int(combox.get())


##--------------------------------------##
#           FENETRE D'EDITION            #
##--------------------------------------##

##
# Création de la classe de fenêtre d'édition dérivé de Frame
#
# @version 1.2.0
# @since 20/11/2022
class edit_window(tk.Frame):

    # compteur pour savoir quel évènement afficher
    selected = 0
    # initialisation de la liste des données initiale à vide
    initial = []

    ##
    # Fonction d'initialisation de la fenêtre d'édition
    # @param show_win : la fenêtre utilisé pour l'édition
    # @param path : le chemin du fichier à modifier
    def __init__(self,show_win,path) -> None:
        super().__init__()

        # on initialise la fenêtre et le chemin de la calsse avec les paramètres donnés
        self.show_win = show_win
        self.path = path

        # nom de la fenêtre
        self.show_win.title("Modifier le fichier")

        # on créer un contenant sous forme de grille
        self.content_frame = ttk.Frame(self.show_win)
        self.content_frame.grid()
        
        # on vérifie si le fichier est un ics
        if(self.path.endswith(".ics")):
            
            # création des label permettant d'afficher les informations du fichier
            self.summ_lbl = ttk.Label(self.content_frame,padding=10)
            self.summ_lbl.grid(sticky=W,column=0,row=2)
            self.desc_lbl = ttk.Label(self.content_frame,padding=10)
            self.desc_lbl.grid(sticky=W,column=0,row=3)
            self.locat_lbl = ttk.Label(self.content_frame,padding=10)
            self.locat_lbl.grid(sticky=W,column=0,row=4)
            self.start_lbl = ttk.Label(self.content_frame,padding=10)
            self.start_lbl.grid(sticky=W,column=0, row=5)
            self.end_lbl = ttk.Label(self.content_frame,padding=10)
            self.end_lbl.grid(sticky=W,column=0,row=6)

            # création des entry permettant de rentrer les modifications à effectuer
            self.summ_entry = ttk.Entry(self.content_frame)
            self.summ_entry.grid(sticky=W,column=1,row=2,padx=10)
            self.desc_entry = ttk.Entry(self.content_frame)
            self.desc_entry.grid(sticky=W,column=1,row=3,padx=10)
            self.locat_entry = ttk.Entry(self.content_frame)
            self.locat_entry.grid(sticky=W,column=1,row=4,padx=10)
            self.start_entry = ttk.Entry(self.content_frame)
            self.start_entry.grid(sticky=W,column=1,row=5,padx=10)
            self.end_entry = ttk.Entry(self.content_frame)
            self.end_entry.grid(sticky=W,column=1,row=6,padx=10)

            # création du bouton d'actualisé la fenêtre pour afficher les autres évenements
            self.see_button = ttk.Button(self.content_frame,padding=10,text="Actualiser", command=self.create_edit).grid(columnspan=2,column=0,row=20)
        
        # on vérifie si le fichier est un vcf
        elif(path.endswith(".vcf")):

            # création des label contenant les informations du fichier
            self.nom_lbl = ttk.Label(self.content_frame,padding=5)
            self.nom_lbl.grid(sticky=W,column=0,row=0,padx=10,pady=10)
            self.prenom_lbl = ttk.Label(self.content_frame,padding=5)
            self.prenom_lbl.grid(sticky=W,column=0,row=1,padx=10)
            self.second_lbl = ttk.Label(self.content_frame,padding=5)
            self.second_lbl.grid(sticky=W,column=0,row=2,padx=10)
            self.nick_lbl = ttk.Label(self.content_frame,padding=5)
            self.nick_lbl.grid(sticky=W,column=0,row=4,padx=10)
            self.org_lbl = ttk.Label(self.content_frame,padding=5)
            self.org_lbl.grid(sticky=W,column=0,row=5,padx=10)
            self.title_lbl = ttk.Label(self.content_frame,padding=5)
            self.title_lbl.grid(sticky=W,column=0,row=6,padx=10)
            self.bday_lbl = ttk.Label(self.content_frame,padding=5)
            self.bday_lbl.grid(sticky=W,column=0,row=7,padx=10)
            self.email_pro_lbl = ttk.Label(self.content_frame,padding=5)
            self.email_pro_lbl.grid(sticky=W,column=0,row=8,padx=10)
            self.email_pri_lbl = ttk.Label(self.content_frame,padding=5)
            self.email_pri_lbl.grid(sticky=W,column=0,row=9,padx=10)
            self.phone_pro_lbl = ttk.Label(self.content_frame,padding=5)
            self.phone_pro_lbl.grid(sticky=W,column=0,row=10,padx=10)
            self.phone_pri_lbl = ttk.Label(self.content_frame,padding=5)
            self.phone_pri_lbl.grid(sticky=W,column=0,row=11,padx=10)
            self.adr_pro_lbl = ttk.Label(self.content_frame,padding=5)
            self.adr_pro_lbl.grid(sticky=W,column=0,row=12,padx=10)
            self.adr_pri_lbl = ttk.Label(self.content_frame,padding=5)
            self.adr_pri_lbl.grid(sticky=W,column=0,row=13,padx=10)

            # création des entry qui permettrons de rentrer les modifications à effectuer
            self.nom_entry = ttk.Entry(self.content_frame)
            self.nom_entry.grid(sticky=W,column=1,row=0,padx=10)
            self.prenom_entry = ttk.Entry(self.content_frame)
            self.prenom_entry.grid(sticky=W,column=1,row=1,padx=10)
            self.second_entry = ttk.Entry(self.content_frame)
            self.second_entry.grid(sticky=W,column=1,row=2,padx=10)
            self.nick_entry = ttk.Entry(self.content_frame)
            self.nick_entry.grid(sticky=W,column=1,row=4,padx=10)
            self.org_entry = ttk.Entry(self.content_frame)
            self.org_entry.grid(sticky=W,column=1,row=5,padx=10)
            self.title_entry = ttk.Entry(self.content_frame)
            self.title_entry.grid(sticky=W,column=1,row=6,padx=10)
            self.bday_entry = ttk.Entry(self.content_frame)
            self.bday_entry.grid(sticky=W,column=1,row=7,padx=10)
            self.email_pro_entry = ttk.Entry(self.content_frame)
            self.email_pro_entry.grid(sticky=W,column=1,row=8,padx=10)
            self.email_pri_entry = ttk.Entry(self.content_frame)
            self.email_pri_entry.grid(sticky=W,column=1,row=9,padx=10)
            self.phone_pro_entry = ttk.Entry(self.content_frame)
            self.phone_pro_entry.grid(sticky=W,column=1,row=10,padx=10)
            self.phone_pri_entry = ttk.Entry(self.content_frame)
            self.phone_pri_entry.grid(sticky=W,column=1,row=11,padx=10)
            self.pro_adr_entry = ttk.Entry(self.content_frame)
            self.pro_adr_entry.grid(sticky=W,column=1,row=12,padx=10)
            self.pri_adr_entry = ttk.Entry(self.content_frame)
            self.pri_adr_entry.grid(sticky=W,column=1,row=13,padx=10)

        # création des boutons permettant de modifié le contenue et de quitter la fenêtre
        # le bouton modification appel la méthode modify de classe
        self.edit_button = ttk.Button(self.content_frame, text="Modifier", padding=10, command=self.modify).grid(columnspan=2,column=1,row=19)
        self.quit_show = ttk.Button(self.content_frame, text="Retour",padding=10, command=self.show_win.destroy).grid(columnspan=2,column=1,row=20)

        # appel de la méthode créant le contenue de la fenêtre
        self.create_edit()
    ##
    # Fonction affichant le contenue du fichier choisi
    def create_edit(self)->None:

        # on vérifie si le fichier est un ics
        if(self.path.endswith(".ics")):
            # on créer l'objet ics
            item = ics(self.path)

            # on récupere le contenue du fichier donné et sa taille
            content = item.get_content_ics(self.path)
            size = len(content)

            # on attribue sont contenue en fonction de l'évenement sélectionné
            summary = content[self.selected][0]
            start = content[self.selected][1]
            end = content[self.selected][2]
            location = content[self.selected][3]
            description = content[self.selected][4]

            # on ajoute dans une liste le contenue initial ainsi que des repères pour mieux s'y retrouver
            self.initial:list = [f"SUMMARY:{summary}",f"DESCRIPTION:{description}",f"LOCATION:{location}",f"DTSTART:{start}",f"DTEND:{end}"]

            # on créer la combobox permettant de choisir l'évenement que l'on souhaite
            i:int = 0
            taille = []
            for i in range(size):
                taille.append(str(i))

            selec_combox = ttk.Combobox(self.content_frame, values=taille)
            selec_combox.grid(sticky=W,column=0, row=0,padx=10,pady=10)
            # la combobox n'est pas modifiable par l'utilisateur
            selec_combox['state'] = 'readonly'
            selec_combox.current(self.selected)

            # on configure les label pour afficher le contenue de base du fichier
            self.summ_lbl.configure(text=f"Evenement : {summary}")
            self.desc_lbl.configure(text=f"description : {description}")
            self.locat_lbl.configure(text=f"lieu : {location}")
            self.start_lbl.configure(text=f"commence le : {start}")
            self.end_lbl.configure(text=f"fini le : {end}")

            # on vide initialement les entry pour s'assurer que plus rien ne s'y trouve 
            self.summ_entry.delete(-1, 'end')
            self.desc_entry.delete(-1, 'end')
            self.locat_entry.delete(-1, 'end')
            self.start_entry.delete(-1, 'end')
            self.end_entry.delete(-1, 'end')
            # puis on y rajoute les informations initiale du fichier qui peuvent être modifié
            self.summ_entry.insert(-1,summary)
            self.desc_entry.insert(-1,description)
            self.locat_entry.insert(-1,location)
            self.start_entry.insert(-1,start)
            self.end_entry.insert(-1,end)

            # lorsque l'utilisateur sélectionne un élément de la combobox, la valeur de selected est modifié
            selec_combox.bind('<<ComboboxSelected>>', lambda _: self.set_selected(selec_combox))
            
        # on vérifie si le fichier est un vcf
        elif(self.path.endswith(".vcf")):

            # on créer l'objet vcf
            item = vcf(self.path)

            # on en récupère le contenue et on l'attribut à des variables
            content = item.get_content_vcf(self.path)
            for elements in content:

                nom = elements[0]
                prenom = elements[1]
                scond = elements[2]
                nickname = elements[3]
                orga = elements[4]
                title = elements[5]
                birth = elements[6]
                pro_mail = elements[8]
                pri_mail = elements[7]
                pro_phone = elements[9]
                pri_phone = elements[10]
                pri_adr = elements[11]
                pro_adr = elements[12]

                # on créer une liste des éléments initiales du fichier
                self.initial:list = [f"FN:{nom}",f"FN:{prenom}",f"FN:{scond}",f"NICKNAME:{nickname}",f"ORG:{orga}",f"TITLE:{title}",f"BDAY:{birth}",f"EMAIL:{pro_mail}",f"EMAIL:{pri_mail}",f"TEL:{pro_phone}",f"TEL:{pri_phone}",f"ADR:{pro_adr}",f"ADR:{pri_adr}"]

            # on modifie les label pour afficher le contenue du fichier
            self.nom_lbl.configure(text=f"Nom : {nom}")
            self.prenom_lbl.configure(text=f"Prenom : {prenom}")
            self.second_lbl.configure(text=f"second prenom : {scond}")
            self.nick_lbl.configure(text=f"alias : {nickname}")
            self.org_lbl.configure(text=f"entreprise : {orga}")
            self.title_lbl.configure(text=f"emploi : {title}")
            self.bday_lbl.configure(text=f"date de naissance : {birth}")
            self.email_pro_lbl.configure(text=f"email pro : {pro_mail}")
            self.email_pri_lbl.configure(text=f"email privée : {pri_mail}")
            self.phone_pro_lbl.configure(text=f"numéro pro : {pro_phone}")
            self.phone_pri_lbl.configure(text=f"numéro privée : {pri_phone}")
            self.adr_pro_lbl.configure(text=f"lieu de travail : {pro_adr}")
            self.adr_pri_lbl.configure(text=f"lieu de résidence : {pri_adr}")

            # on affiche les valeurs initiales dans les entry pour permettre à l'utilisateur de les modifier
            self.nom_entry.insert(-1,nom)
            self.prenom_entry.insert(-1,prenom)
            self.second_entry.insert(-1,scond)
            self.nick_entry.insert(-1,nickname)
            self.org_entry.insert(-1,orga)
            self.title_entry.insert(-1,title)
            self.bday_entry.insert(-1,birth)
            self.email_pro_entry.insert(-1,pro_mail)
            self.email_pri_entry.insert(-1,pri_mail)
            self.phone_pro_entry.insert(-1,pro_phone)
            self.phone_pri_entry.insert(-1,pri_phone)
            self.pro_adr_entry.insert(-1,pro_adr)
            self.pri_adr_entry.insert(-1,pri_adr)

        # mise a jour de la fenêtre pour afficher le contenue du fichier
        self.content_frame.update_idletasks()


    ##
    # Fonction permettant de modifié un fichier donné
    def modify(self):
        
        # on vérifie d'abord le type du fichier
        if(self.path.endswith(".ics")):
            # on récupere à l'aide de la fonction de classe les informations rentré par l'utilisateur
            replace:list = self.get_ics_entry()
            # on créer l'objet ics
            item = ics(self.path)
            # on appel la méthode de modification de la classe ics
            item.modify_ics(self.initial,replace,self.path,self.selected+1)
        else:
            # on récupere les informations rentrés par l'utilisateur à l'aide de la méthode de la classe
            replace:list = self.get_vcf_entry()

            # on créer l'objet vcf
            item = vcf(self.path)
            # on appel la méthode de modification de vcf
            item.modify_vcf(self.initial,replace,self.path)

    ##
    # fonction qui récupère le contenue des entrée pour les fichiers vcf
    # @return la liste des entrées.
    def get_vcf_entry(self)->list:

        # on ajoute dans une liste la valeur de chaque entrée de l'utilisateur
        res:list = []
        res.append(f"FN:{self.nom_entry.get()}")
        res.append(f"FN:{self.prenom_entry.get()}")
        res.append(f"FN:{self.second_entry.get()}")
        res.append(f"NICKNAME:{self.nick_entry.get()}")
        res.append(f"ORG:{self.org_entry.get()}")
        res.append(f"TITLE:{self.title_entry.get()}")
        res.append(f"BDAY:{self.bday_entry.get()}")
        res.append(f"EMAIL;WORK:{self.email_pro_entry.get()}")
        res.append(f"EMAIL;HOME:{self.email_pri_entry.get()}")
        res.append(f"TEL;WORK:{self.phone_pro_entry.get()}")
        res.append(f"TEL;HOME:{self.phone_pri_entry.get()}")
        res.append(f"ADR;WORK:{self.pro_adr_entry.get()}")
        res.append(f"ADR;HOME:{self.pri_adr_entry.get()}")

        return res

    ##
    # fonction qui récupère les entrées de l'utilisateur 
    # @return la liste contenant ses entrées
    def get_ics_entry(self)->list:

        # on ajoute le contenue des entrée dans une liste
        res:list=[]
        res.append(f"SUMMARY:{self.summ_entry.get()}")
        res.append(f"DESCRIPTION:{self.desc_entry.get()}")
        res.append(f"LOCATION:{self.locat_entry.get()}")
        res.append(f"DTSTART:{self.start_entry.get()}")
        res.append(f"DTEND:{self.end_entry.get()}")

        return res
    ##
    # Change la valeur de selection de la combobox
    def set_selected(self,combox)->None:
        # modifie la valeur de selected 
        self.selected = int(combox.get())


##
# fonction principale du programme
def main()->None:

    # création de la fenêtre principale
    root = tk.Tk()
    # création de l'objet main_window
    main = main_window(root)
    root.mainloop()

# appel de la fonction principal
if __name__ == '__main__':
    main()
