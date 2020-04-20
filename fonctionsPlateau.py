import pygricola.util as util
####cette condition est particulière
####si la carte à une methode possibilités, on l'appelle avec Fake=True
####si la liste est vide, on ne peux pas faire l'action
####par ex ni on ne peux ni jouer de mineur ni de majeur, on ne peux pas faire la case
def possibilitesNonVide(partie,carte):
    if not type(carte._possibilites)==dict:
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

def jePeuxJouerSavoirFaireOuNaissance(partie,carte):
    cout=coutSavoirFaire2(partie)
    joueur=partie.joueurQuiJoue()
    savoirFaireOk=joueur.jePeuxJouer(cout)
    tourOk=partie.plateau["tour"]>4
    return jePeuxNaitre(partie,carte) or tourOk or savoirFaireOk
    
    
def possibiliteSavoiFaireOuNaissance(partie,carte,Fake=False):
    possibilites=["p2"]
    joueur=partie.joueurQuiJoue()
    tourOk=partie.plateau["tour"]>4
    if tourOk:
        if joueur.jePeuxNaitre(partie):
            possibilites.append('p3')
    
    partie.changerPointeurs(possibilites ,carte,phrase='p0',Fake=Fake) 

def savoiFaireOuNaissance(partie,choix,possibilites,carte):
    joueur=partie.joueurQuiJoue()
    if possibilites[choix]=="p2":
        cout=coutSavoirFaire2(partie)
        dgsdg
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
def coutSavoirFaire1(partie):
    joueur=partie.joueurQuiJoue()
    if joueur.combienJaiJoueDe('s')==0:
        return {}
    else:
        return {'n':1}

def coutSavoirFaire2(partie):
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

      
    
def choixSavoirFaire(partie,choix,possibilites,carte):
    savoirFaireChoisiUid=possibilites[choix]
    joueur=partie.joueurQuiJoue()
    for c in joueur.cartesEnMain:
        if c.uid==savoirFaireChoisiUid:
            savoirFaireChoisi=c
            break
    #il faut le faire avant car le cout depends du nombre de savoir faire joues
    joueur.mettreAJourLesRessources(util.ajouter(savoirFaireChoisi.cout,carte.cout))
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
        if carteJouee.uid=="m9" and jePeuxNaitre(partie, carte):
            self.partie.ajouterHook(carteJouee,carteJouee.option["hook_possibilites"],carteJouee.owner.djangoUid,'instant')
        else:
            
            partie.log.info([joueur.nom,"p30"])
            partie.premierJoueur=joueur.id

    
    partie.log.info([joueur.nom,"p3",carteJouee])
    partie.changerPointeurs(-1 ,None)   

##################################################################################
#---------------------------------------Majeur          --------------------------
##################################################################################        
def possibilitesAmenagementMajeur(partie,carte,Fake=False):
    possibilites=[]   
    joueur=partie.joueurQuiJoue()
    plateau=partie.plateau
    for k,c in plateau["majeurs"].items():
        if c.visible:
            if joueur.jeRemplisLesConditions(c.conditionAchat):
                if joueur.jePeuxJouer(util.ajouter(c.cout,carte.cout)):
                    possibilites.append(c)
    partie.changerPointeurs(possibilites ,carte,'p34',joueur,Fake=Fake)       
    
def choixAmenagementMajeur(partie,choix,possibilites,carte):
    carteJouee=possibilites[choix]
    joueur=partie.joueurQuiJoue()
    plateau=partie.plateau
    joueur.poserCarteDevantSoi(carteJouee,True)
    partie.messagesPrincipaux.append([joueur.nom,"p14",carteJouee.uid])
    partie.log.info([joueur.nom,"p14",carteJouee.uid])
    #si c'est une action speciale
    if hasattr( carte,"carteQuiMePorte"):
        joueur.mettreAJourLesRessources(util.ajouter(carte.cout,carteJouee.cout))
        carte.carteQuiMePorte.changerEtat(partie.quiJoue)
        partie.changerPointeurs(-1 ,carte)  
    else:
        
        TODO
        carteJouee.jouer()
        partie.changerPointeurs(-1 ,carte)  
##################################################################################
#---------------------------------------MINEUR OU MAJEUR--------------------------
##################################################################################

def possibilitesAmenagementMineurOuMajeur(partie,carte,Fake=False):
    possibilites=[]   
    joueur=partie.joueurQuiJoue()
    plateau=partie.plateau
    for c in  joueur.cartesEnMain:
        if c.uid[0]=="m":
            #ici c'est condition achat... on ne veut pas appeler poss non vide de la carte à acheter
            if joueur.jeRemplisLesConditions(c.conditionAchat):
                #cout de la carte + de l'action (pour foire du travail)
                if joueur.jePeuxJouer(util.ajouter(carte.cout,c.cout)):
                    possibilites.append(c)
                else:
                    partie.log.debug(["p10",c.uid])
                    partie.messagesDetail.append(["p10",c.uid])
            else:
                partie.messagesDetail.append(["p9",c.uid])
                partie.log.debug(["p19",c.uid])
                
                        
    for m in  plateau['majeurs'].keys():
        if plateau['majeurs'][m].visible:
             if joueur.jePeuxJouer(plateau['majeurs'][m].cout):
                        possibilites.append(plateau['majeurs'][m])   
    partie.changerPointeurs(possibilites ,carte,'p35',joueur,Fake=Fake)       
    
def choixAmenagementMineurOuMajeur(partie,choix,possibilites,carte):
    carteJouee=possibilites[choix]
    carteJouee.jouer()
    TODO
    joueur=partie.joueurQuiJoue()
    plateau=partie.plateau
    Majeur=not carteJouee in joueur.cartesEnMain
    joueur.poserCarteDevantSoi(carteJouee,Majeur)
    #on paye le cout de la carte
    joueur.mettreAJourLesRessources(carteJouee.cout)
    partie.log.info("{} {} {}".format(joueur.nom, "réalise ",carteJouee.uid))
    personnage=joueur.personnages.pop()
    joueur.personnagesPlaces.append(personnage)                  
    carte.mettrePersonnage(personnage)
    encore=False    
    partie.changerPointeurs(-1,None)

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
    partie.messagesPrincipaux.append("{} {} {}".format(partie.joueurQuiJoue().nom, 'abats des arbres en ',caseAbattre))
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
        
    partie.messagesPrincipaux.append("{} {} {}".format(partie.joueurQuiJoue().nom, 'coupe et brûle en ',caseCouper))
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
    
    partie.messagesPrincipaux.append("{} {} {}".format(partie.joueurQuiJoue().nom, 'coupe la tourbe en ',caseCouper))
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
    partie.messagesPrincipaux.append("{} {} {}".format(partie.joueurQuiJoue().nom, 'Laboure 1 champ en ',caseALabourer))
    personnage=partie.joueurQuiJoue().personnages.pop()
    partie.joueurQuiJoue().personnagesPlaces.append(personnage)                  
    carte.mettrePersonnage(personnage)
    partie.changerPointeurs(-1,None)
##################################################################################
#---------------------------------------Piece et Etables--------------------------
##################################################################################

def demanderPlanConstructionDePieceEtOuEtable(partie,carte,Fake=False):
    partie.changerPointeurs('inputtext' ,carte,'p38',Fake)    

    

def planConstructionDePieceEtOuEtable(partie,planStr,possibilites,carte):
    #par ex C2:p,C3:p,C4:e,A1:e
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
            if (ferme.compterEtablesDispo()>=len(casesEtables)):
                pass
            else:
                planCorrect=False
                msg="vous n'avez pas assez d'étables, il en reste  {} ".format(ferme.compterEtablesDispo())                
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
        
    #quand on est la on est bon    
    if(planCorrect):
        for c in casesMaisonOk:
            ferme.etat[c].type=ferme.enQuoiEstLaMaison(False)
        for c in casesEtables:
            ferme.etat[c].type="etable"
        joueur.mettreAJourLesRessources(cout)
        partie.messagesPrincipaux.append("{} construit {} piece(s) et {} etable(s)".format(partie.joueurQuiJoue().nom,
                                                            len(casesMaisonOk),len(casesEtables)))
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
    partie.changerPointeurs(possibilites,carte,phrase="p0",Fake=Fake)

def constructionOuSpectacle(partie,choix,possibilites,carte):
    joueur=partie.joueurQuiJoue()

    if possibilites[choix]=="Spectacle":
        cout=carte.cout.copy()
        carte.vider() #vidage de la carte???
        TTTT # appeller aussi les hook sur spectacle
        partie.messagesPrincipaux.append("{} va sur Spectacle".format(partie.joueurQuiJoue().nom))
    else:
        ferme=joueur.courDeFerme
        cout=joueur.prixDeLaPiece()   
        typeMaison=ferme.enQuoiEstLaMaison(False)
        case=possibilites[choix][1]
        ferme.etat[case].type=typeMaison  
        partie.messagesPrincipaux.append("{} construit 1 pièce en {}".format(partie.joueurQuiJoue().nom,case))

    joueur.mettreAJourLesRessources(cout)    
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
    etablesOk=ferme.compterEtablesDispo()>0
     
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


def demanderPlanSemailleEtOuCuisson(partie,carte,Fake=False):
    partie.changerPointeurs('inputtext',carte,phrase='p33',Fake=Fake) 
    

        
def planSemailleEtOuCuisson(partie,planStr,possibilites,carte):
    #par ex C2:c,C3:l,c:4
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
                msg="la vous ne pouvez pas semer de {}".format(util.short2Long[type])
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
            partie.messagesPrincipaux.append("{} sème {} cereale(s), {} légume(s) et {} bois, et cuit {} céréale(s) pour {} pn".format(
                partie.joueurQuiJoue().nom,cout['c']-cerealesACuire,cout['l'],cout['b'],cerealesACuire,-cout['n']))                                                      
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
        partie.phraseChoixPossibles="Indiquez votre plan de semaille et cuisson de pain"
        partie.changerPointeurs('inputtext',carte,alert=msg)
    
    


