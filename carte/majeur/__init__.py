from pygricola.carte import Carte 
from util import dummy


class AmenagementMajeur(Carte):

    def __init__(self,nom,description,cout={},condition={},effet={},option={},activer=dummy,visible=False,devoile=None,sansPion=True):
        self.visible=visible
        self.devoile=devoile
        super().__init__(nom,description,cout=cout,condition=condition,effet=effet,option=option,activer=activer,sansPion=sansPion)
        



        
      
        