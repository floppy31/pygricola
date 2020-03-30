import pygricola.variablesGlobales


def rVide():
    return {'b':0,'a':0,'p':0,'r':0,'n':0,'f':0,'c':0,'l':0,'m':0,'s':0,'v':0,'h':0}.copy()

def dummy():
    pass



# ~ listeReponse=["9","o","1","o","8","o","7","o","6","o"]
# ~ listeReponse=[]
# ~ listeReponse=["9","o","0","o","0","o","0","o","-1","o"]

idx=0





def customInput(msg):
    global idx
    normalInput=True
    try:
        variablesGlobales.listeReponse[idx]
        normalInput=False
    except:
        pass
    if normalInput:
        return input(msg)
    else:
        ret=variablesGlobales.listeReponse[idx]
        idx+=1
        return ret        
    
#dans certains cas, on ne veux pas que l'action soit annulable, par exemple 
#quand on veut savoir si on construit la deuxieme piece
def printPossibilities(message,possibilites,annulable=True):
    
    choixValide=False
    confirmation=False
    choix=-1
    while(not confirmation):
        while(not choixValide):
            
            for p in possibilites:
                
                if hasattr(p, 'nom'):
                    nom=p.nom
                else:
                    nom=p
                print("{} : {}".format(possibilites.index(p),nom))
            if annulable:
                print('a pour anuler:')     
            g = customInput(message+"   ") 
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
                print('Vous avez fait un choix invalide!! Recommencez')
        
        
        stri="Vous avez choisi {}\n Vous confirmez?(o/n)   ".format(possibilites[choix])
        conf = customInput(stri) 
        if(conf=='o'):
            confirmation=True
        elif conf=='n':
            choixValide=False
        else:
            print('Vous avez fait un choix invalide (il faut "o" ou "n"!! Recommencez')
        
    return choix 

