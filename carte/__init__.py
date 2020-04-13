import pygricola.util as util
import pygricola.fonctionsPlateau as fct
from pygricola.traduction import trad
import pygricola.carte.fonctionsCartes as fctCarte

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
            self._coutinit=cout  #on le garde en mémoire pour remettre le cout init quand on appelle vider

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
    
    def vider(self):
        self._cout=self._coutinit

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
        #si la condition est dict vide on appelle possibilitesNonVide qui est le défaut
        if self._condition=={}:
            reponse=fct.possibilitesNonVide(self.partie,self)     
        #si c'est un dico non vide
        elif type(self._condition)==dict:
            reponse=self._condition and fct.possibilitesNonVide(self.partie,self)  
        else:
            #sino on appelle la condition
            reponse= self._condition(self.partie,self)
        return reponse        
    #pour le cas de l'achat de foyer simple par ex:
    #il a une methode possibilite, mais on a pas envie de l'appeler quand on souhaite l'acheter
    #sans ça si on a rien pour cuire par ex, condition de foyer appelle posNovide qui est vide
    #alors qu'on voudrait quand même pouvoir l'acheter....
    @property   
    def conditionAchat(self):
        #si c'est un dico non vide
        if type(self._condition)==dict:
            reponse=self._condition
        else:
            #sino on appelle la condition
            reponse= self._condition(self.partie,self)
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
        if type(self._possibilites)==dict:
            return [] #on n'a pas de choix à faire
        elif type(self._possibilites)==list:
            return self._possibilites
        else:
            print("carte possibilites:",self.partie,self)
            return self._possibilites(self.partie,self)        


        
    def jouer(self):
        print("JOUER",self.uid,self.cout) 
        #on parcourt les cartes jouees de tout le monde 
        for jid,j in self.partie.joueurs.items():
            for cuid,c in j.cartesDevantSoi.items():
                if hasattr(c, 'hook'):
                    if c.hook != ():
                        if c.hook[0]==self.uid:
                            #si le hook est jouable
                            if c.hookStatus==0:
                                print("hook sur",self.uid,'avec',c.uid,c.hookStatus)
                                self.partie.uidSave=self.uid 
                                #si le hook me concerne
                                if(c.hook[1]=="s"):
                                    #si il y a plusieurs possibilites
                                    print(c)
                                    choixPossibles=c.possibilites()
                                    if len(choixPossibles)>1:
                                        self.partie.choixPossibles=choixPossibles
                                        self.partie.sujet=self
                                        print('IM HERE',choixPossibles)
                                        return (choixPossibles,c,True,"hook")
                                    else:
                                    #sinon
                                        c.effet(0,choixPossibles)
                                # a pour all
                                elif (c.hook[1]=="a"):
                                    ffff
                            else:
                                print("JOUER,HOOK UTILISE")               
        
        encore=True # on va encore pouvoir jouer après
        #on regarde si la carte a une fonction possibilite
        if not type(self._possibilites)==dict:
            choixPossibles=self._possibilites(self.partie,self)
            self.partie.choixPossibles=choixPossibles
            self.partie.sujet=self
            return (choixPossibles,self,encore,"")
        
        #on regarde si la carte a une option activable (genre epicier)
        elif self.uid=='s21':
            self.partie.messagesPrincipaux.append([self.partie.joueurQuiJoue().nom,"p20",self.uid])
            self.effet(0, [])
            return (-1,self.partie.joueurQuiJoue(),True,self.uid)
        else:
            print("JOUERB",self.uid,self.cout) 
            self.partie.messagesPrincipaux.append("{} {} {}".format(self.partie.joueurQuiJoue().nom,self.phraseJouer,self.uid))
            self.partie.joueurQuiJoue().mettreAJourLesRessources(self.cout,not self.sansPion)
            self.vider()
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


class SavoirFaire(Carte):

    def __init__(self,partie,uid,joueurMini,possibilites={},cout={},condition={},option={},effet={},hook=(),final=util.dummy):
        self.joueurMini=joueurMini
        self.hook=hook
        self.final=final
        self.owner=None
        self.hookStatus=0 #-1 pas jouable, 0 jouable, 
        super().__init__(partie,uid,possibilites,cout=cout,condition=condition,effet=effet,option=option)
        
    @property
    def display(self):
        return [self.uid]            
    
    def bonusRessources(self,rDict):
        gain=util.rVide()
        if 'bonusRessources' in self.option.keys():
            for r,number in rDict .items():
                #si j'ai un bonus sur la ressource et si j'en prend 1
                if r in self.option['bonusRessources' ].keys() and number<0:
                    gain=util.ajouter(gain,self.option['bonusRessources' ][r])
        elif 'bonusRessourcesStrict' in self.option.keys():
            #verif de controle
            if len(self.option['bonusRessourcesStrict' ].keys())>1:
                ERROR
            else:
                dicoStrict=self.option['bonusRessourcesStrict' ].copy()
                resUnique,bonus=dicoStrict.popitem()
                #on verifie que dans rDict il n'y a que resUnique qui est negatif
                appliquerBonus=True
                for r,number in rDict .items():
                    if r !=resUnique:
                        if number <0:
                            appliquerBonus=False
                    else:
                        #dans ce cas c'est pas un gain
                        if number>0:
                            appliquerBonus=False
                if appliquerBonus:
                    gain=util.ajouter(gain,bonus)         

                
        print('bonusRessources',gain)
        return util.inverser(gain)
    
    def effetInstantane(self):
        if "instant"  in self.option.keys():
            #si c'est un dico on traite ça comme un cout
            if type(self.option["instant"])==dict:
                print("#############effetInstantane",self.option["instant"])
                self.owner.mettreAJourLesRessources(self.option["instant"],actionDunePersonne=False)
            #utile quand on veut mettre les ressources sur le tour courant +XXX
            elif self.option["instant"]=='pileTourPlus':
                self.option['pileTour']={}
                for plus,dico in self.option['pileTourPlus'].items():
                    self.option['pileTour'][plus+self.partie.plateau['tour']]=dico
                
 
class Amenagement(Carte):

    def __init__(self,partie,uid,possibilites={},cout={},condition={},option={},effet={},sansPion=True,pointsVictoire=0,pointsSpeciaux=util.dummy):
        self.pointsVictoire=pointsVictoire
        self.pointsSpeciaux=pointsSpeciaux
        super().__init__(partie,uid,possibilites,cout=cout,condition=condition,effet=effet,option=option,sansPion=sansPion)
        
    @property
    def display(self):
        return [self.uid]            
 

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
        coutTot=util.ajouter(self._cout,cout)
        return coutTot.copy()
    
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
mineursDict["m0"]={
    'cout':{'a':1},
    'effet':cuisson,
    'option':{'cuissonDict':{'l':2,'m':1,'s':2,'v':3},'cuissonPain':{'c':2}},    
    'possibilites':possibilitesCuisson,
    'pointsVictoire':1,
    }
mineursDict["m1"]={
    'cout':{'a':2,'p':2},
    'effet':fctCarte.prendre,
    'option':{'n':-1},    
    'hook':'o_cuisson',
    'pointsVictoire':2, 
    }
mineursDict["m2"]={
    'cout':{'b':2},
    'animaux':"abreuvoir",
    'pointsVictoire':1, 
    }
mineursDict["m3"]={
    'condition':fctCarte.avoirXSavoirFaire,
    'hook':'debutTour',
    'effet':fctCarte.choixRessourceSurAction,
    'possibilites':fctCarte.possibilitesRessourceSurAction,
    'option':{'n':-1,'conditionSavoirFaire':3},  
    'nbUtil':5,
    'pointsVictoire':1, 
    }

mineursDict["m4"]={
    'cout':{'n':2},
    'condition':fctCarte.avoirXSavoirFaire,
    'hook':'s_finAction',
    'effet':fctCarte.sixiemeSens,
    'pointsVictoire':1, 
    'option':{'conditionSavoirFaire':1}, 
    }

mineursDict["m5"]={
    'cout':{'a':2},
    'hook':'final',
    'effet':fctCarte.final_access,
    'pointsVictoire':1, 
    }


mineursDict["m6"]={
    'cout':{'a':2,'b':1},
    'condition':fctCarte.avoirMoinsDeXCartesEnMain,
    'instant':{'n':-2},
    'option':{'conditionMoinsDeXCartesEnMain':4},
    'hook':'final',
    'effet':fctCarte.final_administration,
    }

mineursDict["m7"]={
    'cout':[{'b':1},{'a',1}],
    'instant':fctCarte.possibilitesOptions,
    'option':{'possibilitesOptions':[{'r':-1},{'p':-1}]}, 
    'effet':fctCarte.choixCout,
    'passableAGauche':True,
    }

mineursDict["m8"]={
    'hook':"s_construction_pierre",
    'effet':fctCarte.aiguilleRoche,
    }

mineursDict["m9"]={
    'condition':fctCarte.avoirXSavoirFaire,
    'passableAGauche':True,
    'instant':fctCarte.choixNaissanceOUPremier,
    'option':{'conditionSavoirFaire':2}, 
    }

mineursDict["m10"]={
    'cout':{'p':1},
    'animaux':"abreuvoirChevaux",
    }

savoirFaireDict={}
savoirFaireDict["s0"]={
    'joueurMini':4,
    'hook':'debutTour',
    'effet':fctCarte.prendreSiTourEgal,
    'option':{'prendreSiTourEgal':{7:{'n':1,"m":-1},10:{'n':1,"s":-1},14:{'n':1,"b":-1}}}
    }
savoirFaireDict["s1"]={
    'joueurMini':3,
    'hook':'o_firstTimePrendsBois',
    'effet':fctCarte.choixAchat,
    'option':{'n':1,"b":-1},
    'recharge':'tour'
    }
savoirFaireDict["s2"]={
    'joueurMini':4,
    'hook':'o_firstTimePrendsPierre',
    'effet':fctCarte.choixAchat,
    'option':{'n':1,"p":-1,'victime':{'n':-1}},
    'recharge':'tour'
    }
savoirFaireDict["s3"]={
    'joueurMini':4,
    'hook':'o_firstTimePrendsRoseau',
    'effet':fctCarte.choixAchat,
    'option':{'n':1,"r":-1,'victime':{'n':-1}},
    'recharge':'tour'
    }

savoirFaireDict["s4"]={
    'joueurMini':4,
    'hook':'s_spectacle',
    'effet':fctCarte.acrobate,
    }

savoirFaireDict["s5"]={
    'joueurMini':1,
    'final':fctCarte.final_actrice,
    }

savoirFaireDict["s6"]={
    'joueurMini':3,
    'hook':('a1','a','p'),
    'possibilites':fctCarte.possibilitesOptions,
    'option':{'possibilitesOptions':[{'c':-1},{'b':-1},{'a':-1},{'r':-1},{'m':-1}]}, 
    'effet':fctCarte.depiler,    
    }

savoirFaireDict["s7"]={
    'joueurMini':3,
    'hook':['debutTour','finTour'],
    'effet':fctCarte.agrarien,
    'option':{'c':-1,'b':-1,'a':-1,'r':-1,'m':-1}
    }
savoirFaireDict["s8"]={
    'joueurMini':4,
    'hook':('a5','s','t'),
    'effet':fctCarte.choixCout,
    'possibilites':['l'],
    'option':{'choixCout':{'l':{'l':-1}}}, 
    }
savoirFaireDict["s9"]={
    'joueurMini':3,
    'hook':'recolte_finchamps',
    'effet':fctCarte.aideMoissonneur,
    }
savoirFaireDict["s10"]={
    'joueurMini':1,
    'hook':('a5','s','t'),
    'effet':fctCarte.choixCout,
    'possibilites':fctCarte.possibilitesSaisonier,
    'option':{'choixCout':{'c':{'c':-1},'l':{'l':-1}}}, 
    }
savoirFaireDict["s11"]={
    'joueurMini':3,
    'hook':('a2','s','p'), #p comme personnage on réinit à chaque fin de personnage
    'effet':fctCarte.choixCout,
    'possibilites':['l'],
    'option':{'choixCout':{'l':{'l':-1}}}, 
    }
savoirFaireDict["s12"]={
    'joueurMini':1,
    'hook':('ressourcesActionPersonne','s','p'), #p comme personnage on réinit à chaque fin de personnage
    'option':{'bonusRessources':{'a':{'a':-1},'b':{'a':-1}}}, 
    }
savoirFaireDict["s13"]={
    'joueurMini':3,
    'hook':('a17','s','p'), #p comme personnage on réinit à chaque fin de personnage
    'option':{    'instant':{'l':-1}
                 ,'choixCout':{'l':{'c':-1}}}, 
    'effet':fctCarte.choixCout,
    'possibilites':['l'],
    }
savoirFaireDict["s14"]={
    'joueurMini':3,
    'hook':('ressourcesActionPersonne','s','p'), #p comme personnage on réinit à chaque fin de personnage
    'option':{'bonusRessources':{'b':{'n':-1}}}, 

    }
savoirFaireDict["s15"]={
    'joueurMini':1,
    'hook':('ressourcesActionPersonne','s','p'), #p comme personnage on réinit à chaque fin de personnage
    'option':{'bonusRessourcesStrict':{'a':{'a':-2}}}, 
    }
savoirFaireDict["s16"]={
    'joueurMini':1,
    'hook':('ressourcesActionPersonne','s','p'), #p comme personnage on réinit à chaque fin de personnage
    'option':{'bonusRessources':{'b':{'b':-1}}}, 
    }
savoirFaireDict["s17"]={
    'joueurMini':3,
    'hook':('debutTour','s','p'), #p comme personnage on réinit à chaque fin de personnage
    'option':{'pile':[{'r':-1},{'r':-1},{'r':-1},{'r':-1}]}, 
    'effet':fctCarte.depiler,
    }
savoirFaireDict["s18"]={
    'joueurMini':1,
    'hook':('debutTour','s','p'), #p comme personnage on réinit à chaque fin de personnage
    'option':{'pile':[{'b':-1},{'b':-1},{'b':-1},{'b':-1},{'b':-1}]}, 
    'effet':fctCarte.depiler,
    }

savoirFaireDict["s19"]={
    'joueurMini':1,
    'hook':('debutTour','s','p'), #p comme personnage on réinit à chaque fin de personnage
    'option':{'pileTour':{8:{'b':-1},9:{'b':-1},10:{'b':-1},11:{'b':-1},12:{'b':-1},
                          13:{'b':-1},14:{'b':-1}}}, 
    'effet':fctCarte.depiler,
    }
savoirFaireDict["s20"]={
    'joueurMini':1,
    'hook':('debutTour','s','p'), #p comme personnage on réinit à chaque fin de personnage
    'option':{'pileTour':{8:{'a':-1},9:{'a':-1},10:{'a':-1},11:{'a':-1},12:{'a':-1},
                          13:{'a':-1},14:{'a':-1}}}, 
    'effet':fctCarte.depiler,
    }

savoirFaireDict["s21"]={
    'joueurMini':1,
    'option':{'pile':[{'l':-1,'n':1},{'r':-1,'n':1},{'a':-1,'n':1},
                      {'b':-1,'n':1},{'l':-1,'n':1},{'p':-1,'n':1},
                      {'c':-1,'n':1},{'r':-1,'n':1}]}, 
    'effet':fctCarte.depiler,
    'condition':fctCarte.conditionEpicier
    }

savoirFaireDict["s22"]={
    'joueurMini':1,
    }

savoirFaireDict["s23"]={
    'joueurMini':1,
    'hook':('a2','s','t'),
    'effet':fctCarte.gardeChampetre,
    'possibilites':fctCarte.possibilitesGardeChampetre,
    }

savoirFaireDict["s24"]={
    'joueurMini':4,
    'hook':('debutTour','s','p'), #p comme personnage on réinit à chaque fin de personnage
    'option':{'pileTourPlus':{5:{'v':-1},9:{'v':-1}},'instant':'pileTourPlus'}, 
    'effet':fctCarte.depiler,
    }

savoirFaireDict["s25"]={
    'joueurMini':4,
    'hook':('debutTour','s','p'), #p comme personnage on réinit à chaque fin de personnage
    'option':{'pileTourPlus':{4:{'m':-1},7:{'m':-1},9:{'m':-1},11:{'m':-1}},'instant':'pileTourPlus'}, 
    'effet':fctCarte.depiler,
    }

savoirFaireDict["s26"]={
    'joueurMini':4,
    'hook':('debutTour','s','p'), #p comme personnage on réinit à chaque fin de personnage
    'option':{'pileTourPlus':{4:{'s':-1},7:{'s':-1},10:{'s':-1}},'instant':'pileTourPlus'}, 
    'effet':fctCarte.depiler,
    }

savoirFaireDict["s27"]={
    'joueurMini':4,
    'hook':('a28','s','t'), #il manque l'autre spectacle, jouable à 4 joeurs seulement
    'effet':fctCarte.choixCout,
    'possibilites':['c'],
    'option':{'choixCout':{'c':{'c':-1}}}, 
    }

savoirFaireDict["s28"]={
    'joueurMini':3,
    'hook':('a2','s','t'),
    'effet':fctCarte.bonimenteur,
    'possibilites':fctCarte.possibilitesBonimenteur,
    }



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



    
