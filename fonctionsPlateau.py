import pygricola.util as util
####cette condition est particulière
####si la carte à une methode possibilités, on l'appelle avec Fake=True
####si la liste est vide, on ne peux pas faire l'action
####par ex ni on ne peux ni jouer de mineur ni de majeur, on ne peux pas faire la case
def possibilitesNonVide(partie,carte):
    if not type(carte._possibilites)==dict:
        if type(carte._possibilites)==list:
            return len(carte._possibilites)>0
        else:
            carte._possibilites(partie,carte,Fake=True)
            if len(partie.choixPossibles)==0:
                partie.log.debug("{} : possibilites vides".format(carte.uid))
                partie.messagesDetail.append("{} : possibilites vides".format(carte.uid) )
            return len(partie.choixPossibles)>0
    return True
    
    
##################################################################################
#---------------------------------------Action dependant des joueurs--------------
##################################################################################

def possibiliteBetail(partie,carte,Fake=False):
    joueur=partie.joueurQuiJoue()
    possibilites=["u0","u1"]
    if(joueur.jePeuxJouer({'n':1})):
        possibilites.append("u2")
    partie.changerPointeurs(possibilites ,carte,phrase='p0',Fake=Fake) 


def betail(partie,choix,possibilites,carte):
    cout={}
    joueur=partie.joueurQuiJoue()
    if possibilites[choix]=="u0":
        cout={"n":-1,"m":-1}
    elif possibilites[choix]=="u1":
        cout={"s":-1}
    else:
        cout={"n":1,"v":-1}
    personnage=joueur.personnages.pop()
    joueur.personnagesPlaces.append(personnage)                  
    carte.mettrePersonnage(personnage)
    joueur.mettreAJourLesRessources(cout)
    partie.messagesPrincipaux.append([joueur.nom,"p1",possibilites[choix]])

    partie.changerPointeurs(-1,None) 
              
def possibiliteRoseauPnOuPierrePn(partie,carte,Fake=False):
    possibilites=["u4","u5"]
    partie.changerPointeurs(possibilites ,carte,phrase='p0',Fake=Fake) 

def roseauPnOuPierrePn(partie,choix,possibilites,carte):
    cout={}
    joueur=partie.joueurQuiJoue()

    if possibilites[choix]=="u4":
        cout={"p":-1,"n":-1}
    else:
        cout={"r":-1,"n":-1}
        
    personnage=joueur.personnages.pop()
    joueur.personnagesPlaces.append(personnage)                  
    carte.mettrePersonnage(personnage)
    joueur.mettreAJourLesRessources(cout)
    partie.changerPointeurs(-1,None) 
       
##################################################################################
#---------------------------------------Renovation--------------
##################################################################################       
       
def jePeuxRenover(partie, carte ):
    
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme   
    typeMaison=ferme.enQuoiEstLaMaison()
    if typeMaison=='S':
        return False
    else:
        return joueur.jePeuxJouer(joueur.prixDeLaRenovation())   
    
    
    
    
def renovation(partie,carte,Fake=False):
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme   
    typeMaison=ferme.enQuoiEstLaMaison()
    cout=joueur.prixDeLaRenovation()
    if typeMaison=='B':
        nouveauType='maisonArgile'
    elif typeMaison=='A':
        nouveauType='maisonPierre'
    else:
        error
    for m in ferme.tousLes('maison'):
        ferme.etat[m].type=nouveauType
    joueur.mettreAJourLesRessources(cout)
    
    partie.log.info('{} {}'.format(joueur.nom,'p52'))
    partie.messagesPrincipaux.append([joueur.nom,'p52'])
    if carte.uid=='a15':
        possibilitesAmenagementMineurOuMajeur(partie,carte,Fake=False,possibiliteRien=True)
    elif carte.uid=='a23':
        demanderPlanCloture(partie,carte,Fake=False)

    
            
##################################################################################
#---------------------------------------Naissances--------------
##################################################################################
def jePeuxNaitre(partie,carte):
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme
    nbPions=len(joueur.personnages)+len(joueur.personnagesPlaces)
    nbMaison=ferme.compter('maison')
    if nbMaison>nbPions:
        return True
    else:
        return False
    
def moinsDeCinqPerso(partie,carte):
    joueur=partie.joueurQuiJoue()
    nbPions=len(joueur.personnages)+len(joueur.personnagesPlaces)
    return nbPions<5
    
def jePeuxJouerSavoirFaireOuNaissance(partie,carte):
    cout=coutSavoirFaire2(partie,carte)
    joueur=partie.joueurQuiJoue()
    savoirFaireOk=joueur.jePeuxJouer(cout)
    tourOk=partie.plateau["tour"]>4
    return (jePeuxNaitre(partie,carte) and tourOk) or savoirFaireOk
    
    
def possibiliteSavoiFaireOuNaissance(partie,carte,Fake=False):
    possibilites=["p2"]
    joueur=partie.joueurQuiJoue()
    tourOk=partie.plateau["tour"]>4
    if tourOk:
        if jePeuxNaitre(partie,carte):
            possibilites.append('p3')
    partie.changerPointeurs(possibilites ,carte,phrase='p0',djangoJoueur=joueur.djangoUid,Fake=Fake,jouerEgalEffet=not Fake)   
    
def possibilitesSavoirFaireGratuit(partie,carte,Fake=False):
    partie.log.debug('possibilitesSavoirFaireGratuit')
    possibilites=[]   
    joueur=partie.joueurQuiJoue()
    for c in joueur.cartesEnMain:
        if c.uid[0]=='s':
            if joueur.jeRemplisLesConditions(c.conditionAchat):
                possibilites.append(c.uid)
    partie.changerPointeurs(possibilites ,carte,phrase='p0',Fake=Fake,djangoJoueur=joueur.djangoUid) 
    
    
def savoiFaireOuNaissance(partie,choix,possibilites,carte):
    joueur=partie.joueurQuiJoue()
    if possibilites[choix]=="p2":
        cout=coutSavoirFaire2(partie,carte)
        coutCarte=carte.vider()
        coutAAppliquer=util.ajouter(cout,coutCarte)
        joueur.mettreAJourLesRessources(coutAAppliquer)
        possibilitesSavoirFaireGratuit(partie,carte)
    #feinte pour faire un savoir faire par la voie classique sauf qu'on le paye pas    
    elif possibilites[choix][0]=='s':
        choixSavoirFaire(partie,choix,possibilites,carte,payant=False)
    
    
    else:
        #on trouve l'emplacement pour le nouveau ne
        emplacements=[]
        nbJoueurs=0
        for p in joueur.personnages+joueur.personnagesPlaces:
            emplacements.append(p.localisationInit)
            nbJoueurs+=1
        emplacements=set(emplacements)
        emplacementsMaisons=set(ferme.tousLes('maison'))
        nouveauNe=Personnage(emplacementsMaisons.difference(emplacements).pop(),nbJoueurs+1,joueur.couleur)
        carte.mettrePersonnage(nouveauNe)
        nouveauNe.consomationNourriture=1
        joueur.personnagesPlaces.append(nouveauNe)
        personnage=joueur.personnages.pop()
        joueur.personnagesPlaces.append(personnage)                  
        carte.mettrePersonnage(personnage)
        partie.changerPointeurs(-1,None) 
         
         
           
def naissancePuisMineur(partie,choix,possibilites,carte):
    from pygricola.joueur.personnage import Personnage

    joueur=partie.joueurs[partie.quiJoue]
    ferme=joueur.courDeFerme
    #on a deja verifie qu'on peut naitre
    #on regarde les enplacement des pions existants (useless???)
    emplacements=[]
    nbJoueurs=0
    for p in joueur.personnages+joueur.personnagesPlaces:
        emplacements.append(p.localisationInit)
        nbJoueurs+=1
    emplacements=set(emplacements)
    emplacementsMaisons=set(ferme.tousLes('maison'))
    
    locBebe=emplacementsMaisons.difference(emplacements).pop()
    nouveauNe=Personnage(locBebe,nbJoueurs+1,joueur.couleur)
    ferme.mettrePersonnage(nouveauNe,locBebe)
    carte.mettrePersonnage(nouveauNe)
    nouveauNe.consomationNourriture=1
    joueur.personnagesPlaces.append(nouveauNe)
    
    return choixAmenagementMineur(partie,choix,possibilites,carte)

  
        

##################################################################################
#---------------------------------------SAVOIR FAIRE------------------------------
##################################################################################
def coutSavoirFaire1(partie,carte):
    joueur=partie.joueurQuiJoue()
    if joueur.combienJaiJoueDe('s')==0:
        return {}
    else:
        return {'n':1}

def coutSavoirFaire2(partie,carte):
    if partie.joueurs[partie.quiJoue].combienJaiJoueDe('s')<2:
        return {'n':1}
    else:
        return {'n':2}
    
def possibilitesSavoirFaire(partie,carte,Fake=False):
    possibilites=[]   
    joueur=partie.joueurQuiJoue()
    for c in joueur.cartesEnMain:
        if c.uid[0]=='s':
            if joueur.jeRemplisLesConditions(c.conditionAchat):
                #cout de la carte + de l'action (pour foire du travail)
                if joueur.jePeuxJouer(util.ajouter(c.cout,carte.cout)):            
                    possibilites.append(c.uid)
    partie.changerPointeurs(possibilites ,carte,phrase='p0',Fake=Fake,djangoJoueur=joueur.djangoUid) 

      
    
def choixSavoirFaire(partie,choix,possibilites,carte,payant=True):
    savoirFaireChoisiUid=possibilites[choix]
    joueur=partie.joueurQuiJoue()
    for c in joueur.cartesEnMain:
        if c.uid==savoirFaireChoisiUid:
            savoirFaireChoisi=c
            break
    #il faut le faire avant car le cout depends du nombre de savoir faire joues
    #payant par defaut mais gratuit dans le cas savoirfaire ou naissance
    if payant:
        joueur.mettreAJourLesRessources(util.ajouter(savoirFaireChoisi.cout,carte.cout))
    else:
        joueur.mettreAJourLesRessources(savoirFaireChoisi.cout)
    joueur.poserCarteDevantSoi(savoirFaireChoisi)    
    personnage=joueur.personnages.pop()
    joueur.personnagesPlaces.append(personnage)                  
    carte.mettrePersonnage(personnage)    
    partie.messagesPrincipaux.append([joueur.nom,"p20",'p2',savoirFaireChoisi.uid])
    partie.log.info([joueur.nom,"p20",'p2',savoirFaireChoisi.uid])
    partie.changerPointeurs(-1 ,None) 


##################################################################################
#---------------------------------------MINEUR          --------------------------
##################################################################################

def possibilitesAmenagementMineur(partie,carte,Fake=False):
    possibilites=[]   
    joueur=partie.joueurQuiJoue()
    plateau=partie.plateau
    for c in  joueur.cartesEnMain:
        if c.uid[0]=="m":
            #ici c'est condition achat... on ne veut pas appeler poss non vide de la carte à acheter
            if joueur.jeRemplisLesConditions(c.conditionAchat):
                
                #pour gerer les cout listes
                if type(c.cout)==list:
                    for coutSimple in c.cout:
                        #cout de la carte + de l'action (pour foire du travail)
                        if joueur.jePeuxJouer(util.ajouter(carte.cout,coutSimple)):
                            
                            possibilites.append('{}_cout{}'.format(c.uid,c.cout.index(coutSimple)))
                        else:
                            partie.messagesDetail.append(["p10",c.uid])
                else:
                
                    #cout de la carte + de l'action (pour foire du travail)
                    if joueur.jePeuxJouer(util.ajouter(carte.cout,c.cout)):
                        possibilites.append(c)
                    else:
                        partie.messagesDetail.append(["p10",c.uid])
            else:
                partie.messagesDetail.append(["p9",c.uid])
    #si on appelle cette methode via l'action spéciale 
    #on n'ajoute pas la possibilité u3 (ne rien faire)
    #ainsi on ne peux pas faire l'action spéciale si on ne peux construire aucun
    #ammenagement grace à possibiliteNonVide
    if not hasattr(carte,"carteQuiMePorte"):
        possibilites.append('u3')
    partie.changerPointeurs(possibilites ,carte,phrase='p29',djangoJoueur=joueur.djangoUid,Fake=Fake,jouerEgalEffet=not Fake)   
                 
    
def choixAmenagementMineur(partie,choix,possibilites,carte):
    carteChoisie=possibilites[choix]
    joueur=partie.joueurQuiJoue()
    plateau=partie.plateau
    
    #si vrai il y a un coup variable
    if type(carteChoisie)==str:
        if "_cout" in carteChoisie:
            carteUid=carteChoisie.split('_cout')[0]
            coutChoisi=int(carteChoisie.split('_cout')[1])
            carteJouee=util.findCarte(joueur.cartesEnMain,carteUid)
            
            coutChoisi=carteJouee.cout[coutChoisi]
        else:
            carteJouee=carteChoisie

    else:
        carteJouee=carteChoisie
        coutChoisi=carteJouee.cout
    
    
    
    if hasattr(carte,"carteQuiMePorte"):
            joueur.mettreAJourLesRessources(util.ajouter(carte.cout,coutChoisi))
            carte.carteQuiMePorte.changerEtat(partie.quiJoue)
            joueur.poserCarteDevantSoi(carteJouee)
            partie.messagesPrincipaux.append([joueur.nom,"p3",carteJouee])
    else:        
        personnage=joueur.personnages.pop()
        joueur.personnagesPlaces.append(personnage)                  
        carte.mettrePersonnage(personnage)               
        if carteJouee=="u3":
            #on ne fait pas de mineur
            partie.log.info([joueur.nom, "p16"])
            partie.messagesPrincipaux.append([joueur.nom, "p16"])   
                
        else:    
            joueur.mettreAJourLesRessources(util.ajouter(carte.cout,coutChoisi))
            joueur.poserCarteDevantSoi(carteJouee)
            partie.messagesPrincipaux.append([joueur.nom,"p3",carteJouee])
 
        
    if carte.uid=="a1":#premier joueur + mineur
        #cas special pour les amants
        if not carteJouee=="u3" and carteJouee.uid=="m9" and jePeuxNaitre(partie, carte):
            self.partie.ajouterHook(carteJouee,carteJouee.option["hook_possibilites"],carteJouee.owner.djangoUid,'instant')
        else:
            
            partie.log.info([joueur.nom,"p30"])
            partie.premierJoueur=joueur.id

    
    partie.log.info([joueur.nom,"p3",carteJouee])
    partie.changerPointeurs(-1 ,None)   

##################################################################################
#---------------------------------------Majeur          --------------------------
##################################################################################        
# def possibilitesAmenagementMajeur(partie,carte,Fake=False):
#     possibilites=[]   
#     joueur=partie.joueurQuiJoue()
#     plateau=partie.plateau
#     for k,c in plateau["majeurs"].items():
#         if c.visible:
#             if joueur.jeRemplisLesConditions(c.conditionAchat):
#                 if joueur.jePeuxJouer(util.ajouter(c.cout,carte.cout)):
#                     possibilites.append(c)
#     partie.changerPointeurs(possibilites ,carte,'p34',joueur,Fake=Fake)       

def possibilitesAmenagementMajeur(partie,carte,Fake=False):
    possibilites=[]   
    joueur=partie.joueurQuiJoue()
    plateau=partie.plateau
    for k,c in plateau["majeurs"].items():
        if c.uid[0]=="M" and c.visible:
            #ici c'est condition achat... on ne veut pas appeler poss non vide de la carte à acheter
            if joueur.jeRemplisLesConditions(c.conditionAchat):
                
                #pour gerer les cout listes
                if type(c.cout)==list:
                    for coutSimple in c.cout:
                        #cout de la carte + de l'action (pour foire du travail)
                        if joueur.jePeuxJouer(util.ajouter(carte.cout,coutSimple)):
                            
                            possibilites.append('{}_cout{}'.format(c.uid,c.cout.index(coutSimple)))
                        else:
                            partie.messagesDetail.append(["p10",c.uid])
                else:
                
                    #cout de la carte + de l'action (pour foire du travail)
                    if joueur.jePeuxJouer(util.ajouter(carte.cout,c.cout)):
                        possibilites.append(c)
                    else:
                        partie.messagesDetail.append(["p10",c.uid])
            else:
                partie.messagesDetail.append(["p9",c.uid])
    #si on appelle cette methode via l'action spéciale 
    #on n'ajoute pas la possibilité u3 (ne rien faire)
    #ainsi on ne peux pas faire l'action spéciale si on ne peux construire aucun
    #ammenagement grace à possibiliteNonVide
    partie.changerPointeurs(possibilites ,carte,phrase='34',djangoJoueur=joueur.djangoUid,Fake=Fake,jouerEgalEffet=not Fake)   
                 
    
    
def choixAmenagementMajeur(partie,choix,possibilites,carte):
    carteJouee=possibilites[choix]
    joueur=partie.joueurQuiJoue()
    plateau=partie.plateau
    partie.messagesPrincipaux.append([joueur.nom,"p14",carteJouee.uid])
    partie.log.info([joueur.nom,"p14",carteJouee.uid])
    #si c'est une action speciale
    if hasattr( carte,"carteQuiMePorte"):
        joueur.mettreAJourLesRessources(util.ajouter(carte.cout,carteJouee.cout))
        carte.carteQuiMePorte.changerEtat(partie.quiJoue)
        joueur.poserCarteDevantSoi(carteJouee,Majeur=True)
        partie.changerPointeurs(-1 ,None)  
   
        
    else:
        
        TODO

##################################################################################
#---------------------------------------MINEUR OU MAJEUR--------------------------
##################################################################################

def possibilitesAmenagementMineurOuMajeur(partie,carte,Fake=False,possibiliteRien=False):
    possibilites=[]   
    joueur=partie.joueurQuiJoue()
    plateau=partie.plateau
    
    for c in  joueur.cartesEnMain:
        if c.uid[0]=="m":
            #ici c'est condition achat... on ne veut pas appeler poss non vide de la carte à acheter
            if joueur.jeRemplisLesConditions(c.conditionAchat):
                
                #pour gerer les cout listes
                if type(c.cout)==list:
                    for coutSimple in c.cout:
                        #cout de la carte + de l'action (pour foire du travail)
                        if joueur.jePeuxJouer(util.ajouter(carte.cout,coutSimple)):
                            
                            possibilites.append('{}_cout{}'.format(c.uid,c.cout.index(coutSimple)))
                        else:
                            partie.messagesDetail.append(["p10",c.uid])
                else:
                
                    #cout de la carte + de l'action (pour foire du travail)
                    if joueur.jePeuxJouer(util.ajouter(carte.cout,c.cout)):
                        possibilites.append(c)
                    else:
                        partie.messagesDetail.append(["p10",c.uid])
            else:
                partie.messagesDetail.append(["p9",c.uid])    
                
                        
    for m in  plateau['majeurs'].keys():
        if plateau['majeurs'][m].visible:
             if joueur.jePeuxJouer(plateau['majeurs'][m].cout):
                        possibilites.append(plateau['majeurs'][m])   
    if possibiliteRien:
        possibilites.append('u3')
    partie.changerPointeurs(possibilites ,carte,phrase='p35',djangoJoueur=joueur.djangoUid,Fake=Fake,jouerEgalEffet=not Fake)  
    
     
def choixAmenagementMineurOuMajeur(partie,choix,possibilites,carte):
    
    carteChoisie=possibilites[choix]
    joueur=partie.joueurQuiJoue()
    plateau=partie.plateau
    
    #si vrai il y a un coup variable
    if type(carteChoisie)==str:
        if "_cout" in carteChoisie:
            carteUid=carteChoisie.split('_cout')[0]
            coutChoisi=int(carteChoisie.split('_cout')[1])
            carteJouee=util.findCarte(joueur.cartesEnMain,carteUid)
            
            coutChoisi=carteJouee.cout[coutChoisi]
        else:
            carteJouee=carteChoisie

    else:
        carteJouee=carteChoisie
        coutChoisi=carteJouee.cout
    
    
    personnage=joueur.personnages.pop()
    joueur.personnagesPlaces.append(personnage)                  
    carte.mettrePersonnage(personnage)               
      
    joueur.mettreAJourLesRessources(util.ajouter(carte.cout,coutChoisi))
    Majeur=not carteJouee in joueur.cartesEnMain
    joueur.poserCarteDevantSoi(carteJouee,Majeur=Majeur)
    partie.messagesPrincipaux.append([joueur.nom,"p3",carteJouee])
 
        
    
    partie.log.info([joueur.nom,"p3",carteJouee])
    partie.changerPointeurs(-1 ,None)   
    
#     
#     carteJouee=possibilites[choix]
#     carteJouee.jouer()
#     TODO
#     joueur=partie.joueurQuiJoue()
#     plateau=partie.plateau
#     Majeur=not carteJouee in joueur.cartesEnMain
#     joueur.poserCarteDevantSoi(carteJouee,Majeur)
#     #on paye le cout de la carte
#     joueur.mettreAJourLesRessources(carteJouee.cout)
#     partie.log.info("{} {} {}".format(joueur.nom, "réalise ",carteJouee.uid))
#     personnage=joueur.personnages.pop()
#     joueur.personnagesPlaces.append(personnage)                  
#     carte.mettrePersonnage(personnage)
#     encore=False    
#     partie.changerPointeurs(-1,None)

##################################################################################
#---------------------------------------Actions spé-------------------------------
##################################################################################
def possibilitesAbattreDesArbres(partie,carte,Fake=False):
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme
    partie.changerPointeurs(ferme.tousLes('foret') ,carte,'p27',joueur,Fake=Fake)    
        


def choixAbattreDesArbres(partie,choix,possibilites,carte):
    caseAbattre=possibilites[choix]
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme
    ferme.etat[caseAbattre].type="vide"
    joueur.mettreAJourLesRessources(util.ajouter(joueur.coutAbattre(),carte.cout))
    carte.carteQuiMePorte.changerEtat(partie.quiJoue)
    partie.messagesPrincipaux.append([partie.joueurQuiJoue().nom, 'p41',caseAbattre])
    partie.changerPointeurs(-1,None)

def possibilitesCouperBruler(partie,carte,Fake=False):
    possibilites=[]
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme
    forets=ferme.tousLes('foret') 
    #les champs doivent se toucher
    if(ferme.compter("champ")!=0):
        foretsAdjChamp=[]
        for f in forets:
            voiz=ferme.voisin(f)
            for direction in voiz.keys():
                if voiz[direction]: #si not None
                    if ferme.etat[voiz[direction]].type=='champ':
                        if not f in foretsAdjChamp:
                            foretsAdjChamp.append(f)
        partie.changerPointeurs(foretsAdjChamp ,carte,'p28',joueur,Fake=Fake)    
    else:
        partie.changerPointeurs(ferme.tousLes('foret') ,carte,'p28',joueur,Fake=Fake)    
        

def choixCouperBruler(partie,choix,possibilites,carte):
    caseCouper=possibilites[choix]
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme
    ferme.etat[caseCouper].type="champ"
    joueur.mettreAJourLesRessources(carte.cout)
    carte.carteQuiMePorte.changerEtat(partie.quiJoue)
        
    partie.messagesPrincipaux.append([partie.joueurQuiJoue().nom,'p42',caseCouper])
    partie.changerPointeurs(-1,None)


def possibilitesCouperLaTourbe(partie,carte,Fake=False):
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme
    partie.log.debug('possibilitesCouperLaTourbe!!!!!!!!!!!!!!!!!!!!')
    partie.changerPointeurs(ferme.tousLes('tourbe'),carte,phrase="p32",Fake=Fake,jouerEgalEffet=not Fake)
        

def choixCouperLaTourbe(partie,choix,possibilites,carte):
    caseCouper=possibilites[choix]
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme
    ferme.etat[caseCouper].type="vide"
    joueur.mettreAJourLesRessources(util.ajouter(joueur.coutTourbe(),carte.cout))
    carte.carteQuiMePorte.changerEtat(partie.quiJoue)
    
    partie.messagesPrincipaux.append([partie.joueurQuiJoue().nom,'p43',caseCouper])
    encore=False    
    partie.changerPointeurs(-1,None)
##################################################################################
#---------------------------------------LABOURAGE---------------------------------
##################################################################################

def possibilitesLabourage(partie,carte,Fake=False):
    possibilites=[]
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme
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
    partie.changerPointeurs(possibilites,carte,phrase="p37",Fake=Fake)


def labourage(partie,choix,possibilites,carte):
    caseALabourer=possibilites[choix]
    ferme=partie.joueurQuiJoue().courDeFerme
    ferme.etat[caseALabourer].type="champ"
    partie.messagesPrincipaux.append([partie.joueurQuiJoue().nom,'p22',caseALabourer])
    personnage=partie.joueurQuiJoue().personnages.pop()
    partie.joueurQuiJoue().personnagesPlaces.append(personnage)                  
    carte.mettrePersonnage(personnage)
    partie.changerPointeurs(-1,None)



def naissanceSansPieceLibre(partie,choix,possibilites,carte):
    
    
    from pygricola.joueur.personnage import Personnage

    joueur=partie.joueurs[partie.quiJoue]
    ferme=joueur.courDeFerme
    locBebe='B1'
    nouveauNe=Personnage(locBebe,1+len(joueur.personnages)+len(joueur.personnagesPlaces),joueur.couleur)
    nouveauNe.consomationNourriture=1
    joueur.personnagesPlaces.append(nouveauNe)
    nouveauNe.localisation=carte
    carte.occupants.append(nouveauNe)
    personnage=joueur.personnages.pop()
    joueur.personnagesPlaces.append(personnage)                  
    carte.mettrePersonnage(personnage)    
    partie.changerPointeurs(-1,None)    
##################################################################################
#---------------------------------------Cloture--------------------------
##################################################################################

def jePeuxCloturer(partie,carte):
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme
    cout=ferme.coutMiniCloture()
    ressourceOk=joueur.jePeuxJouer(cout)
    resteClotureOk=ferme.cloturesDispo>0
    #si je n'en ai pas
    if ferme.compter('paturages')==0:
        placeOk=ferme.compter('vide')
        return ressourceOk and placeOk
    else:
    #si j'en ai je regarde si j'en ai un de divisable
        divisableOk=False
        for pat in ferme.tousLes('paturages'):
            if pat.estDivisable():
                divisableOk=True
        if divisableOk:
            return ressourceOk
        else:
            #dans ce cas aucun n'est divisable
            #il faut une case vide ou etable seule
            caseVideOuEtableSeule=False
            for pat in ferme.tousLes('paturages'):
                voiz=ferme.voisin(c)
                for direction in voiz.keys():
                    if voiz[direction]: #si not None
                        if ferme.etat[voiz[direction]].type=='vide' or ferme.etat[voiz[direction]].type=='etable':
                                caseVideOuEtableSeule=True
                                break
            
            return ressourceOk and caseVideOuEtableSeule
    
    
    return resteClotureOk and ressourceOk and (placeOk or divisableOk)

def demanderPlanCloture(partie,carte,Fake=False):
    partie.changerPointeurs('inputtext' ,carte,'p53',Fake=False)    


def randomPlanCloture(partie):
    return partie.joueurQuiJoue().courDeFerme.tousLes('vide')[0]
    
def planCloture(partie,planStr,possibilites,carte):
    #par ex C2,C3-C4  ou 
    #C2-C3-C4,B5
    #obligé de faire ça pour les tests aleatoir django... 
    #la bas on ne connais pas la partie etc...
    
    if planStr=="randomPlanCloture":
        planStr=randomPlanCloture(partie)
    
    partie.log.debug('planCloture {}'.format(planStr))    
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme                                  
    planCorrect=True
    cout=util.rVide()
    msg=""
    listePaturagesNouveaux=[]
    tupListePaturagesADiviser=[]
    listePaturageDejaTraite=[]
    
    ferme.tmpPaturage=[] #reinit au cas ou
    
    
    #dans le cas RenoPuiCloture il se peut qu'on ne fasse pas de cloture
    if planStr=='0' and carte.uid=='a23':
        partie.messagesPrincipaux.append([partie.joueurQuiJoue().nom,'p70'])
        personnage=partie.joueurQuiJoue().personnages.pop()
        partie.joueurQuiJoue().personnagesPlaces.append(personnage)                  
        carte.mettrePersonnage(personnage)
        partie.changerPointeurs(-1,None)    
        return        
    
    for paturage in planStr.split(','):
        #si c'est une seule case
        if len(paturage)==2:
            if paturage in ferme.etat.keys():
                if ferme.etat[paturage].type in ['vide','etable']:
                    #on regarde si le paturage est déjà pris en compte
                    listePaturagesNouveaux.append(paturage)
                    listePaturageDejaTraite.append(paturage)
                elif ferme.etat[paturage].type =='paturage':
                    #la case est déja dans un paturage on veut diviser....
                    #controle
                    if paturage in ferme.etat[paturage].cases:
                        if len ( ferme.etat[paturage].cases)==1:
                            planCorrect=False
                            msg="plan invalide: {}, le paturage {} existe déjà et n'est plus modifiable".format(planStr,paturage)
                            partie.log.debug(msg)
                            partie.changerPointeurs('inputtext',carte,alert=msg)
                            return     

                        else:
                            listePaturageDejaTraite.append(paturage)
                            tupListePaturagesADiviser.append((paturage,ferme.etat[paturage]))
                    else:
                        impossible
                    
                else:
                    planCorrect=False
                    msg="plan invalide: {}, doit être vide ou être une étable".format(planStr)
                    partie.log.debug(msg)
                    partie.changerPointeurs('inputtext',carte,alert=msg)
                    return                                        
            else:
                planCorrect=False
                msg="plan invalide: {}, n'est pas une case de ferme {}".format(planStr,paturage)
                partie.log.debug(msg)
                partie.changerPointeurs('inputtext',carte,alert=msg)
                return  
        else:
            sp=paturage.split('-')
            if len(sp)<2:
                planCorrect=False
                msg="plan invalide: {}, un paturage multiple doit contenir un au moins un - {}".format(planStr,paturage)
                partie.log.debug(msg)
                partie.changerPointeurs('inputtext',carte,alert=msg)
                return  
            else:
                #ici sp est de la forme AX-BY-CZ ....
                #une case doit être dans la cour de ferme et voisine de la précédente...           
                #les cases doivent être soit vide ou étables casA
                #si l'une est paturages elles doivent être dans le même casB
                casA=None
                casB=None                
                listePrecedent=[]              
                for case in sp:
                    if case in ferme.etat.keys():                      
                        if ferme.etat[case].type in ['vide','etable']:  
                            casA=True 
                            if len(listePrecedent)>0:
                                #il doit y avoir un voisin dans les précédents
                                voizOk=False
                                for casePrecedent in listePrecedent:
                                    if ferme.estVoisin(case,casePrecedent):
                                        voizOk=True
                                        break

                                if not voizOk:
                                    planCorrect=False
                                    msg="plan invalide: {}, lors d'un paturage multiple chacune des cases separees par un - doit être un des voisines des autres".format(planStr,listePrecedent)
                                    partie.log.debug(msg)
                                    partie.changerPointeurs('inputtext',carte,alert=msg)  
                                    return
                            if casB is None:
                                listePrecedent.append(case)
                            else:
                                planCorrect=False
                                msg="plan invalide: {}, un groupe de case separé par un tiret est soit dans un paturage deja existant, soit a l'exterieur {}".format(planStr,sp)
                                partie.log.debug(msg)
                                partie.changerPointeurs('inputtext',carte,alert=msg) 
                                return                    
                        elif ferme.etat[case].type in ['paturage']:
                            casB=True  
                            pAdiviser=ferme.etat[case]
                            if precedente:
                                if not ferme.estVoisin(case,precedente):
                                    planCorrect=False
                                    msg="plan invalide: {}, lors d'un paturage multiple deux cases separees par un - doivent être des voisines: {} et {} ne le sont pas".format(planStr,precedente,case)
                                    partie.log.debug(msg)
                                    partie.changerPointeurs('inputtext',carte,alert=msg)
                                    return
                            if casA is None:
                                precedente=case
                            else:
                                planCorrect=False
                                msg="plan invalide: {}, un groupe de case separé par un tiret est soit dans un paturage deja existant, soit a l'exterieur {}".format(planStr,sp)
                                partie.log.debug(msg)
                                partie.changerPointeurs('inputtext',carte,alert=msg)  
                                return                         
                        else:
                            planCorrect=False
                            msg="plan invalide: {}, n'est pas cloturable {}".format(planStr,case)
                            partie.log.debug(msg)
                            partie.changerPointeurs('inputtext',carte,alert=msg)   
                            return
                        
                                              
                    else:
                        planCorrect=False
                        msg="plan invalide: {}, n'est pas une case de ferme {}".format(planStr,case)
                        partie.log.debug(msg)
                        partie.changerPointeurs('inputtext',carte,alert=msg) 
                        return
                #verif de controle
                if casA is None and casB is None:
                    Impossible
                elif casA is None:
                    if not casB:
                        Impossible
                elif casB is None:
                    if not casA:
                        Impossible
                else:
                    Impossible
                if casA:
                   listePaturagesNouveaux.append(sp)    
                else:
                   tupListePaturagesADiviser.append((sp,pAdiviser)) 
                for paturage in sp:
                    listePaturageDejaTraite.append(paturage)        
                                        
    partie.log.debug('listePaturagesNouveaux {}'.format(listePaturagesNouveaux))
    partie.log.debug('tupListePaturagesADiviser {}'.format(tupListePaturagesADiviser))
    partie.log.debug('listePaturageDejaTraite {}'.format(listePaturageDejaTraite))
    
    #on regarde si les paturage est déjà fait
    if len(set(listePaturageDejaTraite)) != len(listePaturageDejaTraite):
        planCorrect=False
        msg="plan invalide: {}, une case ne peut apparaitre qu'une seule fois dans le plan".format(planStr)
        partie.log.debug(msg)
        partie.changerPointeurs('inputtext',carte,alert=msg)  
        return               
    
    
    partie.log.debug(planCorrect)
    coutTotal={'b':0}
    #on traite les nouveaux paturages...
    for paturage in listePaturagesNouveaux:
        partie.log.debug("traitement de {}".format(paturage))
        if type(paturage)==str:
            cout=ferme.coutCreerPaturage([paturage])
            coutTotal=util.ajouter(coutTotal,cout)
            ferme.tmpPaturage.append(paturage)
        else:
            cout=ferme.coutCreerPaturage(paturage)
            coutTotal=util.ajouter(coutTotal,cout)
            for pat in paturage:
                ferme.tmpPaturage.append(pat)
    
    jokerPremierPaturage=True        
    #toutes les cases de tmpPaturages doivent se toucher
    for tPat in ferme.tmpPaturage:
        voiz=ferme.voisin(tPat)
        caseIsolee=True
        print('test ADJ',tPat)
        for direction in voiz.keys():
            if voiz[direction] in ferme.tmpPaturage or voiz[direction] in  ferme.tousLes('paturage'): #si not None
                print('non isolee',voiz[direction])
                caseIsolee=False
                jokerPremierPaturage=False
        if caseIsolee:
            print('isole',jokerPremierPaturage)
            #soit c'est la premier construction  soit non
            if ferme.compter('paturage')>0 or not jokerPremierPaturage:
                planCorrect=False
                msg="plan invalide: {}, la case {} est isolée or les paturages doivent se toucher".format(planStr,tPat)
                partie.log.debug(msg)
                partie.changerPointeurs('inputtext',carte,alert=msg)  
                return               
            else:
                jokerPremierPaturage=False
                print('tata',jokerPremierPaturage)
    
    ferme.tmpPaturage=[] #on reinitialise
    #on a evalué le cout total
    partie.log.debug(coutTotal)
    partie.log.debug("ETABLES       {}".format(ferme.reserveEtable))
    if joueur.jePeuxJouer(coutTotal):
        for paturage in listePaturagesNouveaux:
            if type(paturage)==str:
                ferme.creerPaturageSimple(paturage,etable=ferme.etat[paturage].type=='etable')
            else:
                ferme.creerPaturageMultiple(paturage)
        partie.log.debug("ETABLES       {}".format(ferme.reserveEtable))
        joueur.mettreAJourLesRessources(coutTotal)
        partie.messagesPrincipaux.append([partie.joueurQuiJoue().nom,'p54'])
        personnage=partie.joueurQuiJoue().personnages.pop()
        partie.joueurQuiJoue().personnagesPlaces.append(personnage)                  
        carte.mettrePersonnage(personnage)
        partie.changerPointeurs(-1,None)            
    else:
        planCorrect=False
        msg="plan invalide: {}, vous n'avez pas assez de ressources, vous avez {}\n il faut {}".format(planStr,joueur.ressources,coutTotal)
        partie.log.debug(msg)
        partie.changerPointeurs('inputtext',carte,alert=msg) 
        return
            
    
    
##################################################################################
#---------------------------------------Piece et Etables--------------------------
##################################################################################

def demanderPlanConstructionDePieceEtOuEtable(partie,carte,Fake=False):
    partie.changerPointeurs('inputtext' ,carte,'p38',Fake=False)    


def randomPlanConstructionDePieceEtOuEtable(partie):
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme     
    coutPiece=joueur.prixDeLaPiece()
    if joueur.jePeuxJouer(coutPiece):
        piecePossible=False
        #on regarde si on peut mettre la maison
        for c in ferme.tousLes('maison'):
            voiz=ferme.voisin(c)
            for direction in voiz.keys():
                if voiz[direction]: #si not None
                    if ferme.etat[voiz[direction]].type=='vide':
                        piecePossible=True
                        break
        if piecePossible:
            return "{}:P".format(voiz[direction])
    #si on est la on ne peux pas faire de piece
    #on fait une etable sur la premier case venue
    return "{}:E".format(ferme.tousLes('vide')[0])
    
    
def planConstructionDePieceEtOuEtable(partie,planStr,possibilites,carte):
    #par ex C2:P,C3:P,C4:E,A1:E
    #obligé de faire ça pour les tests aleatoir django... 
    #la bas on ne connais pas la partie etc...
    
    if planStr=="randomPlanConstructionDePieceEtOuEtable":
        planStr=randomPlanConstructionDePieceEtOuEtable(partie)
    
    partie.log.debug('planConstructionDePieceEtOuEtable {}'.format(planStr))
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme                                  
    planCorrect=True
    casesMaison=[]
    casesEtables=[]
    cout=util.rVide()
    typeMaison=ferme.enQuoiEstLaMaison()
    msg=""
    for tup in planStr.split(','):
        try:
            case=tup.split(':')[0]
            type=tup.split(':')[1]
        except:
            planCorrect=False
            msg="format de plan invalide {}".format(planStr)
            partie.log.debug(msg)
            partie.changerPointeurs('inputtext',carte,alert=msg)
            return
        #la case doit exister 
        if case in ferme.etat.keys():
            #et etre vide
            if ferme.etat[case].type=='vide':
                #p comme piece        
                if(type=='P'):
                    casesMaison.append(case)
                    cout=util.ajouter(cout,joueur.prixDeLaPiece())
                elif(type=='E'): 
                    casesEtables.append(case)
                    cout=util.ajouter(cout,{'b':2})
                else:
                    planCorrect=False
                    msg="type de case {} invalide... Soit soit 'E' soit 'P'".format(type)
                    break
            
            elif ferme.etat[case].type=='paturage':
                #on regarde combien il a d'étables
                if len(ferme.etat[case].cases)>len(ferme.etat[case].etables):
                    casesEtables.append(case)
                    cout=util.ajouter(cout,{'b':2})
                else:
                    planCorrect=False
                    msg="le paturage ne peut plus accueillir d'étables".format(case)
                    break                    
            
            
            else:
                planCorrect=False
                msg="la case {} n'est pas vide".format(case)
                break
        else:
            planCorrect=False
            msg="la case {} n'existe pas".format(case)
            break
    #si pour le moment on est bon
    if (planCorrect):
        if(joueur.jePeuxJouer(cout)):
            if (ferme.etablesDispo<len(casesEtables)):
                planCorrect=False
                msg="vous n'avez pas assez d'étables, il en reste  {} ".format(ferme.etablesDispo)                
        else:
            planCorrect=False
            msg="vous ne pouvez pas payer le cout {} ".format(cout)
    
    if (planCorrect):
        if len(set(casesEtables).intersection(set(casesMaison)))>0:
            planCorrect=False
            msg="Vous une case est soit une pièce soit une étable mais pas les deux! piece:{} etables:{}".format(casesMaison,casesEtables)            
    
    #les maison doivent se toucher                
    if (planCorrect):   
        
        casesMaisonOk=[]
        casesMaisonKo=[]
        while(len(casesMaison)>0):
            case= casesMaison.pop()
            voiz=ferme.voisin(case)
            toucheUneMaison=False
            for direction in voiz.keys():
                if voiz[direction]:
                    if 'maison' in ferme.etat[voiz[direction]].type:
                        toucheUneMaison=True
                        casesMaisonOk.append(case)
                        break
            if(not toucheUneMaison):
                casesMaisonKo.append(case)
        compteur=len(casesMaisonKo)
        while(compteur>0):
            ko=casesMaisonKo.pop(0)
            #si il y a des cases dans casesMaisonKO
            #sont elle voisin de ok
            voisinAuFinal=False 
            for ok in casesMaisonOk:
                if ferme.estVoisin(ok,ko):
                    voisinAuFinal=True
                    casesMaisonOk.append(ko)
                    compteur-=1
            if not voisinAuFinal:
                casesMaisonKo.append(ko)
                compteur-=1
        if len(casesMaisonKo)>0:
            planCorrect=False
            msg="les maisons ne se touchent pas {} ".format(casesMaisonKo)      
    partie.log.debug(msg)
    #quand on est la on est bon    
    if(planCorrect):
        for c in casesMaisonOk:
            ferme.etat[c].type=ferme.enQuoiEstLaMaison(False)
        for c in casesEtables:
            if ferme.etat[c].type=='vide':
                ferme.etat[c].type="etable"
                ferme.reserveEtable.pop()
            elif ferme.etat[c].type=='paturage':
                ferme.etat[c].etables.append(c)
                ferme.reserveEtable.pop()
                
        joueur.mettreAJourLesRessources(cout)
        partie.messagesPrincipaux.append([partie.joueurQuiJoue().nom,'p44',len(casesMaisonOk),'p45',len(casesEtables),'p46'])
        personnage=partie.joueurQuiJoue().personnages.pop()
        partie.joueurQuiJoue().personnagesPlaces.append(personnage)                  
        carte.mettrePersonnage(personnage)
        partie.changerPointeurs(-1,None)
    else:
        #on est pas bon        
        partie.changerPointeurs('inputtext',carte,phrase='p31',alert=msg)


def possibiliteConstructionOuSpectacle(partie,carte,Fake=False):
    possibilites=["u6"]
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme
    cout=joueur.prixDeLaPiece()
    ressourcesOk=joueur.jePeuxJouer(cout)
    if ressourcesOk:    
        for c in ferme.tousLes('maison'):
            voiz=ferme.voisin(c)
            for direction in voiz.keys():
                if voiz[direction]: #si not None
                    if ferme.etat[voiz[direction]].type=='vide':
                        possibilites.append(['u7',voiz[direction]])
    partie.changerPointeurs(possibilites ,carte,phrase='p0',djangoJoueur=joueur.djangoUid,Fake=Fake,jouerEgalEffet=not Fake)  

def constructionOuSpectacle(partie,choix,possibilites,carte):
    joueur=partie.joueurQuiJoue()

    if possibilites[choix]=="u6":
        coutAAppliquer=carte.vider()
        partie.messagesPrincipaux.append([joueur.nom,'p47','u6'])
        partie.log.info("{} va sur Spectacle".format(joueur.nom))

    else:
        ferme=joueur.courDeFerme
        cout=joueur.prixDeLaPiece()   
        coutCase=carte.vider()
        coutAAppliquer=util.ajouter(coutCase,cout)
        typeMaison=ferme.enQuoiEstLaMaison(False)
        case=possibilites[choix][1]
        ferme.etat[case].type=typeMaison  
        partie.messagesPrincipaux.append([partie.joueurQuiJoue().nom,'p44',1,'p48',case])
        partie.log.info("{} construit 1 pièce en {}".format(partie.joueurQuiJoue().nom,case))

    joueur.mettreAJourLesRessources(coutAAppliquer,actionDunePersonne=True)
    personnage=partie.joueurQuiJoue().personnages.pop()
    partie.joueurQuiJoue().personnagesPlaces.append(personnage)                  
    carte.mettrePersonnage(personnage)
    
    partie.changerPointeurs(-1,None)


def jePeuxContruireUnePiece(partie):    
    joueur=partie.joueurQuiJoue()
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
 
def jePeuxContruireUneEtable(partie):    
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme   
     
    ressourcesOk=joueur.jePeuxJouer({"b":2})
    placeOk=(ferme.compter('vide')>0)
    etablesOk=ferme.etablesDispo>0
    
     
    return (placeOk and ressourcesOk and etablesOk)
 
def jePeuxFaireConstructionDePieceEtOuEtable(partie,carte):
    return jePeuxContruireUneEtable(partie) or jePeuxContruireUnePiece(partie)    



##################################################################################
#---------------------------------------Semaille et Cuisson--------------------------
##################################################################################  

    
def jePeuxFaireSemailleEtOuCuisson(partie,carte):    
    return jePeuxSemer(partie) or jePeuxCuireDuPain(partie)

def jePeuxSemer(partie):
    joueur=partie.joueurQuiJoue()
    possibilites=[]
    ferme=joueur.courDeFerme
    champOk=ferme.compter('champ')>0

    deQuoiSemer=False
    for r in joueur.quePuisJeSemer():
        if joueur.ressources[r]>0:
            deQuoiSemer=True
    return deQuoiSemer and champOk


def jePeuxCuireDuPain(partie):
    fourOk=False
    #j'ai au moins un cereal
    joueur=partie.joueurQuiJoue()
    for uid,c in joueur.cartesDevantSoi.items():
        if 'cuissonPain' in c.option.keys():
            fourOk=True
    return joueur.ressources['c']>0 and fourOk


def demanderPlanSemaille(partie,carte,Fake=False):
    if carte.uid=='a13':
        partie.changerPointeurs('inputtext',carte,phrase='p33',Fake=Fake)
    elif carte.uid=='a21':
        partie.changerPointeurs('inputtext',carte,phrase='p69',Fake=Fake)
    
def randomPlanSemailleEtOuCuisson(partie):
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme    
    #on essaye de semer
    if ferme.compter('champ')>0 and (joueur.ressources['c']>0 or joueur.ressources['l']>0):
        maxSemis=min(ferme.compter('champ'),joueur.ressources['c']+joueur.ressources['l'])
        sem={'c':0,'l':0}
        stri=""
        for champ in ferme.tousLes('champ'):
            if maxSemis==0:
                break
            #on seme un sur 2
            if maxSemis%2==0:
                res='c' if (joueur.ressources['c']-sem['c'])>0 else 'l'
            else:
                res='l' if (joueur.ressources['l']-sem['l'])>0 else 'c'
            stri+="{}:{},".format(champ,res)
            sem[res]+=1
            maxSemis-=1
        return stri[0:-1]   
    
    #sinon on cuit une céréale
    return "c:1"
        
def planSemailleEtOuCuisson(partie,planStr,possibilites,carte):
    #par ex C2:c,C3:l,c:4
    
    #pour tests django et random
    if planStr=="randomPlanSemailleEtOuCuisson":
        planStr=randomPlanSemailleEtOuCuisson(partie)
    partie.log.debug(planStr)
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme                                  
    planCorrect=True
    cout=util.rVide()
    validTup=[]
    cerealesACuire=0
    msg=""
    cout={'b':0,'c':0,'l':0} #on ne peut semer que ces 3 trucs
    cuissonPassee=False
    for tup in planStr.split(','):
        try:
            case=tup.split(':')[0]
            type=tup.split(':')[1]
        except:
            planCorrect=False
            msg="format de plan invalide {}".format(planStr)
            partie.changerPointeurs('inputtext',carte,alert=msg)
            return

        
        if case == "c":
            if cuissonPassee:
                planCorrect=False
                msg="plan invalide, il ne peux y avoir qu'une instruction de cuisson"
                partie.changerPointeurs('inputtext',carte,alert=msg)             
            else:
                try:
                    if int(type)<1:
                        nimportequoi #pour passer dans except
                    cout['c']+=int(type)
                    cerealesACuire=int(type)
                    cuissonPassee=True
                except:
                    planCorrect=False
                    msg="Pour la cuisson avec c:X, X doit être un entier strictement positif"
                    partie.changerPointeurs('inputtext',carte,alert=msg)
        else:
            if type in ['b','c','l']:
                #la case doit exister 
                if case in ferme.etat.keys():
                    #et etre un champ
                    if ferme.etat[case].type=='champ':
                        
                        #n'est pas déjà passé
                        if case in [k for k,v in validTup]:
                            planCorrect=False
                            msg="vous avez déjà semé sur cette case {}".format(case)
                            break

                        else:
                            #vide
                            if util.estVide(ferme.etat[case].ressources):
                                cout[type]+=1
                                validTup.append((case,type))
                            else:
                                planCorrect=False
                                msg="la case {} n'est pas vide".format(case)
                                break
                    else:
                        planCorrect=False
                        msg="la case {} n'est pas un champ".format(case)
                        break
                else:
                    planCorrect=False
                    msg="la case {} n'existe pas".format(case)
                    break                           
            else:
                planCorrect=False
                msg="la vous ne pouvez pas semer de {}".format(type)
                break
    #si pour le moment on est bon
    if (planCorrect): 
        if(joueur.jePeuxJouer(cout)):
            #on est OK
            #on cuit les céréales
            cout['n']=-joueur.pouvoirCuisson(cerealesACuire)
            joueur.mettreAJourLesRessources(cout)
            for case,type in validTup:
                ferme.etat[case].semer(type)
            partie.messagesPrincipaux.append([partie.joueurQuiJoue().nom,'p49',cout['c']-cerealesACuire,'rc',',',
                                  cout['l'],'rl',cout['b'],'rb',',','p50',cerealesACuire,'p51',  -cout['n'],'rn'])         
            personnage=partie.joueurQuiJoue().personnages.pop()
            partie.joueurQuiJoue().personnagesPlaces.append(personnage)                  
            carte.mettrePersonnage(personnage)
            partie.changerPointeurs(-1,None)
        else:
            planCorrect=False
            msg="vous ne pouvez pas payer le cout {} ".format(cout)
            partie.changerPointeurs('inputtext',carte,alert=msg)
     
    else:
        #on est pas bon
        print(msg)
        partie.phraseChoixPossibles="Indiquez votre plan de semaille et cuisson de pain"
        partie.changerPointeurs('inputtext',carte,alert=msg)
    
    
def planLabourageSemaille(partie,planStr,possibilites,carte):
    #par ex L:B3,C2:c,C3:l,c:4
    
    #pour tests django et random
    if planStr=="randomPlanLabourageSemaille":
        planStr=randomPlanLabourageSemaille(partie)
    partie.log.debug(planStr)
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme                                  
    planCorrect=True
    cout=util.rVide()
    validTup=[]
    msg=""
    cout={'b':0,'c':0,'l':0} #on ne peut semer que ces 3 trucs
    caseLabour=[] #pour les cartes plus tard
    
    for tup in planStr.split(','):
        try:
            first=tup.split(':')[0]
            second=tup.split(':')[1]
        except:
            planCorrect=False
            msg="format de plan invalide {}".format(planStr)
            partie.changerPointeurs('inputtext',carte,alert=msg)
            return
        #instruction labourage
        if first=='L':
            if second in ferme.etat.keys():
                if ferme.etat[second].type=='vide':
                    if len(caseLabour)==0:
                        #OK
                        caseLabour.append(second)
                    else:
                        planCorrect=False
                        msg="vous ne pouvez labourer une seule case {} est en trop".format(second)
                        break
                else:
                    planCorrect=False
                    msg="la case {} n'est pas vide".format(second)
                    break
            else:
                planCorrect=False
                msg="la case {} n'existe pas".format(second)
                break     
            pass
        #instruction semaille
        else:
            if second in ['b','c','l']:
                #la case doit exister 
                if first in ferme.etat.keys():
                    #et etre un champ
                    if ferme.etat[first].type=='champ':
                        #déja semée
                        if first in [k for k,v in validTup]:
                            planCorrect=False
                            msg="vous avez déjà semé sur cette case {}".format(first)
                            break
                        else:
                            #vide
                            if util.estVide(ferme.etat[first].ressources):
                                cout[second]+=1
                                validTup.append((first,second))
                            else:
                                planCorrect=False
                                msg="la case {} n'est pas vide".format(first)
                                break
                    elif first in caseLabour:
                        cout[second]+=1
                        validTup.append((first,second))
                        
                    else:
                        planCorrect=False
                        msg="la case {} n'est pas un champ".format(first)
                        break
                else:
                    planCorrect=False
                    msg="la case {} n'existe pas".format(first)
                    break                           
            else:
                planCorrect=False
                msg="vous ne pouvez pas semer de {}".format(second)
                break
    #si pour le moment on est bon
    if (planCorrect): 
        if(joueur.jePeuxJouer(cout)):
            joueur.mettreAJourLesRessources(cout)
            #OK, d'abord laboure le champ
            if len(caseLabour)>0:
                caseALabourer=caseLabour.pop()
                ferme.etat[caseALabourer].type="champ"
                partie.messagesPrincipaux.append([joueur.nom,'p22',caseALabourer])
            #maintenant on seme
            for case,type in validTup:
                ferme.etat[case].semer(type)
                partie.messagesPrincipaux.append([joueur.nom,'p49',cout['c'],'rc',',',
                                      cout['l'],'rl',cout['b'],'rb'])         
                personnage=partie.joueurQuiJoue().personnages.pop()
                partie.joueurQuiJoue().personnagesPlaces.append(personnage)                  
                carte.mettrePersonnage(personnage)
                partie.changerPointeurs(-1,None)                
            
        else:
            planCorrect=False
            msg="vous ne pouvez pas payer le cout {} ".format(cout)
            partie.changerPointeurs('inputtext',carte,alert=msg)        
            
    else:
        print(msg)

