
materiaux=['bois','argile','pierre','roseau','pn','feu']
plantes=['cereale','legume']
animaux=['mouton','sanglier','boeuf','cheval']


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
# class Ressource(object):
# 
#     def __init__(self, nom,description):
#         self.nom = nom
#         self.description = description
#         super().__init__()
#         
# class Materiau(Ressource):
# 
#     def __init__(self, nom,description):
#         super().__init__(nom,description)
#         
# 
# class Plante(Ressource):
# 
#     def __init__(self, nom,description):
#         super().__init__(nom,description)
#         
#         
# class Animal(Ressource):
# 
#     def __init__(self, nom,description):
#         super().__init__(nom,description)
#         

def jouable(a,b,dbg=False):
    #true if a>=b
    #valable pour cout et condition
    res=True
    
    for k in a.keys():
        if k in b.keys():
            if (b[k]>0):
                if a[k]<b[k]:
                    if (dbg):
                        print(k,a[k],b[k])
                    res=False
                    break
    return res
        