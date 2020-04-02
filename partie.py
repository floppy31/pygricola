from pygricola.joueur import Joueur 
from pygricola.carte.action import CarteAction,CaseAppro
from pygricola.carte import deck
from pygricola.carte.majeur import AmenagementMajeur
import pygricola.fonctionsPlateau as fct

import pygricola.util as util
import json


example={
    0:('Romain','blue'),
    1:('Daniel','yellow'),
    2:('Gauthier','red'),
    3:('Damien','green'),
    4:('Arthur','violet'),
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


                       
    


      
def naissancePuisMineur(partie):
    joueur=partie.joueurs[partie.quiJoue]
    ferme=joueur.courDeFerme
    #on a deja verifie qu'on peut naitre
    #on regarde les enplacement des pions existants (useless???)
    emplacements=[]
    nbJoueurs=0
    for p in joueur.personnages+joueur.personnagesPlaces[partie.quiJoue]:
        emplacements.append(p.localisationInit)
        nbJoueurs+=1
    emplacements=set(emplacements)
    emplacementsMaisons=set(ferme.tousLes('maison'))
    
    nouveauNe=Personnage(emplacementsMaisons.difference(emplacements).pop(),nbJoueurs+1,joueur.couleur)
    carte.mettrePersonnage(nouveauNe)
    nouveauNe.consomationNourriture=1
    joueur.personnagesPlaces.append(nouveauNe)
    
    choixAmenagementMineur()
    
    

    
        
def jePeuxRenover(partie):
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

class Partie(object):
    
    def __init__(self):
        self._offset=16
        self.plateau = dict()
        self.joueurs = dict()
        self.quiJoue=0
        self.nombreJoueurs=0
        self.premierJoueur=0
        self.quiAFini=[]
        self.listeReponse=[]
        self.streamName=""
        self.messagesPrincipaux=[]
        self.choixPossibles=[] #on garde ça en memoire
        self.phraseChoixPossibles="" #on garde ça en memoire
        self.sujet="" #on garde ça en memoire
        
    #je separe la fonction d'init... a cause de save/load
    #on a besoin de creer un objet partie sans tout réinitialiser
    def initialiser(self,nombreJoueurs,listeReponse,streamName=""):   
        print("sn:",streamName) 
        self.nombreJoueurs=nombreJoueurs
        self.streamName=streamName
        self.listeReponse=listeReponse       
        self._initJoueurs()       
        self.initOrdre()
        (positionTourbes,positionForets)=self.genererCourDeferme()
        self.faireCourDeferme(positionTourbes,positionForets)      
        self.draft()
        self.actionSurTours=self.faireActionSurTours()
        self._genererPlateau(nombreJoueurs)    
            
        
    def _initJoueurs(self):

        
        for j in range(self.nombreJoueurs):

            (n,c)=example[j]
            self.joueurs[j]=Joueur(partie=self,id=j,nom=n,couleur=c)


        
    def _genererPlateau(self,nombre):
        self.plateau["cases"]=dict()
        self.plateau["actionsSpeciales"]=dict()
        self.plateau["tour"]=1

        if nombre==2:
            self.plateau["cases"][1]=CarteAction(self,"","toto",visible=False)
            self.plateau["cases"][2]=CarteAction(self,"","toto",visible=False)
            self.plateau["cases"][3]=CarteAction(self,"","toto",visible=False)
            self.plateau["cases"][4]=CarteAction(self,"","toto",visible=False)
            self.plateau["cases"][5]=CarteAction(self,"","toto",visible=False)
            self.plateau["cases"][6]=CarteAction(self,"","toto",visible=False)        
        elif nombre ==3:
            self.plateau["cases"][1]=CarteAction(self,"","toto",visible=False)
            self.plateau["cases"][2]=CarteAction(self,"","toto",visible=False)
            self.plateau["cases"][3]=CaseAppro(self,"1 argile","toto",{'a':-1},visible=True)
            self.plateau["cases"][4]=CaseAppro(self,"2 bois","toto",{'b':-2},visible=True)
            self.plateau["cases"][5]=CarteAction(self,"Roseau ou Pierre + pn","toto",possibilites=fct.possibiliteRoseauPnOuPierrePn,effet=fct.roseauPnOuPierrePn,visible=True)
            self.plateau["cases"][6]=CarteAction(self,"1 savoir faire pour 2 pn","toto",cout={'n':2},visible=True)       
        elif nombre==4:
            self.plateau["cases"][1]=CaseAppro(self,"Spectacle","toto",{'n':-1},visible=True)
            self.plateau["cases"][2]=CarteAction(self,"1 savoir faire pour 1 ou 2 pn","toto",cout=fct.coutSavoirFaire2,visible=True)
            self.plateau["cases"][3]=CaseAppro(self,"2 argiles","toto",{'a':-2},visible=True)
            self.plateau["cases"][4]=CaseAppro(self,"2 bois","toto",{'b':-2},visible=True)
            self.plateau["cases"][5]=CaseAppro(self,"1 bois","toto",{'b':-1},visible=True)
            self.plateau["cases"][6]=CarteAction(self,"Roseau pierre pn","toto",cout={'n':-1,'p':-1,'r':-1},visible=True)
        elif nombre ==5:
            self.plateau["cases"][1]=CaseAppro(self,"Construction d'un pièce ou Spectacle","toto",{'n':-1},possibilites=fct.possibiliteConstructionOuSpectacle,effet=fct.constructionOuSpectacle,visible=True)
            self.plateau["cases"][2]=CarteAction(self,"1 savoir faire pour 1 ou 2 pn ou Naissance","toto",condition=fct.jePeuxJouerSavoirFaireOuNaissance,possibilites=fct.possibiliteSavoiFaireOuNaissance,effet=fct.savoiFaireOuNaissance,visible=True)
            self.plateau["cases"][3]=CaseAppro(self,"3 argiles","toto",{'a':-3},visible=True)
            self.plateau["cases"][4]=CaseAppro(self,"4 bois","toto",{'b':-4},visible=True)
            self.plateau["cases"][5]=CarteAction(self,"Bétail","toto",visible=True,possibilites=fct.possibiliteBetail,effet=fct.betail)
            self.plateau["cases"][6]=CaseAppro(self,"Roseau pierre bois","toto",{'r':-1},cout={'b':-1,'p':-1},visible=True)        #il y a 30 case
        #6 1eres sont celles qui dependent du nombre de joueur
        #

        self.plateau["cases"][7]=CarteAction(self,"Construction de pièce et/ou d'étable","toto",visible=True,condition=fct.jePeuxFaireConstructionDePieceEtOuEtable,effet=fct.planConstructionDePieceEtOuEtable,possibilites=fct.demanderPlanConstructionDePieceEtOuEtable)
        self.plateau["cases"][8]=CarteAction(self,"Premier joueur et aménagement mineur","toto",visible=True,possibilites=fct.possibilitesAmenagementMineur,effet=fct.choixAmenagementMineur)
        self.plateau["cases"][9]=CarteAction(self,"1 céréale","toto",cout={'c':-1},visible=True)
        self.plateau["cases"][10]=CarteAction(self,"Labourage d'un champ","toto",visible=True,effet=fct.labourage,possibilites=fct.possibilitesLabourage)
        self.plateau["cases"][11]=CarteAction(self,"1 savoir faire","toto",cout=fct.coutSavoirFaire1,visible=True)
        self.plateau["cases"][12]=CarteAction(self,"Journalier","toto",cout={'n':-2},visible=True)
        self.plateau["cases"][13]=CaseAppro(self,"3 bois ","toto",{'b':-3},visible=True)
        self.plateau["cases"][14]=CaseAppro(self,"1 argile","toto",{'a':-1},visible=True)
        self.plateau["cases"][15]=CaseAppro(self,"1 roseau","toto",{'r':-1},visible=True)
        self.plateau["cases"][16]=CaseAppro(self,"Pêche ","toto",{'n':-1},visible=True)
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
        for m in deck['majeurs'].keys():
            self.plateau["majeurs"][deck['majeurs'][m]['nom']]=AmenagementMajeur(partie=self,**deck['majeurs'][m])
                    
        
                
         
    def genererCourDeferme(self):
        pTourbes=['b2','b3','b4']
        pForets=['a1','a2','a3','a4','a5']  
        return(pTourbes,pForets)  
    
    def faireCourDeferme(self,positionTourbes,positionForets):
        for j in self.joueurs.keys():
            self.joueurs[j].courDeFerme.initTuiles(positionTourbes,positionForets)
        
    def faireActionSurTours(self):
        ordreActions={}
        
        ordreActions[1]=CarteAction(self,'Aménagement majeur ou mineur','toto',effet=fct.choixAmenagementMineurOuMajeur,possibilites=fct.possibilitesAmenagementMineurOuMajeur)
        ordreActions[2]=CarteAction(self,'Cloture','toto',effet=cloture,visible=False)
        ordreActions[3]=CaseAppro(self,'1 mouton','toto',{'m':-1},visible=False)
        ordreActions[4]=CarteAction(self,'Semaille et/ou cuisson de pain','toto',visible=False,possibilites=fct.demanderPlanSemailleEtOuCuisson,effet=fct.planSemailleEtOuCuisson,condition=fct.jePeuxFaireSemailleEtOuCuisson)
        ordreActions[5]=CarteAction(self,'Naissance puis aménagement mineur','toto',visible=False,effet=naissancePuisMineur,condition=fct.jePeuxNaitre)
        ordreActions[6]=CarteAction(self,'Rénovation puis aménagement majeur','toto',visible=False,effet=renoPuisMajeur,condition=jePeuxRenover)
        ordreActions[7]=CaseAppro(self,'1 pierre','toto',{'p':-1},visible=False)
        ordreActions[8]=CaseAppro(self,'1 légume','toto',{'l':-1},visible=False)
        ordreActions[9]=CaseAppro(self,'1 sanglier','toto',{'s':-1},visible=False)
        ordreActions[10]=CaseAppro(self,'1 boeuf','toto',{'b':-1},visible=False)
        ordreActions[11]=CaseAppro(self,'1 pierre','toto',{'p':-1},visible=False)
        ordreActions[12]=CarteAction(self,'Labourage semaille','toto',effet=labourageSemaille,visible=False)
        ordreActions[13]=CarteAction(self,'Naissance même sans pièce libre','toto',effet=naissanceSansPieceLibre,visible=False)
        ordreActions[14]=CarteAction(self,'Rénovation puis cloture','toto',effet=renoPuisCloture,visible=False)
        return ordreActions
                    
    def initOrdre(self):
        pass
    
    
    def draft(self):
        pass
    
    
    def avancerJusquaLaProchaineInterraction(self):
        pass
    
    
    def demarragePartie(self):
        #boucle infinie
        print("début de la partie")
        self.messagesPrincipaux.append("début de la partie")
    
                
    def demarrageTour(self):


        print("début du tour : {}".format(self.plateau['tour']))
        self.messagesPrincipaux.append("début du tour : {}".format(self.plateau['tour']))
        #on reappro les cases
        
        self.plateau['cases'][self._offset+self.plateau['tour']].visible=True
        
#         ##############"TO DEBUG
#         for c in self.plateau['cases'].keys():
#             self.plateau['cases'][c].visible=True
        ##############"TO DEBUG

        
        for i in range(1,self._offset+self.plateau['tour']+1):
            self.plateau['cases'][i].reappro()
                     
                     
        print(self.printCasesVisibles())     
        self.quiJoue=self.premierJoueur        
        
    def initChoix(self):
        print('INIT CHOIX!!')
        sujet=self.joueurQuiJoue()
        self.sujet=sujet
        self.choixPossibles=[]
        self.phraseChoixPossibles="QUE VOULEZ VOUS FAIRE?"
        sujet.possibilites()
  
        
    def joueurQuiJoue(self):    
        return self.joueurs[self.quiJoue]
        
    def joueurSuivant(self):
        if self.joueurQuiJoue().jaiFini():
            self.quiAFini.append(self.quiJoue)
        if (len(self.quiAFini)==self.nombreJoueurs):
            return -1 #le tour est fini
        else:
            self.quiJoue=(1 + self.quiJoue )%self.nombreJoueurs
            if(self.joueurQuiJoue().jaiFini()):
                self.quiJoue=(1 + self.quiJoue )%self.nombreJoueurs  
                return self.joueurSuivant()
            else:
                return self.quiJoue
            
            
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
    
    def jouer(self,choix):
        if choix==-1:
            self.possibilitesJoueur()
        else:
            #ACTION CONFIRMEE
            #si c'est un action ou on ne joue pas de pion (as ou utilisation d'un foyer)
            if self.casesJouables[choix].sansPion :
                self.casesJouables[choix].activer()
                self.mettreAJourLesRessources(self.casesJouables[choix].cout)
                self.listerPossibilites()
#     TODO        elif self.casesJouables[choix] in actionsSpeJouables:
#                 pass
            else:
            
                personnage=self.joueurs[self.quiJoue].personnages.pop()
                self.joueurs[self.quiJoue].personnagesPlaces.append(personnage)    
                caseJouee=self.casesJouables[choix].jouer(personnage)
                print('je joue sur la case:',caseJouee)
                self.joueurs[self.quiJoue].mettreAJourLesRessources(caseJouee.cout)
                self.joueurs[self.quiJoue].tourFini= len(self.joueurs[self.quiJoue].personnages)==0
                if self.joueurs[self.quiJoue].tourFini:
                    self.quiAFini.append(self.quiJoue)
                    

    def finDuTour(self):
        if self.plateau['tour']==14:
            print("FIN DE PARTIE")
            return -1
        else:
            for id in self.joueurs.keys():
                while(len(self.joueurs[id].personnagesPlaces)>0):
                    p=self.joueurs[id].personnagesPlaces.pop()
                    p.retourMaison()
                    self.joueurs[id].personnages.append(p)
             
            self.quiAFini.clear()
            self.plateau['tour']+=1
        return self.plateau['tour']

    
    def printCasesVisibles(self):
        vis=[]
        for i in range(1,31):
            if self.plateau['cases'][i].visible:
                vis.append(self.plateau['cases'][i].nom)
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
        for c in range(10):
            dico={
                'nom':"Majeur",
                'type':"Majeur",
                }
            cases.append(dico.copy())
        for c in self.plateau["cases"].keys():
            dico={
                'nom':self.plateau["cases"][c].nom,
                'type':"Action",
                'class': "" if self.plateau["cases"][c].visible else "disabled",
                }
            ressources=""
            for t in self.plateau["cases"][c].cout.keys():
                if self.plateau["cases"][c].cout[t]<0:
                    ressources+="{} x {}".format(util.short2Long[t],-self.plateau["cases"][c].cout[t])    
            dico['res']=ressources
            dico['perso']=[]
            for perso in self.plateau["cases"][c].occupants:
                dico['perso'].append(perso.couleur)

            
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
        dico["listeReponse"]=self.listeReponse        
        return json.dumps(dico)

    
    
    def load(self):
        pass

