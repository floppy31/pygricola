import pygricola.util as util
from collections import OrderedDict
# from collections import Counter, OrderedDict
# from pandas.core.common import flatten
# from collections import Counter
# import numpy as np




parseList=[]
for l in ['A','B','C']:
    for i in range(1,6):
        parseList.append("{}{}".format(l,i))
        
        
class CourDeFerme(object):

    def __init__(self,partie):
        self.partie=partie
        self.etat=OrderedDict()
        for case in parseList:
            self.etat[case]=Tuile('vide')
        self.etat["B1"]=Tuile('maisonBois')
        self.etat["C1"]=Tuile('maisonBois')
        self.paturagesContigus = {} #vrai paturage put être de plusieurs cases
        self.cloturesDispo=15 #liste des 15 clotures
        self.reserveEtable=['e','e','e','e']
        self.annexe=[]
        self.tmpPaturage=[] #tempo... pour connaitre le coup de cloture
        #on doit le simuler avant voir coutCreerPaturage
    
    
    #####ANIMAUX
    
    def calculerCapaciteStockage(self):
        
        dico={}
        buf=[]
        patDejaPasse=[]
        for p in self.tousLes('paturage'):
            if not p in patDejaPasse:
                cap=self.etat[p].calculer_capacite
                dico[p]=cap
                buf.append(cap)
            for case in self.etat[p].cases:
                patDejaPasse.append(case)
                
            
        dico['etableSimple']=self.compter('etable')
        #une place par etable
        for e in self.tousLes('etable'):
            buf.append(1)
        
        #1 place adns la maison
        buf.append(1)
        
        dico['tot']=sum(dico.values())+1 #+1 dans la maison
        
        buf.sort(reverse=True)
        dico['list']=buf
        print(dico)
        
        return dico
        
        
           
        
    def initTuiles(self,positionTourbes,positionForets):   
        for t in positionTourbes:
            self.etat[t]=Tuile('tourbe')
        for f in positionForets:
            self.etat[f]=Tuile('foret')               
    
    def __str__(self):
           return self.prettyPrint()
       
    def enQuoiEstLaMaison(self,court=True):
        if court:
            return util.long2Short[self.etat["B1"].type.split('maison')[1].lower()]
        else:
            return self.etat["B1"].type
    @property
    def etablesDispo(self):
        return len(self.reserveEtable)
    @property
    def etablesJouees(self):
        simple=self.compter('etable')
        dansPaturage=0
        for key,pat in self.paturagesContigus.items():
            dansPaturage+=len(pat.etables)
        return simple+dansPaturage
    
    def coutMiniCloture(self):
        
        if self.compter('paturage')==0:
            #jouter ici les bonnus
            return {'b':4}
        elif self.compter('paturage')==1: # 1 paturage de 1 case
            return {'b':3}
        elif self.compter('paturage')==2: 
            #soit  1 paturage de 2 cases
            if len(self.paturagesContigus.keys())==1:
                return {'b':1} #on peut le diviser
            else:
                return {'b':3} #il faut en faire un nouveau
        elif self.compter('paturage')==3:
            #soit  1 paturage de 3 cases
            if len(self.paturagesContigus.keys())<3:
                return {'b':1} #on peut le diviser 
            else:
                #3 paturages simple
                #cas compact : on referme un carré -->2  sinon 3
                
                #si tous sur la même ligne ou la même colonne 3 sinon 2
                cases=self.tousLes('paturages')
                cols=[case[0] for case in cases ] #AAA, ABA,...
                lines =[case[1] for case in cases ]
                
                if len(set(cols)) ==1 or len(set(lines)) ==1:
                    return {'b':3}
                else:
                    return {'b':2}
        elif self.compter('paturage')==4:
            #soit 1 paturage de 4 cases
            if len(self.paturagesContigus.keys())==1:
                #si il a 8 cloture c'est un carre
                if self.paturagesContigus.values()[0].cloturesUtilises==8:
                    return {'b':2} #on peut le diviser
                else:
                    return {'b':1}
            elif len(self.paturagesContigus.keys())==2:
                return {'b':1}
            elif len(self.paturagesContigus.keys())==3:
                return {'b':1}
            else:
                return 10000000000 #on ne peux plus 4 paturages simples    
             
        elif self.compter('paturage')==5:
            TODO
        elif self.compter('paturage')==6:
            #soit 2 bois cas compact soit b 1 
            TODO
    
    def contient(self,type):
        return type in self.etat.keys()
    
    def compter(self,type):
        if type=='paturage':
            return len(self.paturagesContigus.keys())
        else:
            
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
    
    def estVoisin(self,coord1,coord2):
        voiz=self.voisin(coord1)
        reponse=False
        for k in voiz.keys():
            print(voiz[k],coord2,voiz[k]==coord2)
            if voiz[k]==coord2:
                reponse=True
        return reponse
        
        
    
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
        
        if ligne=="A":
            voisins["s"]="B"+str(colonne)
        elif ligne=="B":
            voisins["n"]="A"+str(colonne)
            voisins["s"]="C"+str(colonne)
        elif ligne=="C":
            voisins["n"]="B"+str(colonne)
            
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
    
    def mettrePersonnage(self,perso,case):
        perso.localisation=case
        self.etat[case].occupants.append(perso)   

        
    def save(self):
        #TODO: doit retourner un dico ou ordered dico
        dico={}
        dico['clotures']=self.cloturesDispo
        dico['etables']=len(self.reserveEtable)
        rep=[]
        for case in parseList:
            (picto,etable)= self.etat[case].pictos(case)
            rep.append({'type':self.etat[case].type,'picto':picto,'etable':etable,'occupants':len(self.etat[case].occupants)})
        dico['ferme']=rep
        dico['stockage']=self.calculerCapaciteStockage()['list']
        return dico
    
    def load(self,dico):
        print('loadFerme',dico)
        #TODO : doit refaire la cour de ferme à partir d'un dico
        return 0
    
    def creerPaturageSimple(self,case,etable=False):
        pature = Paturage([case],[],self)
        if etable:
            pature.etables.append(case)
            #on remet une etable dans etable dispo
            self.reserveEtable.append('e')
        self.etat[case]=pature
        cout=self.coutCreerPaturage([case])
        self.cloturesDispo-=cout['b']
        pature.cloturesUtilises=cout['b']
        self.paturagesContigus[case]=pature
 
    def creerPaturageMultiple(self,casesList):
        pature = Paturage(casesList,[],self)
        for c in casesList:
            if self.etat[c].type=='etable':
                pature.etables.append(c)
                #on remet une etable dans etable dispo
            self.etat[c]=pature
        cout=self.coutCreerPaturage(casesList)        
        self.cloturesDispo-=cout['b']
        pature.cloturesUtilises=cout['b']
        self.paturagesContigus['-'.join(casesList)]=pature

    def coutCreerPaturage(self,casesList):

        #d'abord sans les voisins
        if len (casesList)==1:        
            coutSansVoisins=4
        elif len (casesList)==2:
            coutSansVoisins=6
        elif len (casesList)==3:
            coutSansVoisins=8
        elif len (casesList)==4:
            #si c'est en carre (chaque case à 2 voisines
            enCarre=True
            for c in casesList:
                compteur=0
                for voiz in self.voisin(c).values():
                    if voiz in casesList:
                        compteur +=1
                if compteur<2:
                    print('pas en carré',c,casesList)
                    enCarre=False
                    break
            print("EN CARRE",enCarre,compteur)
            if enCarre:
                coutSansVoisins=8
            else:
                coutSansVoisins=10
        elif len (casesList)==5:
            #je crois 2 cas possible
            #A compact --> 10 (tous 2 voisin sauf 1 cases 
            #B autre 12    
            compacte=True
            caseSoloPassee=False
            for c in casesList:
                compteur=0
                for voiz in self.voisin(c).values():
                    if voiz in casesList:
                        compteur +=1
                if compteur<2 and not caseSoloPassee:
                    caseSoloPassee=True
                elif compteur<2 and caseSoloPassee:
                    #pas compact
                    compacte=False
                    break
            if compacte:
                coutSansVoisins=10
            else:
                coutSansVoisins=12            
        elif len (casesList)==6: 
            #cas compacte 10 tout le monde à 2 voisins
            #cas bof tous le monde à deux voisin sauf 2 cases
            #cas moisi
             
            compacte=True
            bof=False
            caseSolo=[]
            for c in casesList:
                compteur=0
                for voiz in self.voisin(c).values():
                    if voiz in casesList:
                        compteur +=1
                 
                if compteur<2:
                    compacte=False
                    caseSolo.append(c)
                     
            if compacte:
                coutSansVoisins=10
            else:
                if len(caseSolo)==2:
                    coutSansVoisins=12
                else:
                    coutSansVoisins=14
        print('COUTSANSVOISINS',coutSansVoisins)                  
        reducBois=0
        
        for c in casesList:
            voiz=self.voisin(c)
            for direction in voiz.keys():
                if voiz[direction]: #si not None
                    #on saut les cases qui sont elles même dans le paturage
                    if voiz[direction] not in casesList:
                        if self.etat[voiz[direction]].type=='paturage':
                            reducBois+=1
                        elif voiz[direction] in self.tmpPaturage:
                            reducBois+=1          
                    else:
                        print('skip',voiz[direction])
        print('COUTSANSVOISINS',coutSansVoisins) 
        print('COUTFINAL',coutSansVoisins-reducBois) 
        return {'b':coutSansVoisins-reducBois}     
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
        self.occupants=[]
        print('TUILE',type)
    def __str__(self):
           return str(self.type)
    @property   
    def short(self):
        return alias[self.type]

    def semer(self,ressource):
        if self.type=="champ":
            combien=0
            if (ressource=='l'):
                combien=2
            else:
                combien=3
                
            self.ressources[ressource]+=combien
        else:
            print("ERREUR vous ne pouvez semer que sur un champ")
            qsfqdfdf
    def pictos(self,case):
        return (alias[self.type],self.type=="etable")
    
        
class Paturage(Tuile):
    #les occupants sont les animaux
    def __init__(self, cases,etables,cour):
        self.cases = cases #liste des cases 
        self.etables = etables
        self.cloturesUtilises=0
        self.cour=cour# la cour de ferme
        super().__init__('paturage')
        print('----> CONSTRUCTION PATURAGE',self.cases,self.etables)
        
    
    @property
    def calculer_capacite(self):
        return (len(self.cases)*2)* (2**len(self.etables))
    
    #on peut le remodifier ou non
    def estDivisable(self):
        return len (self.cases)==1
    
    def pictos(self,case):
        clotures={'n':True,'s':True,'e':True,'w':True}
        ordre=['n','s','e','w']
        voiz=self.cour.voisin(case)
        for direction in voiz.keys():
            if voiz[direction]: #si not None    
                if voiz[direction] in self.cases:
                    clotures[direction]=False
        picto=""
        listVals=list(clotures.values())
        if listVals.count(True)==4:
            picto='p4'
        elif listVals.count(True)==3:
            picto='p3'+list(clotures.keys())[listVals.index(False)]
        elif listVals.count(True)==2:
            picto='p2'
            for dir in ordre:
                if clotures[dir]==True:
                    picto+=dir
        elif listVals.count(True)==1:
            picto='p1'
            for dir in ordre:
                if clotures[dir]==True:
                    picto+=dir
        else:
            picto='p0'
        
        return (picto,case in self.etables)
    
                
#     def checkClotures(self):
#         if len (self.cases)==1:
#             voiz=self.cour.voisin(self.cases[0])
#             reduc=0
#             for direction in voiz.keys():
#                 if voiz[direction]: #si not None
#                     if self.cour.etat[voiz[direction]].type=='paturage':
#                         reduc+=1
#             print('toto',self.cloturesUtilises,reduc)
#             return self.cloturesUtilises==4-reduc
#         elif len (self.cases)==2:
#             return self.cloturesUtilises==6
#         elif len (self.cases)==3:
#             return self.cloturesUtilises==8
#         elif len (self.cases)==4:
#             #si c'est en carre (chaque case à 2 voisines
#             enCarre=True
#             for c in self.cases:
#                 compteur=0
#                 for voiz in self.cour.voisin(c):
#                     if voiz in self.cases:
#                         compteur +=1
#                 if compteur<2:
#                     enCarre=False
#                     break
#             if enCarre:
#                 return self.cloturesUtilises==8
#             else:
#                 return self.cloturesUtilises==10
#         elif len (self.cases)==5:
#             #je crois 2 cas possible
#             #A compact --> 10 (tous 2 voisin sauf 1 cases 
#             #B autre 12    
#             compacte=True
#             caseSoloPassee=False
#             for c in self.cases:
#                 compteur=0
#                 for voiz in self.cour.voisin(c):
#                     if voiz in self.cases:
#                         compteur +=1
#                 if compteur<2 and not caseSoloPassee:
#                     caseSoloPassee=True
#                 elif compteur<2 and caseSoloPassee:
#                     #pas compact
#                     compacte=False
#                     break
#             if compacte:
#                 return self.cloturesUtilises==10
#             else:
#                 return self.cloturesUtilises==12            
#         elif len (self.cases)==6: 
#             #cas compacte 10 tout le monde à 2 voisins
#             #cas bof tous le monde à deux voisin sauf 2 cases
#             #cas moisi
#             
#             compacte=True
#             bof=False
#             caseSolo=[]
#             for c in self.cases:
#                 compteur=0
#                 for voiz in self.cour.voisin(c):
#                     if voiz in self.cases:
#                         compteur +=1
#                 
#                 if compteur<2:
#                     compacte=False
#                     caseSolo.append(c)
#                     
#             if compacte:
#                 return self.cloturesUtilises==10
#             else:
#                 if len(caseSolo)==2:
#                     return self.cloturesUtilises==12
#                 else:
#                     return self.cloturesUtilises==14              
#                
#             
#         
# class PaturageOld(object):
# 
#     def __init__(self):
#         self.casesDesPaturages = []
#         self.capacite = []
#         self.aCloture = False
# 
#     def construireUnPaturage(self):
#         possibilitesInitiales=[]
#         ferme=self.partie.joueurs[self.partie.quiJoue].courDeFerme
#         print(ferme.prettyPrint())
#         for coord in ferme.etat.keys():
#             #Test s'il y a deja d'autres paturage
#             if not ferme.paturages.casesDesPaturages:
#                 if ferme.etat[coord].type=='vide':
#                     possibilitesInitiales.append(coord)
#             #TODO GERER L ADJACENCE AVEC UN AUTRE PATURAGE
#             else:
#                 if (ferme.etat[coord].type=='vide'):
#                     list_case_adj = estAdjacentA(coord)
#                     list_case_paturage = list(flatten(ferme.paturages.casesDesPaturages))
#                     intersect = ([x for x in list_case_adj if x in list_case_paturage])
#                     if not intersect:
#                         pass
#                     else:
#                         possibilitesInitiales.append(coord)
#         choix=util.printPossibilities("Où voulez vous cloturer? :",possibilitesInitiales)
#         print("Cloture de la case ", possibilitesInitiales[choix])
#         print("")
#         casesDuPaturage = []
#         casesDuPaturage.append(possibilitesInitiales[choix])
#         paturageTermine = False
#         
#         while paturageTermine==False:
#             caseSupplementaire = []
#             for i in range(len(casesDuPaturage)):
#                 for i in estAdjacentA(casesDuPaturage[i]):
#                     if (ferme.etat[i].type=='vide') and ((i in casesDuPaturage)==False):
#                         caseSupplementaire.append(i)
#             if not caseSupplementaire:
#                 paturageTermine = True
#             else:
#                 choix=util.printPossibilities("Ajouter une case au paturage en cours ? :",caseSupplementaire)        
#                 if choix == -1:
#                     paturageTermine = True
#                 else:
#                     casesDuPaturage.append(caseSupplementaire[choix])
# 
#         print("Construction d un paturage en : ", casesDuPaturage)
#         check = ferme.clotures.construireLesClotures(ferme, casesDuPaturage)
#         
#         print("Bois restant: {}, Clotures Restantes: {}".format(self.partie.joueurs[self.partie.quiJoue].ressources['b'], self.partie.joueurs[self.partie.quiJoue].cloturesRestantes))
#         print(ferme.prettyPrint())
# 
#         if check == 1:
#             self.casesDesPaturages.append(casesDuPaturage)
#             self.aCloture = True
#             
#         self.calculer_capacite()
#         ferme.printPaturages()
#         
#         
#     def diviserUnPaturage(self):
#         possibilitesInitiales=[]
#         ferme=self.partie.joueurs[self.partie.quiJoue].courDeFerme
#         cases_gros_paturages = []
#         # Choix de la case initiale
#         if not self.casesDesPaturages:
#             return
#         else:
#             for i in self.casesDesPaturages:
#                 if len(i)>1:
#                     cases_gros_paturages.append(i)
#         choix=util.printPossibilities("diviser quel paturage pour en faire un nouveau ? :",cases_gros_paturages)
#         
#         stop = False
#         cases_a_diviser = []
#         paturage_selectionne = cases_gros_paturages[choix]
#         choix=util.printPossibilities("Selectionner une case ? :",paturage_selectionne)
#         cases_a_diviser.append(paturage_selectionne[choix])
#         while (len(paturage_selectionne)-len(cases_a_diviser) >1) and (stop==False):
#             cases_possibles = []
#             for coord in paturage_selectionne:
#                 list_case_adj = estAdjacentA(coord)
#                 list_case_paturage = list(flatten(cases_a_diviser))
#                 intersect = ([x for x in list_case_adj if x in list_case_paturage])
#                 if not intersect:
#                     pass
#                 else:
#                     cases_possibles.append(coord)
#             choix=util.printPossibilities("Ajouter une case au nouveau paturage divise ? :",cases_possibles)
#             if choix == -1:
#                 stop = True
#             else:
#                 cases_a_diviser.append(cases_possibles[choix])
#             
#         print("Division d un paturage en : ", cases_a_diviser)
#         check = ferme.clotures.construireLesClotures(ferme, cases_a_diviser)                    
#         print("Bois restant: {}, Clotures Restantes: {}".format(self.partie.joueurs[self.partie.quiJoue].ressources['b'], self.partie.joueurs[self.partie.quiJoue].cloturesRestantes))
#         print(ferme.prettyPrint())
# 
#         if check == 1:
#             for i in self.casesDesPaturages:
#                 if i == paturage_selectionne:
#                     #suppression ancien paturage
#                     self.casesDesPaturages.remove(paturage_selectionne)
#                     #Ajout du nouveau
#                     self.casesDesPaturages.append(cases_a_diviser)
#                     for k in cases_a_diviser:
#                         paturage_selectionne.remove(k)
#                         cases_restantes =  paturage_selectionne
#             while len(cases_restantes)>0:
#                 nouveau_pat=[]
#                 el = cases_restantes[0]
#                 nouveau_pat.append(el)
#                 el_adj = estAdjacentA(el)
#                 cases_restantes.remove(el)
#                 for i in cases_restantes:
#                     intersect = ([x for x in el_adj if x in cases_restantes])
#                     if not intersect:
#                         pass
#                     else:
#                         nouveau_pat.append(i)
#                         cases_restantes.remove(i)
#  
#                 self.casesDesPaturages.append(nouveau_pat)
#                 
#         self.calculer_capacite()
#         ferme.printPaturages()
#                     

# 
# class Clotures(object):
# 
#     def __init__(self):
#         self.cases = []
#         self.positions = np.array(['00V', '01V', '02V', '03V', '04V', '05V',\
#                           '10V', '11V', '12V', '13V', '14V', '15V',\
#                           '20V', '21V', '22V', '23V', '24V', '25V',\
#                           '00H', '01H', '02H', 'O3H', '04H',\
#                           '10H', '11H', '12H', '13H', '14H',\
#                           '20H', '21H', '22H', '23H', '24H',\
#                           '30H', '31H', '32H', '33H', '34H'])
#                                                    
#         self.adjacenteA = np.array([['00H', '10H', '10V'], ['00H', '01H', '10H', '11H', '11V'], ['01H', '02H', '11H', '12H', '12V'], ['02H', '03H', '12H', '13H', '13V'], ['03H', '04H', '13H', '14H', '14V'], ['04H', '14H', '15V'], \
#                           ['10H', '20H', '00V', '20V'], ['10H', '11H', '20H', '21H', '01V', '21V'], ['11H', '12H', '21H', '22H', '02V', '22V'], ['12H', '13H', '22H', '23H', '03V', '23V'], ['13H', '14H', '23H', '24H', '04V', '24V'], ['14H', '24H', '05V', '25V'],\
#                           ['20H', '30H', '10V'], ['20H', '21H', '30H', '31H', '11V'], ['21H', '22H', '31H', '32H', '12V'], ['22H', '23H', '32H', '33H', '13V'], ['23H', '24H', '33H', '34H', '14V'], ['24H', '34H', '15V'],\
#                           ['00V', '01V', '01H'], ['01V', '02V', '00H', '02H'], ['02V', '03V', '01H', '03H'], ['03V', '04V', '02H', '04H'], ['04V', '05V', '03H'],\
#                           ['00V', '01V', '10V', '11V', '11H'], ['01V', '02V', '11V', '12V','10H', '12H'], ['02V', '03V', '12V', '13V','11H', '13H'], ['03V', '04V', '13V', '14V','12H', '14H'], ['04V', '05V', '14V', '15V' '13H'],\
#                           ['10V', '11V', '20V', '21V', '21H'], ['11V', '12V', '21V', '22V','20H', '22H'], ['12V', '13V', '22V', '23V','21H', '23H'], ['13V', '14V', '23V', '24V','22H', '24H'], ['14V', '15V', '24V', '25V' '23H'],\
#                           ['20V', '21V', '21H'], ['21V', '22V', '20H', '22H'], ['22V', '23V', '21H', '23H'], ['23V', '24V', '22H', '24H'], ['24V', '25V', '23H']])
#         
#         self.estConstruite = []
#         for i in range(len(self.positions)):
#             self.estConstruite.append(False)
#         self.estConstruite = np.array(self.estConstruite)
#                          
#         
#     
#     def construireLesClotures(self, ferme, casesDuPaturage):
#         listClotures = []
#         listCloturesADuPaturage = []
#         listCloturesAConstruire = []
#         #Determination de la liste des clotures constituant le paturage
#         for i in casesDuPaturage:
#             clotures = cloturesPourUneCase(i)
#             listClotures.append(clotures)
#         #Suppression des clotures communes aux deux cases
#         for i in Counter(list(flatten(listClotures))).most_common():
#             if i[1]==1:
#                 listCloturesADuPaturage.append((i[0]))
#         #Suppression des clotures deja construite
#         for i in listCloturesADuPaturage:
#             if self.estConstruite[np.where(self.positions == i)] == False:
#                 listCloturesAConstruire.append(i)
#         #Verification de la quantite de bois
#         if len(listCloturesAConstruire) > self.partie.joueurs[self.partie.quiJoue].ressources['b']:
#             print('le joueur n a pas assez de bois pour construire ces clotures')
#             return 0
#         if len(listCloturesAConstruire) > self.partie.joueurs[self.partie.quiJoue].cloturesRestantes:
#             return 0
#         else:
#             self.partie.joueurs[self.partie.quiJoue].ressources['b'] += -len(listCloturesAConstruire)
#             self.partie.joueurs[self.partie.quiJoue].cloturesRestantes += -len(listCloturesAConstruire)            
#             for i in casesDuPaturage:
#                 ferme.etat[i].type="paturage"
#             for i in listCloturesAConstruire:
#                 self.estConstruite[np.where(self.positions==i)] = True
#         return 1
#         
# def cloturesPourUneCase(case):
# 
# 
#     if case == 'a1':
#         return ['00H', '10H', '00V', '01V']
#     if case == 'a2':
#         return ['01H', '11H', '01V', '02V']
#     if case == 'a3':
#         return ['02H', '12H', '02V', '03V']
#     if case == 'a4':
#         return ['03H', '13H', '03V', '04V']
#     if case == 'a5':
#         return ['04H', '14H', '04V', '05V']
#         
#     if case == 'b1':
#         return ['10H', '20H', '10V', '11V']
#     if case == 'b2':
#         return ['11H', '21H', '11V', '12V']
#     if case == 'b3':
#         return ['12H', '22H', '12V', '13V']
#     if case == 'b4':
#         return ['13H', '23H', '13V', '14V']
#     if case == 'b5':
#         return ['14H', '24H', '14V', '15V']
#         
#     if case == 'c1':
#         return ['20H', '30H', '20V', '21V']
#     if case == 'c2':
#         return ['21H', '31H', '21V', '22V']
#     if case == 'c3':
#         return ['22H', '32H', '22V', '23V']
#     if case == 'c4':
#         return ['23H', '33H', '23V', '24V']
#     if case == 'c5':
#         return ['24H', '34H', '24V', '25V']     
# 
#         
# def estAdjacentA(case):
#     if case == 'a1':
#         return ['a2', 'b1']
#     if case == 'a2':
#         return ['a1', 'a3', 'b2']
#     if case == 'a3':
#         return ['a2', 'a4', 'b3']
#     if case == 'a4':
#         return ['a3', 'a5', 'b4']
#     if case == 'a5':
#         return ['a4', 'b5']
#         
#     if case == 'b1':
#         return ['a1', 'b2', 'c1']
#     if case == 'b2':
#         return ['a2', 'b1', 'b3', 'c2']
#     if case == 'b3':
#         return ['a3', 'b2', 'b4', 'c3']
#     if case == 'b4':
#         return ['a4', 'b3', 'b5', 'c4']
#     if case == 'b5':
#         return ['a5', 'b4', 'c5']
#         
#     if case == 'c1':
#         return ['c2', 'b1']
#     if case == 'c2':
#         return ['c1', 'c3', 'b2']
#     if case == 'c3':
#         return ['c2', 'c4', 'b3']
#     if case == 'c4':
#         return ['c3', 'c5', 'b4']
#     if case == 'c5':
#             return ['c4', 'b5']  
#             
 
