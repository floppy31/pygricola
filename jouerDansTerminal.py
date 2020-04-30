import pygricola.util as util
from partie import Partie,avancer

import logging


logger = logging.getLogger('root')
fmt="##%(levelname)s## %(funcName)s():%(lineno)i: %(message)s"
logging.basicConfig(format=fmt)
logger.setLevel(logging.DEBUG)
#permet de jouer les premier coup automatiquemetn
nJoueurs=3
p=Partie(logger)
p.initialiser(nJoueurs)    
p.demarragePartie()
p.demarrageTour()
p.pointerSurPremier()
while(True):
    id=util.coupAuClavier(p)
    print(id)
    pointeur=avancer(p,id)
#     
