import pygricola.util as util
import pygricola.fonctionsPlateau as fct
from pygricola.traduction import trad

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

    def __init__(self,partie,uid,possibilites={},cout={},condition={},effet={},option={},activer=util.dummy,sansPion=False):
        self.uid=uid
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
    def nom(self):
        return self.nomTrad('fr')
    
    def nomTrad(self,lang):
        return trad[self.uid][lang][0]
       
    def descTrad(self,lang):
        return trad[self.uid][lang][1]
                    
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


class Amenagement(Carte):

    def __init__(self,partie,uid,possibilites={},cout={},condition={},option={},effet={},activer=util.dummy,sansPion=True,pointsVictoire=0,pointsSpeciaux=util.dummy):
        self.pointsVictoire=pointsVictoire
        self.pointsSpeciaux=pointsSpeciaux
        super().__init__(partie,uid,possibilites,cout=cout,condition=condition,effet=effet,option=option,activer=activer,sansPion=sansPion)
        
    @property
    def display(self):
        return "Activer: {}".format(self.nom)            
 

class AmenagementMineur(Amenagement):

    def __init__(self,partie,uid,possibilites={},cout={},condition={},option={},effet={},activer=util.dummy,passableAGauche=False,sansPion=True,pointsVictoire=0,pointsSpeciaux=util.dummy):
        self.passableAGauche=passableAGauche
        super().__init__(partie,uid,possibilites=possibilites,cout=cout,condition=condition,effet=effet,option=option,activer=activer,sansPion=sansPion,pointsVictoire=pointsVictoire,pointsSpeciaux=pointsSpeciaux)

class AmenagementMajeur(Amenagement):

    def __init__(self,partie,uid,possibilites={},cout={},condition={},effet={},option={},activer=util.dummy,visible=False,devoile=None,sansPion=True,pointsVictoire=0,pointsSpeciaux=util.dummy):
        self.visible=visible
        self.devoile=devoile
        super().__init__(partie,uid,possibilites=possibilites,cout=cout,condition=condition,effet=effet,option=option,activer=activer,sansPion=sansPion,pointsVictoire=pointsVictoire,pointsSpeciaux=pointsSpeciaux)




class CarteActionSpeciale(Carte):

    def __init__(self,partie,uid):
        self.etat=0 #0 dispo, 1 achetable, -1 plus dispo
        self.listeActionSpeciale=[]
        super().__init__(partie,uid)
    
    def listAs(self):
        stri="Action spéciale: <br>"
        for l in self.listeActionSpeciale:
            stri+="{} <br>".format(l.nom)
        return stri
    
    
class ActionSpeciale(Carte):
    def __init__(self,partie,uid,carteQuiMePorte,cout={},effet={},possibilites={}):
        self.carteQuiMePorte=carteQuiMePorte
        super().__init__(partie,uid,cout=cout,effet=effet,sansPion=True,possibilites=possibilites)    
            
    @property   
    def cout(self):
        cout={'n':0}
        if self.carteQuiMePorte.etat==0:
            pass
        elif self.carteQuiMePorte.etat==1:
            cout['n']+=2
        print('cout actionspe dbg',self.carteQuiMePorte.etat,self._cout,cout)
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
    actionSpecialeDict["b0"]={
        'cout':{'n':1,'h':-1},
        }
    actionSpecialeDict["b1"]={
        'cout':{'h':-1},
        }
    actionSpecialeDict["b2"]={
        'cout':{'n':-1},
        }
    actionSpecialeDict["b3"]={
        'cout':{'f':1},
        'possibilites':fct.possibilitesAmenagementMineur,
        'effet':fct.choixAmenagementMineur
        }
    actionSpecialeDict["b4"]={
        'cout':{'f':1,'n':1},
        'possibilites':fct.possibilitesAmenagementMajeur,
        'effet':fct.choixAmenagementMajeur
        }
    actionSpecialeDict["b5"]={
        'cout':{'b':-2},
        'possibilites':fct.possibilitesAbattreDesArbres,
        'effet':fct.choixAbattreDesArbres        
        }
    actionSpecialeDict["b6"]={
        'possibilites':fct.possibilitesCouperBruler,
        'effet':fct.choixCouperBruler   
        }
    actionSpecialeDict["b7"]={
        'possibilites':fct.possibilitesCouperLaTourbe,
        'effet':fct.choixCouperLaTourbe  
        }
    carteActionSpecialeDict={1:[],#pas d'as avec 1 seul joueur
                             2:[
    ["b0","b2","b3","b4"],
    ["b5","b6","b7"]],
                         3:[
    ["b1","b2","b3","b4"],
    ["b5","b6","b7"]],
                         4:[
    ["b1","b5"],
    ["b2","b3","b4"],
    ["b6","b7"]],
                         5:[
    ["b0"],
    ["b3","b4"],
    ["b6","b7"],
    ["b2","b5"]]
                        }
    for listActions in carteActionSpecialeDict[njoueurs]:
        
        CAS=CarteActionSpeciale(partie,'AS{}'.format(carteActionSpecialeDict[njoueurs].index(listActions)))
        for a in listActions:
            aS=ActionSpeciale(partie,a,CAS,**actionSpecialeDict[a])
            CAS.listeActionSpeciale.append(aS)
        listeCarteActionSpeciale.append(CAS)
    return listeCarteActionSpeciale
    
#3

#4

#5            


majeursDict={}
majeursDict["M0"]={
    'cout':{'a':2},
    'activer':cuisson,
    "possibilites":possibilitesCuisson,
    'option':{'cuissonDict':{'l':2,'m':2,'s':2,'v':3},'cuissonPain':{'c':2}},
    'visible':True,
    'devoile': "M2",   
    'pointsVictoire':1,
    }
majeursDict["M1"]={
    'cout':{'a':3},
    'activer':cuisson ,
    "possibilites":possibilitesCuisson,
    'option':{'cuissonDict':{'l':2,'m':2,'s':2,'v':3},'cuissonPain':{'c':2}},
    'visible':True,
    'devoile': "M3",     
    'pointsVictoire':1, 
    }

majeursDict["M2"]={
    'cout':{'a':1,'p':1},
    'activer':cuisson ,
    "possibilites":possibilitesCuisson,    
    'option':{'cuissonDict':{'l':1,'m':1,'s':1,'v':2,'h':1}},
    'visible':False,
    'pointsVictoire':2,     
    }
majeursDict["M3"]={
    'cout':{'a':1,'p':1},
    'activer':cuisson ,
    "possibilites":possibilitesCuisson,
    'option':{'cuissonDict':{'l':1,'m':1,'s':1,'v':2,'h':1}},
    'visible':False,
    'pointsVictoire':2,     
    }
majeursDict["M4"]={
    'cout':{'p':1},
    'visible':True,
    'devoile': "M5",  
    'pointsVictoire':1,   
    }
majeursDict["M5"]={
    'cout':{'p':1,'r':1,'a':1},
    'visible':False,
    'pointsVictoire':3,
    }
majeursDict["M6"]={
    'cout':{'a':2,'b':1},
    'visible':True,
    'devoile': "M7",     
    'pointsVictoire':1,
    }
majeursDict["M7"]={
    'cout':{'a':1,'b':2,'r':1},
    'visible':False,
    'devoile': "Ecuries",     
    'pointsVictoire':3,
    }
majeursDict["M8"]={
    'cout':{'a':4},
    'activer':cuisson ,
    "possibilites":possibilitesCuisson,
    'option':{'cuissonDict':{'l':3,'m':2,'s':3,'v':4},'cuissonPain':{'c':3}},
    'visible':True,
    'devoile': "M9",     
    'pointsVictoire':1, 
    }
majeursDict["M9"]={
    'cout':{'a':5},
    'activer':cuisson ,
    "possibilites":possibilitesCuisson,
    'option':{'cuissonDict':{'l':3,'m':2,'s':3,'v':4},'cuissonPain':{'c':3}},
    'visible':True,
    'devoile': "M10",     
    'pointsVictoire':1, 
    }
majeursDict["M10"]={
    'cout':{'a':6},
    'activer':cuisson ,
    "possibilites":possibilitesCuisson,
    'option':{'cuissonDict':{'l':3,'m':2,'s':3,'v':4},'cuissonPain':{'c':3}},
    'visible':False,
    'pointsVictoire':2, 
    }
majeursDict["M11"]={
    'cout':{'a':6},
    'activer':cuisson ,
    "possibilites":possibilitesCuisson,
    'option':{'cuissonDict':{'l':3,'m':2,'s':3,'v':4},'cuissonPain':{'c':3}},
    'visible':False,
    'pointsVictoire':2, 
    }

majeursDict["M12"]={
    'cout':{'p':3,'b':1},
    'option':{'reservePuit':{'n':5}},
    'visible':True,
    'pointsVictoire':3, 
    'devoile': "M13",
    }
majeursDict["M13"]={
    'cout':{'p':4,'b':2,'n':-2},
    'option':{'chauffage':0},
    'visible':False,
    'pointsVictoire':4, 
    }

majeursDict["M14"]={
    'cout':{'a':3,'p':1},
    'option':{'cuissonPain':{'c':5}},
    'visible':True,
    'pointsVictoire':2, 
    'devoile': "M14",
    }
majeursDict["M15"]={
    'cout':{'a':1,'p':1,'c':-2},
    'visible':False,
    'pointsVictoire':1, 
    }
majeursDict["M16"]={
    'cout':{'p':3,'a':1},
    'option':{'cuissonPain':{'c':4}},
    'visible':True,
    'pointsVictoire':3, 
    'devoile': "M17",
    }
majeursDict["M17"]={
    'cout':{'a':2,'p':1},
    'visible':False,
    'pointsVictoire':1, 
    }
majeursDict["M18"]={
    'cout':{'p':2,'b':2},
    'visible':True,
    'pointsVictoire':2, 
    'devoile': "M19",
    }
majeursDict["M19"]={
    'cout':{'p':1,'b':1},
    'visible':False,
    'pointsVictoire':2, 
    'option':{'echange':{'b':1,'a':-1}},
    }

majeursDict["M20"]={
    'cout':{'p':2,'a':2},
    'visible':True,
    'pointsVictoire':2, 
    'devoile': "M21",
    }
majeursDict["M21"]={
    'cout':{'p':1,'a':1},
    'visible':False,
    'pointsVictoire':2, 
    'option':{'echange':{'a':1,'b':-1}},
    }

majeursDict["M22"]={
    'cout':{'p':2,'r':2},
    'visible':True,
    'pointsVictoire':2, 
    'devoile': "M23",
    }
majeursDict["M23"]={
    'cout':{'p':1,'r':1},
    'visible':False,
    'pointsVictoire':2, 
    'option':{'echange':{}},
    }


mineursDict={}
# mineursDict["foyer simple"]={
#     'nom':'Foyer simple',
#     'description':"Vous pouvez transformer à tout moment...",
#     'cout':{'a':1},
#     'activer':cuisson,
#     'option':{'cuissonDict':{'l':2,'m':1,'s':2,'v':3},'cuissonPain':{'c':2}},    
#     'sansPion':True,
#     'possibilites':possibilitesCuisson,
#     }

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



    
