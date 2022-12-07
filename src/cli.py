"""!
    Programme permettant d'éxectuer toutes les actions propre au CLI à savoir, 
    - afficher l'aide pour donner à l'utilisateur la marche à suivre,
    - permettre à l'utilisateur de chercher récursivement dans des répertoire pour trouver des fichiers ics et vcf
    - afficher le contenu d'un fichier ics ou vcf donné,
    - créer un fragment de code html et un squelette de page html contenant les informations
    - ajouter dans un fichier csv les information d'un ics ou d'un vcf

    @author VOLQUARDSEN Alex
    @since 13/11/2022
    @version 1.0.3
"""

## IMPORTATION ##
from classes import * # Importe les classes pour traiter les ics et les vcf
import sys
import os


##
# Fonction ayant effet de main
def main()->None:

    try:
        # Si l'argument '1' n'existe pas retourne une erreur car c'est interdit !
        arg1:str = str(sys.argv[1]) 

        # Si l'argument '1' est '-h' alors on appel la fonction d'aide
        if((arg1 == "-h") or (arg1 == "-help")):
            
            # création d'un items pour pouvoir utiliser ses fonction de base
            item = items("") 
            item.help() # fonction d'affichage de l'aide

        # Si l'argument 1 est "-d" on va parcourir le répertoire donné
        elif(arg1 == "-d"):
            
            # on essaye de parcourir le répertoire 
            try:
                # on créer l'objet items
                item = items("")
                path = sys.argv[2] # on récupère le deuxième argument qui devrait être un répertoire
                item.path = os.path.abspath(path) # on attribue le chemin absolue à l'objet
                item.list_files(path,0) # on appel la fonction qui permet la recherche
            
            except:
                # Si jamais l'argument '2' à savoir le répertoire dans lequel on veut lancer la recherche on affiche une erreur
                print("\u001b[31m Votre second argument n'est pas bon...(répertoire incorrect) essayer de taper \"python3 cli.py -h\" pour savoir quoi faire \u001b[37m")

        # si l'argument 1 est -i on va essayer d'effectuer les affichages et créations de fragment de fichier
        elif(arg1 == "-i"):

            try:
                # on récupere l'argument censé être le chemin du fichier
                path = sys.argv[2]
                # si c'est un fichier .ics on agis en conséquence
                if(".ics" in path):

                    # on créer l'objet ics
                    item = ics("")
                    # on lui attribue en chemin par défaut le chemin donné
                    item.path = os.path.abspath(path)

                    # Si on as exactement 5 arguments, on sait qu'on va créer des fichier
                    if(len(sys.argv)==5):
                        # on récupère la commande que l'utilisateur veut effectuer
                        commande:str = sys.argv[3]
                        # on récupère les informations du fichier à l'aide d'une fonction de l'objet ics
                        calendar:list = item.get_content_ics(path)
                        # on récupère le chemin et nom du fichier à créer ( si seul le nom est donné, le fichier est créer dans le répertoire courant)
                        filename:str = sys.argv[4]
            
                        # si la commande est -h, on va créer le fragment html
                        if(commande =="-h"):

                            # on vérifie que lle fichier dans lequel on veut créer le fragment à la bonne extension
                            if(".html" in filename):
                                # on appele la méthode de création du fragment
                                item.fragment_ics(calendar,filename)
                        # si la commande est -c, on va créer le fichier csv
                        elif(commande == "-c"):
                            # on vérifie encore une fois l'extension du fichier de sortie
                            if(".csv" in filename):
                                # Si c'est bon on appel la méthode de création du csv
                                item.csv_ics(calendar,filename)
                        # si la commande est -p, on créer un squelette de fichier html
                        elif(commande == "-p"):
                            #on vérifier que l'on créer bien un fichier html
                            if(".html" in filename):
                                # si c'est bon on appel la méthode de création de l'objet ics
                                item.page_ics(calendar,filename)
                    # si le nombre d'argument n'est pas 5, on afficher juste le contenue du fichier       
                    else:
                        # on récupere les informations du fichier
                        calendar:list = item.get_content_ics(path)
                        # on appel la méthode d'affichage
                        item.afficher(calendar)
                # si jamais le fichier est un vcf on effectuer les actions en conséquence
                elif(".vcf" in path):

                    # on créer l'objet vcf 
                    item = vcf("")
                    # on lui donne comme chemin de base le chemin en argument
                    item.path = os.path.abspath(path)
                    # comme pour les ics on vérifie le nombre d'argument
                    if(len(sys.argv) == 5):
                        commande:str = sys.argv[3]
                        vcard:list = item.get_content_vcf(path)
                        filename:str = sys.argv[4]
                        # on vérifie la commande rentrée et on agis en conséquence
                        if(commande == "-h"):
                            if(".html" in filename):
                                item.fragment_vcf(vcard,filename)
                        elif(commande == "-c"):
                            if(".csv" in filename):
                                item.csv_vcf(vcard,filename)
                        elif(commande == "-p"):
                            if(".html" in filename):
                                item.page_vcf(vcard,filename)
                    # Si on as pas d'autres arguments on affiche juste le contenue
                    else:
                        vcard:list = item.get_content_vcf(path)
                        item.afficher(vcard)

            except:
                #si jamais l'argument '2' n'est pas bon, on retourne une erreur
                print("\u001b[31m *sigh* votre second argument n'est pas bon... essayer de taper \"python3 cli.py -h\" pour savoir quoi faire \u001b[37m")
    except:
        # Si une erreur est retourner, afficheras ce message
        print("\u001b[31m Aie ! il semble vous manquer quelque chose, essayer \"python3 cli.py -h\" \u001b[37m")

if __name__ == "__main__":
    # on lance le main
    main()