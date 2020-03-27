import variablesGlobales
from pygricola.joueur import Joueur 
from pygricola.carte.action import CarteAction,CaseAppro
from pygricola.carte import deck
from pygricola.carte.majeur import AmenagementMajeur
from pygricola.joueur.personnage import Personnage
import util


example={
    0:('alpha','bleu'),
    1:('beta','blanc'),
    2:('gamma','rouge'),
    3:('delta','vert'),
    4:('epsilon','violet'),
      }

recoltes=[4,7,9,11,13,14]




    

def coutSavoirFaire1():
    if variablesGlobales.quiJoue in variablesGlobales.joueurs.keys():
        if variablesGlobales.joueurs[variablesGlobales.quiJoue].combienJaiJoueDe('SavoirFaire')==0:
            return {}
    else:
        return {'n':1}

def coutSavoirFaire2():
    if variablesGlobales.joueurs[variablesGlobales.quiJoue].combienJaiJoueDe('SavoirFaire')<2:
        return {'n':1}
    else:
        return {'n':2}
    
def choixAmenagementMineur():

    
    cartesJouables=[]   

    for c in  variablesGlobales.joueurs[variablesGlobales.quiJoue].cartesEnMain:
        if variablesGlobales.joueurs[variablesGlobales.quiJoue].jePeuxJouer(c.condition):
             if variablesGlobales.joueurs[variablesGlobales.quiJoue].jePeuxJouer(c.cout):
                        cartesJouables.append(c)
    choix=util.printPossibilities("choissisez un aménagement mineur:",cartesJouables)
    if choix != -1:
        cartesJouables[choix].jouer()
        variablesGlobales.joueurs[variablesGlobales.quiJoue].mettreAJourLesRessources(cartesJouables[choix])       
    return
    


def choixAmenagementMineurOuMajeur():
    print("ON A APPELLE choixAmenagementMineurOuMajeur")
    cartesJouables=[]   
    joueur=variablesGlobales.joueurs[variablesGlobales.quiJoue]
    plateau=variablesGlobales.plateau
    for c in  joueur.cartesEnMain:
        if joueur.jePeuxJouer(c.condition):
             if joueur.jePeuxJouer(c.cout):
                        cartesJouables.append(c)
                        
    for m in  plateau['majeurs'].keys():
        if plateau['majeurs'][m].visible:
             if joueur.jePeuxJouer(plateau['majeurs'][m].cout):
                        cartesJouables.append(plateau['majeurs'][m])                        
    choix=util.printPossibilities("choissisez un aménagement mineur ou majeur:",cartesJouables)
    carteJouee=cartesJouables[choix]
    if choix != -1:
        carteJouee.jouer()
        joueur.mettreAJourLesRessources(carteJouee.cout)       
        joueur.cartesDevantSoi.append(carteJouee)
        if carteJouee in joueur.cartesEnMain:
        #on la pose
            joueur.cartesEnMain.remove(carteJouee)
            joueur.cartesDevantSoi.append(carteJouee)
        else:
            #on enleve le majeur et on gere les cartes dessous
            del plateau['majeurs'][carteJouee.nom]
            if not carteJouee.devoile is None:
                plateau['majeurs'][carteJouee.devoile].visible=True


def labourage():
    #
    possibilites=[]
    ferme=variablesGlobales.joueurs[variablesGlobales.quiJoue].courDeFerme
    print(ferme.prettyPrint())
    for coord in ferme.etat.keys():
        if ferme.etat[coord].type=='vide':
            possibilites.append( coord)
    choix=util.printPossibilities("Où voulez vous labourer? :",possibilites)
    if choix != -1:
        caseALabourer=possibilites[choix]
        ferme.etat[caseALabourer].type="champ"
        
    
        
    
def cloture():
    pass
    
def semailleEtOuCuisson():
    pass

def naissancePuisMineur():
    pass

def renoPuisMajeur():
    pass

def labourageSemaille():
    pass

def naissanceSansPieceLibre():
    pass

def renoPuisCloture():
    pass

class Partie(object):
    
    
    
    def __init__(self, nombreJoueurs):
        

        variablesGlobales.init(nombreJoueurs)
        self._offset=16
        self._initJoueurs()
        
        self.initOrdre()
        (positionTourbes,positionForets)=self.genererCourDeferme()
        self.faireCourDeferme(positionTourbes,positionForets)
        
        self.draft()
        
        
        self.actionSurTours=self.faireActionSurTours()
        
        self._genererPlateau(nombreJoueurs)

        
    def _initJoueurs(self):

        
        for j in range(variablesGlobales.nombreJoueurs):
            variablesGlobales.pions[j]=[Personnage("b1",1),Personnage("c1",2)]
            variablesGlobales.pionsPlaces[j]=[]
            (n,c)=example[j]
            variablesGlobales.joueurs[j]=Joueur(nom=n,couleur=c)
        
    def _genererPlateau(self,nombre):
        variablesGlobales.plateau["cases"]=dict()
        variablesGlobales.plateau["actionsSpeciales"]=dict()
        variablesGlobales.plateau["tour"]=1

        if nombre==2:
            pass
        elif nombre ==2:
            pass
        elif nombre==4:
            pass
        elif nombre ==5:
            pass
        #il y a 30 case
        #6 1eres sont celles qui dependent du nombre de joueur
        #
        variablesGlobales.plateau["cases"][1]=CarteAction("TODO   ","toto")
        variablesGlobales.plateau["cases"][2]=CarteAction("TODO   ","toto")
        variablesGlobales.plateau["cases"][3]=CarteAction("TODO   ","toto")
        variablesGlobales.plateau["cases"][4]=CarteAction("TODO   ","toto")
        variablesGlobales.plateau["cases"][5]=CarteAction("TODO   ","toto")
        variablesGlobales.plateau["cases"][6]=CarteAction("TODO   ","toto")
        
        
        variablesGlobales.plateau["cases"][7]=CarteAction("Construction de pièce et/ou d'étable","toto",visible=True)
        variablesGlobales.plateau["cases"][8]=CarteAction("Premier joueur et aménagement mineur","toto",visible=True,effet=choixAmenagementMineur)
        variablesGlobales.plateau["cases"][9]=CarteAction("1 céréale","toto",cout={'c':-1},visible=True)
        variablesGlobales.plateau["cases"][10]=CarteAction("Labourage d'un champ","toto",visible=True,effet=labourage)
        

        
        variablesGlobales.plateau["cases"][11]=CarteAction("1 savoir faire","toto",cout=coutSavoirFaire1,visible=True)
        variablesGlobales.plateau["cases"][12]=CarteAction("Journalier","toto",{'n':-2},visible=True)
        variablesGlobales.plateau["cases"][13]=CaseAppro("3 bois ","toto",{'b':-3},visible=True)
        variablesGlobales.plateau["cases"][14]=CaseAppro("1 argile","toto",{'a':-1},visible=True)
        variablesGlobales.plateau["cases"][15]=CaseAppro("1 roseau","toto",{'r':-1},visible=True)
        variablesGlobales.plateau["cases"][16]=CaseAppro("Pêche ","toto",{'pn':-1})
        variablesGlobales.plateau["cases"][17]=self.actionSurTours[1]
        variablesGlobales.plateau["cases"][18]=self.actionSurTours[2]
        variablesGlobales.plateau["cases"][19]=self.actionSurTours[3]
        variablesGlobales.plateau["cases"][20]=self.actionSurTours[4]
        variablesGlobales.plateau["cases"][21]=self.actionSurTours[5]
        variablesGlobales.plateau["cases"][22]=self.actionSurTours[6]
        variablesGlobales.plateau["cases"][23]=self.actionSurTours[7]
        variablesGlobales.plateau["cases"][24]=self.actionSurTours[8]
        variablesGlobales.plateau["cases"][25]=self.actionSurTours[9]
        variablesGlobales.plateau["cases"][26]=self.actionSurTours[10]
        variablesGlobales.plateau["cases"][27]=self.actionSurTours[11]
        variablesGlobales.plateau["cases"][28]=self.actionSurTours[12]
        variablesGlobales.plateau["cases"][29]=self.actionSurTours[13]
        variablesGlobales.plateau["cases"][30]=self.actionSurTours[14]
        
        
        variablesGlobales.plateau["majeurs"]=dict()
        for m in deck['majeurs'].keys():
            variablesGlobales.plateau["majeurs"][deck['majeurs'][m]['nom']]=AmenagementMajeur(**deck['majeurs'][m])
                    
        
                
         
    def genererCourDeferme(self):
        pTourbes=['b2','b3','b4']
        pForets=['a1','a2','a3','a4','a5']  
        return(pTourbes,pForets)  
    
    def faireCourDeferme(self,positionTourbes,positionForets):
        for j in variablesGlobales.joueurs.keys():
            variablesGlobales.joueurs[j].courDeFerme.initTuiles(positionTourbes,positionForets)
        
    def faireActionSurTours(self):
        ordreActions={}
        
        ordreActions[1]=CarteAction('Aménagement majeur ou mineur','toto',effet=choixAmenagementMineurOuMajeur)
        ordreActions[2]=CarteAction('Cloture','toto',effet=cloture)
        ordreActions[3]=CaseAppro('1 mouton','toto',{'m':-1})
        ordreActions[4]=CarteAction('Semaille et/ou cuisson de pain','toto',effet=semailleEtOuCuisson)
        ordreActions[5]=CarteAction('Naissance puis aménagement mineur','toto',effet=naissancePuisMineur)
        ordreActions[6]=CarteAction('Rénovation puis aménagement majeur','toto',effet=renoPuisMajeur)
        ordreActions[7]=CaseAppro('1 pierre','toto',{'p':-1})
        ordreActions[8]=CaseAppro('1 légume','toto',{'l':-1})
        ordreActions[9]=CaseAppro('1 sanglier','toto',{'s':-1})
        ordreActions[10]=CaseAppro('1 boeuf','toto',{'b':-1})
        ordreActions[11]=CaseAppro('1 pierre','toto',{'p':-1})
        ordreActions[12]=CarteAction('Labourage semaille','toto',effet=labourageSemaille)
        ordreActions[13]=CarteAction('Naissance même sans pièce libre','toto',effet=naissanceSansPieceLibre)
        ordreActions[14]=CarteAction('Rénovation puis cloture','toto',effet=renoPuisCloture)
        return ordreActions
                    
    def initOrdre(self):
        pass
    
    
    def draft(self):
        pass
    
    
    def demarragePartie(self):
        #boucle infinie
        print("début de la partie")
        self.demarrageTour()
    
                
    def demarrageTour(self):


        print("début du tour : {}".format(variablesGlobales.plateau['tour']))
        #on reappro les cases
        
        variablesGlobales.plateau['cases'][self._offset+variablesGlobales.plateau['tour']].visible=True
        
        for i in range(1,self._offset+variablesGlobales.plateau['tour']+1):
            variablesGlobales.plateau['cases'][i].reappro()
                     
                     
        print(self.printCasesVisibles())             
        
        while(True):                         
            if (len(variablesGlobales.quiAFini)==variablesGlobales.nombreJoueurs):
                break
            else:

        
                if(variablesGlobales.quiJoue in variablesGlobales.quiAFini):
                    variablesGlobales.quiJoue=1 + variablesGlobales.quiJoue
                else:
                    print("-------------------------------\n\n\n")
                    print("JOUEUR:",variablesGlobales.quiJoue)
                    print(variablesGlobales.joueurs[variablesGlobales.quiJoue].courDeFerme.prettyPrint())
                    print(variablesGlobales.joueurs[variablesGlobales.quiJoue].ressources)
                    for p in variablesGlobales.pionsPlaces[variablesGlobales.quiJoue]:
                        print("pion: ",p.id,' est deja placé sur ',p.localisation)
                    for p in variablesGlobales.pions[variablesGlobales.quiJoue]:
                        print("pion: ",p.id,' est sur ',p.localisation)
                    variablesGlobales.joueurs[variablesGlobales.quiJoue].listerPossibilites()
                    if variablesGlobales.joueurs[variablesGlobales.quiJoue].tourFini:
                        variablesGlobales.quiAFini.append(variablesGlobales.quiJoue)
                    
                    
                    variablesGlobales.quiJoue=(1 + variablesGlobales.quiJoue )%variablesGlobales.nombreJoueurs


        
        #action qu'on peut faire tout le temps
        #placer un personnage
        #prendre une action speciale
        
    
        print(self.prettyPrintPlateau())
        if variablesGlobales.plateau['tour']==14:
            print("FIN DE PARTIE")
        else:
            for j in variablesGlobales.pionsPlaces.keys():
                while(len(variablesGlobales.pionsPlaces[j])>0):
                    p=variablesGlobales.pionsPlaces[j].pop()
                    p.retourMaison()
                    variablesGlobales.pions[j].append(p)

                    
            variablesGlobales.quiAFini.clear()
            variablesGlobales.plateau['tour']+=1
            self.demarrageTour()   
    
    def printCasesVisibles(self):
        vis=[]
        for i in range(1,31):
            if variablesGlobales.plateau['cases'][i].visible:
                vis.append(variablesGlobales.plateau['cases'][i].nom)
        return vis
    
    def aQuiLeTour(self):

        quiJouait=globOrdreJoueurs.index(variablesGlobales.quiJoue)+1
        print(variablesGlobales.joueurs[quiJouait].nom,quiJouait,' jouais')
        if variablesGlobales.joueurs[quiJouait].tourFini:
            print(variablesGlobales.joueurs[quiJouait].nom,quiJouait,' à fini son tour')
            print(globOrdreJoueurs)
            globOrdreJoueurs.remove(quiJouait)
            print(globOrdreJoueurs)

        
        
        variablesGlobales.quiJoue=globOrdreJoueurs[quiJouait%len(globOrdreJoueurs)]
        print(joueurs[variablesGlobales.quiJoue].nom,quiJouait,' doit jouer')
        return variablesGlobales.quiJoue


    
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
            d.append(variablesGlobales.plateau['cases'][i].short)
        for i in range(1,5):
            d.append(variablesGlobales.plateau['cases'][i].printCout())   
        for i in range(5,9):
            d.append(variablesGlobales.plateau['cases'][i].short)
        for i in range(5,9):
            d.append(variablesGlobales.plateau['cases'][i].printCout())               
        for i in range(9,13):
            d.append(variablesGlobales.plateau['cases'][i].short)
        for i in range(9,13):
            d.append(variablesGlobales.plateau['cases'][i].printCout())   
        for i in range(13,17):
            d.append(variablesGlobales.plateau['cases'][i].short)
        for i in range(13,17):
            d.append(variablesGlobales.plateau['cases'][i].printCout()) 
        for i in range(17,24):
            d.append(variablesGlobales.plateau['cases'][i].short)
        for i in range(17,24):
            d.append(variablesGlobales.plateau['cases'][i].printCout())             
        for i in range(24,31):
            d.append(variablesGlobales.plateau['cases'][i].short)
        for i in range(24,31):
            d.append(variablesGlobales.plateau['cases'][i].printCout())                                 
        d=tuple(d)
        return str.format(*d)
        



