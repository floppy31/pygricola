import pygricola.util as util


##################################################################################
#---------------------------------------Action dependant des joueurs--------------
##################################################################################

def possibiliteBetail(partie,carte):
    partie.phraseChoixPossibles="Choissisez une action:"
    partie.sujet=carte
    joueur=partie.joueurQuiJoue()

    possibilite=["1 mouton et 1 Pn","1 sanglier"]
    if(joueur.jePeuxJouer({'n':1})):
        possibilite.append("1 pn pour 1 boeuf")
        
    return possibilite

def betail(partie,choix,possibilites,carte):
    cout={}
    joueur=partie.joueurQuiJoue()
    if possibilites[choix]=="1 mouton et 1 Pn":
        cout={"n":-1,"m":-1}
    elif possibilites[choix]=="1 sanglier":
        cout={"s":-1}
    else:
        cout={"n":1,"v":-1}
    personnage=joueur.personnages.pop()
    joueur.personnagesPlaces.append(personnage)                  
    carte.mettrePersonnage(personnage)
    joueur.mettreAJourLesRessources(cout)

    return (-1,carte,False,"") #on ne peux plus en jouer                
        

def jePeuxNaitre(partie):
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme
    nbPions=len(joueur.personnages)+len(joueur.personnagesPlaces)
    nbMaison=ferme.compter('maison')
    if nbMaison>nbPions:
        return True
    else:
        return False

def jePeuxJouerSavoirFaireOuNaissance(partie):
    cout=coutSavoirFaire2(partie)
    joueur=partie.joueurQuiJoue()
    savoirFaireOk=joueur.jePeuxJouer(cout)
    tourOk=partie.plateau["tour"]>4
    return jePeuxNaitre(partie) or tourOk or savoirFaireOk
    
    
def possibiliteSavoiFaireOuNaissance(partie,carte):
    possibilites=["Savoir faire"]
    joueur=partie.joueurQuiJoue()
    tourOk=partie.plateau["tour"]>4
    if tourOk:
        if joueur.jePeuxNaitre(partie):
            possibilites.append('Naissance')
    partie.phraseChoixPossibles="Choissisez une action:"
    partie.sujet=carte
    return possibilites     

def savoiFaireOuNaissance(partie,choix,possibilites,carte):
    joueur=partie.joueurQuiJoue()
    if possibilites[choix]=="Savoir faire":
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
    


def possibiliteRoseauPnOuPierrePn(partie,carte):
    possibilites=["1 pierre et 1 pn","1 roseau et 1 pn"]   
    partie.phraseChoixPossibles="Choissisez une action:"
    partie.sujet=carte
    return possibilites     

def roseauPnOuPierrePn(partie,choix,possibilites,carte):
    cout={}
    joueur=partie.joueurQuiJoue()

    if possibilites[choix]=="1 pierre et 1 pn":
        cout={"p":-1,"n":-1}
    else:
        cout={"r":-1,"n":-1}
        
    personnage=joueur.personnages.pop()
    joueur.personnagesPlaces.append(personnage)                  
    carte.mettrePersonnage(personnage)
    joueur.mettreAJourLesRessources(cout)

    return (-1,carte,False,"") #on ne peux plus en jouer        
        

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

def possibilitesAmenagementMineur(partie,carte):
    possibilites=[]   
    joueur=partie.joueurQuiJoue()
    plateau=partie.plateau
    for c in  joueur.cartesEnMain:
        if joueur.jePeuxJouer(c.condition):
             if joueur.jePeuxJouer(c.cout):
                        possibilites.append(c)
                        
    partie.phraseChoixPossibles="Choissisez un aménagement mineur:"
    partie.sujet=carte
    return possibilites                       
    
def choixAmenagementMineur(partie,choix,possibilites,carte):
    carteJouee=possibilites[choix]
    carteJouee.jouer()
    joueur=partie.joueurQuiJoue()
    plateau=partie.plateau
    joueur.cartesDevantSoi.append(carteJouee)
    joueur.cartesEnMain.remove(carteJouee)
    typeCarte="aménagement mineur"           
    partie.messagesPrincipaux.append("{} {} {} {}".format(joueur.nom, "réalise l'",typeCarte,carteJouee.nom))
    
    if(carte.nom=="Premier joueur et aménagement mineur"):
        personnage=joueur.personnages.pop()
        joueur.personnagesPlaces.append(personnage)                  
        carte.mettrePersonnage(personnage)
        partie.premierJoueur=joueur.id
        encore=False    
        return (-1,carte,False,"") #on ne peux plus en jouer
    else:
        dfsdfsf
        

##################################################################################
#---------------------------------------MINEUR OU MAJEUR--------------------------
##################################################################################

def possibilitesAmenagementMineurOuMajeur(partie,carte):
    possibilites=[]   
    joueur=partie.joueurQuiJoue()
    plateau=partie.plateau
    for c in  joueur.cartesEnMain:
        if joueur.jePeuxJouer(c.condition):
             if joueur.jePeuxJouer(c.cout):
                        possibilites.append(c)
                        
    for m in  plateau['majeurs'].keys():
        if plateau['majeurs'][m].visible:
             if joueur.jePeuxJouer(plateau['majeurs'][m].cout):
                        possibilites.append(plateau['majeurs'][m])   
                                             
    partie.phraseChoixPossibles="Choissisez un aménagement mineur ou majeur:"
    partie.sujet=carte
    return possibilites                       
    
def choixAmenagementMineurOuMajeur(partie,choix,possibilites,carte):
    carteJouee=possibilites[choix]
    carteJouee.jouer()
    joueur=partie.joueurQuiJoue()
    plateau=partie.plateau
    joueur.cartesDevantSoi.append(carteJouee)
    if carteJouee in joueur.cartesEnMain:
    #on la pose
        joueur.cartesEnMain.remove(carteJouee)
        typeCarte="aménagement mineur"
    else:
        #on enleve le majeur et on gere les cartes dessous
        del plateau['majeurs'][carteJouee.nom]
        typeCarte="aménagement majeur"
        if not carteJouee.devoile is None:
            plateau['majeurs'][carteJouee.devoile].visible=True
            
    partie.messagesPrincipaux.append("{} {} {} {}".format(joueur.nom, "réalise l'",typeCarte,carteJouee.nom))
    personnage=joueur.personnages.pop()
    joueur.personnagesPlaces.append(personnage)                  
    carte.mettrePersonnage(personnage)
    encore=False    
    return (-1,carte,False,"") #on ne peux plus en jouer
##################################################################################
#---------------------------------------LABOURAGE---------------------------------
##################################################################################

def possibilitesLabourage(partie,carte):
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
    #par ex c2:p,c3:p,d4:e,a1:e
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
                if(type=='p'):
                    casesMaison.append(case)
                    cout=util.ajouter(cout,joueur.prixDeLaPiece())
                elif(type=='e'): 
                    casesEtables.append(case)
                    cout=util.ajouter(cout,{'b':2})
                else:
                    planCorrect=False
                    msg="type de case {} invalide... Soit soit 'e' soit 'p'".format(type)
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
            ferme.etat[c].type="E"
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


def possibiliteConstructionOuSpectacle(partie,carte):
    possibilites=["Spectacle"]
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
                        possibilites.append("construire en {}".format(voiz[direction]))
                    
    partie.phraseChoixPossibles="Que voulez vous faire? :"
    partie.sujet=carte
    return possibilites   

def constructionOuSpectacle(partie,choix,possibilites,carte):
    joueur=partie.joueurQuiJoue()

    if possibilites[choix]=="Spectacle":
        cout=carte.ressources.copy()
        carte.ressources=util.rVide()
        partie.messagesPrincipaux.append("{} va sur Spectacle".format(partie.joueurQuiJoue().nom))
    else:
        ferme=joueur.courDeFerme
        cout=joueur.prixDeLaPiece()   
        typeMaison=ferme.enQuoiEstLaMaison(False)
        case=possibilites[choix].split("construire en ")[-1]
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
 
def jePeuxFaireConstructionDePieceEtOuEtable(partie):
    return jePeuxContruireUneEtable(partie) or jePeuxContruireUnePiece(partie)    



##################################################################################
#---------------------------------------Semaille et Cuisson--------------------------
##################################################################################  

    
def jePeuxFaireSemailleEtOuCuisson(partie):    
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
    for c in joueur.cartesDevantSoi:
        if 'cuissonPain' in c.option.keys():
            fourOk=True
    return joueur.ressources['c']>0 and fourOk


def demanderPlanSemailleEtOuCuisson(partie,carte):
    partie.phraseChoixPossibles="Indiquez votre plan de semaille et cuisson de pain: "
    partie.sujet=carte
    return 'inputtext'
    

        
def planSemailleEtOuCuisson(partie,planStr,possibilites,carte):
    #par ex c2:c,c3:l,d4:c,cuisson:4
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme                                  
    planCorrect=True
    cout=util.rVide()
    validTup=[]
    cerealesACuire=0
    msg=""
    cout={'b':0,'c':0,'l':0} #on ne peut semer que ces 3 trucs
    for tup in planStr.split(','):
        try:
            case=tup.split(':')[0]
            type=tup.split(':')[1]
        except:
            planCorrect=False
            msg="format de plan invalide {}".format(planStr)
            return ('inputtext',carte,True,msg)
        
        if case == "cuisson":
            cout['c']+=1
            cerealesACuire+=1
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
                msg="la vous ne pouvez pas semer de ".format(util.short2Long(type))
                break
    #si pour le moment on est bon
    if (planCorrect):
        if(joueur.jePeuxJouer(cout)):
            #on est OK
            
            #on cuit les céréales
            cout['n']=-joueur.pouvoirCuisson(cerealesACuire)
            joueur.mettreAJourLesRessources(cout)

            partie.messagesPrincipaux.append("{} sème {} cereale(s), {} légume(s) et {} bois, et cuit {} céréale(s) pour {} pn".format(
                partie.joueurQuiJoue().nom,cout['c']-cerealesACuire,cout['l'],cout['b'],cerealesACuire,-cout['n']))                                                      
            personnage=partie.joueurQuiJoue().personnages.pop()
            partie.joueurQuiJoue().personnagesPlaces.append(personnage)                  
            carte.mettrePersonnage(personnage)
            return (-1,carte,False,msg)            
        else:
            planCorrect=False
            msg="vous ne pouvez pas payer le cout {} ".format(cout)
     
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

