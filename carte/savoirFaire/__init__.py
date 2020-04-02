from pygricola.carte import Carte 


class SavoirFaire(Carte):

    def __init__(self,partie,nom,description,cout={}):
        self.etat=0 #0 dispo, 1 achetable, -1 plus dispo
        super().__init__(nom,description,cout={})
        
