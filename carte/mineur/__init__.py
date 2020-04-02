from pygricola.carte import Carte 
from pygricola.util import dummy


class AmenagementMineur(Carte):

    def __init__(self,partie,nom,description,possibilites={},cout={},condition={},option={},effet={},activer=dummy,passableAGauche=False,sansPion=True):
        self.passableAGauche=passableAGauche
        super().__init__(partie,nom,description,possibilites,cout=cout,condition=condition,effet=effet,option=option,activer=activer,sansPion=sansPion)
        



        
      
        