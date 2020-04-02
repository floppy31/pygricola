from pygricola.carte import Carte 
from pygricola.util import dummy


class AmenagementMajeur(Carte):

    def __init__(self,partie,nom,description,cout={},condition={},effet={},option={},activer=dummy,visible=False,devoile=None,sansPion=True):
        self.visible=visible
        self.devoile=devoile
        super().__init__(partie,nom,description,cout=cout,condition=condition,effet=effet,option=option,activer=activer,sansPion=sansPion)
        



        
      
        
