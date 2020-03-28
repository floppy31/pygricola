
from partie import Partie

listeReponse=["17","o","0","o","0","o","0","o","-1","o","0","o","0","o","0","o"]
 #/pour prédefinir les premières reponses tapes au clavier
#permet de jouer les premier coup automatiquemetn

nJoueurs=2
p=Partie(nJoueurs,listeReponse)    
p.demarragePartie()
# for j in range(1,nJoueurs+1):
#     print(p.joueurs[j])
#     
