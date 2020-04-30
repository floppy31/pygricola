from pygricola.traduction import trad

def findCarte(carteList,uid):
    for c in carteList:
        if c.uid==uid:
            return c
    

         

# def parcourirLesHooks(partie,typeHook,logger):
#     hookFinis=False
#     for jid,j in partie.joueurs.items():
#         for cuid,c in j.cartesDevantSoi.items():
#             if hasattr(c, 'hook'):
#                 if c.hook != ():
# #                     logger.debug("{} {} {}".format(c.uid,'a un hook',c.hook[0]))
#                     if c.hook[0]==typeHook:
#                         #si le hook est jouable
#                         if c.hookStatus==0:
#                             logger.debug("parcourirLesHooks sur {} avec {} {}".format(typeHook,c.uid,c.hookStatus))
#                             #si le hook me concerne
#                             if(c.hook[1]=="s"):
#                                 #si il y a plusieurs possibilites
#                                 c.possibilites(Fake=False)
#                                 #partie.choixPossibles
#                                 #soit une liste soit un int
#                                 if partie.choixPossibles==-1:
#                                     logger.debug("parcourirLesHooks fait une action automatique")
#                                     c.effet(0,partie.choixPossibles)
#                                 elif type(partie.choixPossibles)==list:
#                                     if len(partie.choixPossibles)>1:
#                                         logger.debug("parcourirLesHooks demande un choix utilisateur {} {}\n possibilites {}".format(c.uid,c.hookStatus,partie.choixPossibles))
#                                         return hookFinis
#                                     else:
#                                     #sinon
#                                         logger.debug("parcourirLesHooks fait une action automatique car un seul choix")
#                                         c.effet(0,partie.choixPossibles)
#                                 else: 
#                                     UNKNOWN
#                         else:
#                             logger.debug("parcourirLesHooks: hook déjà consomé",c.uid,c.hookStatus) 
#     hookFinis=True 
#     return  hookFinis              

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

def traduire(stri):
    if isinstance(stri,list):
        s=""
        for i in stri:
            if i in trad.keys():
                s+="{} ".format(trad[i]['fr'])
            elif i[0] in ['A','B','C']:
                s+=i
            else:
                s+='NO TRAD'+i
        return s
    elif isinstance(stri,str):
        if stri in trad.keys():
            return "{} ".format(trad[stri]['fr'])
        elif stri[0] in ['A','B','C']:
            return stri
        else:
            return 'PAS DE TRADUCTION str'+stri



# ~ listeReponse=["9","o","1","o","8","o","7","o","6","o"]
# ~ listeReponse=[]
# ~ listeReponse=["9","o","0","o","0","o","0","o","-1","o"]



idx=0


def tradUidOrSelf(o):
    if hasattr(o, 'uid'):
        return traduire(o.uid)
    else:
        return o
        
def uidOrSelf(o):
    if hasattr(o, 'uid'):
        return o.uid
    else:
        return o

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
                print("{} : {}".format(possibilites.index(p),tradUidOrSelf(p)))
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
        
        
        stri="Vous avez choisi {}\n Vous confirmez?(o/n)   ".format(tradUidOrSelf(possibilites[choix]))
        conf = customInput(partie,stri) 
        if(conf=='o'):
            confirmation=True
        elif conf=='n':
            choixValide=False
        else:
            print('Vous avez fait un choix invalide (il faut "o" ou "n"!! Recommencez')
        
    return choix 

def coupAuClavier(partie):
    choixValide=False
    while(not choixValide):
        for p in partie.pointeur.possibilites:
            print("{} : {}".format(partie.pointeur.possibilites.index(p),tradUidOrSelf(p)))
        g = input(traduire(partie.pointeur.phrase)+'\n') 
        try:
            choixValide=(int(g)<len(partie.pointeur.possibilites))
            choix=int(g)
        except:
            pass

    return uidOrSelf(partie.pointeur.possibilites[choix])




short2Long={
    'b':'rb',
    'a':'ra',
    'p':'rp',
    'r':'rr',
    'n':'rn',
    'f':'rf',
    'c':'rc',
    'l':'rl',
    'm':'rm',
    's':'rs',
    'v':'rv',
    'h':'rh',
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

#si b est une liste on renvoie une liste
def ajouter(a,b):
    
    
    if type(b)==list:
        somme=[]
        for c in b:
            dicoSomme={}
            for k in list(set(a.keys()).union(set(c.keys()))):
                if k not in a.keys():
                    dicoSomme[k]=c[k]
                elif k not in c.keys():
                    dicoSomme[k]=a[k]
                else:
                    dicoSomme[k]=a[k]+c[k]
            somme.append(dicoSomme)
        return somme.copy()
    else:
        somme={}
        for k in list(set(a.keys()).union(set(b.keys()))):
            if k not in a.keys():
                somme[k]=b[k]
            elif k not in b.keys():
                somme[k]=a[k]
            else:
                somme[k]=a[k]+b[k]
        return somme.copy()

def inverser(a):
    reponse={}
    for k in a.keys():
        reponse[k]=-a[k]
    return reponse



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
        print('sontEgaux: NON!',a,b)
    
    return egaux


def jouable(constA,constB):
    #true if a>=b
    #valable pour cout et condition
    a=ajouter(constA,rVide())
    
    if type(constB)==dict:
        bList=[ajouter(constB,rVide())]
        resultatList=[True]
        raisonList=['OK']
    elif type(constB)==list:
        bList=[]
        resultatList=[]
        raisonList=[]
        for bitem in constB:
            print(bitem)
            bList.append(ajouter(bitem,rVide()))
            resultatList.append(True) 
            raisonList.append('OK')       
    else:
        error
    
    for b in bList:
        res=True
        raison="OK"
        index=bList.index(b)
        ressourcesProbleme=[]
        for k in a.keys():
            #print('dbg',k)
            
            if (b[k]>0):
                if a[k]<b[k]:
                    res=False
                    raison=["p15",k,a[k],b[k]]
                    ressourcesProbleme.append(k)  
        #s'il n'y a qu'un probleme de combustible
        if ressourcesProbleme==['f']:
            diffBois=b['f']-a['f']
            if not (a['b']-diffBois)<b['b']:
                raison="utilisation du bois"
                res=True
        resultatList[index]=res
        raisonList[index]=raison
    if True in set(resultatList):
        return True,raisonList
    else:
        return False,raisonList                   

def prettyGain(a):
    stri=""
    for k in a.keys():
        if (a[k]!=0):
            stri+="+{} {} ".format(str(-a[k]),short2Long[k])
    return stri

        
