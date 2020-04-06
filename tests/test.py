import random
import unittest

import pygricola.util as util
from pygricola.partie import Partie
import pygricola.fonctionsPlateau as fct
from pygricola.carte import Carte
from pygricola.carte.action import CarteAction
import pygricola.util as util



class FonctionsPlateau(unittest.TestCase):
    def test_Betail(self):
        p=Partie()
        p.initialiser(5,[])  
        joueur=p.joueurs[0]
        joueur.ressources['n']=0 
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
            
    def test_RoseauPnOuPierrePn(self):
        p=Partie()
        p.initialiser(3,[])  
        joueur=p.joueurs[0]
        joueur.ressources['n']=0 
        rPnOuPPn=CarteAction(p,"a26",possibilites=fct.possibiliteRoseauPnOuPierrePn,effet=fct.roseauPnOuPierrePn,visible=True)
        p.sujet=rPnOuPPn
        (choixPossibles,sujet,encore,message)=rPnOuPPn.jouer()
        (choixPossibles,sujet,encore,message)=sujet.effet(1,p.choixPossibles)
        self.assertTrue(util.sontEgaux(joueur.ressources,{'n':1,'r':1}))

    def test_Naissance(self):
        p=Partie()
        p.initialiser(1,[])  
        joueur=p.joueurs[0]
        #test de la carte naissance puis aménagement mineur
        nPuisMineur=CarteAction(p,"a14",visible=False,possibilites=fct.possibilitesAmenagementMineur,effet=fct.naissancePuisMineur,condition=fct.jePeuxNaitre)
        p.sujet=nPuisMineur
        self.assertFalse(fct.jePeuxNaitre(p))
        #je rajoute une maison 
        joueur.courDeFerme.etat["a1"].type="maisonBois"
        self.assertTrue(fct.jePeuxNaitre(p))
        (choixPossibles,sujet,encore,message)=nPuisMineur.jouer()
        self.assertTrue(choixPossibles==['u3'])#ne peux pas jouer de mineur
        (choixPossibles,sujet,encore,message)=sujet.effet(0,p.choixPossibles)
        #je ne peux plus naitre
        self.assertFalse(fct.jePeuxNaitre(p))
        joueur.courDeFerme.etat["a2"].type="maisonBois"
        #TODO
        #ajouter un mineur et le jouer avec naissance puis mineur
        #puis ajouter une piece et faire savoir faire ou naissance
        #avant le tour 5 --> faux
        #on change le tour
        #---> vrai
        
        
class PartieTest(unittest.TestCase):
    def test_partie(self):
        """Test le fonctionnement de la fonction 'random.choice'."""
        p=Partie()
        p.initialiser(2,[])   
        self.assertTrue(True)
        
        
        
        
         
 
        
unittest.main()