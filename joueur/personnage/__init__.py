
from pygricola.carte import Carte

class Personnage(object):

    def __init__(self,loc,id):
        self.localisation=loc
        self.localisationInit=loc
        self.consomationNourriture=2
        self.id=id
        
    def retourMaison(self):
        if isinstance(self.localisation,Carte):
            self.localisation.libre=True
            self.localisation=self.localisationInit
    
        

