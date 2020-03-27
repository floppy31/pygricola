from pygricola.carte import Carte 


resourceAlias={
            'bois':'B',
            'argile':'A',
            'pierre':'P',
            'roseau':'R',
            'pn':'N',
            'feu':'F',
            }


class CarteAction(Carte):

    def __init__(self,nom,desc,cout={},condition={},effet={},visible=False,activer=True,sansPion=False):
        self.visible=visible
        self.activer=activer
        self.libre=True
        super().__init__(nom,desc,cout=cout,effet=effet,condition=condition,sansPion=sansPion)
        
    def reappro(self):
        pass
    

        
    
    def faireAction(Carte):
        pass

    def jouer(self,pion):
        pion.localisation=self
        self.libre=False
        return super().jouer()
            

        
class CaseAppro(CarteAction):

    def __init__(self,nom,desc,appro,visible=False,sansPion=False):
        self.appro=appro
        super().__init__(nom,desc,visible=visible,sansPion=sansPion)
        
    def reappro(self):
        for k in self.appro.keys():
            if k in self.cout.keys():
                self.cout[k]+=self.appro[k]
            else:
                self.cout[k]=self.appro[k]
            
            
#     
#     def effet(self,faire=False):
#         if not faire:
#             return self.cout
#         else:
#             ressource=self.cout
#             self.libre=False
#             return ressource


                
