
def rVide():
    return {'b':0,'a':0,'p':0,'r':0,'n':0,'f':0,'c':0,'l':0,'m':0,'s':0,'v':0,'h':0}.copy()

def estVide(r):
    vide=True
    for k in r.keys():
        if r[k]!=0:
            vide=False
    return vide

def dummy():
    pass





# ~ listeReponse=["9","o","1","o","8","o","7","o","6","o"]
# ~ listeReponse=[]
# ~ listeReponse=["9","o","0","o","0","o","0","o","-1","o"]



idx=0



def customInput(partie,msg):
    global idx
    normalInput=True
    try:
        partie.listeReponse[idx]
        normalInput=False
    except:
        pass
    if normalInput:
        return input(msg)
    else:
        ret=partie.listeReponse[idx]
        idx+=1
        return ret        
    
#dans certains cas, on ne veux pas que l'action soit annulable, par exemple 
#quand on veut savoir si on construit la deuxieme piece
def printPossibilities(partie,message,possibilites,annulable=True):
    
    choixValide=False
    confirmation=False
    choix=-1
    while(not confirmation):
        while(not choixValide):
            
            for p in possibilites:
                if hasattr(p, 'display'):
                    nom=p.display
                elif hasattr(p, 'nom'):
                    nom=p.nom
                else:
                    nom=p
                print("{} : {}".format(possibilites.index(p),nom))
            if annulable:
                print('a pour anuler:')     
            g = customInput(partie,message+"   ") 
            try:
                if g=='a':
                    if not annulable:
                        print("impossible de faire annuler sur ce choix")  
                    else:
                        print('anulation!') 
                        return -1
                else:    
                    choixValide=(int(g)<len(possibilites))
                    choix=int(g)
            except:
                pass
            if not choixValide:
                print('Vous avez fait un choix invalide!!',g,' Recommencez')
        
        
        stri="Vous avez choisi {}\n Vous confirmez?(o/n)   ".format(possibilites[choix])
        conf = customInput(partie,stri) 
        if(conf=='o'):
            confirmation=True
        elif conf=='n':
            choixValide=False
        else:
            print('Vous avez fait un choix invalide (il faut "o" ou "n"!! Recommencez')
        
    return choix 


short2Long={
    'b':'bois',
    'a':'argile',
    'p':'pierre',
    'r':'roseau',
    'n':'pn',
    'f':'feu',
    'c':'cereale',
    'l':'legume',
    'm':'mouton',
    's':'sanglier',
    'v':'boeuf',
    'h':'cheval',
    }
long2Short={
    'bois':'b',
    'argile':'a',
    'pierre':'p',
    'roseau':'r',
    'pn':'n',
    'feu':'f',
    'cereale':'c',
    'legume':'l',
    'mouton':'m',
    'sanglier':'s',
    'boeuf':'v',
    'cheval':'h',
    }


def ajouter(a,b):
    somme={}
    for k in list(set(a.keys()).union(set(b.keys()))):
        if k not in a.keys():
            somme[k]=b[k]
        elif k not in b.keys():
            somme[k]=a[k]
        else:
            somme[k]=a[k]+b[k]
    print("somme",a,b,somme)
    return somme.copy()

def sontEgaux(a,b):
    egaux=True
    for k in list(set(a.keys()).union(set(b.keys()))):
        if k not in a.keys():
            if b[k]!=0:
                egaux=False
                break
        elif k not in b.keys():
            if a[k]!=0:
                egaux=False
                break
        else:
            if a[k]!=b[k]:
                egaux=False
                break
    if not egaux:
        print(a,b)
    
    return egaux


def jouable(a,b):
    #true if a>=b
    #valable pour cout et condition
    res=True
    raison="OK"
    for k in a.keys():
        if k in b.keys():
            if (b[k]>0):
                if a[k]<b[k]:
                    res=False
                    raison="non jouable {} {} {}".format(k,a[k],b[k])
                    break
    return res,raison

def prettyGain(a):
    stri=""
    for k in a.keys():
        if (a[k]!=0):
            stri+="+{} {} ".format(str(-a[k]),short2Long[k])
    return stri

        
