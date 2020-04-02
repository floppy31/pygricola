from pygricola.carte import Carte 


class CarteActionSpeciale(Carte):

    def __init__(self,partie,nom,desc):
        self.etat=0 #0 dispo, 1 achetable, -1 plus dispo
        self.listeActionSpeciale=[]
        super().__init__(nom,desc)
        
    
    
class ActionSpeciale(Carte):
    def __init__(self,partie,nom,desc,cout,effet):
        super().__init__(nom,desc)    
            