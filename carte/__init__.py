import variablesGlobales
import util
from pygricola.ressources import short2Long




class Carte:

    def __init__(self, nom,description,cout={},condition={},effet={},activer=util.dummy,sansPion=False):
        self.nom = nom
        self.description = description
        if type(cout)==dict:
            self._cout=cout.copy()
        else:
            self._cout=cout
        if type(condition)==dict:
            self._condition=condition.copy()
        else:
            self._condition=condition      
        self.activer=activer 
        self._effet=effet
        self.sansPion=sansPion
        self.phraseJouer='je joue :'
#        super().__init__()
    
    def __str__(self):
           return self.nom
       
    @property   
    def short(self):
        return self.nom[0:7]
    
    @property   
    def cout(self):
        if type(self._cout)==dict:
            return self._cout
        else:
            return self._cout()
    
    @property   
    def condition(self):
        if type(self._condition)==dict:
            return self._condition
        else:
            return self._condition()        

    
    def effet(self):
        if type(self._effet)==dict:
                
            return self._effet
        else:
            return self._effet()    
        
    def jouer(self):
        print(self.phraseJouer,self.nom)
        self.effet()
        return self
        
    def printCout(self):
        return str(self.cout)
        
def byPassNaissance():
    pass

def avoirXChamp(type,x):
    pass

def avoirXSavoirFaire(type,x):
    pass


def cuisson1():
    dictCuisson={'l':2,'m':2,'s':2,'v':3,'c':2}
    
    print("cuisson1",variablesGlobales.joueurs.keys())
    possibilites=[]
    for res in ['l','m','s','v']:
        if (variablesGlobales.joueurs[variablesGlobales.quiJoue].ressources[res]>0):
            possibilites.append(Carte("cuire un {} pour {} pn".format(short2Long[res],dictCuisson[res]),"toto",cout={res:1,'n':-dictCuisson[res]}),sansPion=True)        
    choix=util.printPossibilities("Que voulez vous cuire? :",possibilites)
    if choix != -1:
        possibilites[choix].jouer() 
        variablesGlobales.joueurs[variablesGlobales.quiJoue].mettreAJourLesRessources(possibilites[choix].cout)       
    return

def payerLeCout():
    variablesGlobales.joueurs[variablesGlobales.quiJoue].mettreAJourLesRessources(possibilites[choix].cout)
    
def cuisson(dico):
    #{'l':2,'m':2,'s':2,'b':3,'c':2}
    print("cuisson")
# class Paillasse(AmenagementMineur):
#     def __init__(self,nom,description,cout={'b':1},condition=avoirXChamp('c',2),effet=byPassNaissance):
#         self.passableAGauche=passableAGauche
#         super().__init__(nom,description,cout=cout,effet=effet)    



majeursDict={}
majeursDict["foyer à 2"]={
    'nom':'Foyer à 2',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'a':2},
    'activer':cuisson1,
    'visible':True,
    'devoile': "abatoir à chevaux 1",   
    }
majeursDict["foyer à 3"]={
    'nom':'Foyer à 3',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'a':3},
    'activer':cuisson({'l':2,'m':2,'s':2,'b':3,'c':2}) ,
    'visible':True,
    'devoile': "abatoir à chevaux 2",      
    }

majeursDict["abatoir à chevaux 1"]={
    'nom':'abatoir à chevaux 1',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'a':1,'p':1},
    'activer':cuisson({'l':1,'m':1,'s':1,'b':2,'h':1}) ,
    'visible':False     
    }
majeursDict["abatoir à chevaux 2"]={
    'nom':'abatoir à chevaux 2',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'a':1,'p':1},
    'activer':cuisson({'l':1,'m':1,'s':1,'b':2,'h':1}) ,
    'visible':False     
    }

mineursDict={}
mineursDict["foyer simple"]={
    'nom':'Foyer simple',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'a':1},
    'activer':cuisson({'l':2,'m':1,'s':2,'b':3,'c':2})
    
    }

savoirFaireDict={}

utilitaireDict={}
utilitaireDict["c cru"]=Carte("manger cru une cereale pour 1 pn","toto",cout={'c':1,'n':-1},sansPion=True)
utilitaireDict["l cru"]=Carte("manger cru un légume pour 1 pn","toto",cout={'l':1,'n':-1},sansPion=True)


deck={
    'mineurs':mineursDict,
    'majeurs':majeursDict,
    'savoirFaires':savoirFaireDict,
    'utilitaire':utilitaireDict
    }



    
