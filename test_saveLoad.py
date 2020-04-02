
from partie import Partie

listeReponse=["17","o","0","o","0","o","0","o","0", "o", "-1","o","0","o","0","o","1","o","0","o","1","o","-1","o"]
 #/pour prédefinir les premières reponses tapes au clavier
#permet de jouer les premier coup automatiquemetn

nJoueurs=2
p=Partie()
p.initialiser(nJoueurs,listeReponse)   
print(p.save())
#p.demarragePartie()    


# for j in range(1,nJoueurs+1):
#     print(p.joueurs[j])
#     
