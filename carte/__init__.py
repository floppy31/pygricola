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
    for res in ['l','m','s','v','h']:
        if (partie.joueurQuiJoue().ressources[res]>0):
            possibilites.append(Carte(partie,"u"+res,cout={res:1,'n':-dictCuisson[res]},sansPion=True))  
    if not Fake:
        partie.phraseChoixPossibles="Que voulez vous cuire? :"
        partie.sujet=carte
    return possibilites       

     
def cuisson(partie,choix,possibilites,carte):
    #on recupere le dict cuisson dans option
    dictCuisson=carte.option['cuissonDict']
    print('cuissonDBG',choix,possibilites,carte,possibilites[choix])
    possibilites[choix].jouer()
    return (-1,carte,True,"")
##################################################################################          




class Carte:

    def __init__(self,partie,uid,possibilites={},cout={},condition={},effet={},option={},sansPion=False):
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
        self._effet=effet
        self._possibilites=possibilites
        self.sansPion=sansPion
        self.phraseJouer='joue :'
        self.occupants=[]
#        super().__init__()
    
    def __str__(self):
           return self.uid


#     @property   
#     def nom(self):
# #        return self.nomTrad('fr')
#         return self.uid

    
    def nomTrad(self,lang):
        return trad[self.uid][lang][0]
       
    def descTrad(self,lang):
        return trad[self.uid][lang][1]
                    
#     @property   
#     def short(self):
#         return self.nom[0:7]
    
    @property   
    def cout(self):
        if type(self._cout)==dict:
            return self._cout
        else:
            return self._cout(self.partie)
    
    @property   
    def condition(self):
        print('carte condition')
        #si la condition est dict vide on appelle possibilitesNonVide qui est le défaut
        if self._condition=={}:
            print('carte conditionA')
            reponse=fct.possibilitesNonVide(self.partie,self)     
        #si c'est un dico non vide
        elif type(self._condition)==dict:
            print('carte conditionB')
            reponse=self._condition and fct.possibilitesNonVide(self.partie,self)  
        else:
            #sino on appelle la condition
            print('carte conditionC')
            reponse= self._condition(self.partie,self)
        print("reponse",reponse)
        return reponse        
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
            return self._possibilites(self.partie,self)        

        
    def jouer(self):
        encore=True # on va encore pouvoir jouer après
        #on regarde si la carte a une fonction possibilite
        if not type(self._possibilites)==dict:
            print("jouerDBG1")
            choixPossibles=self._possibilites(self.partie,self)
            self.partie.choixPossibles=choixPossibles
            self.sujet=self
            return (choixPossibles,self,encore,"")
        else:
            print("jouerDBG2",self.uid)
            self.partie.messagesPrincipaux.append("{} {} {}".format(self.partie.joueurQuiJoue().nom,self.phraseJouer,self.uid))
            self.partie.joueurQuiJoue().mettreAJourLesRessources(self.cout)
            self._cout=util.rVide()
            if self.sansPion==True:
                if isinstance(self,ActionSpeciale):
                    #ici passe foire du travail
                    
                    self.carteQuiMePorte.changerEtat(self.partie.quiJoue)
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
        print('titi',perso.localisationInit,self.partie.joueurQuiJoue().courDeFerme.etat[perso.localisationInit])
        print('titi',self.partie.joueurQuiJoue().courDeFerme.etat[perso.localisationInit].occupants)

        self.partie.joueurQuiJoue().courDeFerme.etat[perso.localisationInit].occupants.pop()
        perso.localisation=self
        self.occupants.append(perso)
        self.libre=False
            
    def printCout(self):
        return str(self.cout)
    
    def save(self):
        return {'uid':self.uid}
    
def loadCarte(stri,partie):
    print('loadCarte',stri)
    pass
        
        
def byPassNaissance():
    pass

def avoirXChamp(type,x):
    pass

def avoirXSavoirFaire(type,x):
    pass


class Amenagement(Carte):

    def __init__(self,partie,uid,possibilites={},cout={},condition={},option={},effet={},sansPion=True,pointsVictoire=0,pointsSpeciaux=util.dummy):
        self.pointsVictoire=pointsVictoire
        self.pointsSpeciaux=pointsSpeciaux
        super().__init__(partie,uid,possibilites,cout=cout,condition=condition,effet=effet,option=option,sansPion=sansPion)
        
    @property
    def display(self):
        return ["p5",self.uid]            
 

class AmenagementMineur(Amenagement):

    def __init__(self,partie,uid,possibilites={},cout={},condition={},option={},effet={},passableAGauche=False,sansPion=True,pointsVictoire=0,pointsSpeciaux=util.dummy):
        self.passableAGauche=passableAGauche
        super().__init__(partie,uid,possibilites=possibilites,cout=cout,condition=condition,effet=effet,option=option,sansPion=sansPion,pointsVictoire=pointsVictoire,pointsSpeciaux=pointsSpeciaux)

class AmenagementMajeur(Amenagement):

    def __init__(self,partie,uid,possibilites={},cout={},condition={},effet={},option={},visible=False,devoile=None,sansPion=True,pointsVictoire=0,pointsSpeciaux=util.dummy):
        self.visible=visible
        self.devoile=devoile
        super().__init__(partie,uid,possibilites=possibilites,cout=cout,condition=condition,effet=effet,option=option,sansPion=sansPion,pointsVictoire=pointsVictoire,pointsSpeciaux=pointsSpeciaux)




class CarteActionSpeciale(Carte):
 
    def __init__(self,partie,uid):
        self.etat=-2 #-2 dispo, sinon numero du joueur qui l'a pris, -1 plus dispo
        self.listeActionSpeciale=[]
        super().__init__(partie,uid)
    
    def listAs(self):
        list=["p4"]
        for l in self.listeActionSpeciale:
            list.append(l.uid)
        return list
    
    def changerEtat(self,nouveau):
        #si l'ancien etat etait positif ou nul alors je mets -1 (fini)
        if self.etat>-1:
            self.etat=-1
            print("AS: ",self.uid,"changement d'etat:",self.etat,"-->",-1)
        else:
            print("AS: ",self.uid,"changement d'etat:",self.etat,"-->",nouveau)
            self.etat=nouveau
        
    
class ActionSpeciale(Carte):
    def __init__(self,partie,uid,carteQuiMePorte,cout={},effet={},possibilites={}):
        self.carteQuiMePorte=carteQuiMePorte
        super().__init__(partie,uid,cout=cout,effet=effet,sansPion=True,possibilites=possibilites)    
            
    @property   
    def cout(self):
        cout={'n':0}
        #carte dispo
        if self.carteQuiMePorte.etat==-2:
            pass
        #carte prise par un autre
        elif self.carteQuiMePorte.etat!=self.partie.quiJoue:
            cout['n']+=2
        elif self.carteQuiMePorte.etat==self.partie.quiJoue:
            jelaiprisemoi
        else:
            impossible
        print('cout actionspe dbg',self.carteQuiMePorte.etat,self._cout,cout)
        coutTot=util.ajouter(self._cout,cout)
        return coutTot
    
    @property
    def display(self):
        if self.carteQuiMePorte.etat==-2:
            return ["p4",self.uid]
        elif self.carteQuiMePorte.etat>-1:
            return ["p6",self.uid,"(","p7",")"]
        else:
            return "CAS IMPOSSIBLE ".format(self.uid)        

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
    'effet':cuisson,
    "possibilites":possibilitesCuisson,
    'option':{'cuissonDict':{'l':2,'m':2,'s':2,'v':3},'cuissonPain':{'c':2}},
    'visible':True,
    'devoile': "M2",   
    'pointsVictoire':1,
    }
majeursDict["M1"]={
    'cout':{'a':3},
    'effet':cuisson ,
    "possibilites":possibilitesCuisson,
    'option':{'cuissonDict':{'l':2,'m':2,'s':2,'v':3},'cuissonPain':{'c':2}},
    'visible':True,
    'devoile': "M3",     
    'pointsVictoire':1, 
    }

majeursDict["M2"]={
    'cout':{'a':1,'p':1},
    'effet':cuisson ,
    "possibilites":possibilitesCuisson,    
    'option':{'cuissonDict':{'l':1,'m':1,'s':1,'v':2,'h':1}},
    'visible':False,
    'pointsVictoire':2,     
    }
majeursDict["M3"]={
    'cout':{'a':1,'p':1},
    'effet':cuisson ,
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
    'effet':cuisson ,
    "possibilites":possibilitesCuisson,
    'option':{'cuissonDict':{'l':3,'m':2,'s':3,'v':4},'cuissonPain':{'c':3}},
    'visible':True,
    'devoile': "M9",     
    'pointsVictoire':1, 
    }
majeursDict["M9"]={
    'cout':{'a':5},
    'effet':cuisson ,
    "possibilites":possibilitesCuisson,
    'option':{'cuissonDict':{'l':3,'m':2,'s':3,'v':4},'cuissonPain':{'c':3}},
    'visible':True,
    'devoile': "M10",     
    'pointsVictoire':1, 
    }
majeursDict["M10"]={
    'cout':{'a':6},
    'effet':cuisson ,
    "possibilites":possibilitesCuisson,
    'option':{'cuissonDict':{'l':3,'m':2,'s':3,'v':4},'cuissonPain':{'c':3}},
    'visible':False,
    'pointsVictoire':2, 
    }
majeursDict["M11"]={
    'cout':{'a':6},
    'effet':cuisson ,
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
#     'effet':cuisson,
#     'option':{'cuissonDict':{'l':2,'m':1,'s':2,'v':3},'cuissonPain':{'c':2}},    
#     'sansPion':True,
#     'possibilites':possibilitesCuisson,
#     }

savoirFaireDict={}

utilitaireDict={}
utilitaireDict["c0"]={
    'cout':{'c':1,'n':-1},
    'sansPion':True
    }

utilitaireDict["c1"]={
    'cout':{'l':1,'n':-1},
    'sansPion':True
    }


deck={
    'mineurs':mineursDict,
    'majeurs':majeursDict,
    'savoirFaires':savoirFaireDict,
    'utilitaire':utilitaireDict
    }



    
