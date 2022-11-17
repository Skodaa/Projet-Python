"""!
    Ce fichier contient la fonction principale du CLI

    @author VOLQUARDSEN Alex
    @since 13/11/2022
    @version 1.0.2
"""

from classes import items
import sys
import os


##
# Fonction ayant effet de main
def main()->None:

    item = items("")

    try:
        # Si l'argument '1' n'existe pas retourne une erreur 
        arg1:str = str(sys.argv[1]) 

        if(arg1 == "-h"): # Si l'argument '1' est '-h' alors on appel la fonction d'aide

            item.help()

        elif(arg1 == "-d"):
            
            try:
                path = sys.argv[2]
                item.path = path
                item.list_files(path,0)
            
            except:
                # Si jamais l'argument '2' n'est pas bon, on retourne une erreur
                print("\u001b[31m *sigh* votre second argument n'est pas bon... essayer de taper \"python3 cli.py -h\" pour savoir quoi faire \u001b[37m")

        elif(arg1 == "-i"):

            try:
                path = sys.argv[2]
                item.path = path
                item.read_ics(path)

            except:
                #si jamais l'argument '2' n'est pas bon, on retourne une erreur
                print("\u001b[31m *sigh* votre second argument n'est pas bon... essayer de taper \"python3 cli.py -h\" pour savoir quoi faire \u001b[37m")
    except:
        # Si une erreur est retourner, afficheras ce message
        print("\u001b[31m Aie ! il semble vous manquer quelque chose, essayer \"python3 cli.py -h\" \u001b[37m")

if __name__ == "__main__":
    main()