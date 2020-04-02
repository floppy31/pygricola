from pygricola.carte import Carte 




class CarteAction(Carte):

    def __init__(self,partie,nom,desc,possibilites={},cout={},condition={},effet={},visible=False,activer=True,sansPion=False):
        self.visible=visible
        self.activer=activer
        self.libre=True
        super().__init__(partie,nom,desc,possibilites=possibilites,cout=cout,effet=effet,condition=condition,sansPion=sansPion)
        
    def reappro(self):
        pass
    

        
    
    def faireAction(Carte):
        pass



        
class CaseAppro(CarteAction):

    def __init__(self,partie,nom,desc,appro,possibilites={},effet={},cout={},visible=False,sansPion=False):
        self.appro=appro
        super().__init__(partie,nom,desc,possibilites=possibilites,cout=cout,effet=effet,visible=visible,sansPion=sansPion)
        
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


                
