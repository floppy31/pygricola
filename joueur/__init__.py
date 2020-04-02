import pygricola.util as util

from pygricola.joueur.courDeFerme import CourDeFerme 
from pygricola.joueur.personnage import Personnage
from pygricola.carte import deck,Carte
from pygricola.carte.mineur import AmenagementMineur

class Joueur(object):

    def __init__(self, partie,nom,id,couleur):
        self.partie=partie
        self.nom=nom
        self.id=id
        self.couleur=couleur
        self.courDeFerme=CourDeFerme(partie)
        self.cartesEnMain=[AmenagementMineur(partie=self.partie,**deck['mineurs']["foyer simple"])]
        self.cartesDevantSoi=[AmenagementMineur(partie=self.partie,**deck['mineurs']["foyer simple"])]       
        self.tourFini=False
        self.cartesActivables=[]
        self.personnages=[Personnage("b1",1,self.couleur),Personnage("c1",2,self.couleur)]
        self.personnagesPlaces=[]
        self.ressources={
            'b':10,
            'a':4,
            'p':4,
            'r':4,
            'n':4,
            'f':4,
            'c':4,
            'l':4,
            'm':0,
            's':0,
            'v':0,
            'h':0,
            }


    def __str__(self):
           return 'nom: {}\n'.format(self.nom)
       
    def possibilites(self):
            
        actionsSpeJouables=[]
        for aS in self.partie.plateau["actionsSpeciales"].keys():
            if self.jePeuxFaireActionSpeciale(aS):
                actionsSpeJouables.append(aS)
        
        casesJouables=[]
        
        for i in range(1,31):
            if self.partie.plateau['cases'][i].visible and self.partie.plateau['cases'][i].libre:
                if self.jePeuxJouer(self.partie.plateau['cases'][i].cout):
                    if self.jeRemplisLesConditions(self.partie.plateau['cases'][i].condition):
                        casesJouables.append(self.partie.plateau['cases'][i])
        
        #on regarde si on a des cases activables
        for c in self.cartesDevantSoi:
            if not c.activer == util.dummy:
                casesJouables.append(c)
        #manger cru        
        for k in ['l','c']:
            if self.ressources[k]>0:
                casesJouables.append(Carte(partie=self.partie,**deck['utilitaire'][k+" cru"]))

        casesJouables=casesJouables+self.cartesActivables
        self.partie.choixPossibles=casesJouables
#         choix=util.printPossibilities(self.partie,"QUE VOULEZ VOUS FAIRE?",casesJouables)
#         if choix==-1:
#             self.listerPossibilites()
#             
#         #ACTION CONFIRMEE
#         #si c'est un action ou on ne joue pas de pion (as ou utilisation d'un foyer)
#         if casesJouables[choix].sansPion :
#             casesJouables[choix].activer()
#             self.mettreAJourLesRessources(casesJouables[choix].cout)
#             self.listerPossibilites()
#         elif casesJouables[choix] in actionsSpeJouables:
#             pass
#         else:
#         
#             personage=self.personnages.pop()
#             self.personnagesPlaces.append(personnage)    
#             caseJouee=casesJouables[choix].jouer(personage)
#             print('je joue sur la case:',caseJouee)
#             self.mettreAJourLesRessources(caseJouee.cout)
#             self.tourFini= len(self.personnages)==0
# #             carteJouee=casesJouables[choix].effet(faire=True)
# #             carteJouee.jouer()
#                       
#         return actionPossibles   
    
    def pouvoirCuisson(self,ncereal):
        #combien j'ai de bouffe au max si je cuis ncereal
        return 2*ncereal
            
    #doit retourner, soit -1 action fini, soit le sujet s'il y a encore des possibilites
    def jouer(self,choix):
        if choix==-1:
            return self
        else:
            #ACTION CONFIRMEE
            #si c'est un action ou on ne joue pas de pion (as ou utilisation d'un foyer)
            if self.partie.casesJouables[choix].sansPion :
                self.partie.casesJouables[choix].activer()
                self.mettreAJourLesRessources(self.partie.casesJouables[choix].cout)
                self.possibilites()
#     TODO        elif self.casesJouables[choix] in actionsSpeJouables:
#                 pass
            else:
            
 
                (choixPossibles,caseJouee)=self.partie.casesJouables[choix].jouer()
                if choixPossibles==-1:
                    print('je joue sur la case:',caseJouee)
                    
                    rcode=-1
                    self.mettreAJourLesRessources(caseJouee.cout)
                    personnage=self.personnages.pop()
                    self.personnagesPlaces.append(personnage)                   
                    caseJouee.mettrePersonnage(personnage)
                    self.tourFini= len(self.personnages)==0
                    if self.tourFini:
                        self.partie.quiAFini.append(self.partie.quiJoue)
                    return rcode
                else:
                    return (choixPossibles,caseJouee)
     
    def jePeuxJouer(self,cout): #cout ou condition
        return util.jouable(self.ressources,cout,True)
         
    def jeRemplisLesConditions(self,cond):
        #on traita ça comme un cout
        if type(cond)==dict:
            return util.jouable(self.ressources,cond,True)
        else:
            #sinon on appelle la fonction
            return cond
    
    def jaiFini(self):
        return len(self.personnages)==0
    
    def quePuisJeSemer(self):
        #methode modifiable si certaines cartes sont jouees
        return ['c','l']
    
    def jePeuxFaireActionSpeciale(self,carte):
        
        #
        carte.condition()   
        
    def prixDeLaPiece(self):
        return {'r':2,self.courDeFerme.enQuoiEstLaMaison():5}    

     
    def combienJaiJoueDe(self,string):
        count=0
        for c in self.cartesDevantSoi:
            if type(c)==string:
                count+=1
        return count
        
    def mettreAJourLesRessources(self,rDict):
        #on n affiche que si ca bouge
        jePrint=False
        sauv=self.ressources.copy()

        for r in self.ressources.keys():
            if r in rDict.keys():
                self.ressources[r]-=rDict[r]
                jePrint=True
                if self.ressources[r]<0:
                    print('RESSOURCES < 0 !!!')
                    exit
        if jePrint:
            print("cout: ",rDict)
            print("avant:")
            print(sauv)
            print("apres:")
            print(self.ressources)   
            
    def save(self):
        dico={}
        dico['nom']=self.nom
        dico['id']=self.id
        dico['couleur']=self.couleur
        dico['courDeFerme']=self.courDeFerme.save()
        dico['cartesEnMain']=[c.save() for c in self.cartesEnMain]
        dico['cartesDevantSoi']=[c.save() for c in self.cartesDevantSoi]
        dico['tourFini']=self.tourFini
        dico['cartesActivables']=[c.save() for c in self.cartesActivables]
        dico['ressources']=self.ressources
        dico['personnages']=[p.save() for p in self.personnages]
        dico['personnagesPlaces']=[p.save() for p in self.personnagesPlaces]
        return dico
        

           
