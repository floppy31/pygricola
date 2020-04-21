import pygricola.util as util
import pygricola.fonctionsPlateau as fct

def acrobate(selfCarte):
    NOTIMPL

def agrarien(selfCarte):
    NOTIMPL  

def aideMoissonneur(selfCarte):
    NOTIMPL  
    
    
def aiguilleRoche(selfCarte):
    NOTIMPL

def avoirMoinsDeXCartesEnMain(selfCarte):
    X=selfCarte['option']['conditionMoinsDeXCartesEnMain']
    mesCartes=len(selfCarte.parte.joueurQuiJoue().cartesEnMain)
    print("avoirMoinsDeXCartesEnMain",mesCartes,X)
    return mesCartes<=X
def avoirXPieces(partie,carte):
    X=carte.option['conditionPiece']
    nbre=partie.joueurQuiJoue().courDeFerme.compter("maison")
    print("avoirXPieces",nbre,X)
    return nbre>=X

def avoirXSavoirFaire(partie,carte):
    X=carte.option['conditionSavoirFaire']
    mesSavoirsfaire=partie.joueurQuiJoue().combienJaiJoueDe('s')
    print("avoirXSavoirFaire",mesSavoirsfaire,X)
    return mesSavoirsfaire>=X

def avoirXMajeurs(partie,carte):
    X=carte.option['conditionMajeurs']
    mesMajeurs=partie.joueurQuiJoue().combienJaiJoueDe('M')
    print("avoirXMajeurs",mesMajeurs,X)
    return mesMajeurs>=X

def boisSurLaBerge(partie,choix,possibilites,carte):
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme
    nombre=ferme.compter("foret")
    if nombre>0:
        if nombre>2:
            nombre=3
        joueur.mettreAJourLesRessources({"b":-nombre})    

def conditionEpicier(partie,carte):
    
    joueur=partie.joueurQuiJoue()
    coutOk=joueur.jePeuxJouer({'n':1})
    pileOk=len(carte.option['pile'])>0
    return pileOk and coutOk


def depiler(partie,choix,possibilites,carte):
    #soit c'est une liste et on regarde dans pile
    #on prends les ressources dans un certain ordre
    partie.log.debug(carte.uid)
    if 'pile' in carte.option.keys():
        if len(carte.option['pile'])>0:
            cout=carte.option['pile'].pop()
            print("depiler, il reste:",carte.option['pile'])
            carte.owner.mettreAJourLesRessources(cout)

    #soit on prend un certain type chaque tour
    elif 'pileTour' in carte.option.keys():
        if len(carte.option['pileTour'].keys())>0:
            if partie.plateau['tour'] in carte.option['pileTour'].keys():
                cout=carte.option['pileTour'][partie.plateau['tour']]
                del carte.option['pileTour'][partie.plateau['tour']]
                print("depiler, il reste:",len(carte.option['pileTour'].keys()),'tours')
                carte.owner.mettreAJourLesRessources(cout)
     
    partie.changerPointeurs(-1,None)            

def enleverPossibilitesOptions(partie,choix,possibilites,carte):
    res=selfCarte['possibilitesOptions'].pop(choix)
    carte.owner.mettreAJourLesRessources(res)
    partie.changerPointeurs(-1,None)   
#     return (-1,carte,False,str(res))    


def blocTourbe(partie,choix,possibilites,carte):
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme
    nombre=ferme.compter("tourbe")
    if nombre>0:
        joueur.mettreAJourLesRessources({"f":-nombre})

def gardeChampetre(partie,choix,possibilites,carte):
    caseALabourer=possibilites[choix]
    ferme=partie.joueurQuiJoue().courDeFerme
    ferme.etat[caseALabourer].type="champ"
    partie.messagesPrincipaux.append([partie.joueurQuiJoue().nom,"p22",caseALabourer])
    carte.hookStatus=-1    
    partie.changerPointeurs(-1,None)   

def bonimenteur(partie,choix,possibilites,carte):
    
    if possibilites[choix]=='p24':
        joueur=partie.joueurQuiJoue()
        carte.owner.mettreAJourLesRessources({"c":-1,"l":-1})
        for id,j in partie.joueurs.items():
            if id==joueur.id:
                pass
            else:
                j.mettreAJourLesRessources({"c":-1})
        partie.messagesPrincipaux.append([partie.joueurQuiJoue().nom,"p21","s28"])
    else:
        partie.messagesPrincipaux.append([partie.joueurQuiJoue().nom,"p26","s28"])
    carte.hookStatus=-1    
    partie.changerPointeurs(-1,None)   

def possibilitesFake(partie,selfCarte):
    print("possibilitesFake")
    #genre pour l'epicier
    return ['fake']        

def possibilitesRessourceSurAction(partie,carte,Fake=False):
    #on liste les actions visibles
    possibilites=[]
    #si j'en ai encore
    if len(carte.option['ressourceSurAction'])>0:
        for i in range(1,31):
            if carte.partie.plateau['cases'][i].visible:
                possibilites.append(carte.partie.plateau['cases'][i].uid)
    partie.changerPointeurs(possibilites,carte,[carte.uid,'p18'],carte.owner,Fake=Fake)               
#             partie.phraseChoixPossibles=[carte.uid,'p18']
#             partie.sujet=carte

def choixAchat(selfCarte):
    pass

def conditionAnnexe(partie,carte):
    poss=possibilitesAnnexe(partie,carte)
    if len(poss)==0:
        return False   
    else:
        typeMaison=partie.joueurQuiJoue().courDeFerme.enQuoiEstLaMaison()
        typeCarte=carte.option['annexe']
        return typeCarte==typeMaison


def possibilitesAnnexe(partie,carte):
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme
    possibilites=[]
    for c in ferme.tousLes('maison'):
        voiz=ferme.voisin(c)
        for direction in voiz.keys():
            if voiz[direction]: #si not None
                if ferme.etat[voiz[direction]].type=='vide':
                    possibilites.append(voiz[direction])
    #on ne change pas le pointeur ici
    return possibilites                


def coutArbrePourCitoyens(partie):
    joueur=partie.joueurQuiJoue()
    if joueur.aiJeJoue('M18') or joueur.aiJeJoue('m16'):
        return {}
    else:
        return {'b':3} 

def finalArbrePourCitoyens(partie):
    NOTIMPL


def ajoutRessourceChampsEnsemmances(partie,choix,possibilites,carte):
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme
    
    TODO    

def constructionAnnexe(partie,choix,possibilites,carte):
    joueur=partie.joueurQuiJoue()
    ferme=joueur.courDeFerme
    typeMaison=ferme.enQuoiEstLaMaison(False)
    case=possibilites[choix]
    ferme.etat[case].type=typeMaison  
    partie.messagesPrincipaux.append("{} construit 1 pièce avec l'annexe en {}".format(partie.joueurQuiJoue().nom,case))
    partie.log.info("{} construit 1 pièce avec l'annexe en {}".format(partie.joueurQuiJoue().nom,case))


def possibilitesPremierOuNaissance(partie,carte):
    possibilites=['premier']
    if carte.owner.jePeuxNaitre(partie,carte):
        possibilites.append('naissance')
    return possibilites
        

def choixPremierOuNaissance(partie,choix,possibilites,carte):
    NOTIMPL

def choixRessourceSurAction(partie,choix,possibilites,carte):
    uidChoisi=possibilites[choix]
    joueur=carte.owner
    plateau=partie.plateau
    mess=""
    optionRessource=carte.option['ressourceSurAction'].pop()
    for i in range(1,31):
        if partie.plateau['cases'][i].uid==uidChoisi:
            mess=["p19",optionRessource,"p20",uidChoisi]
            partie.log.debug(mess)
            partie.plateau['cases'][i].coutBonus=util.ajouter(
                partie.plateau['cases'][i].coutBonus,optionRessource)
    carte.hookstatus=-1
    partie.changerPointeurs(-1,None)   
    

def possibilitesOptions(selfCarte):
    return selfCarte['option']['possibilitesOptions']


def possibilitesGardeChampetre(partie,carte,Fake=False):
    fct.possibilitesLabourage(partie,carte,Fake)

def possibilitesBonimenteur(partie,carte,Fake=False):
    
    possibilites=['p24','p25']
    partie.changerPointeurs(possibilites,carte,'p23',carte.owner,Fake=Fake)               


def possibilitesSaisonier(partie,carte,Fake=False):
    possibilites=['c']
    if partie.plateau['tour']>5:
        possibilites.append('l')
    partie.changerPointeurs(possibilites,carte,['s10',':','p0'],carte.owner,Fake=Fake)               
    


def choixCout(partie,choix,possibilites,carte):
    choixOption=possibilites[choix]
    cout=carte.option['choixCout'][choixOption]
    carte.owner.mettreAJourLesRessources(cout)
    #on ne peut plus jouer ce hook
    
    carte.hookStatus=-1    
    if len(possibilites)==1:
        #on a fait un choix automatique
        partie.log.debug('choix automatique sur {}'.format(carte.uid))
    else:
        partie.log.debug('choix manuel sur {}'.format(carte.uid))
    partie.changerPointeurs(-1,None)

def prendre(partie,choix,possibilites,carte):
    print('prendre',choix,possibilites,carte)
    carte.owner.mettreAJourLesRessources(possibilites[choix])

def prendreSiTourEgal(selfCarte):
    dico=selfCarte['option']['prendreSiTourEgal']
                             
    if selfCarte.partie.plateau['tour'] in dico.keys() :
        selfCarte.owner.mettreAJourLesRessources(dico[partie.plateau['tour']])
    
    pass
    
def volerRessource(partie,choix,possibilites,carte):
    cible=partie.joueurQuiJoue()
    voleur=carte.owner
    
    cout=carte.option['vol']
    for res,nombre in cout.items():
        cible.ressources[res]-=nombre
        voleur.ressources[res]+=nombre
    partie.log.info("{} vole des ressources à {} avec {}".format(voleur,cible,carte.uid))
        
    
def sixiemeSens(selfCarte):
    NOTIMPL

def final_access(selfCarte):
    NOTIMPL
def final_actrice(selfCarte):
    NOTIMPL
def final_administration(selfCarte):
    NOTIMPL



