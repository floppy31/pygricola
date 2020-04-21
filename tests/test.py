import random
import unittest

import pygricola.util as util
from pygricola.partie import Partie,avancer
import pygricola.fonctionsPlateau as fct
from pygricola.carte import Carte,CarteAction,AmenagementMajeur,AmenagementMineur,deck,SavoirFaire
import pygricola.util as util

import logging

logger = logging.getLogger('root')
fmt="##%(levelname)s## %(funcName)s():%(lineno)i: %(message)s"
logging.basicConfig(format=fmt)
logger.setLevel(logging.DEBUG)



def simulerPartieOLD(listeRep,p):
        p.demarragePartie()
        p.demarrageTour()        
        p.initChoix()
        p.sujet.possibilites()
        while len(listeRep)>0:
            id=listeRep.pop(0)
            compteur=3
            while type(p.choixPossibles)==int and compteur>0:
                if p.choixPossibles==-1:
                    p.sujet.possibilites()
                else:
                    eeee
                
                if p.choixPossibles==-1:
                    suivant=p.joueurSuivant()
                    p.initChoix()
                    if suivant==-1:
                        logger.debug('--------simulerPartie: fin du tour')
                        p.finDuTour()
                        p.traiterLesHooks()
                        p.demarrageTour()  
                        p.traiterLesHooks()    
                
                compteur-=1
                print('\n\n\n\n\FFFF',p.choixPossibles)
            print('\n\n\n\n\nKKKKKKKKKKK',id,p.choixPossibles)
            p.jouerUid(id)
            p.traiterLesHooks()  
        return p   


def simulerPartie(listeRep,p,faireInit=True):
    if faireInit: 
        p.demarragePartie()
        p.demarrageTour()        
        p.pointerSurPremier()
    
    for id in listeRep:
        p.log.info("\n\n\n\n\n\n================ID: {} \n========{}\n\n".format(id,p.pointeur))
        pointeur=avancer(p,id)
    if len(p.hooks)>0:
        ddddd
    return p   



class FonctionsPlateau(unittest.TestCase):
    
    
    #TODO: tester avec loge et cheval
    def test_AsAbattre(self):
        #1 ère fois
        p=Partie(logger)
        p.initialiser(3)  
        joueur=p.joueurs[0]
        joueur2=p.joueurs[1]
        joueur3=p.joueurs[2]
        joueur.ressources=util.rVide()
        joueur2.ressources=util.rVide()
        for CAS in p.plateau["actionsSpeciales"]:
            for l in CAS.listeActionSpeciale:
                if l.uid=='b5':
                    carte=l
        p.pointeur.sujet=carte
        carte.jouer()
        #pas encore joué
        self.assertTrue(util.sontEgaux(joueur.ressources,{'b':0}))
        #5 forets au début
        self.assertTrue(len(p.choixPossibles)==5)
        caseAbattue=p.choixPossibles[0]
        p.sujet.effet(0,p.choixPossibles)   
        self.assertTrue(util.sontEgaux(joueur.ressources,{'b':2}))
        
        #pas de Pn pour racheter
        self.assertFalse(joueur.jePeuxFaireActionSpeciale(carte))
        joueur.ressources['n']=2
        #toujours pas car je l'ai déja prise
        self.assertFalse(joueur.jePeuxFaireActionSpeciale(carte))
        p.pointerSurJoueurSuivant()
        #joueur2 sans pn
        self.assertFalse(joueur2.jePeuxFaireActionSpeciale(carte))        
        joueur2.ressources['n']=2
        self.assertTrue(joueur2.jePeuxFaireActionSpeciale(carte))  
        #si je me vire toutes mes foret je ne peux plus
        for tuile in joueur2.courDeFerme.tousLes('foret'):
            joueur2.courDeFerme.etat[tuile].type="vide"
        self.assertFalse(joueur2.jePeuxFaireActionSpeciale(carte))  
        #je remets la derniere foret
        joueur2.courDeFerme.etat[tuile].type="foret"
        #je mets la loge devant moi
        #je me prends un cheval
        joueur2.ressources['h']=1
        joueur2.cartesDevantSoi["M6"]=AmenagementMajeur(p,'M6',**deck['majeurs']['M6'])
        
        self.assertTrue(joueur2.jePeuxFaireActionSpeciale(carte)) 
        carte.jouer()
        p.sujet.effet(0,p.choixPossibles)         
        self.assertTrue(util.sontEgaux(joueur2.ressources,{'b':4,'h':1}))
        p.pointerSurJoueurSuivant()
        joueur3.ressources['n']=10
        #impossible de racheter  
        self.assertFalse(joueur3.jePeuxFaireActionSpeciale(carte)) 
        p.finDuTour()
        #maintenant je peux
        self.assertTrue(joueur3.jePeuxFaireActionSpeciale(carte)) 
    
    def test_AsCouperBruler(self):
        #1 ère fois
        p=Partie(logger)
        p.initialiser(3)  
        joueur=p.joueurs[0]
        joueur2=p.joueurs[1]
        joueur3=p.joueurs[2]
        joueur.ressources=util.rVide()
        joueur2.ressources=util.rVide()
        for CAS in p.plateau["actionsSpeciales"]:
            for l in CAS.listeActionSpeciale:
                if l.uid=='b6':
                    carte=l
        p.pointeur.sujet=carte
        carte.jouer()
        #pas encore joué
        self.assertTrue(joueur.courDeFerme.compter('champ')==0)
        #5 forets au début
        self.assertTrue(len(p.choixPossibles)==5)
        
        p.sujet.effet(0,p.choixPossibles)   
        self.assertTrue(joueur.courDeFerme.compter('champ')==1)
        self.assertTrue(joueur.courDeFerme.compter('foret')==4)
        #pas de Pn pour racheter
        self.assertFalse(joueur.jePeuxFaireActionSpeciale(carte))
        joueur.ressources['n']=2
        #toujours pas car je l'ai déja prise
        self.assertFalse(joueur.jePeuxFaireActionSpeciale(carte))
        p.pointerSurJoueurSuivant()
        #joueur2 sans pn
        self.assertFalse(joueur2.jePeuxFaireActionSpeciale(carte))        
        joueur2.ressources['n']=2
        self.assertTrue(joueur2.jePeuxFaireActionSpeciale(carte))  
        
        #si je me vire toutes mes forets je ne peux plus
        for tuile in joueur2.courDeFerme.tousLes('foret'):
            joueur2.courDeFerme.etat[tuile].type="vide"
        self.assertFalse(joueur2.jePeuxFaireActionSpeciale(carte))  
        #je remets une foret en A5
        joueur2.courDeFerme.etat['A5'].type="foret"
        #je mets un champs en C5
        joueur2.courDeFerme.etat['C5'].type="champ"
        carte.jouer()
        #les champs ne se touchent pas
        self.assertFalse(joueur2.jePeuxFaireActionSpeciale(carte)) 
        joueur2.courDeFerme.etat['B5'].type="champ"
        #il faut remettre à jour
        carte.jouer()
                            
        self.assertTrue(joueur2.jePeuxFaireActionSpeciale(carte)) 
        carte.jouer()
        self.assertTrue(p.choixPossibles==["A5"]) 
        

    def test_AsCheval(self):
        #2,3,4,5 joueurs
        p=Partie(logger)
        p.initialiser(2)      
        partieSimulee=simulerPartie(['b0'],p)
        self.assertTrue(p.plateau["actionsSpeciales"][0].etat==0)
    
        #plus de place
        
        #rachat      
        
        pass   
    def test_AsFoireDuTravail(self):
        p=Partie(logger)
        p.initialiser(3)  
        joueur=p.joueurs[0]
        joueur.ressources=util.rVide()
        for CAS in p.plateau["actionsSpeciales"]:
            for l in CAS.listeActionSpeciale:
                if l.uid=='b3':
                    carte=l        
        #possibilitesVides
        carte.possibilites()
        self.assertTrue(len(p.choixPossibles)==0)
        #je me mets un mineur en main et les ressources pour l'acheter
        joueur.cartesEnMain.append(AmenagementMineur(p,'m0',**deck['mineurs']['m0']))
        carte.possibilites()
        self.assertTrue(len(p.choixPossibles)==0)
        joueur.ressources['a']=1
        carte.possibilites()
        #je peux pas payer le feu
        self.assertTrue(len(p.choixPossibles)==0)
        
        joueur.ressources['f']=1
        carte.possibilites()
        #maintenant ok
        self.assertTrue(len(p.choixPossibles)==1)
        joueur.ressources['f']=0
        joueur.ressources['b']=1
        #on teste avec 1 bois
        carte.possibilites()
        self.assertTrue(len(p.choixPossibles)==1)

        #on la joue
        carte.effet(0,p.choixPossibles) 
        self.assertTrue(p.choixPossibles==-1)
        self.assertTrue(util.sontEgaux(joueur.ressources,util.rVide()))
        self.assertTrue(carte.carteQuiMePorte.etat==joueur.id)
    
    def test_AsTravailClandestin(self):
        p=Partie(logger)
        p.initialiser(3)  
        joueur=p.joueurs[0]
        joueur.ressources=util.rVide()
        for CAS in p.plateau["actionsSpeciales"]:
            for l in CAS.listeActionSpeciale:
                if l.uid=='b4':
                    carte=l        
        #possibilitesVides
        carte.jouer()
        self.assertTrue(len(p.choixPossibles)==0)
        #si je me mets 1 pn et 1 bois c'est idem
        joueur.ressources['b']=1
        joueur.ressources['n']=1
        carte.jouer()
        self.assertTrue(len(p.choixPossibles)==0)
        #mais avec 2 argiles c'est ok
        joueur.ressources['a']=2
        carte.jouer()
        self.assertTrue(len(p.choixPossibles)==1)        
        #on la joue
        carte.effet(0,p.choixPossibles) 
        self.assertTrue(p.choixPossibles==-1)
        self.assertTrue(util.sontEgaux(joueur.ressources,util.rVide()))               


    
    def test_AsTourbe(self):
        #1 ère fois
        p=Partie(logger)
        p.initialiser(3)  
        joueur=p.joueurs[0]
        joueur2=p.joueurs[1]
        joueur3=p.joueurs[2]
        joueur.ressources=util.rVide()
        joueur2.ressources=util.rVide()
        for CAS in p.plateau["actionsSpeciales"]:
            for l in CAS.listeActionSpeciale:
                if l.uid=='b7':
                    carte=l
        p.pointeur.sujet=carte
        carte.jouer()
        #pas encore joué
        self.assertTrue(util.sontEgaux(joueur.ressources,{'f':0}))
        #3 tourbes au début
        self.assertTrue(len(p.choixPossibles)==3)
        
        p.sujet.effet(0,p.choixPossibles)   
        self.assertTrue(util.sontEgaux(joueur.ressources,{'f':3}))
        
        #pas de Pn pour racheter
        self.assertFalse(joueur.jePeuxFaireActionSpeciale(carte))
        joueur.ressources['n']=2
        #toujours pas car je l'ai déja prise
        self.assertFalse(joueur.jePeuxFaireActionSpeciale(carte))
        p.pointerSurJoueurSuivant()
        #joueur2 sans pn
        self.assertFalse(joueur2.jePeuxFaireActionSpeciale(carte))        
        joueur2.ressources['n']=2
        self.assertTrue(joueur2.jePeuxFaireActionSpeciale(carte))  
        #si je me vire toutes mes tourbes je ne peux plus
        for tuile in joueur2.courDeFerme.tousLes('tourbe'):
            joueur2.courDeFerme.etat[tuile].type="vide"
        self.assertFalse(joueur2.jePeuxFaireActionSpeciale(carte))  
        #je remets la derniere tourbe
        joueur2.courDeFerme.etat[tuile].type="tourbe"
        #je mets le four a toure
        joueur2.cartesDevantSoi["M4"]=AmenagementMajeur(p,'M4',**deck['majeurs']['M4'])        
        self.assertTrue(joueur2.jePeuxFaireActionSpeciale(carte)) 

        carte.jouer()
        p.sujet.effet(0,p.choixPossibles)         
        self.assertTrue(util.sontEgaux(joueur2.ressources,{'f':4}))
        p.pointerSurJoueurSuivant()
        joueur3.ressources['n']=10
        #impossible de racheter  
        self.assertFalse(joueur3.jePeuxFaireActionSpeciale(carte)) 
        p.finDuTour()
        #maintenant je peux
        self.assertTrue(joueur3.jePeuxFaireActionSpeciale(carte)) 
    
    def test_Betail(self):
        p=Partie(logger)
        p.initialiser(5)  
        joueur=p.joueurs[0]
        joueur.ressources=util.rVide()
        betail=CarteAction(p,"a38",visible=True,possibilites=fct.possibiliteBetail,effet=fct.betail)
        p.pointeur.sujet=betail
        betail.jouer()
        self.assertTrue(len(p.choixPossibles)==2)
        p.joueurs[0].ressources['n']=1 
        betail.jouer()
        self.assertTrue(len(p.choixPossibles)==3)
        #test de la carte 
        joueur.ressources['n']=1
        joueur.ressources['m']=0
        joueur.ressources['s']=0
        joueur.ressources['b']=0
        
        #test mouton pn
        p.sujet.effet(0,p.choixPossibles)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'n':2,'m':1}))
        betail.jouer()
        #test beuf contre pn
        p.sujet.effet(2,p.choixPossibles)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'n':1,'m':1,'v':1}))    
            
    def test_ConstructionDePieceEtOuEtable(self):
        p=Partie(logger)
        p.initialiser(1)  
        joueur=p.joueurs[0]
        joueur.ressources=util.rVide()   
        carte=p.plateau["cases"][7]
        
        joueur.possibilites()        
        carteEstDispo=False
        for c in p.choixPossibles:
            if c.uid==carte.uid:
                carteEstDispo=True
        self.assertFalse(carteEstDispo)
        #si on se mets 2 bois alors elle doit être dispo
        joueur.ressources['b']=2
        joueur.possibilites()        
        carteEstDispo=False
        for c in p.choixPossibles:
            if c.uid==carte.uid:
                carteEstDispo=True
        self.assertTrue(carteEstDispo)      
        #on va faire joujou avec le plan de construction
        joueur.ressources['b']=18 #on veut aller jusqu'a 4 étables et 2 pièces
        joueur.ressources['r']=4
        ferme=joueur.courDeFerme
        ferme.etat["A1"].type="vide"
        ferme.etat["A2"].type="vide"
        ferme.etat["B2"].type="tourbe"
        ferme.etat["C2"].type="vide"
        carte.jouer()
        self.assertTrue(p.choixPossibles=='inputtext')
        inputTextNonValables=["toto","A1:f","B1:E","B1:P","B2:P","C2:P,C3:P,C4:P","C2:P,C4:P",
                              "A1:E,A2:E,C4:E,C2:E,C3:E"]
        
        for it in inputTextNonValables:
            p.sujet.effet(it,p.choixPossibles) 
            self.assertTrue(p.choixPossibles=='inputtext') 
        inputTextValablesEtRessources=[
            ("A1:P",{'b':13,'r':2}),#1 pièce
            ("A1:P,C2:P",{'b':8,'r':0}),#2 pièce
            ("A1:P,C2:E",{'b':11,'r':2}),#1 pièce, 1 etable
            ]
        for it,reste in inputTextValablesEtRessources:
            #je me remets les ressources
            joueur.ressources['b']=18
            joueur.ressources['r']=4   
            #et la ferme    
            ferme.etat["A1"].type="vide"
            ferme.etat["A2"].type="vide"
            ferme.etat["B2"].type="tourbe"
            ferme.etat["C2"].type="vide"  

            p.sujet.effet(it,p.choixPossibles) 
            self.assertTrue(p.choixPossibles==-1) 
            self.assertTrue(util.sontEgaux(joueur.ressources,reste))
            #on remets le personnage artificiellement 
            perso=joueur.personnagesPlaces.pop()
            joueur.personnages.append(perso)
            ferme.mettrePersonnage(perso,perso.localisationInit) 
            p.pointeur.sujet=carte
               

       
    def test_ConstructionOuSpectacle(self):

        #je ne la vois qu'a 5
        for njoueurs in range(1,5):
            p=Partie(logger)
            p.initialiser(njoueurs)  
            joueur=p.joueurs[0]
            joueur.ressources=util.rVide()   
            carte=p.plateau["cases"][1]
            self.assertFalse(carte.uid=="a34")
        p=Partie(logger)
        p.initialiser(5)  
        joueur=p.joueurs[0]
        joueur.ressources=util.rVide()   
        carte=p.plateau["cases"][1]
        self.assertTrue(carte.uid=="a34")        

        joueur.possibilites()        
        carteEstDispo=False
        for c in p.choixPossibles:
            if c.uid==carte.uid:
                carteEstDispo=True
        #on peut toujours faire spectacle
        self.assertTrue(carteEstDispo)
        
        #je ne peux faire que spectacle
        p.pointeur.sujet=carte
        carte.jouer()
        self.assertTrue(len(p.choixPossibles)==1)
        self.assertTrue(p.choixPossibles[0]=="u6")
        joueur.ressources['b']=5 
        joueur.ressources['r']=2        
        ferme=joueur.courDeFerme
        ferme.etat["A1"].type="foret"
        ferme.etat["B2"].type="tourbe"
        ferme.etat["C2"].type="foret"  
        joueur.possibilites()
        carte.jouer()
        #on n'a pas de place pour la maison
        self.assertTrue(len(p.choixPossibles)==1)
        self.assertTrue(p.choixPossibles[0]=="u6")        
        #par contre si je fais de la place
        ferme.etat["A1"].type="vide"
        ferme.etat["B2"].type="vide"
        ferme.etat["C2"].type="vide"
        joueur.possibilites()
        carte.jouer()
        self.assertTrue(len(p.choixPossibles)==4)  #spectacle + 3 possibilites
        sujet=carte
        caseChoisie=p.choixPossibles[1][1] 
        p.sujet.effet(1,p.choixPossibles) 
        self.assertTrue(p.choixPossibles==-1)
        self.assertTrue(util.sontEgaux(joueur.ressources,util.rVide() ))
        self.assertFalse(carte.libre)

    def test_Labourage(self):
        p=Partie(logger)
        p.initialiser(1)  
        joueur=p.joueurs[0]
        joueur.ressources=util.rVide()
        
        carte=p.plateau["cases"][10] #bof mais a priori c'est elle         #1er labour
        carte.jouer()
        self.assertTrue(len(p.choixPossibles)==5)# 5 endroits vides au début
        self.assertTrue(joueur.courDeFerme.compter('champ')==0)
        p.sujet.effet(0,p.choixPossibles) 
        self.assertTrue(joueur.courDeFerme.compter('champ')==1)
        self.assertTrue(p.choixPossibles==-1)
        
        
        

    def test_Naissance(self):
        p=Partie(logger)
        p.initialiser(1)  
        joueur=p.joueurs[0]
        #test de la carte naissance puis aménagement mineur
        nPuisMineur=CarteAction(p,"a14",visible=False,possibilites=fct.possibilitesAmenagementMineur,effet=fct.naissancePuisMineur,condition=fct.jePeuxNaitre)
        p.pointeur.sujet=nPuisMineur
        self.assertFalse(fct.jePeuxNaitre(p,nPuisMineur))
        #je rajoute une maison 
        joueur.courDeFerme.etat["A1"].type="maisonBois"
        self.assertTrue(fct.jePeuxNaitre(p,nPuisMineur))
        nPuisMineur.jouer()
        self.assertTrue(p.choixPossibles==['u3'])#ne peux pas jouer de mineur
        p.sujet.effet(0,p.choixPossibles)
        #je ne peux plus naitre
        self.assertFalse(fct.jePeuxNaitre(p,nPuisMineur))
        joueur.courDeFerme.etat["A2"].type="maisonBois"
        #TODO
        #ajouter un mineur et le jouer avec naissance puis mineur
        #puis ajouter une piece et faire savoir faire ou naissance
        #avant le tour 5 --> faux
        #on change le tour
        #---> vrai

    def test_Majeurs(self):
        #visibilité
        p=Partie(logger)
        p.initialiser(3)  
        joueur=p.joueurs[0]
        joueur.ressources=util.rVide()
        
        carte=p.plateau["cases"][17] #bof mais a priori c'est elle 
        carte.jouer()
        #pas de ressources pas de possibilites
        self.assertTrue(len(p.choixPossibles)==0)
        #on teste la condition possibilites non vide
        self.assertFalse(joueur.jeRemplisLesConditions(carte.condition))
        #avec 2 argiles je peux faire seulement le foyer à 2
        joueur.ressources['a']=2
        self.assertTrue(joueur.jeRemplisLesConditions(carte.condition))
        carte.jouer()
        self.assertTrue(len(p.choixPossibles)==1)
        self.assertTrue(p.choixPossibles[0].uid=="M0")
        sujet=carte
        #je le fais
        p.sujet.effet(0,p.choixPossibles)   
        #peux plus rejouer
        self.assertTrue(p.choixPossibles==-1) 
        #je n'ai plus de ressource
        self.assertTrue(util.sontEgaux(joueur.ressources,{}))
        #j'ai bien le majeur joué devant moi
        self.assertTrue(joueur.aiJeJoue('M0'))  
        #si je pouvais re jouer alors je ne pourrais pas activer le foyer 
        joueur.possibilites()    
        activable=False
        sujet=util.findCarte(p.choixPossibles,"M0")
        self.assertTrue(sujet==None)     
        #mais avec un mouton si!
        joueur.ressources['m']=1
        joueur.possibilites()    
        sujet=util.findCarte(p.choixPossibles,"M0")

        self.assertTrue(sujet.uid=="M0")     
        #que puis-je activer
        sujet.possibilites()
        self.assertTrue(p.choixPossibles[0].uid=="um") #cuire un mouton
        p.sujet.effet(0,p.choixPossibles)   
        #on a gagné 2 pn et perdu le mouton
        self.assertTrue(util.sontEgaux(joueur.ressources,{'n':2}))
        #on passe au joueur suivant
        p.pointerSurJoueurSuivant()
        joueur=p.joueurs[1]
        joueur.possibilites() 
        joueur.ressources=util.rVide()
        joueur.ressources['a']=2
        carte.jouer()
        self.assertFalse(joueur.jeRemplisLesConditions(carte.condition))        
        #par contre si je me mets 1 argile en plus je peux 
        joueur.ressources['a']=3
        self.assertTrue(joueur.jeRemplisLesConditions(carte.condition))  
        #si je me mets une pierre en plus
        joueur.ressources['p']=1
        #je peux jouer 4 trucs (foyer à 3, four a tourbe, four en brique, et abatoir à chevaux 1
        joueur.possibilites() #on réinitialise
        carte.jouer()
        uidPossibles=["M1","M2","M4","M14"]
        for am in p.choixPossibles:
            uidPossibles.remove(am.uid)
        self.assertTrue(len(uidPossibles)==0)  
        
        

        
    def test_RoseauPnOuPierrePn(self):
        p=Partie(logger)
        p.initialiser(3)  
        joueur=p.joueurs[0]
        joueur.ressources=util.rVide()
        rPnOuPPn=CarteAction(p,"a26",possibilites=fct.possibiliteRoseauPnOuPierrePn,effet=fct.roseauPnOuPierrePn,visible=True)
        p.pointeur.sujet=rPnOuPPn
        rPnOuPPn.jouer()
        p.sujet.effet(1,p.choixPossibles)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'n':1,'r':1}))
        
    def test_SemailleCuisson(self):
        #pas de céréale ni cuisson
        p=Partie(logger)
        p.initialiser(1)  
        joueur=p.joueurs[0]
        joueur.ressources=util.rVide()   
        for ind,c in p.plateau["cases"].items():
            if c.uid=="a13":
                #au debut la case est pas dispo
                self.assertFalse(c.visible)
                #mais bon on la rend visible
                c.visible=True
                carte=c
                break
        #la carte à beau être visible, si je peux rien en faire 
        #il ne faut pas qu'elle apparaisse
        joueur.possibilites()        
        carteEstDispo=False
        for c in p.choixPossibles:
            if c.uid==carte.uid:
                carteEstDispo=True       
        self.assertFalse(carteEstDispo)
        
        #si j'ai un champ 
        ferme=joueur.courDeFerme
        ferme.etat["A1"].type="champ"   
        #et un four non plus (la je mets tous les fours artificiellement
        for uid,v in p.plateau["majeurs"].items():
            if 'cuissonPain' in v.option.keys():
                joueur.cartesDevantSoi[uid]=v
                
        joueur.possibilites()        
        carteEstDispo=False
        for c in p.choixPossibles:
            if c.uid==carte.uid:
                carteEstDispo=True       
        self.assertFalse(carteEstDispo)
        
        #mais si je prends des céréales alors là je peux!!
        joueur.ressources['c']=2
        joueur.possibilites()        
        carteEstDispo=False
        for c in p.choixPossibles:
            if c.uid==carte.uid:
                carteEstDispo=True       
        self.assertTrue(carteEstDispo)        
        carte.jouer()

        self.assertTrue(p.choixPossibles=='inputtext')
        ferme.etat["A1"].type="champ"   
        ferme.etat["A2"].type="champ"   
        ferme.etat["A3"].type="champ"   
        ferme.etat["A3"].ressources['c']=1  
        ferme.etat["B3"].type="tourbe" 
        inputTextNonValables=["toto","A1:f","A1:l","B3:c","A1:c,c:2","A3:c"]
        
        for it in inputTextNonValables:
            p.sujet.effet(it,p.choixPossibles) 
            self.assertTrue(p.choixPossibles=='inputtext') 
            
        joueur.ressources['c']=5
        joueur.ressources['l']=5
        
        inputTextValablesEtRessources=[
            ("A1:c",{'c':4,'l':5},{'A1':'3c'}),
            ("A1:l,c:2",{'c':3,'l':4,'n':9},{'A1':'2l'}),
            ("A1:c,A2:l,c:4",{'c':0,'l':4,'n':16},{'A1':'3c','A2':'2l'}),

            ]
        for it,reste,etatChamp in inputTextValablesEtRessources:
            #je me remets les ressources
            joueur.ressources['c']=5
            joueur.ressources['l']=5
            joueur.ressources['n']=0
            #et la ferme    
            ferme.etat["A1"].type="champ"   
            ferme.etat["A1"].ressources=util.rVide()
            ferme.etat["A2"].type="champ"   
            ferme.etat["A2"].ressources=util.rVide()
            ferme.etat["A3"].type="champ"   
            ferme.etat["A3"].ressources=util.rVide()
            ferme.etat["B3"].type="tourbe" 
            ferme.etat["B3"].ressources=util.rVide()

            p.sujet.effet(it,p.choixPossibles) 
            self.assertTrue(p.choixPossibles==-1) 
            self.assertTrue(util.sontEgaux(joueur.ressources,reste))
            #on remets le personnage artificiellement 
            perso=joueur.personnagesPlaces.pop()
            joueur.personnages.append(perso)
            ferme.mettrePersonnage(perso,perso.localisationInit) 
            for k,v in etatChamp.items():
                nb=int(v[0])
                type=v[1]
                self.assertTrue(ferme.etat[k].ressources[type]==nb)     
            p.pointeur.sujet=carte
                
      
        #cuisson seule
        #semaille et cuisson
        #test plan dispo ressource etc...
        #test sans cuisson
        pass    
        
    def test_Tour_1(self): 
        listeRep=['a2','b0','b6','A1','b7','B2','a9','a6','a8',]
        p=Partie(logger)
        p.initialiser(2)  
        partieSimulee=simulerPartie(listeRep,p)   
        print() 
        # simuler un tour avec plusieurs joueurs, des nombres différents de personnages
        # fin du tour au bon moment
        
        #tour suivant
        #verif le premier joueur a bien changé
        pass
                
class Util(unittest.TestCase):
    
    
    #TODO: tester avec loge et cheval
    def test_BoisFeu(self):
        r1=util.rVide()
        r1['b']=1
        r2=util.rVide()
        r2['f']=1
        r3=util.rVide()
        r3['b']=3
        r3['f']=3
        r4=util.rVide()
        r4['f']=6     
        result,raison=util.jouable(r1,r1)
        self.assertTrue(result)
        result,raison=util.jouable(r1,r2)
        self.assertTrue(result)
        result,raison=util.jouable(r2,r1)
        self.assertFalse(result)
        result,raison=util.jouable(r3,r4)
        self.assertTrue(result)        
        result,raison=util.jouable(r4,r3)
        self.assertFalse(result)    
        self.assertTrue(util.jouable({'b':1,'f':1},{'b':1})[0])  
        self.assertFalse(util.jouable({'b':1},{'b':1,'f':1})[0])  
        
class PartieDeTest(unittest.TestCase):
    def test_alpha(self):
        listeRep=[ "a2","a9","a8","a5", #fin tour1
                  "b5",'A3', #idem abattre en A3
                  "a5",
                  "a6","a7",'a2',#fin tour 2
                  "a7","a6",
                  ]
        p=Partie(logger)
        p.initialiser(2)  
        partieSimulee=simulerPartie(listeRep,p)
        print(p.joueurs[0].ressources)
        print(p.joueurs[1].ressources)
        self.assertTrue(util.sontEgaux(p.joueurs[0].ressources,{'n':2,'c':2,'r':1,'b':8,'a':1}))
        self.assertTrue(util.sontEgaux(p.joueurs[1].ressources,{'n':8,'a':2,'b':3}))

#     def test_beta(self):
#         listeRep= ['a4','s10','b0','a5','a10','m21'] 
#         p=Partie(logger)
#         p.initialiser(2)  
#         partieSimulee=simulerPartie(listeRep,p)
        
        
    def test_gamma(self):
        listeRep= ['b6', 'A1', 'b0', 'a1', 'u3', 'a5', 'a2', 'a6', 'a5', 'a8', 'a7', 'b6', 'A1', 'a0','a6']
        p=Partie(logger)
        p.initialiser(2)  
        partieSimulee=simulerPartie(listeRep,p)

    def test_delta(self):
        p=Partie(logger)
        p.initialiser(5,draftDict={0:['s27']})
        joueur=p.joueurs[0]  
        listeRep= ['a35','p2', 's27']
        partieSimulee=simulerPartie(listeRep,p)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'n':1}))
        self.assertTrue(joueur.aiJeJoue('s27'))



    def test_piece(self):
        p=Partie(logger)
        p.initialiser(2)  
        joueur=p.joueurs[0]
        joueur.ressources['b']=7
        joueur.ressources['r']=2
        listeRep=['a0','C2:P,C4:E','a9']
        partieSimulee=simulerPartie(listeRep,p) 
        self.assertTrue(util.sontEgaux(joueur.ressources,{'n':2}))
        self.assertTrue(joueur.courDeFerme.compter('maison')==3)
        self.assertTrue(util.sontEgaux(p.joueurs[1].ressources,{'n':4}))
        

    def test_random_a0(self):
        p=Partie(logger)
        p.initialiser(2)
        joueur=p.joueurs[0]
        joueur.ressources['b']=5
        joueur.ressources['r']=2
        listeRep= ['a0','randomPlanConstructionDePieceEtOuEtable']
        partieSimulee=simulerPartie(listeRep,p)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'n':2}))
        self.assertTrue(joueur.courDeFerme.compter('maison')==3)
        
        p=Partie(logger)
        p.initialiser(2)
        joueur=p.joueurs[0]
        joueur.ressources['b']=2
        listeRep= ['a0','randomPlanConstructionDePieceEtOuEtable']
        partieSimulee=simulerPartie(listeRep,p)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'n':2}))
        self.assertTrue(joueur.courDeFerme.compter('etable')==1)        
        
    def test_random_a13(self):
        p=Partie(logger)
        p.initialiser(2)
        joueur=p.joueurs[0]
        joueur.courDeFerme.etat["A1"].type="champ"  
        joueur.courDeFerme.etat["A2"].type="champ" 
        joueur.courDeFerme.etat["A3"].type="champ" 
        joueur.courDeFerme.etat["A4"].type="champ"
        joueur.ressources['c']=2
        joueur.ressources['l']=2
        for num,case in p.plateau["cases"].items():
            if case.uid=='a13':
                case.visible=True        
        listeRep= ['a13','randomPlanSemailleEtOuCuisson']
        partieSimulee=simulerPartie(listeRep,p)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'n':2}))
        
        p=Partie(logger)
        p.initialiser(2)
        joueur=p.joueurs[0]
        joueur.ressources['c']=1
        joueur.poserCarteDevantSoi(p.plateau['majeurs']['M0'],Majeur=True)
        for num,case in p.plateau["cases"].items():
            if case.uid=='a13':
                case.visible=True           
        listeRep= ['a13','randomPlanSemailleEtOuCuisson']
        partieSimulee=simulerPartie(listeRep,p)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'n':4}))
class TestMineurs(unittest.TestCase):
    
    def test_m0(self): 
        p=Partie(logger)
        p.initialiser(2)  
        joueur0=p.joueurs[0]
        joueur1=p.joueurs[1]
        joueur1.ressources['m']=1
        joueur1.cartesEnMain.append(AmenagementMineur(p,'m0',**deck['mineurs']['m0']))
        partieSimulee=simulerPartie(['a2','a7','a5','a1','m0','m0','um'],p)    
        self.assertTrue(util.sontEgaux(joueur0.ressources,{'c':1,'n':4}))
        self.assertTrue(util.sontEgaux(joueur1.ressources,{'n':4}))
        self.assertTrue(p.quiJoue==1)
                        
    def test_m3(self): 
        p=Partie(logger)
        p.initialiser(2)  
        joueur=p.joueurs[0]
        joueur2=p.joueurs[1]
        joueur.ressources=util.rVide()
        joueur.cartesEnMain.append(AmenagementMineur(p,'m3',**deck['mineurs']['m3']))
        joueur.cartesDevantSoi['s24']=SavoirFaire(p,'s24',**deck['savoirFaires']['s24'])
        joueur.cartesDevantSoi['s25']=SavoirFaire(p,'s25',**deck['savoirFaires']['s25'])
        joueur.cartesDevantSoi['s26']=SavoirFaire(p,'s26',**deck['savoirFaires']['s26'])
        joueur.ressources['f']=1
        partieSimulee=simulerPartie(['b3','m3','a2','a6','a7','a5',#fin du tour
                                     'a6',#case ou on a mis la bouffe
                                     ],p)
        
    def test_m7(self):
        #1 ère fois
        p=Partie(logger)
        p.initialiser(2)  
        joueur=p.joueurs[0]
        joueur2=p.joueurs[1]
        joueur.ressources=util.rVide()
        m7=AmenagementMineur(p,'m7',**deck['mineurs']['m7'])
        self.assertFalse(joueur.jePeuxJouer(m7.cout))
        joueur.ressources['b']=1
        self.assertTrue(joueur.jePeuxJouer(m7.cout))
        joueur.ressources['a']=1
        joueur.ressources['b']=0
        self.assertTrue(joueur.jePeuxJouer(m7.cout))
        #on remet le bois pour tester le cout multiple
        joueur.ressources['b']=1
       
        joueur.cartesEnMain.append(m7)
        partieSimulee=simulerPartie(['a1','m7_cout0','r'],p)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'r':1,'a':1}))
        self.assertFalse(joueur.aiJeJoue('m7'))
        self.assertTrue(util.findCarte(joueur2.cartesEnMain,'m7'))

    def test_m7bis(self):
        #1 ère fois
        p=Partie(logger)
        p.initialiser(2)  
        joueur=p.joueurs[0]
        joueur2=p.joueurs[1]
        joueur.ressources=util.rVide()
        m7=AmenagementMineur(p,'m7',**deck['mineurs']['m7'])
        self.assertFalse(joueur.jePeuxJouer(m7.cout))
        joueur.ressources['b']=1
        self.assertTrue(joueur.jePeuxJouer(m7.cout))
        joueur.ressources['a']=1
        joueur.ressources['b']=0
        self.assertTrue(joueur.jePeuxJouer(m7.cout))
        #on remet le bois pour tester le cout multiple
        joueur.ressources['b']=1
       
        joueur.cartesEnMain.append(m7)
        partieSimulee=simulerPartie(['a10','m7_cout0','r'],p)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'r':1,'a':1}))
        self.assertFalse(joueur.aiJeJoue('m7'))
        self.assertTrue(util.findCarte(joueur2.cartesEnMain,'m7'))

    def test_m11(self):
        #1 ère fois
        p=Partie(logger)
        p.initialiser(2)  
        joueur=p.joueurs[0]
        joueur2=p.joueurs[1]
        joueur.ressources=util.rVide()
        m11=AmenagementMineur(p,'m11',**deck['mineurs']['m11'])
        self.assertFalse(joueur.jePeuxJouer(m11.cout))
        joueur.ressources['b']=5
        joueur.ressources['r']=1
        self.assertTrue(joueur.jePeuxJouer(m11.cout))
        ferme=joueur.courDeFerme        
        ferme.etat["A1"].type="champ"   
        ferme.etat["B2"].type="champ"   
        ferme.etat["C2"].type="champ"   
        self.assertFalse(joueur.jeRemplisLesConditions(m11.condition))
        ferme.etat["A1"].type="vide" 
        joueur.cartesEnMain.append(m11)
        partieSimulee=simulerPartie(['a1','m11','a6'],p)
        self.assertTrue(util.sontEgaux(joueur.ressources,{}))
        print(ferme.etat['A1'].type)
        self.assertTrue(ferme.etat['A1'].type=="maisonBois")
        self.assertFalse(joueur.aiJeJoue('m11'))
        self.assertTrue(util.findCarte(joueur2.cartesEnMain,'m11'))        
        self.assertTrue(util.sontEgaux(joueur2.ressources,{'n':3,'b':3}))
        
        #teste avec choix
        #1 ère fois
        p=Partie(logger)
        p.initialiser(2)  
        joueur=p.joueurs[0]
        joueur2=p.joueurs[1]
        joueur.ressources=util.rVide()
        m11=AmenagementMineur(p,'m11',**deck['mineurs']['m11'])
        self.assertFalse(joueur.jePeuxJouer(m11.cout))
        joueur.ressources['b']=5
        joueur.ressources['r']=1
        self.assertTrue(joueur.jePeuxJouer(m11.cout))
        ferme=joueur.courDeFerme        
        ferme.etat["A1"].type="champ"   
        ferme.etat["B2"].type="champ"   
        ferme.etat["C2"].type="champ"   
        self.assertFalse(joueur.jeRemplisLesConditions(m11.condition))
        ferme.etat["A1"].type="vide" 
        ferme.etat["B2"].type="vide" 
        joueur.cartesEnMain.append(m11)
        partieSimulee=simulerPartie(['a1','m11','B2','a6'],p)
        self.assertTrue(util.sontEgaux(joueur.ressources,{}))
        self.assertFalse(joueur.aiJeJoue('m11'))
        self.assertTrue(util.findCarte(joueur2.cartesEnMain,'m11'))        
        self.assertTrue(util.sontEgaux(joueur2.ressources,{'n':3,'b':3}))        
        self.assertTrue(ferme.etat['A1'].type=="vide")
        self.assertTrue(ferme.etat['B2'].type=="maisonBois")
        self.assertTrue(util.findCarte(joueur2.cartesEnMain,'m11'))

    def test_m12(self):
        #1 ère fois
        p=Partie(logger)
        p.initialiser(2)  
        joueur=p.joueurs[0]
        joueur2=p.joueurs[1]
        joueur.ressources=util.rVide()
        m12=AmenagementMineur(p,'m12',**deck['mineurs']['m12'])
        self.assertFalse(joueur.jePeuxJouer(m12.cout))
        joueur.ressources['a']=4
        joueur.ressources['r']=1
        self.assertTrue(joueur.jePeuxJouer(m12.cout))
        ferme=joueur.courDeFerme        
        ferme.etat["A1"].type="champ"   
        ferme.etat["B2"].type="champ"   
        ferme.etat["C2"].type="champ"           
        self.assertFalse(joueur.jeRemplisLesConditions(m12.condition))
        ferme.etat["B1"].type="maisonArgile" 
        ferme.etat["C1"].type="maisonArgile"
        ferme.etat["A1"].type="vide" 
        joueur.cartesEnMain.append(m12)
        partieSimulee=simulerPartie(['a1','m12','a6'],p)
        self.assertTrue(util.sontEgaux(joueur.ressources,{}))
        self.assertTrue(ferme.etat['A1'].type=="maisonArgile")
        self.assertFalse(joueur.aiJeJoue('m12'))
        self.assertTrue(util.findCarte(joueur2.cartesEnMain,'m12'))        
        self.assertTrue(util.sontEgaux(joueur2.ressources,{'n':3,'b':3}))
        
    def test_m13(self):
        #1 ère fois
        p=Partie(logger)
        p.initialiser(2)  
        joueur=p.joueurs[0]
        joueur2=p.joueurs[1]
        joueur.ressources=util.rVide()
        m13=AmenagementMineur(p,'m13',**deck['mineurs']['m13'])
        self.assertFalse(joueur.jePeuxJouer(m13.cout))
        joueur.ressources['p']=3
        joueur.ressources['r']=1
        self.assertTrue(joueur.jePeuxJouer(m13.cout))
        ferme=joueur.courDeFerme        
        ferme.etat["A1"].type="champ"   
        ferme.etat["B2"].type="champ"   
        ferme.etat["C2"].type="champ"           
        self.assertFalse(joueur.jeRemplisLesConditions(m13.condition))
        ferme.etat["B1"].type="maisonPierre" 
        ferme.etat["C1"].type="maisonPierre"
        ferme.etat["A1"].type="vide" 
        joueur.cartesEnMain.append(m13)
        partieSimulee=simulerPartie(['a1','m13','a6'],p)
        self.assertTrue(util.sontEgaux(joueur.ressources,{}))
        self.assertTrue(ferme.etat['A1'].type=="maisonPierre")
        self.assertFalse(joueur.aiJeJoue('m13'))
        self.assertTrue(util.findCarte(joueur2.cartesEnMain,'m13'))        
        self.assertTrue(util.sontEgaux(joueur2.ressources,{'n':3,'b':3}))
  
  
    def test_m15(self):
        #1 ère fois
        p=Partie(logger)
        p.initialiser(2)  
        joueur=p.joueurs[0]
        joueur.ressources=util.rVide()
        m15=AmenagementMineur(p,'m15',**deck['mineurs']['m15'])
        self.assertFalse(joueur.jePeuxJouer(m15.cout))
        joueur.ressources['b']=3
        self.assertTrue(joueur.jePeuxJouer(m15.cout))    
        self.assertFalse(joueur.jeRemplisLesConditions(m15.condition))
        #A FINIR!!

    def test_m22(self):
        #1 ère fois
        p=Partie(logger)
        p.initialiser(2)  
        joueur=p.joueurs[0]
        m22=AmenagementMineur(p,'m22',**deck['mineurs']['m22'])
        joueur.cartesEnMain.append(m22)
        partieSimulee=simulerPartie(['a1','m22','a6','a9'],p)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'n':3,'b':3}))
        #A FINIR!!


    def test_m23(self):
        #1 ère fois
        p=Partie(logger)
        p.initialiser(2)  
        joueur=p.joueurs[0]
        joueur2=p.joueurs[1]
        joueur.ressources['b']=1
        m23=AmenagementMineur(p,'m23',**deck['mineurs']['m23'])
        joueur.cartesEnMain.append(m23)
        joueur.cartesDevantSoi['s24']=SavoirFaire(p,'s24',**deck['savoirFaires']['s24'])
        joueur.cartesDevantSoi['s25']=SavoirFaire(p,'s25',**deck['savoirFaires']['s25'])
        joueur.cartesDevantSoi['s26']=SavoirFaire(p,'s26',**deck['savoirFaires']['s26'])
        partieSimulee=simulerPartie(['a1','m23','a6'],p)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'b':1,'n':2}))
        self.assertTrue(util.sontEgaux(joueur2.ressources,{'n':3,'b':2}))
        
    def test_m25(self):
        p=Partie(logger)
        p.initialiser(2)  
        joueur=p.joueurs[0]
        joueur.ressources['b']=2
        m25=AmenagementMineur(p,'m25',**deck['mineurs']['m25'])
        joueur.cartesEnMain.append(m25)
        joueur.poserCarteDevantSoi(p.plateau['majeurs']['M0'],Majeur=True)
        
        partieSimulee=simulerPartie(['a1','m25','a5','b7','B3','r','a9','a7','a6'],p)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'b':6,'f':4,'n':2,'a':1,'r':1}))
        
        
class TestSavoirFaire(unittest.TestCase):
    def test_cout(self):
        p=Partie(logger)
        p.initialiser(4)  
        listeRep=['a4','s8','a29','s10']
        p.joueurs[0].cartesEnMain.append(SavoirFaire(p,'s8',**deck['savoirFaires']['s8']))
        p.joueurs[1].cartesEnMain.append(SavoirFaire(p,'s10',**deck['savoirFaires']['s10']))
        partieSimulee=simulerPartie(listeRep,p)
        self.assertTrue(util.sontEgaux(p.joueurs[0].ressources,{'n':2}))
        self.assertTrue(util.sontEgaux(p.joueurs[1].ressources,{'n':2}))



#     def test_s6(self): 
#         p=Partie(logger)
#         p.initialiser(2)  
#         listeRep=['a4','s6','a1']
#         p.joueurs[0].cartesEnMain.append(SavoirFaire(p,'s6',**deck['savoirFaires']['s6']))
#         
#         partieSimulee=simulerPartie(listeRep,p)


    
    def test_s8(self): 
        p=Partie(logger)
        p.initialiser(1)  
        listeRep=['a4','s8','a5']
        
        p.joueurs[0].cartesEnMain.append(SavoirFaire(p,'s8',**deck['savoirFaires']['s8']))
        
        partieSimulee=simulerPartie(listeRep,p)
        joueur=partieSimulee.joueurs[0]  
        self.assertTrue(util.sontEgaux(joueur.ressources,{'n':4,'l':1}))
        
    def test_s10(self): 
        p=Partie(logger)
        p.initialiser(1)  
        listeRep=['a4','s10','a5',
                  'a5','l','a2',
                  'a4','s8','a5','c'] #fin du tour 6]
        joueur=p.joueurs[0]
        joueur.cartesEnMain.append(SavoirFaire(p,'s10',**deck['savoirFaires']['s10']))
        joueur.cartesEnMain.append(SavoirFaire(p,'s8',**deck['savoirFaires']['s8']))
        p.plateau['tour']=5
        partieSimulee=simulerPartie(listeRep,p)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'n':7,'l':2,'c':3}))   

    def test_s11(self): 
        p=Partie(logger)
        p.initialiser(1)  
        listeRep=['a4','s11','a2']
        joueur=p.joueurs[0]
        joueur.cartesEnMain.append(SavoirFaire(p,'s11',**deck['savoirFaires']['s11']))
        partieSimulee=simulerPartie(listeRep,p)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'n':2,'l':1,'c':1}))         

    def test_s12(self): 
        p=Partie(logger)
        p.initialiser(1)  
        listeRep=['a4','s12','a6','a7']
        joueur=p.joueurs[0]
        joueur.cartesEnMain.append(SavoirFaire(p,'s12',**deck['savoirFaires']['s12']))
        partieSimulee=simulerPartie(listeRep,p)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'a':4,'b':3,'n':2}))   

    def test_s13(self): 
        p=Partie(logger)
        p.initialiser(1)  
        #on rend visible 1 legume artificiellement
        for num,case in p.plateau["cases"].items():
            if case.uid=='a17':
                case.visible=True
        listeRep=['a4','s13','a17']
        joueur=p.joueurs[0]
        joueur.cartesEnMain.append(SavoirFaire(p,'s13',**deck['savoirFaires']['s13']))
        partieSimulee=simulerPartie(listeRep,p)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'l':2,'c':1,'n':2}))   

    def test_s14(self): 
        p=Partie(logger)
        p.initialiser(1)  
        listeRep=['a4','s14','a6']
        joueur=p.joueurs[0]
        joueur.cartesEnMain.append(SavoirFaire(p,'s14',**deck['savoirFaires']['s14']))
        partieSimulee=simulerPartie(listeRep,p)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'b':3,'n':3}))      
        
    def test_s15(self): 
        p=Partie(logger)
        p.initialiser(1)  
        listeRep=['a4','s15','a7']
        joueur=p.joueurs[0]
        joueur.cartesEnMain.append(SavoirFaire(p,'s15',**deck['savoirFaires']['s15']))
        partieSimulee=simulerPartie(listeRep,p)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'a':3,'n':2}))           
        print("-----------PHASE2")
        #meme chose en ajoutant artificiellement 1 bois sur argile
        p=Partie(logger)
        p.initialiser(1)  
        for num,case in p.plateau["cases"].items():
            if case.uid=='a7':
                case.coutBonus['b']=-1        
                print('\n\n\nrrrr\n\n\n',case.cout,case.appro,case.coutBonus)
        listeRep=['a4','s15','a7']
        joueur=p.joueurs[0]
        joueur.cartesEnMain.append(SavoirFaire(p,'s15',**deck['savoirFaires']['s15']))
        partieSimulee=simulerPartie(listeRep,p)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'b':1,'a':1,'n':2}))                       
 
    def test_s16(self): 
        p=Partie(logger)
        p.initialiser(1)  
        listeRep=['a4','s16','a6']
        joueur=p.joueurs[0]
        joueur.cartesEnMain.append(SavoirFaire(p,'s16',**deck['savoirFaires']['s16']))
        partieSimulee=simulerPartie(listeRep,p)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'b':4,'n':2}))    

    def test_s17(self): 
        p=Partie(logger)
        p.initialiser(1)  
        listeRep=['a4','s17','a6',
                  'a7','a6',
                  'a7','a6',
                  'a7','a6',
                  'a7','a6',
                  'a7','a6']
        joueur=p.joueurs[0]
        joueur.cartesEnMain.append(SavoirFaire(p,'s17',**deck['savoirFaires']['s17']))
        partieSimulee=simulerPartie(listeRep,p)
        self.assertTrue(joueur.ressources['r']==4)    

    def test_s18(self): 
        p=Partie(logger)
        p.initialiser(1)  
        listeRep=['a4','s18','a2',
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',
                  'a2','a9']
        joueur=p.joueurs[0]
        joueur.cartesEnMain.append(SavoirFaire(p,'s18',**deck['savoirFaires']['s18']))
        partieSimulee=simulerPartie(listeRep,p)
        self.assertTrue(joueur.ressources['b']==5)    
 
    def test_s19(self): 
        p=Partie(logger)
        p.initialiser(1)  
        listeRep=['a4','s19','a2',
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',#6
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',
                  'a2','a9', #13
                  'a2','a9',                 
                  ]
        joueur=p.joueurs[0]
        joueur.cartesEnMain.append(SavoirFaire(p,'s19',**deck['savoirFaires']['s19']))
        partieSimulee=simulerPartie(listeRep,p)
        self.assertTrue(joueur.ressources['b']==7)   
    def test_s20(self): 
        p=Partie(logger)
        p.initialiser(1)  
        listeRep=['a4','s20','a2',
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',#6
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',
                  'a2','a9', #13
                  'a2','a9',                 
                  ]
        joueur=p.joueurs[0]
        joueur.cartesEnMain.append(SavoirFaire(p,'s20',**deck['savoirFaires']['s20']))
        partieSimulee=simulerPartie(listeRep,p)
        self.assertTrue(joueur.ressources['a']==7)   

    def test_s21(self): 
        p=Partie(logger)
        p.initialiser(2)  
        listeRep=['a4','s21','a6',
                  's21','s21','s21','s21','s21','s21','s21','s21']
        joueur=p.joueurs[0]
        joueur.ressources['n']=8
        joueur.cartesEnMain.append(SavoirFaire(p,'s21',**deck['savoirFaires']['s21']))
        partieSimulee=simulerPartie(listeRep,p)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'n':0,'r':2,'c':1,'p':1,
                                                          'l':2,'b':1,'a':1}))  
        self.assertTrue(partieSimulee.plateau['tour']==1)
        self.assertTrue(len(joueur.personnages)==1)
        self.assertTrue(partieSimulee.quiJoue==0)
  
    def test_s23(self): 
        p=Partie(logger)
        p.initialiser(1)  
        listeRep=['a4','s23',"a2","C5",
                  'a2',"C4"]
        joueur=p.joueurs[0]
        joueur.courDeFerme.etat["C5"].type='vide'
        joueur.courDeFerme.etat["C4"].type='vide'
        joueur.cartesEnMain.append(SavoirFaire(p,'s23',**deck['savoirFaires']['s23']))
        partieSimulee=simulerPartie(listeRep,p)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'n':2,'c':2})) 
        self.assertTrue(joueur.courDeFerme.compter('champ')==2) 


    def test_s24(self): 
        p=Partie(logger)
        p.initialiser(1)  
        listeRep=['a4','s24','a2',
                  'a2','a9',#+1
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',#+5  un boeuf
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',#+9  un boeuf         
                  ]
        joueur=p.joueurs[0]
        joueur.cartesEnMain.append(SavoirFaire(p,'s24',**deck['savoirFaires']['s24']))
        partieSimulee=simulerPartie(listeRep,p)
        self.assertTrue(joueur.ressources['v']==2)   
    def test_s25(self): 
        p=Partie(logger)
        p.initialiser(1)  
        listeRep=['a4','s25','a2',
                  'a2','a9',#+1
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',#+5  
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',#+9     
                  'a2','a9',
                  'a2','a9',     
                  ]
        joueur=p.joueurs[0]
        joueur.cartesEnMain.append(SavoirFaire(p,'s25',**deck['savoirFaires']['s25']))
        partieSimulee=simulerPartie(listeRep,p)
        self.assertTrue(joueur.ressources['m']==4)    
    def test_s26(self): 
        p=Partie(logger)
        p.initialiser(1)  
        listeRep=['a4','s26','a2',
                  'a2','a9',#+1
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',#+5  
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',
                  'a2','a9',#+9     
                  'a2','a9',
                  'a2','a9',     
                  ]
        joueur=p.joueurs[0]
        joueur.cartesEnMain.append(SavoirFaire(p,'s26',**deck['savoirFaires']['s26']))
        partieSimulee=simulerPartie(listeRep,p)
        self.assertTrue(joueur.ressources['s']==3)     
 
    def test_s28(self): 
        p=Partie(logger)
        p.initialiser(3)  
        listeRep=['a4','s28',
                  'a5','a6',
                  'a2','p24'   
                  ]
        joueur=p.joueurs[0]
        joueur.cartesEnMain.append(SavoirFaire(p,'s28',**deck['savoirFaires']['s28']))
        partieSimulee=simulerPartie(listeRep,p)
        self.assertTrue(util.sontEgaux(p.joueurs[0].ressources,{'n':2,'c':2,'l':1})) 
        self.assertTrue(util.sontEgaux(p.joueurs[1].ressources,{'n':5,'c':1})) 
        self.assertTrue(util.sontEgaux(p.joueurs[2].ressources,{'n':3,'c':1,'b':3})) 


unittest.main()
