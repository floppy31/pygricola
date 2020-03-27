
parseList=[]
for l in ['a','b','c']:
    for i in range(1,6):
        parseList.append("{}{}".format(l,i))
        
        
class CourDeFerme(object):

    def __init__(self):
        self.etat={}
        for case in parseList:
            self.etat[case]=Tuile('vide')
        self.etat["c2"]=Tuile('maisonBois')
        self.etat["b1"]=Tuile('maisonBois')
        self.etat["c1"]=Tuile('maisonBois')
        self.etat["c3"]=Tuile('champ') #DEBUG
        self.annexe=[]
        
    def initTuiles(self,positionTourbes,positionForets):   
        for t in positionTourbes:
            self.etat[t]=Tuile('tourbe')
        for f in positionForets:
            self.etat[f]=Tuile('foret')               
    
    def __str__(self):
           return self.prettyPrint()
       
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
        
alias={
'foret':'F',
'tourbe':'T',
'champ':'C',
'etable':'E',
'carte':'Z',
'maisonBois':'B',
'maisonArgile':'A',
'maisonPierre':'P',
'vide':'V'
    }        

class Tuile(object):
#foret, tourbe, champ, etable, carte, maisonBois,maisonArgile, maisonPierre,vide
    def __init__(self, type):
        self.type=type
    def __str__(self):
           return str(self.type)
    @property   
    def short(self):
        return alias[self.type]
