import sys


def dummy():
    pass

#f1 = sys.stdin

# useAnswerFile=True
# if useAnswerFile:
#     f = open('input.txt','r')
#     sys.stdin = f

listeReponse=["9","o","1","o","8","o","7","o","6","o"]
idx=0

def customInput(msg):
    global idx
    global listeReponse
    normalInput=True
    try:
        listeReponse[idx]
        normalInput=False
    except:
        pass
    if normalInput:
        return input(msg)
    else:
        ret=listeReponse[idx]
        idx+=1
        return ret        
    

def printPossibilities(message,possibilites):
    
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
                print(possibilites.index(p),": ",p)
            print('a pour anuler:')     
            g = customInput(message+"   ") 
            try:
                if g=='a':
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

