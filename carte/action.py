from pygricola.carte import Carte 
import pygricola.util as util




class CarteAction(Carte):

    def __init__(self,partie,uid,possibilites={},cout={},condition={},effet={},visible=False,activer=True,sansPion=False):
        self.visible=visible
        self.activer=activer
        self.libre=True
        super().__init__(partie,uid,possibilites=possibilites,cout=cout,effet=effet,condition=condition,sansPion=sansPion)
        
    def reappro(self):
        pass


    @property
    def display(self):
        return "Faire: {}".format(self.nom)


        
class CaseAppro(CarteAction):

    def __init__(self,partie,uid,appro,possibilites={},effet={},cout={},visible=False,sansPion=False):
        self.appro=appro
        super().__init__(partie,uid,possibilites=possibilites,cout=cout,effet=effet,visible=visible,sansPion=sansPion)
        
    def reappro(self):
        for k in self.appro.keys():
            if k in self.cout.keys():
                self.cout[k]+=self.appro[k]
            else:
                self.cout[k]=self.appro[k]
    def vider(self):
        self._cout=util.rVide()
                        
                
    @property
    def display(self):
        return "Prendre {} sur {}".format(util.prettyGain(self.cout),self.nom)            
            
#     
#     def effet(self,faire=False):
#         if not faire:
#             return self.cout
#         else:
#             ressource=self.cout
#             self.libre=False
#             return ressource


                
