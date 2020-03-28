import variablesGlobales
import util
from collections import Counter, OrderedDict
from pandas.core.common import flatten
from collections import Counter
import numpy as np

from pygricola.ressources import long2Short
import util



parseList=[]
for l in ['a','b','c']:
    for i in range(1,6):
        parseList.append("{}{}".format(l,i))
        
        
class CourDeFerme(object):

    def __init__(self):
        self.etat=OrderedDict()
        for case in parseList:
            self.etat[case]=Tuile('vide')
        self.etat["c2"]=Tuile('maisonBois')
        self.etat["b1"]=Tuile('maisonBois')
        self.etat["c1"]=Tuile('maisonBois')
        self.paturages = Paturage()
        self.clotures = Clotures()
        # ~ self.etat["c4"]=Tuile('champ') #DEBUG
        self.annexe=[]
        
    def initTuiles(self,positionTourbes,positionForets):   
        for t in positionTourbes:
            self.etat[t]=Tuile('tourbe')
        for f in positionForets:
            self.etat[f]=Tuile('foret')               
    
    def __str__(self):
           return self.prettyPrint()
       
    def enQuoiEstLaMaison(self,court=True):
        if court:
            return long2Short[self.etat["b1"].type.split('maison')[1].lower()]
        else:
            return self.etat["b1"].type
    
    def compterEtablesDispo(self):
        #TODO
        return 4
    
    def compter(self,type):
        compteur=0
        for k in self.etat.keys():
            if type in str(self.etat[k]) :
                compteur+=1
        return compteur
    
    def tousLes(self,type):
        #rend la liste de toutes les cases type
        l=[]
        for k in self.etat.keys():
            #comme ça on peut appeler tousLes('maison')
            if type in str(self.etat[k]):
                l.append(k)
        return l
    
    def voisin(self,coord):
        #disco des voisins nord,sud est,ouest
        voisins={
            'n':None,
            'e':None,
            's':None,
            'w':None
            }
        ligne=coord[0]
        colonne=int(coord[1])
        
        if ligne=="a":
            voisins["s"]="a"+str(colonne)
        elif ligne=="b":
            voisins["n"]="a"+str(colonne)
            voisins["s"]="c"+str(colonne)
        elif ligne=="c":
            voisins["n"]="b"+str(colonne)
        if colonne==1:
            voisins["e"]=ligne+str(2)
        elif colonne==5:
            voisins["w"]=ligne+str(4)
        else:
            voisins["e"]=ligne+str(colonne+1)
            voisins["w"]=ligne+str(colonne-1)                
        return voisins

    def prettyPrint(self):
        str="""
        ---------------
        |{}||{}||{}||{}||{}|
        ---------------
        |{}||{}||{}||{}||{}|
        ---------------
        |{}||{}||{}||{}||{}|
        """
        d=tuple(self.etat[case].short for case in parseList)
        return str.format(*d)
        
    def printPaturages(self):
        for i in range(len(self.paturages.casesDesPaturages)):
            print("Paturage en : {}, d une capacite de {} animaux".format(str(self.paturages.casesDesPaturages[i]), str(self.paturages.capacite[i])))
    
   
    def semer(self,ressource):
        combien=0
        if (ressource=='l'):
            combien=2
        else:
            combien=3
            
        self.ressources[ressource]+=combien
        
        
alias={
'foret':'F',
'tourbe':'T',
'champ':'C',
'etable':'E',
'carte':'Z',
'maisonBois':'B',
'maisonArgile':'A',
'maisonPierre':'S',
'vide':'V',
'paturage':'P'
    }        

class Tuile(object):
#foret, tourbe, champ, etable, carte, maisonBois,maisonArgile, maisonPierre,vide
    def __init__(self, type):
        self.type=type
        self.ressources=util.rVide()
    def __str__(self):
           return str(self.type)
    @property   
    def short(self):
        return alias[self.type]
        
class Paturage(object):

    def __init__(self):
        self.casesDesPaturages = []
        self.capacite = []
        self.aCloture = False

    def construireUnPaturage(self):
        possibilitesInitiales=[]
        ferme=variablesGlobales.joueurs[variablesGlobales.quiJoue].courDeFerme
        print(ferme.prettyPrint())
        for coord in ferme.etat.keys():
            #Test s'il y a deja d'autres paturage
            if not ferme.paturages.casesDesPaturages:
                if ferme.etat[coord].type=='vide':
                    possibilitesInitiales.append(coord)
            #TODO GERER L ADJACENCE AVEC UN AUTRE PATURAGE
            else:
                if (ferme.etat[coord].type=='vide'):
                    list_case_adj = estAdjacentA(coord)
                    list_case_paturage = list(flatten(ferme.paturages.casesDesPaturages))
                    intersect = ([x for x in list_case_adj if x in list_case_paturage])
                    if not intersect:
                        pass
                    else:
                        possibilitesInitiales.append(coord)
        choix=util.printPossibilities("Où voulez vous cloturer? :",possibilitesInitiales)
        print("Cloture de la case ", possibilitesInitiales[choix])
        print("")
        casesDuPaturage = []
        casesDuPaturage.append(possibilitesInitiales[choix])
        paturageTermine = False
        
        while paturageTermine==False:
            caseSupplementaire = []
            for i in range(len(casesDuPaturage)):
                for i in estAdjacentA(casesDuPaturage[i]):
                    if (ferme.etat[i].type=='vide') and ((i in casesDuPaturage)==False):
                        caseSupplementaire.append(i)
            if not caseSupplementaire:
                paturageTermine = True
            else:
                choix=util.printPossibilities("Ajouter une case au paturage en cours ? :",caseSupplementaire)        
                if choix == -1:
                    paturageTermine = True
                else:
                    casesDuPaturage.append(caseSupplementaire[choix])

        print("Construction d un paturage en : ", casesDuPaturage)
        check = ferme.clotures.construireLesClotures(ferme, casesDuPaturage)
        
        print("Bois restant: ", variablesGlobales.joueurs[variablesGlobales.quiJoue].ressources['b'])
        print(ferme.prettyPrint())

        if check == 1:
            self.casesDesPaturages.append(casesDuPaturage)
            self.capacite.append(2*len(casesDuPaturage))
            self.aCloture = True
        ferme.printPaturages()
        
class Clotures(object):

    def __init__(self):
        self.cases = []
        self.positions = np.array(['00V', '01V', '02V', '03V', '04V', '05V',\
                          '10V', '11V', '12V', '13V', '14V', '15V',\
                          '20V', '21V', '22V', '23V', '24V', '25V',\
                          '00H', '01H', '02H', 'O3H', '04H',\
                          '10H', '11H', '12H', '13H', '14H',\
                          '20H', '21H', '22H', '23H', '24H',\
                          '30H', '31H', '32H', '33H', '34H'])
                                                   
        self.adjacenteA = np.array([['00H', '10H', '10V'], ['00H', '01H', '10H', '11H', '11V'], ['01H', '02H', '11H', '12H', '12V'], ['02H', '03H', '12H', '13H', '13V'], ['03H', '04H', '13H', '14H', '14V'], ['04H', '14H', '15V'], \
                          ['10H', '20H', '00V', '20V'], ['10H', '11H', '20H', '21H', '01V', '21V'], ['11H', '12H', '21H', '22H', '02V', '22V'], ['12H', '13H', '22H', '23H', '03V', '23V'], ['13H', '14H', '23H', '24H', '04V', '24V'], ['14H', '24H', '05V', '25V'],\
                          ['20H', '30H', '10V'], ['20H', '21H', '30H', '31H', '11V'], ['21H', '22H', '31H', '32H', '12V'], ['22H', '23H', '32H', '33H', '13V'], ['23H', '24H', '33H', '34H', '14V'], ['24H', '34H', '15V'],\
                          ['00V', '01V', '01H'], ['01V', '02V', '00H', '02H'], ['02V', '03V', '01H', '03H'], ['03V', '04V', '02H', '04H'], ['04V', '05V', '03H'],\
                          ['00V', '01V', '10V', '11V', '11H'], ['01V', '02V', '11V', '12V','10H', '12H'], ['02V', '03V', '12V', '13V','11H', '13H'], ['03V', '04V', '13V', '14V','12H', '14H'], ['04V', '05V', '14V', '15V' '13H'],\
                          ['10V', '11V', '20V', '21V', '21H'], ['11V', '12V', '21V', '22V','20H', '22H'], ['12V', '13V', '22V', '23V','21H', '23H'], ['13V', '14V', '23V', '24V','22H', '24H'], ['14V', '15V', '24V', '25V' '23H'],\
                          ['20V', '21V', '21H'], ['21V', '22V', '20H', '22H'], ['22V', '23V', '21H', '23H'], ['23V', '24V', '22H', '24H'], ['24V', '25V', '23H']])
        
        self.estConstruite = []
        for i in range(len(self.positions)):
            self.estConstruite.append(False)
        self.estConstruite = np.array(self.estConstruite)
                         
        
    
    def construireLesClotures(self, ferme, casesDuPaturage):
        listClotures = []
        listCloturesADuPaturage = []
        listCloturesAConstruire = []
        #Determination de la liste des clotures constituant le paturage
        for i in casesDuPaturage:
            clotures = cloturesPourUneCase(i)
            listClotures.append(clotures)
        #Suppression des clotures communes aux deux cases
        for i in Counter(list(flatten(listClotures))).most_common():
            if i[1]==1:
                listCloturesADuPaturage.append((i[0]))
        #Suppression des clotures deja construite
        for i in listCloturesADuPaturage:
            if self.estConstruite[np.where(self.positions == i)] == False:
                listCloturesAConstruire.append(i)
        #Verification de la quantite de bois
        if len(listCloturesAConstruire) > variablesGlobales.joueurs[variablesGlobales.quiJoue].ressources['b']:
            print('le joueur n a pas assez de bois pour construire ces clotures')
            return 0
        else:
            variablesGlobales.joueurs[variablesGlobales.quiJoue].ressources['b'] += -len(listCloturesAConstruire)
            for i in casesDuPaturage:
                ferme.etat[i].type="paturage"
            for i in listCloturesAConstruire:
                self.estConstruite[np.where(self.positions==i)] = True
        return 1
        
def cloturesPourUneCase(case):


    if case == 'a1':
        return ['00H', '10H', '00V', '01V']
    if case == 'a2':
        return ['01H', '11H', '01V', '02V']
    if case == 'a3':
        return ['02H', '12H', '02V', '03V']
    if case == 'a4':
        return ['03H', '13H', '03V', '04V']
    if case == 'a5':
        return ['04H', '14H', '04V', '05V']
        
    if case == 'b1':
        return ['10H', '20H', '10V', '11V']
    if case == 'b2':
        return ['11H', '21H', '11V', '12V']
    if case == 'b3':
        return ['12H', '22H', '12V', '13V']
    if case == 'b4':
        return ['13H', '23H', '13V', '14V']
    if case == 'b5':
        return ['14H', '24H', '14V', '15V']
        
    if case == 'c1':
        return ['20H', '30H', '20V', '21V']
    if case == 'c2':
        return ['21H', '31H', '21V', '22V']
    if case == 'c3':
        return ['22H', '32H', '22V', '23V']
    if case == 'c4':
        return ['23H', '33H', '23V', '24V']
    if case == 'c5':
        return ['24H', '34H', '24V', '25V']     

        
def estAdjacentA(case):
    if case == 'a1':
        return ['a2', 'b1']
    if case == 'a2':
        return ['a1', 'a3', 'b2']
    if case == 'a3':
        return ['a2', 'a4', 'b3']
    if case == 'a4':
        return ['a3', 'a5', 'b4']
    if case == 'a5':
        return ['a4', 'b5']
        
    if case == 'b1':
        return ['a1', 'b2', 'c1']
    if case == 'b2':
        return ['a2', 'b1', 'b3', 'c2']
    if case == 'b3':
        return ['a3', 'b2', 'b4', 'c3']
    if case == 'b4':
        return ['a4', 'b3', 'b5', 'c4']
    if case == 'b5':
        return ['a5', 'b4', 'c5']
        
    if case == 'c1':
        return ['c2', 'b1']
    if case == 'c2':
        return ['c1', 'c3', 'b2']
    if case == 'c3':
        return ['c2', 'c4', 'b3']
    if case == 'c4':
        return ['c3', 'c5', 'b4']
    if case == 'c5':
            return ['c4', 'b5']  
            
 
