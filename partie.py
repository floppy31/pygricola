from pygricola.joueur import Joueur ,loadJoueur


from pygricola.carte import deck,loadCarte,genererActionsSpeciales,AmenagementMajeur,CarteAction,CaseAppro
import pygricola.fonctionsPlateau as fct
from pygricola.traduction import trad

import pygricola.util as util
import json




example={
    0:('Romain','blue',1212),
    1:('Daniel','yellow',1345),
    2:('Gauthier','red',5434),
    3:('Damien','green',3432),
    4:('Anouck','violet',8990),
      }

recoltes=[4,7,9,11,13,14]


        
    
def cloture(partie):
    aTermine = False
    ferme=partie.joueurs[partie.quiJoue].courDeFerme
    ferme.paturages.aCloture=False
    while aTermine == False:
        print(ferme.prettyPrint())
        possibilites=['Construire un nouveau paturage', 'Diviser un paturage existant', 'Terminer l action']
        choix=util.printPossibilities(partie,"Que voulez vous faire? :",possibilites)
        if (choix == 2): 
            if ferme.paturages.aCloture==True:   
                aTermine = True
                print("Fin de l action Cloture")
            else:
                print('Vous n avez pas cloture, action invalide')
        if choix == 0:
            ferme.paturages.construireUnPaturage()

        if choix == 1:
            ferme.paturages.diviserUnPaturage()

        
def jePeuxRenover(partie, carte ):
    joueur=partie.joueurs[partie.quiJoue]
    ferme=joueur.courDeFerme   
    typeMaison=ferme.enQuoiEstLaMaison()
    nbMaison=ferme.compter('maison')
    cout={'r':1,typeMaison:nbMaison}
    return joueur.jePeuxJouer(cout)

def renoPuisMajeur(partie):
    pass

def labourageSemaille(partie):
    pass

def naissanceSansPieceLibre(partie):
    pass

def renoPuisCloture(partie):
    pass

# def avancer2(p,id):
#     logger=p.log
#     logger.debug('--------simulerPartie: {} {}'.format(id,p.sujet))
#     p.sujet.effet(p.choixPossibles.index(id),p.choixPossibles)
# 
#     if p.choixPossibles==-2:
#         comptStop=3
#         while p.choixPossibles==-2 and comptStop>0:
#             
#             print('---------------SIMULERDBG1:',comptStop,p.sujet,p.sujetSauvegarde,id,p.choixPossibles)
#             p.sujet.jouer()
#             comptStop=comptStop-1       
#                 
#             print('---------------SIMULERDBG2',id,p.sujet,p.sujetSauvegarde)
#     
#     if p.choixPossibles==-1:
#         suivant=p.joueurSuivant()
#         p.initChoix()
#         if suivant==-1:
#             logger.debug('--------simulerPartie: fin du tour')
#             p.finDuTour()
#             
           

def avancer(p,id):
    log=p.log
    log.debug('avancer {}'.format(id)) 
    #on ne traite les hook que si il n'y a pas d'autre choix à faire
    if len(p.hooks)>0:
        hookResolu,typeResolu=p.hooks.pop()
        p.pointerSurHook(hookResolu)
        log.debug('traitement du hook \n {}'.format(p.pointeur)) 
        
        
        p.pointeur.sujet.effet(p.choixPossibles.index(id),p.choixPossibles)
#         hookResolu,typeResolu=p.hooks.pop()
        hookASuivre,typeASuivre=p.pointerDernierHook()
        log.debug('hook traité: a suivre: {}'.format(hookASuivre)) 
        if hookASuivre==False:
            if typeResolu=='debutTour':
                p.pointerSurPremier()
                return p.pointeur
            elif typeResolu=='finTour':
                return p.recolteOuDemmarageTour()
                ffff
            elif typeResolu=='instant':
                return p.suivantOuEncore()
            else:
                return p.suivantOuEncore()
        else:
            return hookASuivre
    
    #quand on arrive ici on a un nouvelle iterraction id
    if type(p.choixPossibles)==list:
        if len(p.choixPossibles)<2:
            log.debug('avancer: TODO!!!!')
        log.debug('jouerUid')    
        p.jouerUid(id)
    elif(p.choixPossibles=='inputtext'):
        log.debug('inputtext')
        p.sujet.effet(id,[])
    #on doit traiter un hook interractif    
#     elif(p.choixPossibles=='hook'):
#         hook=p.traiterUnHook()
#         p.changerPointeur(hook.possibilities,hook.sujet,doitRepondre=hook.joueur)
#         p.sujet.effet(p.choixPossibles.index(id),p.choixPossibles)
    else:
        print(p.choixPossibles)
        ee
    #a cet endroit là s'il y a des hook interractifs, il sont dans la partie
    log.debug('fini de jouer le coup, possibilites: {}'.format(p.choixPossibles))
    hook,t=p.pointerDernierHook()
    if hook==False:        
        log.debug('pas de hooks')
        #le joueur joue encore?
        #si non
        if p.choixPossibles==-1:
            p.suivantOuEncore()
            return p.pointeur

        else:
            log.debug('{} doit refaire un choix'.format(p.pointeur.djangoJoueur))
            return p.pointeur
    else:
        log.debug('hook prêt')
        return hook

        


class Pointeur(object):
    def __init__(self,sujet,possibilites,djangoJoueur,phrase="p0",alert=""):
        self.sujet=sujet
        self.possibilites=possibilites
        self.djangoJoueur=djangoJoueur
        self.phrase=phrase
        self.alert=alert
        self.jouerEgalEffet=False
    
    def __str__(self):
        stri="sujet:{}\njoueur:{}\nphrase {}\npossibilites:{}".format(self.sujet,self.djangoJoueur,self.phrase,self.possibilites)
        return stri    
    def save(self):
        dico={'sujet':self.sujet.uid if hasattr(self.sujet, "uid")  else self.sujet,
                'djangoJoueur':self.djangoJoueur,
                'phrase':self.phrase,
                'alert':self.alert}
        uidList=[]
        for pos in self.possibilites:
            if hasattr(pos, 'uid'):
                uidList.append(pos.uid)
            else:
                uidList.append(pos)
        dico['possibilites']=uidList
        return dico


class Partie(object):
    
    def __init__(self,logger):
        self._offset=16
        self.plateau = dict()
        self.joueurs = dict()
        self.quiJoue=0
        self.nombreJoueurs=0
        self.premierJoueur=0
        self.quiAFini=[]
        self.messagesPrincipaux=[]

        self.messagesDetail=[] #pour debug
        self.log=logger
        
#         self.choixPossibles=-1 #on garde ça en memoire
#         self.phraseChoixPossibles="" #on garde ça en memoire
#         self.sujet="" #on garde ça en memoire
#         self.sujetSauvegarde="" #on garde ça en memoire
#         self.uidSave="" #on garde ça en melogging.DEBUGumoire pour les hook        
#         self.doitRepondre=self
        self.pointeur=Pointeur("","","","","")
        self.alert=""
        self.hooks=[]
        self.listeCoupsJoues=[]


    @property
    def choixPossibles(self):
        return self.pointeur.possibilites
    @property
    def sujet(self):
        return self.pointeur.sujet
    #choixPossible ==-1 on va à la suite
    #choixPossible ==-2 on boucle sur les hooks
    #choixPossible ==liste non vide : on a un choix à faire
    #sujet est la methode qui doit appeler effet ensuite
    #doitRepondre est le joueur qui doit répondre à la question
    def changerPointeurs(self,possibilites,sujet,phrase="p0",djangoJoueur=None,alert=None,Fake=False,jouerEgalEffet=False):
        
        if type(possibilites)==int or type(possibilites)==str:
            self.pointeur.possibilites=possibilites
        else:
            self.pointeur.possibilites=possibilites.copy()
        self.pointeur.jouerEgalEffet=jouerEgalEffet
        #si c'est Fake on ne change pas les autres
        if not Fake:
            self.pointeur.djangoJoueur=djangoJoueur
            #si on specifie un sujet, on le change
            if sujet:
                self.pointeur.sujet=sujet

            self.pointeur.phrase=phrase
            self.pointeur.alert=alert
            self.log.debug("changement de pointeurs {}".format(self.pointeur))
    
    def suivantOuEncore(self):
        #c'est finit on passe au suivant
        suivant=self.pointerSurJoueurSuivant()
        if suivant==-1:
            self.log.debug('--------simulerPartie: fin du tour')
            self.finDuTour()
            self.hooks=self.recolterLesHooksInterractifs('finTour')            
            hook,t=self.pointerDernierHook()
            if hook==False:
                self.recolteOuDemmarageTour()
                return self.pointeur
            else:           
                return hook
        else:
            return self.pointeur     
        
               
    def recolteOuDemmarageTour(self):
        self.log.debug("recolteOuDemmarageTour !!!!!!!!!!!!")
        if False:
            recolte
        else:
            self.demarrageTour()
            self.hooks=self.recolterLesHooksInterractifs('debutTour')
            hook,t=self.pointerDernierHook()
            if hook==False:
                self.pointerSurPremier()
                return self.pointeur
            else:
                return hook
    
    def pointerSurHook(self,hook):
        self.pointeur=hook


    def recolterLesHooksInterractifs(self,typeHook,opts={}):
        hooks=[]
        self.log.debug("parcourirLesHooks !!!!!!!!!!!!")
        for jid,j in self.joueurs.items():
            
            for cuid,c in j.cartesDevantSoi.items():
                if hasattr(c, 'hook'):
                    if c.hook != ():
                        self.log.debug("{} {} {}".format(c.uid,'a un hook',c.hook[0]))
                        if c.hook[0]==typeHook:
                            #si le hook est jouable
                            if c.hookStatus==0:
                                #si le hook me concerne
                                if(c.hook[1]=="s"):
                                    #si il y a plusieurs possibilites
                                    if hasattr(c._possibilites, '__call__'):
                                        c.possibilites(Fake=False)
                                        #partie.choixPossibles
                                        #soit une liste soit un int
                                        if self.choixPossibles==-1:
                                            self.log.debug("parcourirLesHooks fait une action automatique")
                                            c.effet(0,self.choixPossibles)
                                        elif type(self.choixPossibles)==list:
                                            if len(self.choixPossibles)>1:
                                                self.log.debug("parcourirLesHooks demande un choix utilisateur {} {}".format(c.uid,c.hookStatus))
                                                hooks.append((Pointeur(c,self.choixPossibles,c.owner.djangoUid),typeHook))
                                            else:
                                            #sinon
                                                self.log.debug("parcourirLesHooks fait une action automatique car un seul choix")
                                                c.effet(0,self.choixPossibles)
                                        else: 
                                            UNKNOWN
                                    else:
                                        self.log.debug("hook recherche ses possibilites")
                                        if len(c._possibilites)==0:
                                            if 'bonusRessources' in c.option.keys() or 'bonusRessourcesStrict' in c.option.keys():
                                                c.bonusRessources(opts['ressources'])
                                            else:
                                                c.effet(0,c._possibilites)
                                        elif len(c._possibilites)==1:
                                            c.effet(0,c._possibilites)
                                        else:
                                            self.log.debug("parcourirLesHooks demande un choix utilisateur {} {}".format(c.uid,c.hookStatus))
                                            hooks.append((Pointeur(c,c._possibilites,c.owner.djangoUid),typeHook))
                                elif (c.hook[1]=="o"):    
                                    if self.joueurQuiJoue()==c.owner:
                                        pass
                                    else:
                                        c.effet(0,c._possibilites)
                                        
                            else:
                                self.log.debug("parcourirLesHooks: hook déjà consomé",c.uid,c.hookStatus) 
         
        return  hooks        

    #je separe la fonction d'init... a cause de save/load
    #on a besoin de creer un objet partie sans tout réinitialiser
    def initialiser(self,nombreJoueurs):   

        self.log.info('initialiser {} joueurs'.format(nombreJoueurs))
        self.nombreJoueurs=nombreJoueurs
        self._initJoueurs()        
        self.initOrdre()
        (positionTourbes,positionForets)=self.genererCourDeferme()
        self.faireCourDeferme(positionTourbes,positionForets)      
        self.draft()
        self.actionSurTours=self.faireActionSurTours()
        self._genererPlateau(nombreJoueurs)    
            
        
    def _initJoueurs(self):
        self.log.debug('_initJoueurs')
        bonusNourriture=[0,1,1,1,2]
        for j in range(self.nombreJoueurs):

            (n,c,duid)=example[j]
            self.joueurs[j]=Joueur(partie=self,id=j,nom=n,couleur=c,djangoUid=duid)
            self.joueurs[j].ressources['n']+=bonusNourriture[j]

        
    def _genererPlateau(self,nombre):
        self.log.debug('_genererPlateau')
        self.plateau["cases"]=dict()
        self.plateau["actionsSpeciales"]=dict()
        self.plateau["tour"]=1
        self.plateau["actionsSpeciales"]=genererActionsSpeciales(self)
        if nombre==2 or nombre==1:
            self.plateau["cases"][1]=CarteAction(self,"a40",visible=False)
            self.plateau["cases"][2]=CarteAction(self,"a40",visible=False)
            self.plateau["cases"][3]=CarteAction(self,"a40",visible=False)
            self.plateau["cases"][4]=CarteAction(self,"a40",visible=False)
            self.plateau["cases"][5]=CarteAction(self,"a40",visible=False)
            self.plateau["cases"][6]=CarteAction(self,"a40",visible=False)        
        elif nombre ==3:
            self.plateau["cases"][1]=CarteAction(self,"a40",visible=False)
            self.plateau["cases"][2]=CarteAction(self,"a40",visible=False)
            self.plateau["cases"][3]=CaseAppro(self,"a24",appro={'a':-1},cout={},visible=True)
            self.plateau["cases"][4]=CaseAppro(self,"a25",appro={'b':-2},cout={},visible=True)
            self.plateau["cases"][5]=CarteAction(self,"a26",possibilites=fct.possibiliteRoseauPnOuPierrePn,effet=fct.roseauPnOuPierrePn,visible=True)
            self.plateau["cases"][6]=CarteAction(self,"a27",cout={'n':2},visible=True)       
        elif nombre==4:
            self.plateau["cases"][1]=CaseAppro(self,"a28",appro={'n':-1},cout={},visible=True)
            self.plateau["cases"][2]=CarteAction(self,"a29",cout=fct.coutSavoirFaire2,possibilites=fct.possibilitesSavoirFaire,effet=fct.choixSavoirFaire,visible=True)
            self.plateau["cases"][3]=CaseAppro(self,"a30",appro={'a':-2},cout={},visible=True)
            self.plateau["cases"][4]=CaseAppro(self,"a31",appro={'b':-2},cout={},visible=True)
            self.plateau["cases"][5]=CaseAppro(self,"a32",appro={'b':-1},cout={},visible=True)
            self.plateau["cases"][6]=CarteAction(self,"a33",cout={'n':-1,'p':-1,'r':-1},visible=True)
        elif nombre ==5:
            self.plateau["cases"][1]=CaseAppro(self,"a34",appro={'n':-1},cout={},possibilites=fct.possibiliteConstructionOuSpectacle,effet=fct.constructionOuSpectacle,visible=True)
            self.plateau["cases"][2]=CarteAction(self,"a35",condition=fct.jePeuxJouerSavoirFaireOuNaissance,possibilites=fct.possibiliteSavoiFaireOuNaissance,effet=fct.savoiFaireOuNaissance,visible=True)
            self.plateau["cases"][3]=CaseAppro(self,"a36",appro={'a':-3},cout={},visible=True)
            self.plateau["cases"][4]=CaseAppro(self,"a37",appro={'b':-4},cout={},visible=True)
            self.plateau["cases"][5]=CarteAction(self,"a38",visible=True,possibilites=fct.possibiliteBetail,effet=fct.betail)
            self.plateau["cases"][6]=CaseAppro(self,"a39",appro={'r':-1},cout={'b':-1,'p':-1},visible=True)        #il y a 30 case
        #6 1eres sont celles qui dependent du nombre de joueur
        #

        self.plateau["cases"][7]=CarteAction(self,"a0",visible=True,condition=fct.jePeuxFaireConstructionDePieceEtOuEtable,effet=fct.planConstructionDePieceEtOuEtable,possibilites=fct.demanderPlanConstructionDePieceEtOuEtable)
        self.plateau["cases"][8]=CarteAction(self,"a1",visible=True,possibilites=fct.possibilitesAmenagementMineur,effet=fct.choixAmenagementMineur)
        self.plateau["cases"][9]=CarteAction(self,"a2",cout={'c':-1},visible=True)
        self.plateau["cases"][10]=CarteAction(self,"a3",visible=True,effet=fct.labourage,possibilites=fct.possibilitesLabourage)
        self.plateau["cases"][11]=CarteAction(self,"a4",cout=fct.coutSavoirFaire1,possibilites=fct.possibilitesSavoirFaire,effet=fct.choixSavoirFaire,visible=True)
        self.plateau["cases"][12]=CarteAction(self,"a5",cout={'n':-2},visible=True)
        self.plateau["cases"][13]=CaseAppro(self,"a6",appro={'b':-3},cout={},visible=True)
        self.plateau["cases"][14]=CaseAppro(self,"a7",appro={'a':-1},cout={},visible=True)
        self.plateau["cases"][15]=CaseAppro(self,"a8",appro={'r':-1},cout={},visible=True)
        self.plateau["cases"][16]=CaseAppro(self,"a9",appro={'n':-1},cout={},visible=True)
        self.plateau["cases"][17]=self.actionSurTours[1]
        self.plateau["cases"][18]=self.actionSurTours[2]
        self.plateau["cases"][19]=self.actionSurTours[3]
        self.plateau["cases"][20]=self.actionSurTours[4]
        self.plateau["cases"][21]=self.actionSurTours[5]
        self.plateau["cases"][22]=self.actionSurTours[6]
        self.plateau["cases"][23]=self.actionSurTours[7]
        self.plateau["cases"][24]=self.actionSurTours[8]
        self.plateau["cases"][25]=self.actionSurTours[9]
        self.plateau["cases"][26]=self.actionSurTours[10]
        self.plateau["cases"][27]=self.actionSurTours[11]
        self.plateau["cases"][28]=self.actionSurTours[12]
        self.plateau["cases"][29]=self.actionSurTours[13]
        self.plateau["cases"][30]=self.actionSurTours[14]
        
        
        self.plateau["majeurs"]=dict()
        for uid,v in deck['majeurs'].items():
            self.plateau["majeurs"][uid]=AmenagementMajeur(self,uid,**v)
                    
    #jouer par rapport à un uid et pas un indice
    def jouerUid(self,uid):
        self.listeCoupsJoues.append(uid)
        rienFait=True
        for c in self.choixPossibles:
            if hasattr(c, 'uid'):
                if c.uid==uid:
                    c.jouer()
                    rienFait=False
            else:
                if c==uid:
                    self.sujet.effet(self.choixPossibles.index(uid),self.choixPossibles)
                    rienFait=False
        if rienFait:
            self.log.critical("jouerUid n'a rien fait")
            self.log.critical(self.choixPossibles)
            planter
#         dbg=""
#         for c in   self.choixPossibles:
#             dbg+=c.uid  +', '
#         self.log.critical('jouerUid : {}'.format(dbg))

         
    def genererCourDeferme(self):
        pTourbes=['B2','B3','B4']
        pForets=['A1','A2','A3','A4','A5']  
        self.log.debug('genererCourDeferme : \n tourbes {} \n forêts {}'.format(pTourbes,pForets))

        return(pTourbes,pForets)  
    
    def faireCourDeferme(self,positionTourbes,positionForets):
        self.log.info('faireCourDeferme')

        for j in self.joueurs.keys():
            self.joueurs[j].courDeFerme.initTuiles(positionTourbes,positionForets)
        
    def faireActionSurTours(self):
        self.log.info('faireActionSurTours')
        ordreActions={}
        
        ordreActions[1]=CarteAction(self,"a10",effet=fct.choixAmenagementMineurOuMajeur,possibilites=fct.possibilitesAmenagementMineurOuMajeur)
        ordreActions[2]=CarteAction(self,"a11",effet=cloture,visible=False)
        ordreActions[3]=CaseAppro(self,"a12",{'m':-1},visible=False)
        ordreActions[4]=CarteAction(self,"a13",visible=False,possibilites=fct.demanderPlanSemailleEtOuCuisson,effet=fct.planSemailleEtOuCuisson,condition=fct.jePeuxFaireSemailleEtOuCuisson)
        ordreActions[5]=CarteAction(self,"a14",visible=False,effet=fct.naissancePuisMineur,condition=fct.jePeuxNaitre)
        ordreActions[6]=CarteAction(self,"a15",visible=False,effet=renoPuisMajeur,condition=jePeuxRenover)
        ordreActions[7]=CaseAppro(self,"a16",{'p':-1},visible=False)
        ordreActions[8]=CarteAction(self,"a17",cout={'l':-1},visible=False)
        ordreActions[9]=CaseAppro(self,"a18",{'s':-1},visible=False)
        ordreActions[10]=CaseAppro(self,"a19",{'b':-1},visible=False)
        ordreActions[11]=CaseAppro(self,"a20",{'p':-1},visible=False)
        ordreActions[12]=CarteAction(self,"a21",effet=labourageSemaille,visible=False)
        ordreActions[13]=CarteAction(self,"a22",effet=naissanceSansPieceLibre,visible=False)
        ordreActions[14]=CarteAction(self,"a23",effet=renoPuisCloture,visible=False)
        return ordreActions
                    
    def initOrdre(self):
        pass
    
    
    def draft(self):
        self.log.info('draft')
        pass
    
 
    
    def demarragePartie(self):
        #boucle infinie
        self.log.info('----------------------\ndébut de la partie')
        self.messagesPrincipaux.append("début de la partie")
    
                
    def demarrageTour(self):

        self.log.info("début du tour : {}".format(self.plateau['tour']))
        self.messagesPrincipaux.append("début du tour : {}".format(self.plateau['tour']))
  
        self.plateau['cases'][self._offset+self.plateau['tour']].visible=True
        
        
        for i in range(1,self._offset+self.plateau['tour']+1):
            self.plateau['cases'][i].reappro()
                     
                     
        print(self.printCasesVisibles())     
        self.quiJoue=self.premierJoueur       
        
#         hooksFinis=util.parcourirLesHooks(self,'debutTour',self.log)
#         return hooksFinis
        
    def hooksDemarrageTour(self):
        hooks=util.recolterLesHooksInterractifs(self,'debutTour',self.log)
        return hooks
    
    def pointerDernierHook(self):
        if len(self.hooks)>0:
            (hook,type)=self.hooks[-1]
            self.pointerSurHook(hook)
            self.log.debug('on pointe sur le hook {} de type {}'.format(hook,type))
            return hook,type  
        else:
            return False,False #on a fini        

    def ajouterHook(self,sujet,possibilites,owner,type):
        self.log.debug('ajouterHook')
        self.hooks.append((Pointeur(sujet,possibilites,owner),type))
        
    

        
#     def initChoix(self):
#         self.changerPointeurs(-1,self.joueurQuiJoue(),"p0",
#             djangoJoueur=self.joueurQuiJoue())
  
        
    def joueurQuiJoue(self):    
        return self.joueurs[self.quiJoue]
        
    def pointerSurJoueurSuivant(self):
  
        if (len(self.quiAFini)>self.nombreJoueurs-1):
            return -1 #le tour est fini
        else:
            self.quiJoue=(1 + self.quiJoue )%self.nombreJoueurs
            if(self.joueurQuiJoue().jaiFini()):
                if self.quiJoue not in self.quiAFini:
                    self.quiAFini.append(self.quiJoue)
                return self.pointerSurJoueurSuivant()
            else:
                joueurSuivant=self.joueurQuiJoue()
                joueurSuivant.possibilites()
#             djangoJoueur=self.joueurQuiJoue())
    def pointerSurPremier(self):    
        joueur=self.joueurs[self.premierJoueur]
        joueur.possibilites()
            
            
    def affichageJoueur(self):
        print("-------------------------------\n\n\n")
        print("JOUEUR:",self.joueurs[self.quiJoue])
        print(self.joueurs[self.quiJoue].courDeFerme.prettyPrint())
        print(self.joueurs[self.quiJoue].ressources)
        for p in self.joueurs[self.quiJoue].personnagesPlaces:
            print("personnage: ",p.id,' est deja placé sur ',p.localisation)
        for p in self.joueurs[self.quiJoue].personnages:
            print("personnage: ",p.id,' est sur ',p.localisation)
    
#     def possibilitesJoueur(self,qui):
#         if qui==self.quiJoue:
#             return self.joueurs[self.quiJoue].listerPossibilites()
#         else:
#             return []
    
#     def jouer(self,choix):
#         if choix==-1:
#             self.possibilitesJoueur()
#         else:
#             #ACTION CONFIRMEE
#             #si c'est un action ou on ne joue pas de pion (as ou utilisation d'un foyer)
#             if self.casesJouables[choix].sansPion :
#                 self.casesJouables[choix].activer()
#                 self.mettreAJourLesRessources(self.casesJouables[choix].cout)
#                 self.listerPossibilites()
# #     TODO        elif self.casesJouables[choix] in actionsSpeJouables:
# #                 pass
#             #ACTION SPECIALE
#             elif isinstance(self.casesJouables[choix],ActionSpeciale):
#                 #
#                 self.casesJouables[choix].jouer()
#                 wdfwdf
# 
# 
#             else:
#             
#                 personnage=self.joueurs[self.quiJoue].personnages.pop()
#                 self.joueurs[self.quiJoue].personnagesPlaces.append(personnage)    
#                 caseJouee=self.casesJouables[choix].jouer(personnage)
#                 print('je joue sur la case:',caseJouee)
#                 self.joueurs[self.quiJoue].mettreAJourLesRessources(caseJouee.cout)
#                 self.joueurs[self.quiJoue].tourFini= len(self.joueurs[self.quiJoue].personnages)==0
#                 if self.joueurs[self.quiJoue].tourFini:
#                     self.quiAFini.append(self.quiJoue)
#                     

    def finDuTour(self):
        if self.plateau['tour']==14:
            print("FIN DE PARTIE")
            return -1
        else:
            #on replace les joueurs
            for id in self.joueurs.keys():
                while(len(self.joueurs[id].personnagesPlaces)>0):
                    p=self.joueurs[id].personnagesPlaces.pop()
                    p.retourMaison()
                    self.joueurs[id].courDeFerme.mettrePersonnage(p,p.localisationInit)
                    self.joueurs[id].personnages.append(p)
                #on réinit les hooks qui sont valables une fois par tour
                
                
                self.log.debug('rechargement des hooks')
                for uid,c in self.joueurs[id].cartesDevantSoi.items():
                    if hasattr(c, 'hook'):
                        if c.hook != ():
                            case,type,freq=c.hook
                            if freq=='t':
                                self.log.debug('rechargement de {}'.format(c.uid))
                                c.hookStatus=0
            #on remets les actions spéciales
            for CAS in self.plateau["actionsSpeciales"]:
                CAS.changerEtat(-2)
            self.quiAFini.clear()
            self.plateau['tour']+=1
        return self.plateau['tour']

    
    def printCasesVisibles(self):
        vis=[]
        for i in range(1,31):
            if self.plateau['cases'][i].visible:
                vis.append(trad[self.plateau['cases'][i].uid]['fr'])
        return vis
    
    #pour l'affichage
    def ordreJoueur(self):
        n=0
        ordre=[]
        while(n<self.nombreJoueurs):
            ordre.append((n+self.quiJoue)%self.nombreJoueurs)
            n+=1
        return ordre
    
#     
#     def aQuiLeTour(self):
# 
#         quiJouait=globOrdreJoueurs.index(self.quiJoue)+1
#         print(self.joueurs[quiJouait].nom,quiJouait,' jouais')
#         if self.joueurs[quiJouait].tourFini:
#             print(self.joueurs[quiJouait].nom,quiJouait,' à fini son tour')
#             print(globOrdreJoueurs)
#             globOrdreJoueurs.remove(quiJouait)
#             print(globOrdreJoueurs)
# 
#         
#         
#         self.quiJoue=globOrdreJoueurs[quiJouait%len(globOrdreJoueurs)]
#         print(joueurs[self.quiJoue].nom,quiJouait,' doit jouer')
#         return self.quiJoue


    
    def prettyPrintPlateau(self):
        str="""
        |-------||-------||-------||-------|
        |{}||{}||{}||{}|
        |*{}||*{}||*{}||*{}|
        |{}||{}||{}||{}|
        |*{}||*{}||*{}||*{}|
        |{}||{}||{}||{}|
        |*{}||*{}||*{}||*{}|
        |{}||{}||{}||{}|
        |*{}||*{}||*{}||*{}|
        |-------||-------||-------||-------|
        |-------||-------||-------||-------||-------||-------||-------|
        |{}||{}||{}||{}||{}||{}||{}|
        |*{}||*{}||*{}||*{}||*{}||*{}||*{}|
        |-------||-------||-------||-------||-------||-------||-------|
        |{}||{}||{}||{}||{}||{}||{}|
        |*{}||*{}||*{}||*{}||*{}||*{}||*{}|
        |-------||-------||-------||-------||-------||-------||-------|
        """
        d=list()
        for i in range(1,5):
            d.append(self.plateau['cases'][i].short)
        for i in range(1,5):
            d.append(self.plateau['cases'][i].printCout())   
        for i in range(5,9):
            d.append(self.plateau['cases'][i].short)
        for i in range(5,9):
            d.append(self.plateau['cases'][i].printCout())               
        for i in range(9,13):
            d.append(self.plateau['cases'][i].short)
        for i in range(9,13):
            d.append(self.plateau['cases'][i].printCout())   
        for i in range(13,17):
            d.append(self.plateau['cases'][i].short)
        for i in range(13,17):
            d.append(self.plateau['cases'][i].printCout()) 
        for i in range(17,24):
            d.append(self.plateau['cases'][i].short)
        for i in range(17,24):
            d.append(self.plateau['cases'][i].printCout())             
        for i in range(24,31):
            d.append(self.plateau['cases'][i].short)
        for i in range(24,31):
            d.append(self.plateau['cases'][i].printCout())                                 
        d=tuple(d)
        return str.format(*d)
        
    #pour le graphique    
    def exportPlateau(self):
        cases=[]
        for c in self.plateau['majeurs'].keys():
            if self.plateau['majeurs'][c].visible:
                dico={
                    'uid':self.plateau['majeurs'][c].uid,
                    'type':"Majeur",
                    'devoile':self.plateau['majeurs'][c].devoile
                    }
                cases.append(dico.copy())
        for c in self.plateau["cases"].keys():
            dico={
                'uid':self.plateau["cases"][c].uid,
                'type':"Action",
                'class': "" if self.plateau["cases"][c].visible else "disabled",
                }
            ressourcesList=[]
            for t in self.plateau["cases"][c].cout.keys():
                if self.plateau["cases"][c].cout[t]<0:
                    ressourcesList.append((util.short2Long[t],-self.plateau["cases"][c].cout[t]))    
            dico['res']=ressourcesList
            dico['perso']=[]
            for perso in self.plateau["cases"][c].occupants:
                dico['perso'].append(perso.couleur)

            
            cases.append(dico.copy())
            
        for CAS in self.plateau["actionsSpeciales"]:
            dico={
                'uid':CAS.listAs(),
                'type':"ActionSpeciale",
                
                }
            if CAS.etat==-2:
                dico['etat']={'texte':'','color':"#fff"}
            elif CAS.etat>-1:
                dico['etat']={'texte':'p12','color':self.joueurs[CAS.etat].couleur}
            elif CAS.etat==-1:
                dico['etat']={'texte':'p13','color':"#999"}
            else:
                imposss
            cases.append(dico.copy())            
        return cases
    
    
    def save(self):
        
        dico={}
        dico["plateau"]={}
        dico["plateau"]['cases']=[self.plateau['cases'][c].save() for c in self.plateau['cases']]
        dico["plateau"]['actionsSpeciales']=[c.save() for c in self.plateau['actionsSpeciales']]
        dico["plateau"]['majeurs']=[self.plateau['majeurs'][c].save() for c in self.plateau['majeurs']]
        dico["plateau"]['tour']=self.plateau['tour']
         
        dico["joueurs"]=[self.joueurs[j].save() for j in self.joueurs.keys()]
        dico["quiJoue"]=self.quiJoue
        dico["nombreJoueurs"]=self.nombreJoueurs
        dico["premierJoueur"]=self.premierJoueur
        dico["quiAFini"]=self.quiAFini
        dico["messagesPrincipaux"]=self.messagesPrincipaux    
        dico["pointeur"]=self.pointeur.save()  
        dico["listeCoupsJoues"]=self.listeCoupsJoues
        return json.dumps(dico)

    
    
    def load(self,jsonStr):
        dico=json.loads(jsonStr)
        self.plateau['cases']=[loadCarte(c,self) for c in dico["plateau"]['cases']]
        self.plateau['actionsSpeciales']=[loadCarte(c,self) for c in dico["plateau"]['cases']]
        self.plateau['majeurs']=[loadCarte(c,self) for c in dico["plateau"]['cases']]
        self.plateau['tour']=dico["plateau"]['tour']
        
        self.joueurs =[loadJoueur(j,self) for j in dico["joueurs"]]
        self.quiJoue=dico["quiJoue"]
        self.nombreJoueurs=dico["nombreJoueurs"]
        self.premierJoueur=dico["premierJoueur"]
        self.quiAFini=dico["quiAFini"]
        self.listeReponse=dico["listeReponse"]
        self.messagesPrincipaux=dico["messagesPrincipaux"]
        self.choixPossibles=dico["choixPossibles"] #on garde ça en memoire
        self.phraseChoixPossibles=dico["phraseChoixPossibles"] #on garde ça en memoire
        self.sujet=dico["sujet"] #on garde ça en memoire        

