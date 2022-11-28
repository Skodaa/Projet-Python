"""!
    Ce fichier contient la fonction principale du CLI

    @author VOLQUARDSEN Alex
    @since 13/11/2022
    @version 1.0.3
"""

from classes import items
from classes import ics
from classes import vcf
import sys
import os


##
# Fonction ayant effet de main
def main()->None:

    try:
        # Si l'argument '1' n'existe pas retourne une erreur 
        arg1:str = str(sys.argv[1]) 

        if((arg1 == "-h") or (arg1 == "-help")): # Si l'argument '1' est '-h' alors on appel la fonction d'aide
            
            item = items("")
            item.help()

        elif(arg1 == "-d"):
            
            try:
                item = items("")
                path = sys.argv[2]
                item.path = os.path.abspath(path)
                item.list_files(path,0)
            
            except:
                # Si jamais l'argument '2' n'est pas bon, on retourne une erreur
                print("\u001b[31m *sigh* votre second argument n'est pas bon... essayer de taper \"python3 cli.py -h\" pour savoir quoi faire \u001b[37m")

        elif(arg1 == "-i"):

            try:
                path = sys.argv[2]
                if(".ics" in path):

                    item = ics("")
                    item.path = os.path.abspath(path)

                    if(len(sys.argv)==5):
                        commande:str = sys.argv[3]
            
                        if(commande =="-h"):
                            calendar:list = item.get_content_ics(path)
                            filename:str = sys.argv[4]
                            if(".html" in filename):
                                item.fragment_ics(calendar,filename)
                            elif(".csv" in filename):
                                item.csv_ics(calendar,filename)
                        elif(commande == "-p"):
                            calendar:list = item.get_content_ics(path)
                            filename:str = sys.argv[4]
                            item.page_ics(calendar,filename)
                                
                    else:
                        calendar:list = item.get_content_ics(path)
                        item.afficher(calendar)

                elif(".vcf" in path):

                    item = vcf("")
                    item.path = os.path.abspath(path)

                    if(len(sys.argv) == 5):
                        commande:str = sys.argv[3]

                        if(commande == "-h"):
                            vcard:list = item.get_content_vcf(path)
                            filename:str = sys.argv[4]
                            if(".html" in filename):
                                item.fragment_vcf(vcard,filename)
                            elif(".csv" in filename):
                                item.csv_vcf(vcard,filename)
                                pass
                        elif(commande == "-p"):
                            vcard:list = item.get_content_vcf(path)
                            filename:str = sys.argv[4]
                            item.page_vcf(vcard,filename)
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
    main()