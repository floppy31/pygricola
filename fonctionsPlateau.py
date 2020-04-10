import pygricola.util as util

####cette condition est particulière
####si la carte à une methode possibilités, on l'appelle avec Fake=True
####si la liste est vide, on ne peux pas faire l'action
def possibilitesNonVide(partie,carte):
    if not type(carte._possibilites)==dict:
        pos=carte._possibilites(partie,carte,Fake=True)
        print('posnonvide',pos)
        if len(pos)==0:
            partie.messagesDetail.append("{} : possibilites vides".format(carte.uid) )
        return len(pos)>0
    return True
    
    
##################################################################################
#---------------------------------------Action dependant des joueurs--------------
##################################################################################

def possibiliteBetail(partie,carte,Fake=False):
    joueur=partie.joueurQuiJoue()
    possibilite=["u0","u1"]
    if(joueur.jePeuxJouer({'n':1})):
        possibilite.append("u2")
    if not Fake:
        partie.phraseChoixPossibles="p0"
        partie.sujet=carte 
    return possibilite

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
    partie.messagesPrincipaux.append("{} ~p1~ {}".format(partie.joueurQuiJoue().nom,possibilites[choix]))

    return (-1,carte,False,"") #on ne peux plus en jouer  
              
def possibiliteRoseauPnOuPierrePn(partie,carte,Fake=False):
    possibilites=["u4","u5"]
    if (not Fake):   
        partie.phraseChoixPossibles="p0"
        partie.sujet=carte
    return possibilites     

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

    return (-1,carte,False,"") #on ne peux plus en jouer       
       
##################################################################################
#---------------------------------------Naissances--------------
##################################################################################
def jePeuxNaitre(partie):
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
    return jePeuxNaitre(partie) or tourOk or savoirFaireOk
    
    
def possibiliteSavoiFaireOuNaissance(partie,carte,Fake=False):
    possibilites=["p2"]
    joueur=partie.joueurQuiJoue()
    tourOk=partie.plateau["tour"]>4
    if tourOk:
        if joueur.jePeuxNaitre(partie):
            possibilites.append('p3')
    if (not Fake):
        partie.phraseChoixPossibles="p0"
        partie.sujet=carte
    return possibilites     

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
        return (-1,carte,False,"") 
    
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
    if partie.quiJoue in partie.joueurs.keys():
        if partie.joueurs[partie.quiJoue].combienJaiJoueDe('SavoirFaire')==0:
            return {}
    else:
        return {'n':1}

def coutSavoirFaire2(partie):
    if partie.joueurs[partie.quiJoue].combienJaiJoueDe('SavoirFaire')<2:
        return {'n':1}
    else:
        return {'n':2}

##################################################################################
#---------------------------------------MINEUR          --------------------------
##################################################################################

def possibilitesAmenagementMineur(partie,carte,Fake=False):
    possibilites=[]   
    joueur=partie.joueurQuiJoue()
    plateau=partie.plateau
    for c in  joueur.cartesEnMain:
        if joueur.jeRemplisLesConditions(c.condition):
             if joueur.jePeuxJouer(c.cout):
                        possibilites.append(c)
    possibilites.append('u3')
    if (not Fake):                    
        partie.phraseChoixPossibles="Choissisez un aménagement mineur:"
        partie.sujet=carte
    return possibilites                       
    
def choixAmenagementMineur(partie,choix,possibilites,carte):
    carteJouee=possibilites[choix]
    joueur=partie.joueurQuiJoue()
    plateau=partie.plateau
    if carteJouee=="u3":
        #on ne fait pas de mineur
        partie.messagesPrincipaux.append("{} {}".format(joueur.nom, "ne fais pas de mineur"))
    else:    
        carteJouee.jouer()
        joueur.cartesDevantSoi[carteJouee.uid]=carteJouee
        joueur.cartesEnMain.remove(carteJouee)
        partie.messagesPrincipaux.append("{} {} {} {}".format(joueur.nom, "~p3~",carteJouee.nom))
        
    if carte.uid=="a1":#premier joueur + mineur
        partie.premierJoueur=joueur.id
    elif carte.uid=="a14":#naissance + mineur
        pass
    else:
        if isinstance(carte,ActionSpeciale):
            joueur.mettreAJourLesRessources(carte.cout)
            carte.carteQuiMePorte.changerEtat(partie.quiJoue)
            return (-1,carte,False,"")     
    personnage=joueur.personnages.pop()
    joueur.personnagesPlaces.append(personnage)                  
    carte.mettrePersonnage(personnage)
    encore=False    
    return (-1,carte,False,"") #on ne peux plus en jouer

    ##################################################################################
#---------------------------------------Majeur          --------------------------
##################################################################################        
def possibilitesAmenagementMajeur(partie,carte,Fake=False):
    possibilites=[]   
    joueur=partie.joueurQuiJoue()
    plateau=partie.plateau
    for k,c in plateau["majeurs"].items():
        if joueur.jeRemplisLesConditions(c.condition):
             if joueur.jePeuxJouer(c.cout):
                        possibilites.append(c)
    if (not Fake):                    
        partie.phraseChoixPossibles="Choissisez un aménagement majeur:"
        partie.sujet=carte
    return possibilites                       
    
def choixAmenagementMajeur(partie,choix,possibilites,carte):
    carteJouee=possibilites[choix]
    carteJouee.jouer()
    joueur=partie.joueurQuiJoue()
    plateau=partie.plateau
    joueur.cartesDevantSoi[carteJouee.uid]=carteJouee
    del plateau["majeurs"][carteJouee.uid]
    partie.messagesPrincipaux.append("{} {} {} {}".format(joueur.nom, "réalise l'aménagement majeur",carteJouee.nom))
    

    if isinstance(carte,ActionSpeciale):
        joueur.mettreAJourLesRessources(carte.cout)
        carte.carteQuiMePorte.changerEtat(partie.quiJoue)
        
        return (-1,carte,False,"")
##################################################################################
#---------------------------------------MINEUR OU MAJEUR--------------------------
##################################################################################

def possibilitesAmenagementMineurOuMajeur(partie,carte,Fake=False):
    possibilites=[]   
    joueur=partie.joueurQuiJoue()
    plateau=partie.plateau
    for c in  joueur.cartesEnMain:
        if joueur.jeRemplisLesConditions(c.condition):
             if joueur.jePeuxJouer(c.cout):
                        possibilites.append(c)
                        
    for m in  plateau['majeurs'].keys():
        if plateau['majeurs'][m].visible:
             if joueur.jePeuxJouer(plateau['majeurs'][m].cout):
                        possibilites.append(plateau['majeurs'][m])   
    if (not Fake):                                         
        partie.phraseChoixPossibles="Choissisez un aménagement mineur ou majeur:"
        partie.sujet=carte
    return possibilites                       
    
def choixAmenagementMineurOuMajeur(partie,choix,possibilites,carte):
    carteJouee=possibilites[choix]
    carteJouee.jouer()
    joueur=partie.joueurQuiJoue()
    plateau=partie.plateau
    joueur.cartesDevantSoi[carteJouee.uid]=carteJouee
    if carteJouee in joueur.cartesEnMain:
    #on la pose
        joueur.cartesEnMain.remove(carteJouee)
        typeCarte="aménagement mineur"
    else:
        #on enleve le majeur et on gere les cartes dessous
        del plateau['majeurs'][carteJouee.uid]
        typeCarte="aménagement majeur"
        if not carteJouee.devoile is None:
            plateau['majeurs'][carteJouee.devoile].visible=True
    #on paye le cout de la carte
    joueur.mettreAJourLesRessources(carteJouee.cout)
    partie.messagesPrincipaux.append("{} {} {} {}".format(joueur.nom, "réalise l'",typeCarte,carteJouee.uid))
    personnage=joueur.personnages.pop()
    joueur.personnagesPlaces.append(personnage)                  
    carte.mettrePersonnage(personnage)
    encore=False    
    return (-1,carte,False,"") #on ne peux plus en jouer

##################################################################################
#---------------------------------------Actions spé-------------------------------
##################################################################################
def possibilitesAbattreDesArbres(partie,carte,Fake=False):
    possibilites=[]
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme
    if (not Fake):
        partie.phraseChoixPossibles="Quelle forêt voulez vous abattre? :"
        partie.sujet=carte    
    return ferme.tousLes('foret') 


def choixAbattreDesArbres(partie,choix,possibilites,carte):
    caseAbattre=possibilites[choix]
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme
    ferme.etat[caseAbattre].type="vide"
    joueur.mettreAJourLesRessources(util.ajouter(joueur.coutAbattre(),carte.cout))
    carte.carteQuiMePorte.changerEtat(partie.quiJoue)
    partie.messagesPrincipaux.append("{} {} {}".format(partie.joueurQuiJoue().nom, 'abats des arbres en ',caseAbattre))
    encore=False    
    return (-1,carte,False,"") 

def possibilitesCouperBruler(partie,carte,Fake=False):
    possibilites=[]
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme
    forets=ferme.tousLes('foret') 
    if (not Fake):
        partie.phraseChoixPossibles="Quelle forêt voulez vous couper et brûler? :"
        partie.sujet=carte      
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
                        
        return foretsAdjChamp
    else:
        return forets
        

def choixCouperBruler(partie,choix,possibilites,carte):
    caseCouper=possibilites[choix]
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme
    ferme.etat[caseCouper].type="champ"
    joueur.mettreAJourLesRessources(carte.cout)
    carte.carteQuiMePorte.changerEtat(partie.quiJoue)
        
    partie.messagesPrincipaux.append("{} {} {}".format(partie.joueurQuiJoue().nom, 'coupe et brûle en ',caseCouper))
    encore=False    
    return (-1,carte,False,"") 


def possibilitesCouperLaTourbe(partie,carte,Fake=False):
    possibilites=[]
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme
    tourbe=ferme.tousLes('tourbe') 
    if (not Fake):
        partie.phraseChoixPossibles="Quelle tourbe voulez vous couper? :"
        partie.sujet=carte      
    return tourbe
        

def choixCouperLaTourbe(partie,choix,possibilites,carte):
    caseCouper=possibilites[choix]
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme
    ferme.etat[caseCouper].type="vide"
    joueur.mettreAJourLesRessources(util.ajouter(joueur.coutTourbe(),carte.cout))
    carte.carteQuiMePorte.changerEtat(partie.quiJoue)
    
    partie.messagesPrincipaux.append("{} {} {}".format(partie.joueurQuiJoue().nom, 'coupe la tourbe en ',caseCouper))
    encore=False    
    return (-1,carte,False,"") 

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
    if (not Fake):
        partie.phraseChoixPossibles="Où voulez vous labourer? :"
        partie.sujet=carte
    return possibilites   

def labourage(partie,choix,possibilites,carte):
    caseALabourer=possibilites[choix]
    ferme=partie.joueurQuiJoue().courDeFerme
    ferme.etat[caseALabourer].type="champ"
    partie.messagesPrincipaux.append("{} {} {}".format(partie.joueurQuiJoue().nom, 'Laboure 1 champ en ',caseALabourer))
    personnage=partie.joueurQuiJoue().personnages.pop()
    partie.joueurQuiJoue().personnagesPlaces.append(personnage)                  
    carte.mettrePersonnage(personnage)
    encore=False    
    return (-1,carte,False,"") #on ne peux plus en labourer

##################################################################################
#---------------------------------------Piece et Etables--------------------------
##################################################################################

def demanderPlanConstructionDePieceEtOuEtable(partie,carte):
    partie.phraseChoixPossibles="Indiquez votre plan de construction de pièce ou etable: "
    partie.sujet=carte
    return 'inputtext'
    

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
            return ('inputtext',carte,True,msg)
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
        return (-1,carte,False,msg)
    else:
        #on est pas bon
        partie.phraseChoixPossibles="Indiquez votre plan de construction de pièce ou etable: "

        return ('inputtext',carte,True,msg)


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
    if (not Fake):
        partie.phraseChoixPossibles="Que voulez vous faire? :"
        partie.sujet=carte
    return possibilites   

def constructionOuSpectacle(partie,choix,possibilites,carte):
    joueur=partie.joueurQuiJoue()

    if possibilites[choix]=="Spectacle":
        cout=carte.cout.copy()
        carte._cout=util.rVide() #vidage de la carte???
        TTTT
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
    return (-1,carte,False,"")


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


def demanderPlanSemailleEtOuCuisson(partie,carte):
    partie.phraseChoixPossibles="Indiquez votre plan de semaille et cuisson de pain: "
    partie.sujet=carte
    return 'inputtext'
    

        
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
            return ('inputtext',carte,True,msg)
        
        if case == "c":
            if cuissonPassee:
                planCorrect=False
                msg="plan invalide, il ne peux y avoir qu'une instruction de cuisson"
                return ('inputtext',carte,True,msg)                
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
                    return ('inputtext',carte,True,msg)
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
        print ("sem",cout)
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
            return (-1,carte,False,msg)            
        else:
            planCorrect=False
            msg="vous ne pouvez pas payer le cout {} ".format(cout)
            return ('inputtext',carte,True,msg)
     
    else:
        #on est pas bon
        partie.phraseChoixPossibles="Indiquez votre plan de semaille et cuisson de pain"
        return ('inputtext',carte,True,msg)
    
    


##################################################################################
#---------------------------------------Archives--------------------------
##################################################################################              
                

# 
# def possibilitesConstructionDePiece(partie,carte):
#     possibilites=["je ne veux pas construire de pièce"]
#     joueur=partie.joueurQuiJoue()
#     ferme=joueur.courDeFerme   
#     typeMaison=ferme.enQuoiEstLaMaison()
#     cout=joueur.prixDeLaPiece()
#     #normalement ce if est toujours vrai
#     if joueur.jePeuxJouer(cout):
#         for c in ferme.tousLes('maison'):
#             voiz=ferme.voisin(c)
#             for direction in voiz.keys():
#                 if voiz[direction]: #si not None
#                     if ferme.etat[voiz[direction]].type=='vide':
#                         possibilites.append(voiz[direction])   
#                             
#     partie.phraseChoixPossibles="Où voulez vous construire un pièce en {}? :".format(ferme.enQuoiEstLaMaison(False))
#     partie.sujet=carte
#     return possibilites   
# 
# def possibilitesConstructionEtable(partie,carte):
#     possibilites=["pas d'étable","1 étable","2 étables","3 étables","4 étables"]
#     joueur=partie.joueurQuiJoue()
#     ferme=joueur.courDeFerme   
#     #je peux construire combien d'étables?
#     #il me semble qu'il n'y a aucune reduction ici pour le cout des etables
#     nbois=  joueur.ressources['b']
#     casesVides=ferme.compter("vide")
#     #min entre nb etable qu'on peut construire, etables encore dispo, et place dispo
#     nbEtablesPossibles = int(min(nbois/2,ferme.compterEtablesDispo(),casesVides))
#     possibilites=possibilites[0:nbEtablesPossibles+1]
#     partie.phraseChoixPossibles="Combien d'étables voulez vous construire?"
#     partie.sujet=carte   
#     partie.choixPossibles=possibilites
#     return partie.choixPossibles
#     
# def possibilitesEmplacementEtable(partie,carte):
#     pass
#     
# def constructionEtable(partie,choix,possibilites,carte):
#     nbEtables=choix
#     for e in range(nbEtables):
#         possibles=ferme.tousLes('vide')
#         choix=util.printPossibilities(partie,"Ou placer cette etable? :",possibles,False)
#         ferme.etat[possibles[choix]].type="etable"
#         joueur.mettreAJourLesRessources({'b':2})     
#         
#         
#         
# def constructionDePiece(partie,choix,possibilites,carte):
#     joueur=partie.joueurQuiJoue()
#     ferme=joueur.courDeFerme   
#     typeMaison=ferme.enQuoiEstLaMaison()
#     
#     
#     if possibilites[choix]=='oui' or possibilites[choix]=='non':
#         #dans ce cas la question était "voulez vous encore construire une pièce
#         if possibilites[choix]=='oui':
#             #on réappelle
#             pos=possibilitesConstructionDePiece(partie,carte)
#             partie.phraseChoixPossibles="Où voulez vous construire un pièce en {}? :".format(ferme.enQuoiEstLaMaison(False))
#             partie.sujet=carte
#             partie.choixPossibles=pos
#             return (pos,carte,True)
#         else:
#             #c'est non
#             #dans ce cas on change la methode de la carte
#             carte._possibilites=possibilitesConstructionEtable
#             carte._effet=constructionEtable
#             pos=carte._possibilites(partie,carte)
#             return (pos,carte,True)
#             #on passe à la suite
#     elif possibilites[choix]=="je ne veux pas construire de pièce":
#         #dans ce cas on change la methode de la carte
#         carte._possibilites=possibilitesConstructionEtable
#         carte._effet=constructionEtable   
#         pos=carte._possibilites(partie,carte)   
#         return (pos,carte,True)
#     else:
#         #dans ce cas la question était 'ou voulez vous construire et donc possibilites[choix]
#         #est une case        
#         cout=joueur.prixDeLaPiece()
#         joueur.mettreAJourLesRessources(cout)
#         ferme.etat[possibilites[choix]].type=ferme.enQuoiEstLaMaison(False)
#         #on peut encore construire une pièce?
#         if jePeuxContruireUnePiece(partie):
#             #si oui je pose la question
#             partie.phraseChoixPossibles="Voulez vous encore construire une pièce?"
#             partie.sujet=carte   
#             partie.choixPossibles=["oui","non"]
#             return (partie.choixPossibles,carte,True)
#         else:
#             #dans ce cas on change la methode de la carte
#             carte._possibilites=possibilitesConstructionEtable
#             carte._effet=constructionEtable   
#             pos=carte._possibilites(partie,carte)   
#             return (pos,carte,True)            
    #quand on est là on a fini de construire des pièces
    
#     pos=possibilitesConstructionEtable(partie,carte)
#     return (pos,carte,True)
#     #combien j'ai d'etables
#     if(ferme.compterEtablesDispo()>0):
#         #je peux construire combien d'étables?
#         #il me semble qu'il n'y a aucune reduction ici pour le cout des etables
#         nbois=  joueur.ressources['b']
#         casesVides=ferme.compter("vide")
#         #min entre nb etable qu'on peut construire, etables encore dispo, et place dispo
#         nbEtablesPossibles = int(min(nbois/2,ferme.compterEtablesDispo(),casesVides))
#         possibles=["pas d'étable","1 étable","2 étables","3 étables","4 étables"]
#         possibles=possibles[0:nbEtablesPossibles+1]
#         choix=util.printPossibilities(partie,"Combien d'étables :",possibles,False)
#         nbEtables=choix
#         for e in range(nbEtables):
#             possibles=ferme.tousLes('vide')
#             choix=util.printPossibilities(partie,"Ou placer cette etable? :",possibles,False)
#             ferme.etat[possibles[choix]].type="etable"
#             joueur.mettreAJourLesRessources({'b':2})        
#     #pour constructions multiples
#     jeVeuxConstruire=True
#     while jeVeuxConstruire:
#         cout=joueur.prixDeLaPiece()
#         if joueur.jePeuxJouer(cout):
#             #ou placer la piece
#             emplacementsPossibles=[]
#             for c in ferme.tousLes('maison'):
#                 voiz=ferme.voisin(c)
#                 for direction in voiz.keys():
#                     if voiz[direction]: #si not None
#                         if ferme.etat[voiz[direction]].type=='vide':
#                             emplacementsPossibles.append(voiz[direction])   
#             choix=util.printPossibilities(partie,"Où voulez vous construire? :",emplacementsPossibles,False)
#             if choix == -1:
#                 return -1
#             else:
#                 
#                 joueur.mettreAJourLesRessources(cout)
#                 ferme.etat[emplacementsPossibles[choix]].type=ferme.enQuoiEstLaMaison(False)
#                 
#                 #on recalcule à cause de certaines cartes
#                 cout=joueur.prixDeLaPiece()
#                 if joueur.jePeuxJouer(cout):
#                     emplacementsPossibles=[]
#                     for c in ferme.tousLes('maison'):
#                         voiz=ferme.voisin(c)
#                         for direction in voiz.keys():
#                             if voiz[direction]: #si not None
#                                 if ferme.etat[voiz[direction]].type=='vide':
#                                     emplacementsPossibles.append(voiz[direction])  
#                     if  len(emplacementsPossibles)>0:
#                         #je peux encore construire
#                         ouinon=['oui','non']
#                         choix=util.printPossibilities(partie,"Construire une autre pièce? :",ouinon,False)
#                         if ouinon[choix]=='non':
#                             jeVeuxConstruire=False 
#                     else:
#                         jeVeuxConstruire=False 
#                 else:
#                     jeVeuxConstruire=False        
#     
#     
#     #combien j'ai d'etables
#     if(ferme.compterEtablesDispo()>0):
#         #je peux construire combien d'étables?
#         #il me semble qu'il n'y a aucune reduction ici pour le cout des etables
#         nbois=  joueur.ressources['b']
#         casesVides=ferme.compter("vide")
#         #min entre nb etable qu'on peut construire, etables encore dispo, et place dispo
#         nbEtablesPossibles = int(min(nbois/2,ferme.compterEtablesDispo(),casesVides))
#         possibles=["pas d'étable","1 étable","2 étables","3 étables","4 étables"]
#         possibles=possibles[0:nbEtablesPossibles+1]
#         choix=util.printPossibilities(partie,"Combien d'étables :",possibles,False)
#         nbEtables=choix
#         for e in range(nbEtables):
#             possibles=ferme.tousLes('vide')
#             choix=util.printPossibilities(partie,"Ou placer cette etable? :",possibles,False)
#             ferme.etat[possibles[choix]].type="etable"
#             joueur.mettreAJourLesRessources({'b':2})

