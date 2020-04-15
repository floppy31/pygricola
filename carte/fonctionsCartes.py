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

def avoirXSavoirFaire(partie,carte):
    X=carte.option['conditionSavoirFaire']
    mesSavoirsfaire=partie.joueurQuiJoue().combienJaiJoueDe('s')
    print("avoirXSavoirFaire",mesSavoirsfaire,X)
    return mesSavoirsfaire>=X

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
                
    return (-2,carte,True,carte.uid) 

def enleverPossibilitesOptions(partie,choix,possibilites,carte):
    res=selfCarte['possibilitesOptions'].pop(choix)
    carte.owner.mettreAJourLesRessources(res)
    return (-1,carte,False,str(res))    

def gardeChampetre(partie,choix,possibilites,carte):
    caseALabourer=possibilites[choix]
    ferme=partie.joueurQuiJoue().courDeFerme
    ferme.etat[caseALabourer].type="champ"
    partie.messagesPrincipaux.append([partie.joueurQuiJoue().nom,"p22",caseALabourer])
    carte.hookStatus=-1    
    return (-2,carte,True,"s23") #on ne peux plus en labourer

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
    return (-2,carte,True,"s28") #on ne peux plus en labourer

def possibilitesFake(partie,selfCarte,Fake=False):
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
        if (not Fake):                    
            partie.phraseChoixPossibles=[carte.uid,'p18']
            partie.sujet=carte
    return possibilites          

def choixAchat(selfCarte):
    pass

def choixNaissanceOUPremier(selfCarte):
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
    partie.log.debug("{}".format(joueur.nom))
    return (-2,carte,False,mess)


def possibilitesOptions(selfCarte):
    return selfCarte['option']['possibilitesOptions']


def possibilitesGardeChampetre(partie,carte,Fake=False):
    
    possibilites=fct.possibilitesLabourage(partie,carte,Fake=True)
    if (not Fake):   
        partie.phraseChoixPossibles=['s23',':','p0']
        partie.sujet=carte          
    return possibilites

def possibilitesBonimenteur(partie,carte,Fake=False):
    
    possibilites=['p24','p25']
    if (not Fake):   
        partie.phraseChoixPossibles=['p23']
        partie.sujet=carte          
    return possibilites

def possibilitesSaisonier(partie,carte,Fake=False):
    possibilites=['c']
    if partie.plateau['tour']>5:
        print("SAISONIER LEGUME")
        possibilites.append('l')

    if (not Fake):   
        partie.phraseChoixPossibles=['s10',':','p0']
        partie.sujet=carte        
        
    return possibilites


def choixCout(partie,choix,possibilites,carte):
    print(choix,possibilites)
    choixOption=possibilites[choix]
    print('choixcoup',choixOption)
    cout=carte.option['choixCout'][choixOption]
    carte.owner.mettreAJourLesRessources(cout)
    #on ne peut plus jouer ce hook
    
    carte.hookStatus=-1    
    partie.choixPossibles=[]
    print("choixCout:",carte,carte.hookStatus)
    return (-2,carte,False,str(cout))


def prendre(partie,choix,possibilites,carte):
    print('prendre',choix,possibilites,carte)
    carte.owner.mettreAJourLesRessources(possibilites[choix])

def prendreSiTourEgal(selfCarte):
    dico=selfCarte['option']['prendreSiTourEgal']
                             
    if selfCarte.partie.plateau['tour'] in dico.keys() :
        selfCarte.owner.mettreAJourLesRessources(dico[partie.plateau['tour']])
    
    pass
    
    
def sixiemeSens(selfCarte):
    NOTIMPL

def final_access(selfCarte):
    NOTIMPL
def final_actrice(selfCarte):
    NOTIMPL
def final_administration(selfCarte):
    NOTIMPL



