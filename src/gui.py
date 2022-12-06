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
import os
import sys


path = ""
value = []

selected = 0



##--------------------------------------##
#           FENETRE PRINCIPALE           #
##--------------------------------------##

##
# Classe dérivée de Frame permettant de créer la fenêtre principale du programme 
class main_window(tk.Frame):

    path = ""
    frame = None;
    main_label = None
    select = None
    file_label = None
    show_button = None
    edit_button = None
    quit_button = None

    ##
    # initialisation de la classe
    # @param root : la fenêtre dans laquel on créer le tout
    def __init__(self,root):
        super().__init__()

        self.root = root

        root.title("vViewer")
        
        self.create_main()

    ##
    # Fonction créant le contenue de la fenêtre principale
    def create_main(self):

        self.frame = ttk.Frame(self.root,padding=100)
        self.frame.grid()
        self.main_label = ttk.Label(self.frame,padding=10, text="Vueillez choisir un fichier à visualiser :").grid(column=1,row=0)
        self.select = ttk.Button(self.frame, text="Choisir", command=self.selection).grid(column=1,row=1)
        self.file_label = ttk.Label(self.frame,padding=10, text="aucun fichier sélectionné")
        self.file_label.grid(column=1,row=3)
        self.show_button = ttk.Button(self.frame,text="Afficher contenue",padding=10, state=DISABLED ,command=self.show)
        self.show_button.grid(column=0,row=5)
        self.edit_button = ttk.Button(self.frame,text="Modifier contenue",padding=10, state=DISABLED ,command=self.edit)
        self.edit_button.grid(column=2,row=5)
        self.quit_button = ttk.Button(self.frame, text="Quitter",padding=10 ,command=self.root.destroy).grid(column=1,row=10)

    ##
    # Fonction permettant de chercher et sélectionné un fichier ics ou vcf 
    def selection(self)->None:
            
        file = fd.askopenfilename(initialdir="/",title="choisissez un fichier",filetypes=(("iCalendar","*.ics"),("vCard","*.vcf")))
        
        self.file_label.configure(text=f"Fichier : {file}")
        self.path = file
        self.show_button.configure(state=NORMAL)
        self.edit_button.configure(state=NORMAL)

    ##
    # Fonction permettant de modifier le contenue d'un fichier
    def modify(self)->None:
        
        print(self.path)


    ##
    # Créer la fenêtre d'affichage des informations
    def show(self)->None:

        show_root = tk.Tk()
        affiche = show_window(show_root,self.path)

    ##
    # Créer la fenêtre d'édition des informations
    def edit(self)->None:

        edit_root = tk.Tk()
        modify = edit_window(edit_root,self.path)

    """##
    # Fonction permettant de modifier le contenue du fichier donnée
    def edit(self):
        
        edit_window = Toplevel(self.root)
        edit_window.title("Modification du fichier")

        self.content_frame = ttk.Frame(edit_window)
        split = self.file_label.cget("text").split(" : ")

        path = split[1]

        if(path.endswith(".ics")):
            item = ics(path)



            content = item.get_content_ics(path)
            edit_window.geometry("500x300")
            for elements in content:
                summary = elements[0]
                start = elements[1]
                end = elements[2]
                location = elements[3]
                description = elements[4]
            
            summ_lbl = ttk.Label(self.content_frame,padding=10 ,text=f"Evenement : {summary}").grid(sticky=W,columnspan=1,column=0,row=2)
            desc_lbl = ttk.Label(self.content_frame,padding=10, text=f"description : {description}").grid(sticky=W,column=0,row=3)
            locat_lbl = ttk.Label(self.content_frame,padding=10, text=f"lieu : {location}").grid(sticky=W,column=0,row=4)
            start_lbl = ttk.Label(self.content_frame,padding=10, text=f"commence le : {start}").grid(sticky=W,column=0, row=5)
            end_lbl = ttk.Label(self.content_frame,padding=10, text=f"fini le : {end}").grid(sticky=W,column=0,row=6)

            summ_entry = ttk.Entry(self.content_frame).grid(sticky=W,column=1,row=2)
            desc_entry = ttk.Entry(self.content_frame).grid(sticky=W,column=1,row=3)
            locat_entry = ttk.Entry(self.content_frame).grid(sticky=W,column=1,row=4)
            start_entry = ttk.Entry(self.content_frame).grid(sticky=W,column=1,row=5)
            end_entry = ttk.Entry(self.content_frame).grid(sticky=W,column=1,row=6)


            edit_button = ttk.Button(self.content_frame, text="Modifier", padding=10, command=self.modify).grid(columnspan=2,column=0,row=20)
        
        elif(path.endswith(".vcf")):
            edit_window.geometry("650x500")
            item = vcf(path)

            content = item.get_content_vcf(path)
            for elements in content:

                nom = elements[0]
                prenom = elements[1]
                scond = elements[2]
                gender = elements[3]
                nickname = elements[4]
                orga = elements[5]
                title = elements[6]
                birth = elements[7]
                pro_mail = elements[8]
                pri_mail = elements[9]
                pro_phone = elements[10]
                pri_phone = elements[11]
                pro_adr = elements[12]
                pri_adr = elements[13]



            nom_lbl = ttk.Label(self.content_frame,padding=5,text=f"Nom : {nom}").grid(sticky=W,column=0,row=0)
            prenom_lbl = ttk.Label(self.content_frame,padding=5, text=f"Prenom : {prenom}").grid(sticky=W,column=0,row=1)
            second_lbl = ttk.Label(self.content_frame,padding=5, text=f"second prenom : {scond}").grid(sticky=W,column=0,row=2)
            gender_lbl = ttk.Label(self.content_frame,padding=5, text=f"sexe : {gender}").grid(sticky=W,column=0,row=3)
            nick_lbl = ttk.Label(self.content_frame,padding=5, text=f"alias : {nickname}").grid(sticky=W,column=0,row=4)
            org_lbl = ttk.Label(self.content_frame,padding=5, text=f"entreprise : {orga}").grid(sticky=W,column=0,row=5)
            title_lbl = ttk.Label(self.content_frame,padding=5, text=f"emploi : {title}").grid(sticky=W,column=0,row=6)
            bday_lbl = ttk.Label(self.content_frame,padding=5, text=f"date de naissance : {birth}").grid(sticky=W,column=0,row=7)
            email_pro_lbl = ttk.Label(self.content_frame,padding=5, text=f"email pro : {pro_mail}").grid(sticky=W,column=0,row=8)
            email_pri_lbl = ttk.Label(self.content_frame,padding=5, text=f"email pirvée : {pri_mail}").grid(sticky=W,column=0,row=9)
            phone_pro_lbl = ttk.Label(self.content_frame,padding=5, text=f"numéro pro : {pro_phone}").grid(sticky=W,column=0,row=10)
            phone_pri_lbl = ttk.Label(self.content_frame,padding=5, text=f"numéro privée : {pri_phone}").grid(sticky=W,column=0,row=11)
            adr_pro_lbl = ttk.Label(self.content_frame,padding=5, text=f"lieu de travail : {pro_adr}").grid(sticky=W,column=0,row=12)
            adr_pri_lbl = ttk.Label(self.content_frame,padding=5, text=f"lieu de résidence : {pri_adr}").grid(sticky=W,column=0,row=13)

            nom_entry = ttk.Entry(self.content_frame).grid(sticky=W,column=1,row=0)
            prenom_entry = ttk.Entry(self.content_frame).grid(sticky=W,column=1,row=1)
            second_entry = ttk.Entry(self.content_frame).grid(sticky=W,column=1,row=2)
            gender_entry = ttk.Entry(self.content_frame).grid(sticky=W,column=1,row=3)
            nick_entry = ttk.Entry(self.content_frame).grid(sticky=W,column=1,row=4)
            org_entry = ttk.Entry(self.content_frame).grid(sticky=W,column=1,row=5)
            title_entry = ttk.Entry(self.content_frame).grid(sticky=W,column=1,row=6)
            bday_entry = ttk.Entry(self.content_frame).grid(sticky=W,column=1,row=7)
            email_pro_entry = ttk.Entry(self.content_frame).grid(sticky=W,column=1,row=8)
            email_pri_entry = ttk.Entry(self.content_frame).grid(sticky=W,column=1,row=9)
            phone_pro_entry = ttk.Entry(self.content_frame).grid(sticky=W,column=1,row=10)
            phone_pri_entry = ttk.Entry(self.content_frame).grid(sticky=W,column=1,row=11)
            pro_adr_entry = ttk.Entry(self.content_frame).grid(sticky=W,column=1,row=12)
            pri_adr_entry = ttk.Entry(self.content_frame).grid(sticky=W,column=1,row=13)

            edit_button = ttk.Button(self.content_frame, text="Modifier", padding=10, command=self.modify).grid(columnspan=2,column=0,row=20)


        self.content_frame.pack(expand=TRUE)
        quit_edit = ttk.Button(self.content_frame, text="Retour",padding=10, command=edit_window.destroy).grid(columnspan=2,column=1,row=20)
"""
##--------------------------------------##
#           FENETRE AFFICHAGE            #
##--------------------------------------##

class show_window(tk.Frame):

    selected = 0


    def __init__(self,show_win,path) -> None:
        super().__init__()

        self.show_win = show_win
        self.path = path


        self.show_win.title("Informations du fichier")

        self.content_frame = ttk.Frame(self.show_win)
        self.content_frame.grid()
        
        if(self.path.endswith(".ics")):
            
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

            self.see_button = ttk.Button(self.content_frame,padding=10,text="Actualiser", command=self.create_show).grid(columnspan=2,column=0,row=20)
        

        elif(path.endswith(".vcf")):

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

        self.quit_show = ttk.Button(self.content_frame, text="Retour",padding=10, command=self.show_win.destroy).grid(columnspan=2,column=0,row=21)

        self.create_show()
    ##
    # Fonction affichant le contenue du fichier choisi
    def create_show(self)->None:

        if(self.path.endswith(".ics")):
            item = ics(self.path)


            content = item.get_content_ics(self.path)
            size = len(content)

            self.show_win.geometry("500x300")


            summary = content[self.selected][0]
            start = content[self.selected][1]
            end = content[self.selected][2]
            location = content[self.selected][3]
            description = content[self.selected][4]

            
            i:int = 0
            taille = []
            for i in range(size):
                taille.append(str(i))

            selec_combox = ttk.Combobox(self.content_frame, values=taille)
            selec_combox.grid(sticky=W,column=0, row=0,padx=10,pady=10)
            selec_combox['state'] = 'readonly'
            selec_combox.current(0)


            self.summ_lbl.configure(text=f"Evenement : {summary}")
            self.desc_lbl.configure(text=f"description : {description}")
            self.locat_lbl.configure(text=f"lieu : {location}")
            self.start_lbl.configure(text=f"commence le : {start}")
            self.end_lbl.configure(text=f"fini le : {end}")


            selec_combox.bind('<<ComboboxSelected>>', lambda _: self.set_selected(selec_combox))
            
        
        elif(self.path.endswith(".vcf")):

            
            self.show_win.geometry("550x500")
            item = vcf(self.path)

            content = item.get_content_vcf(self.path)
            for elements in content:

                nom = elements[0]
                prenom = elements[1]
                scond = elements[2]
                nickname = elements[3]
                orga = elements[4]
                title = elements[5]
                birth = elements[6]
                pro_mail = elements[7]
                pri_mail = elements[8]
                pro_phone = elements[9]
                pri_phone = elements[10]
                pri_adr = elements[11]
                pro_adr = elements[12]


            self.nom_lbl.configure(text=f"Nom : {nom}")
            self.prenom_lbl.configure(text=f"Prenom : {prenom}")
            self.second_lbl.configure(text=f"second prenom : {scond}")
            self.nick_lbl.configure(text=f"alias : {nickname}")
            self.org_lbl.configure(text=f"entreprise : {orga}")
            self.title_lbl.configure(text=f"emploi : {title}")
            self.bday_lbl.configure(text=f"date de naissance : {birth}")
            self.email_pro_lbl.configure(text=f"email pro : {pro_mail}")
            self.email_pri_lbl.configure(text=f"email pirvée : {pri_mail}")
            self.phone_pro_lbl.configure(text=f"numéro pro : {pro_phone}")
            self.phone_pri_lbl.configure(text=f"numéro privée : {pri_phone}")
            self.adr_pro_lbl.configure(text=f"lieu de travail : {pro_adr}")
            self.adr_pri_lbl.configure(text=f"lieu de résidence : {pri_adr}")

        self.content_frame.update_idletasks()



    ##
    # Change la valeur de selection de la combobox
    def set_selected(self,combox)->None:

        self.selected = int(combox.get())

##--------------------------------------##
#           FENETRE D'EDITION            #
##--------------------------------------##

class edit_window(tk.Frame):

    selected = 0
    initial = []

    def __init__(self,show_win,path) -> None:
        super().__init__()

        self.show_win = show_win
        self.path = path


        self.show_win.title("Modifier le fichier")

        self.content_frame = ttk.Frame(self.show_win)
        self.content_frame.grid()
        
        if(self.path.endswith(".ics")):
            
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

            self.summ_entry = ttk.Entry(self.content_frame)
            self.summ_entry.grid(sticky=W,column=1,row=2)
            self.desc_entry = ttk.Entry(self.content_frame)
            self.desc_entry.grid(sticky=W,column=1,row=3)
            self.locat_entry = ttk.Entry(self.content_frame)
            self.locat_entry.grid(sticky=W,column=1,row=4)
            self.start_entry = ttk.Entry(self.content_frame)
            self.start_entry.grid(sticky=W,column=1,row=5)
            self.end_entry = ttk.Entry(self.content_frame)
            self.end_entry.grid(sticky=W,column=1,row=6)

            self.see_button = ttk.Button(self.content_frame,padding=10,text="Actualiser", command=self.create_edit).grid(columnspan=2,column=0,row=20)
        

        elif(path.endswith(".vcf")):

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

            self.nom_entry = ttk.Entry(self.content_frame)
            self.nom_entry.grid(sticky=W,column=1,row=0)
            self.prenom_entry = ttk.Entry(self.content_frame)
            self.prenom_entry.grid(sticky=W,column=1,row=1)
            self.second_entry = ttk.Entry(self.content_frame)
            self.second_entry.grid(sticky=W,column=1,row=2)
            self.nick_entry = ttk.Entry(self.content_frame)
            self.nick_entry.grid(sticky=W,column=1,row=4)
            self.org_entry = ttk.Entry(self.content_frame)
            self.org_entry.grid(sticky=W,column=1,row=5)
            self.title_entry = ttk.Entry(self.content_frame)
            self.title_entry.grid(sticky=W,column=1,row=6)
            self.bday_entry = ttk.Entry(self.content_frame)
            self.bday_entry.grid(sticky=W,column=1,row=7)
            self.email_pro_entry = ttk.Entry(self.content_frame)
            self.email_pro_entry.grid(sticky=W,column=1,row=8)
            self.email_pri_entry = ttk.Entry(self.content_frame)
            self.email_pri_entry.grid(sticky=W,column=1,row=9)
            self.phone_pro_entry = ttk.Entry(self.content_frame)
            self.phone_pro_entry.grid(sticky=W,column=1,row=10)
            self.phone_pri_entry = ttk.Entry(self.content_frame)
            self.phone_pri_entry.grid(sticky=W,column=1,row=11)
            self.pro_adr_entry = ttk.Entry(self.content_frame)
            self.pro_adr_entry.grid(sticky=W,column=1,row=12)
            self.pri_adr_entry = ttk.Entry(self.content_frame)
            self.pri_adr_entry.grid(sticky=W,column=1,row=13)

        self.edit_button = ttk.Button(self.content_frame, text="Modifier", padding=10, command=self.modify).grid(columnspan=2,column=1,row=19)
        self.quit_show = ttk.Button(self.content_frame, text="Retour",padding=10, command=self.show_win.destroy).grid(columnspan=2,column=1,row=20)

        self.create_edit()
    ##
    # Fonction affichant le contenue du fichier choisi
    def create_edit(self)->None:

        if(self.path.endswith(".ics")):
            item = ics(self.path)


            content = item.get_content_ics(self.path)
            size = len(content)

            self.show_win.geometry("500x350")


            summary = content[self.selected][0]
            start = content[self.selected][1]
            end = content[self.selected][2]
            location = content[self.selected][3]
            description = content[self.selected][4]

            self.initial:list = [f"SUMMARY:{summary}",f"DESCRIPTION:{description}",f"LOCATION:{location}",f"DTSTART:{start}",f"DTEND:{end}"]

            
            i:int = 0
            taille = []
            for i in range(size):
                taille.append(str(i))

            selec_combox = ttk.Combobox(self.content_frame, values=taille)
            selec_combox.grid(sticky=W,column=0, row=0,padx=10,pady=10)
            selec_combox['state'] = 'readonly'
            selec_combox.current(0)


            self.summ_lbl.configure(text=f"Evenement : {summary}")
            self.desc_lbl.configure(text=f"description : {description}")
            self.locat_lbl.configure(text=f"lieu : {location}")
            self.start_lbl.configure(text=f"commence le : {start}")
            self.end_lbl.configure(text=f"fini le : {end}")

            self.summ_entry.delete(-1, 'end')
            self.desc_entry.delete(-1, 'end')
            self.locat_entry.delete(-1, 'end')
            self.start_entry.delete(-1, 'end')
            self.end_entry.delete(-1, 'end')
            self.summ_entry.insert(-1,summary)
            self.desc_entry.insert(-1,description)
            self.locat_entry.insert(-1,location)
            self.start_entry.insert(-1,start)
            self.end_entry.insert(-1,end)


            selec_combox.bind('<<ComboboxSelected>>', lambda _: self.set_selected(selec_combox))
            
        
        elif(self.path.endswith(".vcf")):

            
            self.show_win.geometry("725x575")
            item = vcf(self.path)

            content = item.get_content_vcf(self.path)
            for elements in content:

                nom = elements[0]
                prenom = elements[1]
                scond = elements[2]
                nickname = elements[3]
                orga = elements[4]
                title = elements[5]
                birth = elements[6]
                pro_mail = elements[7]
                pri_mail = elements[8]
                pro_phone = elements[9]
                pri_phone = elements[10]
                pri_adr = elements[11]
                pro_adr = elements[12]

                self.initial:list = [f"FN:{nom}",f"FN:{prenom}",f"FN:{scond}",f"NICKNAME:{nickname}",f"ORG:{orga}",f"TITLE:{title}",f"BDAY:{birth}",f"EMAIL:{pro_mail}",f"EMAIL:{pri_mail}",f"TEL:{pro_phone}",f"TEL:{pri_phone}",f"ADR:{pro_adr}",f"ADR:{pri_adr}"]

            self.nom_lbl.configure(text=f"Nom : {nom}")
            self.prenom_lbl.configure(text=f"Prenom : {prenom}")
            self.second_lbl.configure(text=f"second prenom : {scond}")
            self.nick_lbl.configure(text=f"alias : {nickname}")
            self.org_lbl.configure(text=f"entreprise : {orga}")
            self.title_lbl.configure(text=f"emploi : {title}")
            self.bday_lbl.configure(text=f"date de naissance : {birth}")
            self.email_pro_lbl.configure(text=f"email pro : {pro_mail}")
            self.email_pri_lbl.configure(text=f"email pirvée : {pri_mail}")
            self.phone_pro_lbl.configure(text=f"numéro pro : {pro_phone}")
            self.phone_pri_lbl.configure(text=f"numéro privée : {pri_phone}")
            self.adr_pro_lbl.configure(text=f"lieu de travail : {pro_adr}")
            self.adr_pri_lbl.configure(text=f"lieu de résidence : {pri_adr}")

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

        self.content_frame.update_idletasks()


    ##
    # Fonction permettant de modifié un fichier donné
    def modify(self):
        
        if(self.path.endswith(".ics")):
            replace:list = self.get_ics_entry()

            item = ics(self.path)
            item.modify_ics(self.initial,replace,self.path,self.selected+1)
        else:
            replace:list = self.get_vcf_entry()

            item = vcf(self.path)
            item.modify_vcf(self.initial,replace,self.path)

    ##
    # fonction qui récupère le contenue des entrée pour les fichiers vcf
    # @return la liste des entrées.
    def get_vcf_entry(self)->list:

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

    def get_ics_entry(self)->list:

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

        self.selected = int(combox.get())



def main()->None:

    root = tk.Tk()
    main = main_window(root)
    root.mainloop()

if __name__ == '__main__':
    main()
