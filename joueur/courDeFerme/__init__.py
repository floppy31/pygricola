
parseList=[]
for l in ['a','b','c']:
    for i in range(1,6):
        parseList.append("{}{}".format(l,i))
        
        
class CourDeFerme(object):

    def __init__(self):
        self.etat={}
        for case in parseList:
            self.etat[case]=Tuile('vide')
        self.etat["b1"]=Tuile('maisonBois')
        self.etat["c1"]=Tuile('maisonBois')

        self.annexe=[]
        
    def initTuiles(self,positionTourbes,positionForets):   
        for t in positionTourbes:
            self.etat[t]=Tuile('tourbe')
        for f in positionForets:
            self.etat[f]=Tuile('foret')               
    
    def __str__(self):
           return self.prettyPrint()

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
