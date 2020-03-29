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
        variablesGlobales.joueurs[variablesGlobales.quiJoue].mettreAJourLesRessources(cartesJouables[choix].cout)       
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
    #si on a pas de champ on peut le mettre ou on veut sur une case libre
    if ferme.compter('champ')==0:
        for coord in ferme.etat.keys():
            if ferme.etat[coord].type=='vide':
                possibilites.append( coord)
    #sinon on ne peut labourer qu'a coté d'un champ
    else:
        for c in ferme.tousLes('champ'):
            voiz=ferme.voisin(c)
            for direction in voiz.keys():
                if voiz[direction]: #si not None
                    if ferme.etat[voiz[direction]].type=='vide':
                        #si elle n'y est pas deje
                        if voiz[direction] not in possibilites:
                            possibilites.append( voiz[direction])
        
    
        
    choix=util.printPossibilities("Où voulez vous labourer? :",possibilites)
    if choix != -1:
        caseALabourer=possibilites[choix]
        ferme.etat[caseALabourer].type="champ"
        
    
        
    
def cloture():
    aTermine = False
    ferme=variablesGlobales.joueurs[variablesGlobales.quiJoue].courDeFerme
    ferme.paturages.aCloture=False
    while aTermine == False:
        print(ferme.prettyPrint())
        possibilites=['Construire un nouveau paturage', 'Diviser un paturage existant', 'Terminer l action']
        choix=util.printPossibilities("Que voulez vous faire? :",possibilites)
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

    
def jePeuxFaireSemailleEtOuCuisson():    
    return jePeuxSemer() and jePeuxCuireDuPain()

def jePeuxSemer():
    joueur=variablesGlobales.joueurs[variablesGlobales.quiJoue]
    possibilites=[]
    ferme=joueur.courDeFerme
    
    for coord in ferme.etat.keys():
        if ferme.etat[coord].type=='champ':
            possibilites.append( coord)
    if len(possibilites)==0:
        return False  
    deQuoiSemer=False
    for r in joueur.quePuisJeSemer():
        if joueur.ressources[r]>0:
            deQuoiSemer=True
    return deQuoiSemer


def jePeuxCuireDuPain():
    #j'ai au moins un cereal
    joueur=variablesGlobales.joueurs[variablesGlobales.quiJoue]
    for c in joueur.cartesDevantSoi:
        if 'cuissonPain' in c.option.keys():
            return True

        
def semailleEtOuCuisson():
    
    joueur=variablesGlobales.joueurs[variablesGlobales.quiJoue]
    possibilites=[]
    ferme=joueur.courDeFerme
    print(ferme.prettyPrint())
    for coord in ferme.etat.keys():
        if ferme.etat[coord].type=='champ':
            possibilites.append( coord)
    if len(possibilites)==0:
        print("Vous n'avez pas de champs!!!!")
    else:
        print("vous pouver semer dans ces cases: ",possibilites)
        print("vous avez {} cereale(s) et {} legume(s): ".format(joueur.ressources['c'],joueur.ressources['l']))
        print("taper votre plan de semaille: voici quelques exemples")
        print("par ex c2:c vous semez un cereale en c2")
        print("par ex b3:l vous semez un legume en b3")
        print("par ex c1:c,c4:l,a1:l vous semez un cereale en c1, un legume en c4 et un legume en a1")
        print("si vous avez une carte qui se comporte comme un champ, utiliser sa ou ses coordonnée(s) supplementaire(s)")
        planIncorrect=True
        while(planIncorrect):
            planSemaille=input('plan de semaille:')
            try:
                #je mets tout on ne sais jamais 
                cout=util.rVide()
                tupList=[]
                for tup in planSemaille.split(','):
                    case=tup.split(':')[0]
                    type=tup.split(':')[1]
                    if not case in possibilites:
                        print("la case:", case," n'est pas semable")
                        nimportequoi #permet de sortir du try et de reboucler
                    if (joueur.ressources[type] - cout[type])==0:
                        print("vous n'avez pas assez de ", short2Long(type))
                        nimportequoi
                    else:
                        cout[type]+=1
                        tupList.append((case,type))
                #si on est là c'est qu'on est ok
                planIncorrect=False
                        
            except:
                print('plan de semaille incorrect')
        
        #effectuer reellement la semaille
        for tup in tupList:
            ferme.etat[tup[0]].semer(tup[1])
        
        joueur.mettreAJourLesRessources(cout)  
                
                       
    

def jePeuxNaitre():
    joueur=variablesGlobales.joueurs[variablesGlobales.quiJoue]
    ferme=joueur.courDeFerme
    nbPions=len(variablesGlobales.pions[variablesGlobales.quiJoue])+len(variablesGlobales.pionsPlaces[variablesGlobales.quiJoue])
    nbMaison=ferme.compter('maison')
    if nbMaison>nbPions:
        return True
    else:
        print("impossible de naitre, il n'y a pas de place")
        return False
      
def naissancePuisMineur():
    possibilites=[]
    joueur=variablesGlobales.joueurs[variablesGlobales.quiJoue]
    ferme=joueur.courDeFerme
    #on a deja verifie qu'on peut naitre
    #on regarde les enplacement des pions existants (useless???)
    emplacements=[]
    nbJoueurs=0
    for p in variablesGlobales.pions[variablesGlobales.quiJoue]+variablesGlobales.pionsPlaces[variablesGlobales.quiJoue]:
        emplacements.append(p.localisationInit)
        nbJoueurs+=1
    emplacements=set(emplacements)
    emplacementsMaisons=set(ferme.tousLes('maison'))
    
    nouveauNe=Personnage(emplacementsMaisons.difference(emplacements).pop(),nbJoueurs+1)
    nouveauNe.localisation='naissance'
    variablesGlobales.pionsPlaces[variablesGlobales.quiJoue].append(nouveauNe)
    choixAmenagementMineur()
    
    
def jePeuxContruireUnePiece():    
    joueur=variablesGlobales.joueurs[variablesGlobales.quiJoue]
    ferme=joueur.courDeFerme   
    typeMaison=ferme.enQuoiEstLaMaison()
    
    cout=joueur.prixDeLaPiece()
    ressourcesOk=joueur.jePeuxJouer(cout)
    placeOk=False
    #je regarde si j'ai la place
    for c in ferme.tousLes('maison'):
        voiz=ferme.voisin(c)
        for direction in voiz.keys():
            if voiz[direction]: #si not None
                if ferme.etat[voiz[direction]].type=='vide':
                    placeOk=True
    return (placeOk and ressourcesOk)

def constructionDePieceEtOuEtable():
    joueur=variablesGlobales.joueurs[variablesGlobales.quiJoue]
    ferme=joueur.courDeFerme   
    typeMaison=ferme.enQuoiEstLaMaison()
    #pour constructions multiples
    jeVeuxConstruire=True
    while jeVeuxConstruire:
        cout=joueur.prixDeLaPiece()
        if joueur.jePeuxJouer(cout):
            #ou placer la piece
            emplacementsPossibles=[]
            for c in ferme.tousLes('maison'):
                voiz=ferme.voisin(c)
                for direction in voiz.keys():
                    if voiz[direction]: #si not None
                        if ferme.etat[voiz[direction]].type=='vide':
                            emplacementsPossibles.append(voiz[direction])   
            choix=util.printPossibilities("Où voulez vous construire? :",emplacementsPossibles,False)
            if choix == -1:
                return -1
            else:
                
                joueur.mettreAJourLesRessources(cout)
                ferme.etat[emplacementsPossibles[choix]].type=ferme.enQuoiEstLaMaison(False)
                
                #on recalcule à cause de certaines cartes
                cout=joueur.prixDeLaPiece()
                if joueur.jePeuxJouer(cout):
                    emplacementsPossibles=[]
                    for c in ferme.tousLes('maison'):
                        voiz=ferme.voisin(c)
                        for direction in voiz.keys():
                            if voiz[direction]: #si not None
                                if ferme.etat[voiz[direction]].type=='vide':
                                    emplacementsPossibles.append(voiz[direction])  
                    if  len(emplacementsPossibles)>0:
                        #je peux encore construire
                        ouinon=['oui','non']
                        choix=util.printPossibilities("Construire une autre pièce? :",ouinon,False)
                        if ouinon[choix]=='non':
                            jeVeuxConstruire=False 
                    else:
                        jeVeuxConstruire=False 
                else:
                    jeVeuxConstruire=False        
    
    
    #combien j'ai d'etables
    if(ferme.compterEtablesDispo()>0):
        #je peux construire combien d'étables?
        #il me semble qu'il n'y a aucune reduction ici pour le cout des etables
        nbois=  joueur.ressources['b']
        casesVides=ferme.compter("vide")
        #min entre nb etable qu'on peut construire, etables encore dispo, et place dispo
        nbEtablesPossibles = int(min(nbois/2,ferme.compterEtablesDispo(),casesVides))
        possibles=["pas d'étable","1 étable","2 étables","3 étables","4 étables"]
        possibles=possibles[0:nbEtablesPossibles+1]
        choix=util.printPossibilities("Combien d'étables :",possibles,False)
        nbEtables=choix
        for e in range(nbEtables):
            possibles=ferme.tousLes('vide')
            choix=util.printPossibilities("Ou placer cette etable? :",possibles,False)
            ferme.etat[possibles[choix]].type="etable"
            joueur.mettreAJourLesRessources({'b':2})
    
        
def jePeuxRenover():
    joueur=variablesGlobales.joueurs[variablesGlobales.quiJoue]
    ferme=joueur.courDeFerme   
    typeMaison=ferme.enQuoiEstLaMaison()
    nbMaison=ferme.compter('maison')
    cout={'r':1,typeMaison:nbMaison}
    return joueur.jePeuxJouer(cout)


        
        
def renoPuisMajeur():
    pass

def labourageSemaille():
    pass

def naissanceSansPieceLibre():
    pass

def renoPuisCloture():
    pass

class Partie(object):
    
    
    
    def __init__(self, nombreJoueurs,listeReponse):
        

        variablesGlobales.init(nombreJoueurs)
        variablesGlobales.listeReponse=listeReponse
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
            variablesGlobales.pions[j]=[]
            variablesGlobales.pions[j].append(Personnage("b1",1))
            variablesGlobales.pions[j].append(Personnage("c1",2))
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
        variablesGlobales.plateau["cases"][7]=CarteAction("Construction de pièce et/ou d'étable","toto",visible=True,condition=jePeuxContruireUnePiece,effet=constructionDePieceEtOuEtable)
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
        ordreActions[4]=CarteAction('Semaille et/ou cuisson de pain','toto',effet=semailleEtOuCuisson,condition=jePeuxFaireSemailleEtOuCuisson)
        ordreActions[5]=CarteAction('Naissance puis aménagement mineur','toto',effet=naissancePuisMineur,condition=jePeuxNaitre)
        ordreActions[6]=CarteAction('Rénovation puis aménagement majeur','toto',effet=renoPuisMajeur,condition=jePeuxRenover)
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
        
        ##############"TO DEBUG
        for c in variablesGlobales.plateau['cases'].keys():
            variablesGlobales.plateau['cases'][c].visible=True
        ##############"TO DEBUG

        
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
        



