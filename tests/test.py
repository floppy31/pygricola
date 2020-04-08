import random
import unittest

import pygricola.util as util
from pygricola.partie import Partie
import pygricola.fonctionsPlateau as fct
from pygricola.carte import Carte,AmenagementMajeur,deck
from pygricola.carte.action import CarteAction
import pygricola.util as util



class FonctionsPlateau(unittest.TestCase):
    
    
    #TODO: tester avec loge et cheval
    def test_AsAbattre(self):
        #1 ère fois
        p=Partie()
        p.initialiser(3,[])  
        joueur=p.joueurs[0]
        joueur2=p.joueurs[1]
        joueur3=p.joueurs[2]
        joueur.ressources=util.rVide()
        joueur2.ressources=util.rVide()
        for CAS in p.plateau["actionsSpeciales"]:
            for l in CAS.listeActionSpeciale:
                if l.uid=='b5':
                    carte=l
        p.sujet=carte
        (choixPossibles,sujet,encore,message)=carte.jouer()
        #pas encore joué
        self.assertTrue(util.sontEgaux(joueur.ressources,{'b':0}))
        #5 forets au début
        self.assertTrue(len(choixPossibles)==5)
        caseAbattue=p.choixPossibles[0]
        (choixPossibles,sujet,encore,message)=sujet.effet(0,p.choixPossibles)   
        self.assertTrue(util.sontEgaux(joueur.ressources,{'b':2}))
        
        #pas de Pn pour racheter
        self.assertFalse(joueur.jePeuxFaireActionSpeciale(carte))
        joueur.ressources['n']=2
        #toujours pas car je l'ai déja prise
        self.assertFalse(joueur.jePeuxFaireActionSpeciale(carte))
        p.joueurSuivant()
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
        (choixPossibles,sujet,encore,message)=sujet.effet(0,p.choixPossibles)         
        self.assertTrue(util.sontEgaux(joueur2.ressources,{'b':4,'h':1}))
        p.joueurSuivant()
        joueur3.ressources['n']=10
        #impossible de racheter  
        self.assertFalse(joueur3.jePeuxFaireActionSpeciale(carte)) 
        p.finDuTour()
        #maintenant je peux
        self.assertTrue(joueur3.jePeuxFaireActionSpeciale(carte)) 
    
    def test_AsCouperBruler(self):
        #1 ère fois
        p=Partie()
        p.initialiser(3,[])  
        joueur=p.joueurs[0]
        joueur2=p.joueurs[1]
        joueur3=p.joueurs[2]
        joueur.ressources=util.rVide()
        joueur2.ressources=util.rVide()
        for CAS in p.plateau["actionsSpeciales"]:
            for l in CAS.listeActionSpeciale:
                if l.uid=='b6':
                    carte=l
        p.sujet=carte
        (choixPossibles,sujet,encore,message)=carte.jouer()
        #pas encore joué
        self.assertTrue(joueur.courDeFerme.compter('champ')==0)
        #5 forets au début
        self.assertTrue(len(choixPossibles)==5)
        
        (choixPossibles,sujet,encore,message)=sujet.effet(0,p.choixPossibles)   
        self.assertTrue(joueur.courDeFerme.compter('champ')==1)
        self.assertTrue(joueur.courDeFerme.compter('foret')==4)
        #pas de Pn pour racheter
        self.assertFalse(joueur.jePeuxFaireActionSpeciale(carte))
        joueur.ressources['n']=2
        #toujours pas car je l'ai déja prise
        self.assertFalse(joueur.jePeuxFaireActionSpeciale(carte))
        p.joueurSuivant()
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
        (choixPossibles,sujet,encore,message)=carte.jouer()
        #les champs ne se touchent pas
        self.assertFalse(joueur2.jePeuxFaireActionSpeciale(carte)) 
        joueur2.courDeFerme.etat['B5'].type="champ"
        #il faut remettre à jour
        (choixPossibles,sujet,encore,message)=carte.jouer()
                            
        self.assertTrue(joueur2.jePeuxFaireActionSpeciale(carte)) 
        (choixPossibles,sujet,encore,message)=carte.jouer()
        self.assertTrue(choixPossibles==["A5"]) 
        

    def test_AsCheval(self):
        #2,3,4,5 joueurs
        
        #plus de place
        
        #rachat      
        
        pass   
    
    def test_AsTourbe(self):
        #1 ère fois
        p=Partie()
        p.initialiser(3,[])  
        joueur=p.joueurs[0]
        joueur2=p.joueurs[1]
        joueur3=p.joueurs[2]
        joueur.ressources=util.rVide()
        joueur2.ressources=util.rVide()
        for CAS in p.plateau["actionsSpeciales"]:
            for l in CAS.listeActionSpeciale:
                if l.uid=='b7':
                    carte=l
        p.sujet=carte
        (choixPossibles,sujet,encore,message)=carte.jouer()
        print((choixPossibles,sujet,encore,message))
        #pas encore joué
        self.assertTrue(util.sontEgaux(joueur.ressources,{'f':0}))
        #3 tourbes au début
        self.assertTrue(len(choixPossibles)==3)
        
        (choixPossibles,sujet,encore,message)=sujet.effet(0,p.choixPossibles)   
        self.assertTrue(util.sontEgaux(joueur.ressources,{'f':3}))
        
        #pas de Pn pour racheter
        self.assertFalse(joueur.jePeuxFaireActionSpeciale(carte))
        joueur.ressources['n']=2
        #toujours pas car je l'ai déja prise
        self.assertFalse(joueur.jePeuxFaireActionSpeciale(carte))
        p.joueurSuivant()
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
        (choixPossibles,sujet,encore,message)=sujet.effet(0,p.choixPossibles)         
        self.assertTrue(util.sontEgaux(joueur2.ressources,{'f':4}))
        p.joueurSuivant()
        joueur3.ressources['n']=10
        #impossible de racheter  
        self.assertFalse(joueur3.jePeuxFaireActionSpeciale(carte)) 
        p.finDuTour()
        #maintenant je peux
        self.assertTrue(joueur3.jePeuxFaireActionSpeciale(carte)) 
    
    def test_Betail(self):
        p=Partie()
        p.initialiser(5,[])  
        joueur=p.joueurs[0]
        joueur.ressources=util.rVide()
        betail=CarteAction(p,"a38",visible=True,possibilites=fct.possibiliteBetail,effet=fct.betail)
        p.sujet=betail
        (choixPossibles,sujet,encore,message)=betail.jouer()
        self.assertTrue(len(choixPossibles)==2)
        p.joueurs[0].ressources['n']=1 
        (choixPossibles,sujet,encore,message)=betail.jouer()
        self.assertTrue(len(choixPossibles)==3)
        #test de la carte 
        joueur.ressources['n']=1
        joueur.ressources['m']=0
        joueur.ressources['s']=0
        joueur.ressources['b']=0
        
        #test mouton pn
        (choixPossibles,sujet,encore,message)=sujet.effet(0,p.choixPossibles)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'n':2,'m':1}))

        #test beuf contre pn
        (choixPossibles,sujet,encore,message)=sujet.effet(2,p.choixPossibles)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'n':1,'m':1,'v':1}))    
            
    def test_ConstructionDePieceEtOuEtable(self):
        #je peux rien faire
        
        #je gagne les ressources
        
        #je peux faire
        
        #je ne peux pas en faire 5
        
        #position impossible
        
        #etables impossibles
        
        #j'en fais plusieurs
        pass
       
    def test_ConstructionOuSpectacle(self):
        #je ne la vois qu'a 5
        
        #je ne peux faire que spectacle
        
        #je peux faire 1 pèce avec les ressources
        
        #je ne peux faire qu'une pièce
        
        #test position
        
        #ok
        pass


    def test_Labourage(self):
        #1er labour
        
        #labour impossible
        
        pass

    def test_Naissance(self):
        p=Partie()
        p.initialiser(1,[])  
        joueur=p.joueurs[0]
        #test de la carte naissance puis aménagement mineur
        nPuisMineur=CarteAction(p,"a14",visible=False,possibilites=fct.possibilitesAmenagementMineur,effet=fct.naissancePuisMineur,condition=fct.jePeuxNaitre)
        p.sujet=nPuisMineur
        self.assertFalse(fct.jePeuxNaitre(p))
        #je rajoute une maison 
        joueur.courDeFerme.etat["A1"].type="maisonBois"
        self.assertTrue(fct.jePeuxNaitre(p))
        (choixPossibles,sujet,encore,message)=nPuisMineur.jouer()
        self.assertTrue(choixPossibles==['u3'])#ne peux pas jouer de mineur
        (choixPossibles,sujet,encore,message)=sujet.effet(0,p.choixPossibles)
        #je ne peux plus naitre
        self.assertFalse(fct.jePeuxNaitre(p))
        joueur.courDeFerme.etat["A2"].type="maisonBois"
        #TODO
        #ajouter un mineur et le jouer avec naissance puis mineur
        #puis ajouter une piece et faire savoir faire ou naissance
        #avant le tour 5 --> faux
        #on change le tour
        #---> vrai

    def test_Majeurs(self):
        #visibilité
        
        #devoiler fonctionne
        
        
        pass
        

        
    def test_RoseauPnOuPierrePn(self):
        p=Partie()
        p.initialiser(3,[])  
        joueur=p.joueurs[0]
        joueur.ressources=util.rVide()
        rPnOuPPn=CarteAction(p,"a26",possibilites=fct.possibiliteRoseauPnOuPierrePn,effet=fct.roseauPnOuPierrePn,visible=True)
        p.sujet=rPnOuPPn
        (choixPossibles,sujet,encore,message)=rPnOuPPn.jouer()
        (choixPossibles,sujet,encore,message)=sujet.effet(1,p.choixPossibles)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'n':1,'r':1}))
        
    def test_Semailles(self):
        #pas de céréale ni cuisson
        #cuisson seule
        #semaille et cuisson
        #test plan dispo ressource etc...
        #test sans cuisson
        pass    
        
    def test_Tour(self):    
        # simuler un tour avec plusieurs joueurs, des nombres différents de personnages
        # fin du tour au bon moment
        
        #tour suivant
        #verif le premier joueur a bien changé
        pass
                
         
 
        
unittest.main()