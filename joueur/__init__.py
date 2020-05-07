import pygricola.util as util

from pygricola.joueur.courDeFerme import CourDeFerme 
from pygricola.joueur.personnage import Personnage,loadPersonnage
from pygricola.carte import deck,Carte,loadCarte,SavoirFaire


class Joueur(object):

    def __init__(self, partie,nom,id,couleur,djangoUid):
        self.partie=partie
        self.nom=nom
        self.id=id
        self.couleur=couleur
        self.djangoUid=djangoUid
        self.courDeFerme=CourDeFerme(partie)
        self.cartesEnMain=[]
        self.cartesDevantSoi={}
        self.cartesMendicite=[]
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
        self._preferencesRecolte={
            'animaux':['h','v','s','m'],
            'M18':'a',
            'M20':'a',
            'M22':'a'}
    #génere la liste du nombre d'animaux et sa correspondance 
    # tri par odre décroissant
    # pour savoir si on a assez de place
    def tupListAnimaux(self):
        animaux=['m','s','v','h']
        dico={}
        for an in animaux:
            if self.ressources[an]>0:
                dico[an]=self.ressources[an]
                
        tupList=sorted(dico.items(), key=lambda x: x[1], reverse=True)
        return tupList
    
    def calculerScore(self):
        detail={}
        f=self.courDeFerme
        #les champs
        nbChamp=f.compter('champ')
        if nbChamp==0 or nbChamp==1:
            detail['p56']=-1
        elif nbChamp==2:
            detail['p56']=1
        elif nbChamp==3:
            detail['p56']=2
        elif nbChamp==4:
            detail['p56']=3 
        elif nbChamp>4:                       
            detail['p56']=4
        #les paturages
        
        nbPat=len(f.paturagesContigus.keys())
        if nbPat==0:
            detail['p57']=-1
        elif nbPat==1:
            detail['p57']=1
        elif nbPat==2:
            detail['p57']=2
        elif nbPat==3:
            detail['p57']=3 
        elif nbPat>3:                       
            detail['p57']=4            
             
        #les etables cloturée
        nbEtablesCloturees=0
        for id,pat in f.paturagesContigus.items():
            nbEtablesCloturees+=len(pat.etables)
        detail['p58']=nbEtablesCloturees

        #cereales
        nCereales=self.ressources['c']
        nLegumes=self.ressources['l']
        for c in f.tousLes('champ'):
            nCereales+=f.etat[c].ressources['c']
            nLegumes+=f.etat[c].ressources['l']
        
        if nCereales==0:     
            detail['rc']=-1
        elif nCereales<4:
            detail['rc']=1
        elif nCereales<6:
            detail['rc']=2   
        elif nCereales<8:
            detail['rc']=3       
        elif nCereales>7:  
            detail['rc']=4
        
        if nLegumes==0:    
            detail['rl']=-1
        else:
            detail['rl']=min(4,nLegumes)
        
        
        #cases vides
        detail['p59']=-1*f.compter('vide')
        
        #moutons
        nMoutons=self.ressources['m']
        if nMoutons==0:
            detail['rm']=-1
        elif nMoutons<4:
            detail['rm']=1
        elif nMoutons<6:
            detail['rm']=2
        elif nMoutons<8:
            detail['rm']=3 
        elif nMoutons>7:                       
            detail['rm']=4    

        #sanglier
        nSanglier=self.ressources['s']
        if nSanglier==0:
            detail['rs']=-1
        elif nSanglier<3:
            detail['rs']=1
        elif nSanglier<5:
            detail['rs']=2
        elif nSanglier<7:
            detail['rs']=3 
        elif nSanglier>6:                       
            detail['rs']=4    
            
        #boeufs
        nBoeufs=self.ressources['v']
        if nMoutons==0:
            detail['rv']=-1
        elif nMoutons<2:
            detail['rv']=1
        elif nMoutons<4:
            detail['rv']=2
        elif nMoutons<6:
            detail['rv']=3 
        elif nMoutons>5:                       
            detail['rv']=4    
            
        #chevaux
        nChevaux=self.ressources['h']
        if nChevaux==0:
            detail['rh']=-1  
        else:
            detail['rh']=nChevaux                    
            
        
        nPiece=f.compter('maison')
        type=f.enQuoiEstLaMaison(False)
        
        if type=='maisonBois':
            detail['p60']=0
        elif type=='maisonArgile':
            detail['p60']=nPiece
        elif type=='maisonPierre':
            detail['p60']=nPiece*2
            
        ptVict=0
        for uid,c in self.cartesDevantSoi.items():
            if not isinstance(c,SavoirFaire):
                ptVict+=c.pointsVictoire
            
        detail['p61']=ptVict
        
        detail['p62']=0
        
        detail['u8']=-3*len(self.cartesMendicite)
        
        
        total=0
        for v in detail.values():
            total+=v
        detail['total']=total
        
        return detail
        
        
        
    def aiJePrisDesAnimaux(self,rDict):
        animaux=['m','s','v','h']
        rep=False
        for an in animaux:
            if an in rDict.keys() and rDict[an]<0:
                rep=True
                break
        return rep
                
                
    @property
    def uid(self):
        return self.nom

    def __str__(self):
           return 'nom: {}\n'.format(self.nom)
    
#     def effet(self,choix,possibilites):
#         self.partie.jouerUid(choix)
    
    def poserCarteDevantSoi(self,carte,Majeur=False):
        
        #si la carte est passable à gauche on la pose pas devant soit mais on la pass
        
        if carte.uid=='u8':
            carte.owner=self 
            self.cartesDevantSoi[carte.uid]=carte 
            
        elif not Majeur and carte.passableAGauche:
            carte.owner=self 
            carte.effetInstantane()
            idGauche=(self.id+1)%self.partie.nombreJoueurs
            self.partie.joueurs[idGauche].cartesEnMain.append(carte)
            self.partie.log.info("{} passe à gauche".format(carte.uid))
        else:
            
            self.cartesDevantSoi[carte.uid]=carte       
            carte.owner=self 
            if Majeur:
                del self.partie.plateau["majeurs"][carte.uid]
                if not carte.devoile is None:
                    self.partie.plateau['majeurs'][carte.devoile].visible=True
            else:
                #permet de jouer des cartes directement genre pour les tests
                if carte in self.cartesEnMain:
                    self.cartesEnMain.remove(carte)
            carte.effetInstantane()
            self.partie.log.info("{} pose {}".format(self.nom,carte.uid))
       
    def possibilites(self):
        
        #je regarde si j'ai des pion au cas ou (à cause de la récolte infirmerie)
        if len(self.personnages)==0:
            self.partie.log.debug("je n'ai pas de personnage je ne peux pas jouer")
            self.partie.changerPointeurs(-1,None)  
        else:
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
                if not v._effet == util.dummy:
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
            self.partie.log.debug("fin de joueur possibilites")
            self.partie.changerPointeurs(casesJouables,self,'p0',djangoJoueur=self.djangoUid)     
        
    
    def cuireAnimal(self,an):
        
        pouvoir=self.pouvoirCuissonAnimaux()
        if self.ressources[an]>0:
            self.ressources[an]-=1
            self.ressources['n']+=pouvoir[an]
            self.partie.log.info('{} {} {} {} {} {}'.format(self.nom,"p50","r"+an,"p51",pouvoir[an],"rn"))
            self.partie.messagesPrincipaux.append([self.nom,"p50","r"+an,"p51",pouvoir[an],"rn"])

        else:
            self.partie.log.debug('{} {}'.format(an,self.ressources))
            impossible
    
    def pouvoirCuissonAnimaux(self):
        #pour chaque animal donne la valeur en nourriture de la cuisson d'un animal
        pouvoir={'m':0,'s':0,'v':0,'h':0}
        for id,c in self.cartesDevantSoi.items():
            self.partie.log.debug('{} {}'.format(id,c.option))
            if 'cuissonDict' in c.option.keys():
                for an,val in pouvoir.items():
                    self.partie.log.debug('{} {}'.format(an,val))
                    if an in c.option['cuissonDict'].keys() and c.option['cuissonDict'][an]>val:
                        pouvoir[an]=c.option['cuissonDict'][an]
        return pouvoir
        
    def aiJeFourCuissonIllimite(self):
        return self.aiJeJoue("M8") or self.aiJeJoue("M9") or self.aiJeJoue("M10") or self.aiJeJoue("M11") or self.aiJeJoue("M0") or self.aiJeJoue("M1")
        
    
    def pouvoirCuisson(self,ncereal):
        #combien j'ai de bouffe au max si je cuis ncereal
        pn=0
        dicoResteCuisson={'M14':1,'M16':2}
        while(ncereal>0):
            self.partie.log.debug('{} {}'.format(ncereal,pn))
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
            else:
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
        return {'r':2,util.maisonRessource[self.courDeFerme.enQuoiEstLaMaison()]:5}  
   
    def prixDeLaRenovation(self):
        if self.courDeFerme.enQuoiEstLaMaison()=='B':
            return {'r':1,'a':self.courDeFerme.compter('maison')}  
        elif self.courDeFerme.enQuoiEstLaMaison()=='A':
            return {'r':1,'p':self.courDeFerme.compter('maison')}  
         
      
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
            self.partie.recolterLesHooksInterractifs('ressourcesActionPersonne',{'ressources':rDictReadOnly})
            if self.aiJeJoue('m25'):
                for k,v in rDictReadOnly.items():
                    if k in ['b','a','p','r']:
                        if v<-3:
                            self.partie.log.info('special m25')
                            self.ressources['f']+=1
        #hook sur la prise d'animaux
        if self.aiJePrisDesAnimaux(rDict):
            self.organiserLesAnimaux()
                
        self.partie.log.debug("\n cout: {}\n avant: {}\n après: {}".format(rDict,sauv,self.ressources))

    
    def organiserLesAnimaux(self,recolte=False):
        tup=self.tupListAnimaux()
        tupSave=tup.copy()
        stockage=self.courDeFerme.calculerCapaciteStockage()
#         print(tup)
#         print(stockage['list'])
        #on rend les deux tupListes comparables
        
        tupComparables=util.tupListComparables(tup,stockage['list'])

#         print(tupComparables)
        # test réel
        stokageOk=True
        while(stokageOk and len(tupComparables)>0):
            an,num=tupComparables.pop(0)
#             print('toto',tupComparables,an,num)
            if len(stockage['list'])>0:
                place=stockage['list'].pop(0)
                if place<num:
                    self.partie.log.debug("Pas assez de place pour {}".format(an))
                    stokageOk=False
                    
                else:
                    self.partie.log.debug("ok")
            else:
                self.partie.log.debug("Pas assez de place pour {}".format(an))
                stokageOk=False
                
#         print(stokageOk,tupComparables)
        if stokageOk:
            self.partie.log.debug("STOKAGE_OK")
            if not recolte:
                self.partie.changerPointeurs(-1,None)
        else:
            self.partie.log.debug("STOKAGE_KO")
            if not recolte:
                #dans ce cas il faut créer un hook
                #on regarde le pouvoir de cuisson des animaux
                pouvoir=self.pouvoirCuissonAnimaux()
                possibilites=[]
                for an,num in tupSave:
                    if pouvoir[an]>0:
                        possibilites.append('u{}'.format(an)) #cuire l'animal
                                    
                for an,num in tupSave:
                    possibilites.append('l{}'.format(an)) #libérer l'animal
    #             print('possibilites',possibilites,tupComparables)
                
                attrsCarteGestion=deck['utilitaire']["c2"].copy()
                attrsCarteGestion['possibilites']=possibilites
        
                carteGestion=Carte(self.partie,"c2",**attrsCarteGestion)
                carteGestion.owner=self
                self.partie.ajouterHook(carteGestion,possibilites,self.djangoUid,'animaux',phrase="p55")
            else:
                #dans ce cas on ne peux que libérer.... 
                #on regarde les préférences utilisateur
                prefAn=self._preferencesRecolte['animaux'].copy()
                animauxPossedes=[an for an,num in tupSave]
                while len(prefAn)>0:
                    anALiberer=prefAn.pop()
                    if anALiberer in animauxPossedes:
                        break
                self.ressources[anALiberer]-=1
                self.partie.log.debug("on libere 1 {} et on réappelle la fonction".format(anALiberer))
                self.organiserLesAnimaux(recolte=True)
                
                
                
                
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
        dico['persoCount']=len(self.personnages)+len(self.personnagesPlaces)
        dico['score']=self.calculerScore()
        dico['preferencesRecolte']=self._preferencesRecolte.copy()
        return dico
        

def loadJoueur(dico,partie):
    j=Joueur(partie=partie,id=dico["id"],nom=dico["nom"],couleur=dico["couleur"])  
    j.courDeFerme.load(dico['courDeFerme']) 
    j.cartesEnMain=[loadCarte(c,partie) for c in dico["cartesEnMain"]]
    j.cartesDevantSoi  = [loadCarte(c,partie) for c in dico["cartesDevantSoi"]]
    j.ressources=dico['ressources']
    j.personnages=[loadPersonnage(p) for p in dico['personnages']]
    j.personnagesPlaces=[loadPersonnage(p) for p in dico['personnagesPlaces']]
