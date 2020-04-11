import pygricola.util as util
from partie import Partie
listeReponse=[] #/pour prédefinir les premières reponses tapes au clavier
#permet de jouer les premier coup automatiquemetn
nJoueurs=3
p=Partie()
p.initialiser(nJoueurs,listeReponse)    
p.demarragePartie()
p.demarrageTour()
while(True):
    while(True):
        encore=True
        while(encore):
            print(p.messagesPrincipaux[-1])
            p.affichageJoueur()
            sujet=p.joueurQuiJoue() #le sujet est l'objet à qui on demande possibilite
            #au debut c'est joueur, après ça peut être un carte,...
            
            casesJouablesStr=sujet.possibilites()
            p.phraseChoixPossibles="QUE VOULEZ VOUS FAIRE?"
            choix=util.printPossibilities(p,p.phraseChoixPossibles,p.choixPossibles,annulable=False)
            
            (choixPossibles,sujet,encore,message)=p.jouerUid(p.choixPossibles[choix].uid)

#             (choixPossibles,sujet,encore,message)=p.choixPossibles[choix].jouer()
            
            while(choixPossibles=='inputtext'):
                g=input(print(p.phraseChoixPossibles))
                (choixPossibles,sujet,encore,message)=sujet.effet(g,[])
                print(message)
                if choixPossibles==-1:
                    break
                
            
            while(choixPossibles!=-1):
                choix=util.printPossibilities(p,p.phraseChoixPossibles,p.choixPossibles,annulable=True)
                (choixPossibles,sujet,encore,message)=sujet.effet(choix,p.choixPossibles)
                print('test',choixPossibles,sujet,encore)

        
        suivant=p.joueurSuivant()
        if suivant==-1:
            print("BREAK")
            break
#         while(True):
#             if sujet==-1:
#                 #action finie
#                 print("action finie")
#                 break
#             (choixPossibles,sujet)=sujet.jouer()
                

    code=p.finDuTour()
    if code==-1:
        break
    p.demarrageTour()    

# for j in range(1,nJoueurs+1):
#     print(p.joueurs[j])
#     
