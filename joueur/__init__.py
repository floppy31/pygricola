import util
import variablesGlobales
from pygricola.ressources import short2Long

from pygricola.joueur.courDeFerme import CourDeFerme 
from pygricola.joueur.personnage import Personnage
from pygricola.ressources import jouable
from pygricola.carte import deck,Carte
from pygricola.carte.mineur import AmenagementMineur

class Joueur(object):

    def __init__(self, nom,couleur):
        self.nom=nom
        self.couleur=couleur
        self.courDeFerme=CourDeFerme()
        self.cartesEnMain=[AmenagementMineur(**deck['mineurs']["foyer simple"])]
        self.cartesDevantSoi=[]       
        self.tourFini=False
        self.cartesActivables=[]
        self.ressources={
            'b':4,
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
        self.localisationAnimaux={
            
            }

    def __str__(self):
           return 'nom: {}\ncouleur: {}\n---\n{}'.format(self.nom,self.couleur,self.courDeferme)
       
    def listerPossibilites(self):
        actionPossibles=[]
            
        actionsSpeJouables=[]
        for aS in variablesGlobales.plateau["actionsSpeciales"].keys():
            if self.jePeuxFaireActionSpeciale(aS):
                actionsSpeJouables.append(aS)
        
        casesJouables=[]
        for i in range(1,31):
            if variablesGlobales.plateau['cases'][i].visible and variablesGlobales.plateau['cases'][i].libre:
                if self.jePeuxJouer(variablesGlobales.plateau['cases'][i].cout):
                    if self.jeRemplisLesConditions(variablesGlobales.plateau['cases'][i].condition):
                        casesJouables.append(variablesGlobales.plateau['cases'][i])
        
        #on regarde si on a des cases activables
        for c in self.cartesDevantSoi:
            if not c.activer == util.dummy:
                casesJouables.append(c)
        #manger cru        
        for k in ['l','c']:
            if self.ressources[k]>0:
                casesJouables.append(deck['utilitaire'][k+" cru"])

        casesJouables=casesJouables+self.cartesActivables
        
        choix=util.printPossibilities("QUE VOULEZ VOUS FAIRE?",casesJouables)
        if choix==-1:
            self.listerPossibilites()
            
        #ACTION CONFIRMEE
        #si c'est un action ou on ne jour pas de pion (as ou utilisation d'un foyer)
        if casesJouables[choix].sansPion :
            casesJouables[choix].jouer()
            self.mettreAJourLesRessources(casesJouables[choix].cout)
            self.listerPossibilites()
        elif casesJouables[choix] in actionsSpeJouables:
            pass
        else:
        
            pion=variablesGlobales.pions[variablesGlobales.quiJoue].pop()
            variablesGlobales.pionsPlaces[variablesGlobales.quiJoue].append(pion)    
            caseJouee=casesJouables[choix].jouer(pion)
            print('je joue sur la case:',caseJouee)
            self.mettreAJourLesRessources(caseJouee.cout)
            self.tourFini= len(variablesGlobales.pions[variablesGlobales.quiJoue])==0
#             carteJouee=casesJouables[choix].effet(faire=True)
#             carteJouee.jouer()
                      
        return actionPossibles   
     
    def jePeuxJouer(self,cout): #cout ou condition
        return jouable(self.ressources,cout,True)
         
    def jeRemplisLesConditions(self,cond):
        #on traita ça comme un cout
        if type(cond)==dict:
            return jouable(self.ressources,cond,True)
        else:
            #sinon on appelle la fonction
            return cond
       
    def jePeuxFaireActionSpeciale(self,carte):
        
        #
        carte.condition()   
        
        

     
    def combienJaiJoueDe(self,string):
        count=0
        for c in self.cartesDevantSoi:
            if type(c)==string:
                count+=1
        return count
        
    def mettreAJourLesRessources(self,rDict):
        print ('rDict:',rDict)
        print("avant:")
        print(self.ressources)
        for r in self.ressources.keys():
            if r in rDict.keys():
                self.ressources[r]-=rDict[r]
                if self.ressources[r]<0:
                    print('RESSOURCES < 0 !!!')
                    exit
        print("apres:")
        print(self.ressources)   
            
        
