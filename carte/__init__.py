import pygricola.util as util
import pygricola.fonctionsPlateau as fct

##################################################################################
#---------------------------------------Cuisson-------------------------
##################################################################################          
def possibilitesCuisson(partie,carte,Fake=False):
    #on recupere le dict cuisson dans option
    dictCuisson=carte.option['cuissonDict']    
    possibilites=[]
    for res in ['l','m','s','v']:
        if (partie.joueurQuiJoue().ressources[res]>0):
            possibilites.append(Carte(partie,"cuire un {} pour {} pn".format(util.short2Long[res],dictCuisson[res]),"toto",cout={res:1,'n':-dictCuisson[res]},sansPion=True))  
    if not Fake:
        partie.phraseChoixPossibles="Que voulez vous cuire? :"
        partie.sujet=carte
    return possibilites       

     
def cuisson(partie,choix,possibilites,carte):
    #on recupere le dict cuisson dans option
    dictCuisson=carte.option['cuissonDict']
    print('cuisson',choix,possibilites,carte,possibilites[choix])
    possibilites[choix].jouer()
    return (-1,carte,True,"")
##################################################################################          




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
        #si la condition est dict vide on appelle possibilitesNonVide qui est le défaut
        if self._condition=={}:
            return fct.possibilitesNonVide(self.partie,self)     
        #si c'est un dico non vide
        elif type(self._condition)==dict:
            return self._condition and util.possibilitesNonVide(self.partie,self)  
        else:
            #sino on appelle la condition
            return self._condition(self.partie,self)        
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
            return (choixPossibles,self,encore,"")
        else:
            self.partie.messagesPrincipaux.append("{} {} {}".format(self.partie.joueurQuiJoue().nom,self.phraseJouer,self.nom))
            self.partie.joueurQuiJoue().mettreAJourLesRessources(self.cout)
            self._cout=util.rVide()
            if self.sansPion==True:
                if isinstance(self,ActionSpeciale):
                    #ici passe foire du travail
                    self.carteQuiMePorte.etat+=1
                    self.partie.joueurSuivant()
                    self.partie.initChoix()
                    return (-1,self,encore,"")
                else:
                    print('vous pouvez jouer encore')
                    self.partie.initChoix()
                    return (-1,self,encore,"")

            else:
                personnage=self.partie.joueurQuiJoue().personnages.pop()
                self.partie.joueurQuiJoue().personnagesPlaces.append(personnage)                  
                self.mettrePersonnage(personnage)
                encore=False
            return (-1,self,encore,"")
    
    def mettrePersonnage(self,perso):
        perso.localisation=self
        self.occupants.append(perso)
        self.libre=False
            
    def printCout(self):
        return str(self.cout)
    
    def save(self):
        return {'nom':self.nom}
    
def loadCarte(stri,partie):
    
    pass
        
        
def byPassNaissance():
    pass

def avoirXChamp(type,x):
    pass

def avoirXSavoirFaire(type,x):
    pass





def payerLeCout():
    variablesGlobales.joueurs[variablesGlobales.quiJoue].mettreAJourLesRessources(possibilites[choix].cout)
    



class CarteActionSpeciale(Carte):

    def __init__(self,partie,nom,description):
        self.etat=0 #0 dispo, 1 achetable, -1 plus dispo
        self.listeActionSpeciale=[]
        super().__init__(partie,nom,description)
    
    def listAs(self):
        stri="Action spéciale: <br>"
        for l in self.listeActionSpeciale:
            stri+="{} <br>".format(l.nom)
        return stri
    
    
class ActionSpeciale(Carte):
    def __init__(self,partie,carteQuiMePorte,nom,description,cout={},effet={},possibilites={}):
        self.carteQuiMePorte=carteQuiMePorte
        super().__init__(partie,nom,description,cout=cout,effet=effet,sansPion=True,possibilites=possibilites)    
            
    @property   
    def cout(self):
        cout={'n':0}
        if self.carteQuiMePorte.etat==0:
            pass
        elif self.carteQuiMePorte.etat==1:
            cout['n']+=2

        coutTot=util.ajouter(self._cout,cout)
        return coutTot
    
    @property
    def display(self):
        if self.carteQuiMePorte.etat==0:
            return "Action Spéciale: {}".format(self.nom)
        elif self.carteQuiMePorte.etat==1:
            return "Racheter action spéciale: {} (coûte 2 pn)".format(self.nom)
        

def genererActionsSpeciales(partie):   
    njoueurs=partie.nombreJoueurs
    listeCarteActionSpeciale=[] 
    actionSpecialeDict={}
    actionSpecialeDict["1 cheval pour 1 pn"]={
        'nom':'Acheter un cheval pour 1 pn',
        'description':"Vous pouvez transformer à tout moment...",
        'cout':{'n':1,'h':-1},
        }
    actionSpecialeDict["1 cheval"]={
        'nom':'Prendre un cheval',
        'description':"Vous pouvez transformer à tout moment...",
        'cout':{'h':-1},
        }
    actionSpecialeDict["1 pn"]={
        'nom':'Foire du travail',
        'description':"Vous pouvez transformer à tout moment...",
        'cout':{'n':-1},
        }
    actionSpecialeDict["Marché noir"]={
        'nom':'Marché noir',
        'description':"Vous pouvez transformer à tout moment...",
        'cout':{'f':1},
        'possibilites':fct.possibilitesAmenagementMineur,
        'effet':fct.choixAmenagementMineur
        }
    actionSpecialeDict["Travail clandestin"]={
        'nom':'Travail clandestin',
        'description':"Vous pouvez transformer à tout moment...",
        'cout':{'f':1,'n':1},
        'possibilites':fct.possibilitesAmenagementMajeur,
        'effet':fct.choixAmenagementMajeur
        }
    actionSpecialeDict["Abattre des arbres"]={
        'nom':'Abattre des arbres',
        'description':"Vous pouvez transformer à tout moment...",
        'cout':{'b':-2},
        'possibilites':fct.possibilitesAbattreDesArbres,
        'effet':fct.choixAbattreDesArbres        
        }
    actionSpecialeDict["Couper et brûler"]={
        'nom':'Couper et brûler',
        'description':"Vous pouvez transformer à tout moment...",
        'possibilites':fct.possibilitesCouperBruler,
        'effet':fct.choixCouperBruler   
        }
    actionSpecialeDict["Couper la tourbe"]={
        'nom':'Couper la tourbe',
        'description':"Vous pouvez transformer à tout moment...",
        'possibilites':fct.possibilitesCouperLaTourbe,
        'effet':fct.choixCouperLaTourbe  
        }
    carteActionSpecialeDict={2:[
    ["1 cheval pour 1 pn","1 pn","Marché noir","Travail clandestin"],
    ["Abattre des arbres","Couper et brûler","Couper la tourbe"]],
                         3:[
    ["1 cheval","1 pn","Marché noir","Travail clandestin"],
    ["Abattre des arbres","Couper et brûler","Couper la tourbe"]],
                         4:[
    ["1 cheval","Abattre des arbres"],
    ["1 pn","Marché noir","Travail clandestin"],
    ["Couper et brûler","Couper la tourbe"]],
                         5:[
    ["1 cheval pour 1 pn"],
    ["Marché noir","Travail clandestin"],
    ["Couper et brûler","Couper la tourbe"],
    ["1 pn","Abattre des arbres"]]
                        }
    for listActions in carteActionSpecialeDict[njoueurs]:
        
        CAS=CarteActionSpeciale(partie,"Action spéciale:" + str(carteActionSpecialeDict[njoueurs].index(listActions)),"as")
        for a in listActions:
            aS=ActionSpeciale(partie,CAS,**actionSpecialeDict[a])
            CAS.listeActionSpeciale.append(aS)
        listeCarteActionSpeciale.append(CAS)
    return listeCarteActionSpeciale
    
#3

#4

#5            


majeursDict={}
majeursDict["foyer à 2"]={
    'nom':'Foyer à 2',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'a':2},
    'activer':cuisson,
    "possibilites":possibilitesCuisson,
    'option':{'cuissonDict':{'l':2,'m':2,'s':2,'v':3},'cuissonPain':{'c':2}},
    'visible':True,
    'devoile': "abatoir à chevaux 1",   
    'pointsVictoire':1,
    }
majeursDict["foyer à 3"]={
    'nom':'Foyer à 3',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'a':3},
    'activer':cuisson ,
    "possibilites":possibilitesCuisson,
    'option':{'cuissonDict':{'l':2,'m':2,'s':2,'v':3},'cuissonPain':{'c':2}},
    'visible':True,
    'devoile': "abatoir à chevaux 2",     
    'pointsVictoire':1, 
    }

majeursDict["abatoir à chevaux 1"]={
    'nom':'abatoir à chevaux 1',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'a':1,'p':1},
    'activer':cuisson ,
    "possibilites":possibilitesCuisson,    
    'option':{'cuissonDict':{'l':1,'m':1,'s':1,'v':2,'h':1}},
    'visible':False,
    'pointsVictoire':2,     
    }
majeursDict["abatoir à chevaux 2"]={
    'nom':'abatoir à chevaux 2',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'a':1,'p':1},
    'activer':cuisson ,
    "possibilites":possibilitesCuisson,
    'option':{'cuissonDict':{'l':1,'m':1,'s':1,'v':2,'h':1}},
    'visible':False,
    'pointsVictoire':2,     
    }
majeursDict["Four à tourbe"]={
    'nom':'four à tourbe',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'p':1},
    'visible':True,
    'devoile': "Musée de la lande",  
    'pointsVictoire':1,   
    }
majeursDict["Musée de la lande"]={
    'nom':'Musée de la land',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'p':1,'r':1,'a':1},
    'visible':False,
    'pointsVictoire':3,
    }
majeursDict["Loge du forestier"]={
    'nom':'Loge du forestier',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'a':2,'b':1},
    'visible':True,
    'devoile': "Ecuries",     
    'pointsVictoire':1,
    }
majeursDict["Ecuries"]={
    'nom':'Ecuries',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'a':1,'b':2,'r':1},
    'visible':False,
    'devoile': "Ecuries",     
    'pointsVictoire':3,
    }
majeursDict["Fourneau à 4"]={
    'nom':'Fourneau à 4',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'a':4},
    'activer':cuisson ,
    "possibilites":possibilitesCuisson,
    'option':{'cuissonDict':{'l':3,'m':2,'s':3,'v':4},'cuissonPain':{'c':3}},
    'visible':True,
    'devoile': "Coquerie 1",     
    'pointsVictoire':1, 
    }
majeursDict["Fourneau à 5"]={
    'nom':'Fourneau à 5',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'a':5},
    'activer':cuisson ,
    "possibilites":possibilitesCuisson,
    'option':{'cuissonDict':{'l':3,'m':2,'s':3,'v':4},'cuissonPain':{'c':3}},
    'visible':True,
    'devoile': "Coquerie 2",     
    'pointsVictoire':1, 
    }
majeursDict["Coquerie 1"]={
    'nom':'Coquerie 1',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'a':6},
    'activer':cuisson ,
    "possibilites":possibilitesCuisson,
    'option':{'cuissonDict':{'l':3,'m':2,'s':3,'v':4},'cuissonPain':{'c':3}},
    'visible':False,
    'pointsVictoire':2, 
    }
majeursDict["Coquerie 2"]={
    'nom':'Coquerie 2',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'a':6},
    'activer':cuisson ,
    "possibilites":possibilitesCuisson,
    'option':{'cuissonDict':{'l':3,'m':2,'s':3,'v':4},'cuissonPain':{'c':3}},
    'visible':False,
    'pointsVictoire':2, 
    }

majeursDict["Puits"]={
    'nom':'Puits',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'p':3,'b':1},
    'option':{'reservePuit':{'n':5}},
    'visible':True,
    'pointsVictoire':3, 
    'devoile': "Eglise du village",
    }
majeursDict["Eglise du village"]={
    'nom':'Eglise du village',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'p':4,'b':2,'n':-2},
    'option':{'chauffage':0},
    'visible':False,
    'pointsVictoire':4, 
    }

majeursDict["Four en brique"]={
    'nom':'Four en briquee',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'a':3,'p':1},
    'option':{'cuissonPain':{'c':5}},
    'visible':True,
    'pointsVictoire':2, 
    'devoile': "Chaudière",
    }
majeursDict["Chaudière"]={
    'nom':'Chaudière',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'a':1,'p':1,'c':-2},
    'visible':False,
    'pointsVictoire':1, 
    }
majeursDict["Four en pierre"]={
    'nom':'Four en pierre',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'p':3,'a':1},
    'option':{'cuissonPain':{'c':4}},
    'visible':True,
    'pointsVictoire':3, 
    'devoile': "Poêle",
    }
majeursDict["Poêle"]={
    'nom':'Poêle',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'a':2,'p':1},
    'visible':False,
    'pointsVictoire':1, 
    }
majeursDict["Menuiserie"]={
    'nom':'Menuiserie',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'p':2,'b':2},
    'visible':True,
    'pointsVictoire':2, 
    'devoile': "Fabricant de meubles",
    }
majeursDict["Fabricant de meubles"]={
    'nom':'Fabricant de meubles',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'p':1,'b':1},
    'visible':False,
    'pointsVictoire':2, 
    'option':{'echange':{'b':1,'a':-1}},
    }

majeursDict["Poterie"]={
    'nom':'Poterie',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'p':2,'a':2},
    'visible':True,
    'pointsVictoire':2, 
    'devoile': "Céramiste",
    }
majeursDict["Céramiste"]={
    'nom':'Céramiste',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'p':1,'a':1},
    'visible':False,
    'pointsVictoire':2, 
    'option':{'echange':{'a':1,'b':-1}},
    }

majeursDict["Vanerie"]={
    'nom':'Vanerie',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'p':2,'r':2},
    'visible':True,
    'pointsVictoire':2, 
    'devoile': "Fabricant de paniers",
    }
majeursDict["Fabricant de paniers"]={
    'nom':'Fabricant de paniers',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'p':1,'r':1},
    'visible':False,
    'pointsVictoire':2, 
    'option':{'echange':{}},
    }


mineursDict={}
mineursDict["foyer simple"]={
    'nom':'Foyer simple',
    'description':"Vous pouvez transformer à tout moment...",
    'cout':{'a':1},
    'activer':cuisson,
    'option':{'cuissonDict':{'l':2,'m':1,'s':2,'v':3},'cuissonPain':{'c':2}},    
    'sansPion':True,
    'possibilites':possibilitesCuisson,
    }

savoirFaireDict={}

utilitaireDict={}
utilitaireDict["c cru"]={
    'nom':"Activer: manger cru une cereale pour 1 pn",
    'description':"toto",
    'cout':{'c':1,'n':-1},
    'sansPion':True
    }

utilitaireDict["l cru"]={
    'nom':"Activer: manger cru un légume pour 1 pn",
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



    
