import random
import unittest

import pygricola.util as util
from pygricola.partie import Partie
import pygricola.fonctionsPlateau as fct
from pygricola.carte import Carte,AmenagementMajeur,AmenagementMineur,deck
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
    def test_AsFoireDuTravail(self):
        p=Partie()
        p.initialiser(3,[])  
        joueur=p.joueurs[0]
        joueur.ressources=util.rVide()
        for CAS in p.plateau["actionsSpeciales"]:
            for l in CAS.listeActionSpeciale:
                if l.uid=='b3':
                    carte=l        
        #possibilitesVides
        (choixPossibles,sujet,encore,message)=carte.jouer()
        self.assertTrue(len(choixPossibles)==0)
        #je me mets un mineur en main et les ressources pour l'acheter
        joueur.cartesEnMain.append(AmenagementMineur(p,'m0',**deck['mineurs']['m0']))
        (choixPossibles,sujet,encore,message)=carte.jouer()
        self.assertTrue(len(choixPossibles)==0)
        joueur.ressources['a']=1
        (choixPossibles,sujet,encore,message)=carte.jouer()
        #je peux pas payer le feu
        self.assertTrue(len(choixPossibles)==0)
        
        joueur.ressources['f']=1
        (choixPossibles,sujet,encore,message)=carte.jouer()
        #maintenant ok
        self.assertTrue(len(choixPossibles)==1)
        joueur.ressources['f']=0
        joueur.ressources['b']=1
        #on teste avec 1 bois
        (choixPossibles,sujet,encore,message)=carte.jouer()
        self.assertTrue(len(choixPossibles)==1)

        #on la joue
        (choixPossibles,sujet,encore,message)=carte.effet(0,p.choixPossibles) 
        self.assertFalse(encore)
        self.assertTrue(util.sontEgaux(joueur.ressources,util.rVide()))
        self.assertTrue(carte.carteQuiMePorte.etat==joueur.id)
    
    def test_AsTravailClandestin(self):
        p=Partie()
        p.initialiser(3,[])  
        joueur=p.joueurs[0]
        joueur.ressources=util.rVide()
        for CAS in p.plateau["actionsSpeciales"]:
            for l in CAS.listeActionSpeciale:
                if l.uid=='b4':
                    carte=l        
        #possibilitesVides
        (choixPossibles,sujet,encore,message)=carte.jouer()
        self.assertTrue(len(choixPossibles)==0)
        #si je me mets 1 pn et 1 bois c'est idem
        joueur.ressources['b']=1
        joueur.ressources['n']=1
        (choixPossibles,sujet,encore,message)=carte.jouer()
        self.assertTrue(len(choixPossibles)==0)
        #mais avec 2 argiles c'est ok
        joueur.ressources['a']=2
        (choixPossibles,sujet,encore,message)=carte.jouer()
        self.assertTrue(len(choixPossibles)==1)        
        #on la joue
        (choixPossibles,sujet,encore,message)=carte.effet(0,p.choixPossibles) 
        self.assertFalse(encore)
        self.assertTrue(util.sontEgaux(joueur.ressources,util.rVide()))               


    
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
        p=Partie()
        p.initialiser(1,[])  
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
        (choixPossibles,sujet,encore,message)=carte.jouer()
        self.assertTrue(p.choixPossibles==choixPossibles=='inputtext')
        inputTextNonValables=["toto","A1:f","B1:E","B1:P","B2:P","C2:P,C3:P,C4:P","C2:P,C4:P",
                              "A1:E,A2:E,C4:E,C2:E,C3:E"]
        
        for it in inputTextNonValables:
            (choixPossibles,sujet,encore,message)=sujet.effet(it,p.choixPossibles) 
            self.assertTrue(choixPossibles=='inputtext') 
            self.assertTrue(encore) 
            print(message)
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

            (choixPossibles,sujet,encore,message)=sujet.effet(it,p.choixPossibles) 
            self.assertTrue(choixPossibles==-1) 
            self.assertFalse(encore)
            self.assertTrue(util.sontEgaux(joueur.ressources,reste))
            #on remets le personnage artificiellement 
            perso=joueur.personnagesPlaces.pop()
            joueur.personnages.append(perso)
            ferme.mettrePersonnage(perso,perso.localisationInit) 
               

       
    def test_ConstructionOuSpectacle(self):

        #je ne la vois qu'a 5
        for njoueurs in range(1,5):
            p=Partie()
            p.initialiser(njoueurs,[])  
            joueur=p.joueurs[0]
            joueur.ressources=util.rVide()   
            carte=p.plateau["cases"][1]
            self.assertFalse(carte.uid=="a34")
        p=Partie()
        p.initialiser(5,[])  
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
        p.sujet=carte
        (choixPossibles,sujet,encore,message)=carte.jouer()
        self.assertTrue(len(choixPossibles)==1)
        self.assertTrue(choixPossibles[0]=="u6")
        joueur.ressources['b']=5 
        joueur.ressources['r']=2        
        ferme=joueur.courDeFerme
        ferme.etat["A1"].type="foret"
        ferme.etat["B2"].type="tourbe"
        ferme.etat["C2"].type="foret"  
        (choixPossibles,sujet,encore,message)=carte.jouer()
        #on n'a pas de place pour la maison
        self.assertTrue(len(choixPossibles)==1)
        self.assertTrue(choixPossibles[0]=="u6")        
        #par contre si je fais de la place
        ferme.etat["A1"].type="vide"
        ferme.etat["B2"].type="vide"
        ferme.etat["C2"].type="vide"
        (choixPossibles,sujet,encore,message)=carte.jouer()
        self.assertTrue(len(choixPossibles)==4)  #spectacle + 3 possibilites
        sujet=carte
        caseChoisie=choixPossibles[1][1] 
        (choixPossibles,sujet,encore,message)=sujet.effet(1,choixPossibles) 
        self.assertFalse(encore)
        self.assertTrue(choixPossibles==-1)
        self.assertTrue(util.sontEgaux(joueur.ressources,util.rVide() ))
        self.assertFalse(carte.libre)

    def test_Labourage(self):
        p=Partie()
        p.initialiser(1,[])  
        joueur=p.joueurs[0]
        joueur.ressources=util.rVide()
        
        carte=p.plateau["cases"][10] #bof mais a priori c'est elle         #1er labour
        (choixPossibles,sujet,encore,message)=carte.jouer()
        self.assertTrue(len(choixPossibles)==5)# 5 endroits vides au début
        self.assertTrue(joueur.courDeFerme.compter('champ')==0)
        (choixPossibles,sujet,encore,message)=sujet.effet(0,choixPossibles) 
        self.assertTrue(joueur.courDeFerme.compter('champ')==1)
        self.assertFalse(encore)
        
        
        

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
        p=Partie()
        p.initialiser(3,[])  
        joueur=p.joueurs[0]
        joueur.ressources=util.rVide()
        
        carte=p.plateau["cases"][17] #bof mais a priori c'est elle 
        (choixPossibles,sujet,encore,message)=carte.jouer()
        #pas de ressources pas de possibilites
        self.assertTrue(len(choixPossibles)==0)
        #on teste la condition possibilites non vide
        self.assertFalse(joueur.jeRemplisLesConditions(carte.condition))
        #avec 2 argiles je peux faire seulement le foyer à 2
        joueur.ressources['a']=2
        self.assertTrue(joueur.jeRemplisLesConditions(carte.condition))
        (choixPossibles,sujet,encore,message)=carte.jouer()
        self.assertTrue(len(choixPossibles)==1)
        self.assertTrue(choixPossibles[0].uid=="M0")
        sujet=carte
        #je le fais
        (choixPossibles,sujet,encore,message)=sujet.effet(0,p.choixPossibles)   
        #peux plus rejouer
        self.assertFalse(encore) 
        #je n'ai plus de ressource
        self.assertTrue(util.sontEgaux(joueur.ressources,{}))
        #j'ai bien le majeur joué devant moi
        self.assertTrue(joueur.aiJeJoue('M0'))  
        #si je pouvais re jouer alors je ne pourrais pas activer le foyer 
        joueur.possibilites()    
        activable=False
        for pos in p.choixPossibles:
            if (pos.uid) =="M0":
                activable=True
        self.assertFalse(activable)     
        #mais avec un mouton si!
        joueur.ressources['m']=1
        joueur.possibilites()    
        activable=False
        for pos in p.choixPossibles:
            if (pos.uid) =="M0":
                activable=True
                sujet=pos
        self.assertTrue(activable)     
        #que puis-je activer
        cuissonPossibles=sujet.possibilites()
        self.assertTrue(cuissonPossibles[0].uid=="um") #cuire un mouton
        (choixPossibles,sujet,encore,message)=sujet.effet(0,cuissonPossibles)   
        #on peut encore jouer
        self.assertTrue(encore) 
        #on a gagné 2 pn et perdu le mouton
        self.assertTrue(util.sontEgaux(joueur.ressources,{'n':2}))
        #on passe au joueur suivant
        p.joueurSuivant()
        joueur=p.joueurs[1]
        joueur.possibilites() 
        joueur.ressources=util.rVide()
        joueur.ressources['a']=2
        (choixPossibles,sujet,encore,message)=carte.jouer()
        self.assertFalse(joueur.jeRemplisLesConditions(carte.condition))        
        #par contre si je me mets 1 argile en plus je peux 
        joueur.ressources['a']=3
        self.assertTrue(joueur.jeRemplisLesConditions(carte.condition))  
        #si je me mets une pierre en plus
        joueur.ressources['p']=1
        #je peux jouer 4 trucs (foyer à 3, four a tourbe, four en brique, et abatoir à chevaux 1
        joueur.possibilites() #on réinitialise
        (choixPossibles,sujet,encore,message)=carte.jouer()
        uidPossibles=["M1","M2","M4","M14"]
        for am in choixPossibles:
            uidPossibles.remove(am.uid)
        self.assertTrue(len(uidPossibles)==0)  
        
        

        
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
        
    def test_SemailleCuisson(self):
        #pas de céréale ni cuisson
        p=Partie()
        p.initialiser(1,[])  
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
        (choixPossibles,sujet,encore,message)=carte.jouer()

        self.assertTrue(p.choixPossibles==choixPossibles=='inputtext')
        ferme.etat["A1"].type="champ"   
        ferme.etat["A2"].type="champ"   
        ferme.etat["A3"].type="champ"   
        ferme.etat["A3"].ressources['c']=1  
        ferme.etat["B3"].type="tourbe" 
        inputTextNonValables=["toto","A1:f","A1:l","B3:c","A1:c,c:2","A3:c"]
        
        for it in inputTextNonValables:
            (choixPossibles,sujet,encore,message)=sujet.effet(it,p.choixPossibles) 
            self.assertTrue(choixPossibles=='inputtext') 
            self.assertTrue(encore) 
            print(message)
            
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

            (choixPossibles,sujet,encore,message)=sujet.effet(it,p.choixPossibles) 
            self.assertTrue(choixPossibles==-1) 
            self.assertFalse(encore)
            self.assertTrue(util.sontEgaux(joueur.ressources,reste))
            #on remets le personnage artificiellement 
            perso=joueur.personnagesPlaces.pop()
            joueur.personnages.append(perso)
            ferme.mettrePersonnage(perso,perso.localisationInit) 
            for k,v in etatChamp.items():
                nb=int(v[0])
                type=v[1]
                self.assertTrue(ferme.etat[k].ressources[type]==nb)     
                
      
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
        p=Partie()
        p.initialiser(2,[])  
        p.demarragePartie()
        p.demarrageTour()        
        listeRep=[ "a2","a9","a8","a5",
                  "a0",'C2:P,C3:E', #1 action
                  "b5",'A3', #idem abattre en A3
                  "a5",
                  "a6"
                  ]
        p.initChoix()
        choixPossibles=-1
        for id in listeRep:
            print('--------',id,choixPossibles)
            #pour ne pas faire ça si p.jouerUidRenvoie inputtext
            if choixPossibles==-1:
                sujet=p.joueurQuiJoue()
                sujet.possibilites()
                (choixPossibles,sujet,encore,message)=p.jouerUid(id)
            elif(choixPossibles=='inputtext'):
                (choixPossibles,sujet,encore,message)=sujet.effet(id,[])
            else:
                (choixPossibles,sujet,encore,message)=sujet.effet(p.choixPossibles.index(id),p.choixPossibles)
            print(p.messagesPrincipaux[-1])
            if choixPossibles==-1:
                suivant=p.joueurSuivant()
                p.initChoix()
                if suivant==-1:
                    p.finDuTour()
                    p.demarrageTour()    
 
        
unittest.main()