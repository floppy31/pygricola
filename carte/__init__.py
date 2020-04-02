import pygricola.util as util




class Carte:

    def __init__(self,partie, nom,description,possibilites={},cout={},condition={},effet={},option={},activer=util.dummy,sansPion=False):
        self.nom = nom
        self.description = description
        self.partie=partie
        if type(cout)==dict:
            self._cout=cout.copy()
        else:
            self._cout=cout
        if type(condition)==dict:
            self._condition=condition.copy()
        else:
            self._condition=condition      
        if type(option)==dict:
            self._option=option.copy()
        else:
            self._option=condition                
        self._activer=activer 
        self._effet=effet
        self._possibilites=possibilites
        self.sansPion=sansPion
        self.phraseJouer='joue :'
        self.occupants=[]
#        super().__init__()
    
    def __str__(self):
           return self.nom
    def activer(self):
        return self._activer(self)      
        
    @property   
    def short(self):
        return self.nom[0:7]
    
    @property   
    def cout(self):
        if type(self._cout)==dict:
            return self._cout
        else:
            return self._cout(self.partie)
    
    @property   
    def condition(self):
        if type(self._condition)==dict:
            return self._condition
        else:
            return self._condition(self.partie)        
    @property   
    def option(self):
        if type(self._option)==dict:
            return self._option
        else:
            return self._option(self.partie)        

    
    def effet(self,choix,choixPossibles):
        if type(self._effet)==dict:
            return self._effet
        else:
            return self._effet(self.partie,choix,choixPossibles,self)    

    def possibilites(self):
        if type(self.possibilites)==dict:
            return -1 #on n'a pas de choix à faire
        else:
            return self._possibilites(self.partie)        

        
    def jouer(self):
        encore=True # on va encore pouvoir jouer après
        #on regarde si la carte a une fonction possibilite
        if not type(self._possibilites)==dict:
            choixPossibles=self._possibilites(self.partie,self)
            self.partie.choixPossibles=choixPossibles
            self.sujet=self
            return (choixPossibles,self,encore,"jouerA")
        else:
            self.partie.messagesPrincipaux.append("{} {} {}".format(self.partie.joueurQuiJoue().nom,self.phraseJouer,self.nom))
            self.partie.joueurQuiJoue().mettreAJourLesRessources(self.cout)
            self._cout=util.rVide()
            if self.sansPion==True:
                print('vous pouvez jouer encore')
                self.partie.initChoix()
                return (-1,self,encore,"jouerB")

            else:
                personnage=self.partie.joueurQuiJoue().personnages.pop()
                self.partie.joueurQuiJoue().personnagesPlaces.append(personnage)                  
                self.mettrePersonnage(personnage)
                encore=False
            return (-1,self,encore,"jouerC")
    
    def mettrePersonnage(self,perso):
        print("Mettre personnage")
        perso.localisation=self
        self.occupants.append(perso)
        self.libre=False
            
    def printCout(self):
        return str(self.cout)
    
    def save(self):
        return {'nom':self.nom}
        
def byPassNaissance():
    pass

def avoirXChamp(type,x):
    pass

def avoirXSavoirFaire(type,x):
    pass



def possibilitesCuisson(partie,carte):
    #on recupere le dict cuisson dans option
    dictCuisson=carte.option['cuissonDict']    
    possibilites=[]
    for res in ['l','m','s','v']:
        if (partie.joueurQuiJoue().ressources[res]>0):
            possibilites.append(Carte(partie,"cuire un {} pour {} pn".format(util.short2Long[res],dictCuisson[res]),"toto",cout={res:1,'n':-dictCuisson[res]},sansPion=True))  
    partie.phraseChoixPossibles="Que voulez vous cuire? :"
    return possibilites            
def cuisson(partie,choix,possibilites,carte):
    #on recupere le dict cuisson dans option
    dictCuisson=carte.option['cuissonDict']
    print('cuisson',choix,possibilites,carte,possibilites[choix])
    possibilites[choix].jouer()
    return 0

def payerLeCout():
    variablesGlobales.joueurs[variablesGlobales.quiJoue].mettreAJourLesRessources(possibilites[choix].cout)
    




majeursDict={}
majeursDict["foyer à 2"]={
    'nom':'Foyer à 2',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'a':2},
    'activer':cuisson,
    'option':{'cuissonDict':{'l':2,'m':2,'s':2,'v':3},'cuissonPain':{'c':2}},

    'visible':True,
    'devoile': "abatoir à chevaux 1",   
    }
majeursDict["foyer à 3"]={
    'nom':'Foyer à 3',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'a':3},
    'activer':cuisson ,
    'option':{'cuissonDict':{'l':2,'m':2,'s':2,'b':3},'cuissonPain':{'c':2}},
    'visible':True,
    'devoile': "abatoir à chevaux 2",      
    }

majeursDict["abatoir à chevaux 1"]={
    'nom':'abatoir à chevaux 1',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'a':1,'p':1},
    'activer':cuisson ,
    'option':{'cuissonDict':{'l':1,'m':1,'s':1,'b':2,'h':1}},
    'visible':False     
    }
majeursDict["abatoir à chevaux 2"]={
    'nom':'abatoir à chevaux 2',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'a':1,'p':1},
    'activer':cuisson ,
    'option':{'cuissonDict':{'l':1,'m':1,'s':1,'b':2,'h':1}},
    'visible':False     
    }

mineursDict={}
mineursDict["foyer simple"]={
    'nom':'Foyer simple',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'a':1},
    'activer':cuisson,
    'option':{'cuissonDict':{'l':2,'m':1,'s':2,'b':3},'cuissonPain':{'c':2}},    
    'sansPion':True,
    'effet':cuisson,
    'possibilites':possibilitesCuisson,
    }

savoirFaireDict={}

utilitaireDict={}
utilitaireDict["c cru"]={
    'nom':"manger cru une cereale pour 1 pn",
    'description':"toto",
    'cout':{'c':1,'n':-1},
    'sansPion':True
    }

utilitaireDict["l cru"]={
    'nom':"manger cru un légume pour 1 pn",
    'description':"toto",
    'cout':{'l':1,'n':-1},
    'sansPion':True
    }


deck={
    'mineurs':mineursDict,
    'majeurs':majeursDict,
    'savoirFaires':savoirFaireDict,
    'utilitaire':utilitaireDict
    }



    
