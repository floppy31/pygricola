
from partie import Partie

listeReponse=[] #/pour prédefinir les premières reponses tapes au clavier
#permet de jouer les premier coup automatiquemetn

nJoueurs=2
p=Partie(nJoueurs,listeReponse)    
p.demarragePartie()
# for j in range(1,nJoueurs+1):
#     print(p.joueurs[j])
#     

