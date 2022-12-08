# Projet Python : gestion de fichier ics / vcf

Réalisé par : VOLQUARDSEN Alex
Le : 18/11/2022
état : Version 1.0
à : L3-I, CY paris cergy université

Le but de ce projet est de créer un programme permettant d'afficher les informations ainsi que modifier ces dernières dans des fichiers au format ics et vcf. Ce projet a pour principe l'utilisation du programme de deux façon différentes, la première à l'aide d'une version CLI (version console) et la deuxième partie étant un GUI (une interface graphique) permettant à l'utilisateur d'effectuer toutes les actions que le programme lui permet.

## Prérequis

Pour utiliser ce programme, vous ddevez disposer de python3.10 au minimum. Pour vous assurer que votre version est correcte vous pouvez utiliser la commande :

sous windows powershell :
        
    python --version

sous linux :
    
    python3 --version

si votre version est inferieur à 3.10 vous devrez la mettre à niveau. Vous pouvez le faire en téléchargeant une version plus récente ici :  <https://www.python.org/downloads/>

## Utilisation :

Vous disposerez de différents moyens d'utiliser le programme, vous pourrez l'utiliser en mode console (CLI) ou à l'aide d'une interface graphique (GUI)
pour utiliser ce programme en mode console, vous devrez commencé votre ligne soit par **python3** sous linux soit par **python** sous windows powershell (je ne possède pas de mac alors je ne sais pas comment le faire sur MacOs déso)

### Utilisation en mode console :

Pour utilise ce programme vous pourrez afficher les diffrentes commandes possible à l'aide de cette commande :

    python cli.py -h

Le programme vous permettras d'afficher des fichier d'extension *.cli* et *.vcf* de façon structuré afin de permettre une meilleure lecture des informations. Vous pourrez aussi à l'aide de l'utilisation de la version ligne de commande créer des fragments html des fichier et d'ajouter ou de créer un fichier csv contenant les informations contenue dans des fichier *.cli* et *.vcf*

**/!\ si vous souhaiter créer un fichier csv ou un fragment html vous devrez vous assurer que l'extension de ces fichier est bien la bonne sinon une erreur sera retourner.**

Enfin vous pourrez créer un squelette de page html contenant des fragments de code html avec les informations contenue dans votre fichier.

### Utilisation en mode graphique :

Pour utiliser le mode graphique vous pouvez soit lancer directement le fichier **gui.py** avec python ou alors rentrer la commande suivante dans votre terminal :

    python gui.py

Depuis cette interface graphique, vous pourrez séléctionner un fichier de type *ics* ou *vcf* et à l'aide d'un bouton en afficher le contenue principal, dans la fenêtre d'affichage il vous seras aussi possible de créer un fragment html ou d'ajouter les informations dans un fichier csv.

Vous pourrez de plus modifié le contenue principal du fichier séléctionné à l'aide de la fenêtre d'édition ( noter que ces modifications ce font sur le fichier initial)

