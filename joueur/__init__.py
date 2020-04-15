import pygricola.util as util

from pygricola.joueur.courDeFerme import CourDeFerme 
from pygricola.joueur.personnage import Personnage,loadPersonnage
from pygricola.carte import deck,Carte,loadCarte


class Joueur(object):

    def __init__(self, partie,nom,id,couleur):
        self.partie=partie
        self.nom=nom
        self.id=id
        self.couleur=couleur
        self.courDeFerme=CourDeFerme(partie)
        self.cartesEnMain=[]
        self.cartesDevantSoi={}
        p1=Personnage("B1",1,self.couleur)
        
        
        self.courDeFerme.mettrePersonnage(p1,"B1")
        p2=Personnage("C1",2,self.couleur)
        self.courDeFerme.mettrePersonnage(p2,"C1")
        self.personnages=[p1,p2]
        self.personnagesPlaces=[]
        self.ressources={
            'b':0,
            'a':0,
            'p':0,
            'r':0,
            'n':2,
            'f':0,
            'c':0,
            'l':0,
            'm':0,
            's':0,
            'v':0,
            'h':0,
            }


    def __str__(self):
           return 'nom: {}\n'.format(self.nom)
       
    def poserCarteDevantSoi(self,carte,Majeur=False):
        self.cartesDevantSoi[carte.uid]=carte       
        carte.owner=self 
        if Majeur:
            del self.partie.plateau["majeurs"][carte.uid]
            if not carte.devoile is None:
                self.partie.plateau['majeurs'][carte.devoile].visible=True
        else:
            self.cartesEnMain.remove(carte)
        self.partie.log.info("{} pose {}".format(self.nom,carte.uid))
       
    def possibilites(self):
            
        actionsSpeJouables=[]
        for CAS in self.partie.plateau["actionsSpeciales"]:
            for aS in CAS.listeActionSpeciale:
                if self.jePeuxFaireActionSpeciale(aS):
                    actionsSpeJouables.append(aS)
                else:
                    self.partie.messagesDetail.append(["p8",aS.uid] )
                    
        
        casesJouables=[]
        
        for i in range(1,31):
            if self.partie.plateau['cases'][i].visible and self.partie.plateau['cases'][i].libre:
                if self.jePeuxJouer(self.partie.plateau['cases'][i].cout):
                    if self.jeRemplisLesConditions(self.partie.plateau['cases'][i].condition):
                        casesJouables.append(self.partie.plateau['cases'][i])
                    else:
                        self.partie.messagesDetail.append(["p9",self.partie.plateau['cases'][i].uid] )
                else:
                    self.partie.messagesDetail.append(["p10",self.partie.plateau['cases'][i].uid] )
            else:
                self.partie.messagesDetail.append([self.partie.plateau['cases'][i].uid,"p11"] )
        
        #on regarde si on a des cases activables
        for k,v in self.cartesDevantSoi.items():
            
            if not v.effet == util.dummy:
                #si le hook est vide
                #je pars du principe qu'une carte est soit activable soit elle a un hook
                peutSactiver=True
                if hasattr(v, "hook"):
                    if not v.hook==():
                        peutSactiver=False
                if peutSactiver:
                    if self.jeRemplisLesConditions(v.condition):
                        casesJouables.append(v)
                    else:
                        self.partie.messagesDetail.append(["p9",v] )
        #manger cru        
        #cereale
        if self.ressources['c']>0:
            casesJouables.append(Carte(self.partie,"c0",**deck['utilitaire']["c0"]))
        #legume
        if self.ressources['l']>0:
            casesJouables.append(Carte(self.partie,"c1",**deck['utilitaire']["c1"]))
            
            
        casesJouables=casesJouables+actionsSpeJouables
        self.partie.choixPossibles=casesJouables
    
    def pouvoirCuisson(self,ncereal):
        #combien j'ai de bouffe au max si je cuis ncereal
        pn=0
        dicoResteCuisson={'M14':1,'M16':2}
                
        while(ncereal>0):
            #on cuit d'abord avec le meilleur four
            if self.aiJeJoue("M14") and dicoResteCuisson['M14']>0 :
                pn+=5
                ncereal-=1
                dicoResteCuisson['M14']-=1
            elif self.aiJeJoue("M16") and dicoResteCuisson['M16']>0 :
                pn+=4
                ncereal-=1
                dicoResteCuisson['M16']-=1
            elif self.aiJeJoue("M8") or self.aiJeJoue("M9") or self.aiJeJoue("M10") or self.aiJeJoue("M11"):
                pn+=3
                ncereal-=1
            elif self.aiJeJoue("M0") or self.aiJeJoue("M1"):
                pn+=2
                ncereal-=1            
        return pn
            
#     #doit retourner, soit -1 action fini, soit le sujet s'il y a encore des possibilites
#     def jouer(self,choix):
#         if choix==-1:
#             return self
#         else:
#             #ACTION CONFIRMEE
#             #si c'est un action ou on ne joue pas de pion (as ou utilisation d'un foyer)
#             if self.partie.casesJouables[choix].sansPion :
#                 self.partie.casesJouables[choix].activer()
#                 self.mettreAJourLesRessources(self.partie.casesJouables[choix].cout)
#                 self.possibilites()
# #     TODO        elif self.casesJouables[choix] in actionsSpeJouables:
# #                 pass
#             else:
#             
#  
#                 (choixPossibles,caseJouee)=self.partie.casesJouables[choix].jouer()
#                 if choixPossibles==-1:
#                     print('je joue sur la case:',caseJouee)
#                     
#                     rcode=-1
#                     self.mettreAJourLesRessources(caseJouee.cout)
#                     personnage=self.personnages.pop()
#                     self.personnagesPlaces.append(personnage)                   
#                     caseJouee.mettrePersonnage(personnage)
#                     
#                     if self.jaiFini():
#                         self.partie.quiAFini.append(self.partie.quiJoue)
#                     return rcode
#                 else:
#                     return (choixPossibles,caseJouee)
     
    def jePeuxJouer(self,cout): #cout ou condition
        (result,message)=util.jouable(self.ressources,cout)
        if message!="OK":
            self.partie.messagesDetail.append(message )
        return result
         
    def jeRemplisLesConditions(self,cond):
        #si cond =False non
        if cond==False:
            return False
        else:
            #on traita ça comme un cout
            if type(cond)==dict:
                return util.jouable(self.ressources,cond)
            else:
                #sinon on appelle la fonction
                return cond
    
    def jaiFini(self):
        #logger.debug('__init__ Partie')

        self.partie.log.debug("joueur reste {}".format(len(self.personnages)))
        rep=len(self.personnages)
        if rep==0:
            if self.id not in self.partie.quiAFini:
                self.partie.quiAFini.append(self.id)
        return rep==0
    
        
    
    def quePuisJeSemer(self):
        #methode modifiable si certaines cartes sont jouees
        return ['c','l']
    
    def jePeuxFaireActionSpeciale(self,carte):
        #je peux payer le cout, et il me reste 1 personnage
        #je remplis les conditions
        #la carte est libre
        if carte.carteQuiMePorte.etat==-1:
            #plus rachetable
            self.partie.log.debug("{} plus rachetable".format(carte) )
            return False
        #c'est moi qui l'ai deja prise
        elif carte.carteQuiMePorte.etat==self.id:
            self.partie.log.debug("j'ai déjà pris {}".format(carte) )
            return False
        #carte.cout prend en compte le cout supplémentaire en cas de rachat
        coutOk=self.jePeuxJouer(carte.cout)
        persoOk=len(self.personnages)>0 
        condOk=self.jeRemplisLesConditions(carte.condition) 
        return coutOk and persoOk and condOk 
        
                #
    def aiJeJoue(self,uidCarte):
        return uidCarte in self.cartesDevantSoi.keys()
    
    def prixDeLaPiece(self):
        return {'r':2,self.courDeFerme.enQuoiEstLaMaison():5}  
      
    def coutAbattre(self):
        if self.aiJeJoue("M6"):
            if self.ressources['h']>0:
                return{'b':-4}
            else:
                return{'b':-3}
        else:
            return{'b':-2}
            
    def coutTourbe(self):
        if self.aiJeJoue("M4"):
            if self.ressources['h']>0:
                return{'f':-5}
            else:
                return{'f':-4}
        else:
            return{'f':-3}
                 
    def combienJaiJoueDe(self,lettre):
        count=0
        for uid,c in self.cartesDevantSoi.items():
            if uid[0]==lettre:
                count+=1
        return count
        
    def mettreAJourLesRessources(self,rDictReadOnly,actionDunePersonne=False):
        #on n affiche que si ca bouge
        sauv=self.ressources.copy()
        sortedKeys=list(self.ressources.keys())
        sortedKeys.sort(reverse=True)
        boisATransformer=0
        rDict=rDictReadOnly.copy()

        for r in sortedKeys:
            if r in rDict.keys():
                self.ressources[r]-=rDict[r]
                jePrint=True
                if self.ressources[r]<0:
                    if r=='f':
                        #on mets les feu à 0
                        boisATransformer=0-self.ressources[r]
                        self.ressources[r]=0
                        if 'b' in rDict.keys():
                            rDict['b']+=boisATransformer
                        else:
                            rDict['b']=boisATransformer
                        
                    else:
                        self.partie.log.critical('!!!!!!!!!!!!!!!!!!!RESSOURCES < 0 !!!\n{}\n{}\n{}'.format(r,self.ressources,rDict))
                        planter
                        
        if actionDunePersonne:
            bonus=util.rVide()
            #on appelle les hooks ressourcesActionPersonne
            for cuid,c in self.cartesDevantSoi.items():
                if hasattr(c, 'hook'):
                    if c.hook !=():
                        print(c.uid,'a un hook',c.hook[0])
                        if c.hook[0]=='ressourcesActionPersonne':
                            #si le hook est jouable
                            if c.hookStatus==0:
                                print("hook sur ressourcesActionPersonne",'avec',c.uid,c.hookStatus)
                                #si le hook me concerne
                                if(c.hook[1]=="s"):
                                    bonus=util.ajouter(bonus,c.bonusRessources(rDictReadOnly))
                
                                    
            self.partie.log.debug("ajout des bonus ressourcesActionPersonne",bonus)
            self.ressources=util.ajouter(self.ressources,bonus)                       
                        
        self.partie.log.debug("\n cout: {}\n avant: {}\n après: {}".format(rDict,sauv,self.ressources))

            
    def save(self):
        dico={}
        dico['nom']=self.nom
        dico['id']=self.id
        dico['couleur']=self.couleur
        dico['courDeFerme']=self.courDeFerme.save()
        dico['cartesEnMain']=[c.save() for c in self.cartesEnMain]
        dico['cartesDevantSoi']=[v.save() for c,v in self.cartesDevantSoi.items()]
        dico['mineursJoues']=self.combienJaiJoueDe('m')
        dico['majeursJoues']=self.combienJaiJoueDe('M')
        dico['savoirFaireJoues']=self.combienJaiJoueDe('s')
        dico['ressources']=self.ressources
        dico['personnages']=[p.save() for p in self.personnages]
        dico['personnagesPlaces']=[p.save() for p in self.personnagesPlaces]
        return dico
        

def loadJoueur(dico,partie):
    j=Joueur(partie=partie,id=dico["id"],nom=dico["nom"],couleur=dico["couleur"])  
    j.courDeFerme.load(dico['courDeFerme']) 
    j.cartesEnMain=[loadCarte(c,partie) for c in dico["cartesEnMain"]]
    j.cartesDevantSoi  = [loadCarte(c,partie) for c in dico["cartesDevantSoi"]]
    j.ressources=dico['ressources']
    j.personnages=[loadPersonnage(p) for p in dico['personnages']]
    j.personnagesPlaces=[loadPersonnage(p) for p in dico['personnagesPlaces']]
