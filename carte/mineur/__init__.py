from pygricola.carte import Carte 
from util import dummy


class AmenagementMineur(Carte):

    def __init__(self,nom,description,cout={},condition={},option={},effet={},activer=dummy,passableAGauche=False,sansPion=True):
        self.passableAGauche=passableAGauche
        super().__init__(nom,description,cout=cout,condition=condition,effet=effet,option=option,activer=activer,sansPion=sansPion)
        



        
      
        