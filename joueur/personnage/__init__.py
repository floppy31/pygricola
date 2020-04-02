
from pygricola.carte import Carte

class Personnage(object):

    def __init__(self,loc,id,couleur):
        self.localisation=loc
        self.localisationInit=loc
        self.consomationNourriture=2
        self.id=id
        self.couleur=couleur
        
    def retourMaison(self):
        if isinstance(self.localisation,Carte):
            self.localisation.libre=True
            #au cas ou ...normalement c'est tjr vrai
            if(self in self.localisation.occupants):
                self.localisation.occupants.pop(self.localisation.occupants.index(self))
            self.localisation=self.localisationInit
    
        
    def save(self):
        dico={}
        dico['localisation']=self.localisation
        dico['localisationInit']=self.localisationInit
        dico['consomationNourriture']=self.consomationNourriture
        dico['id']=self.id
        return dico
