from getcrossdata import get_table,print_table
from validate import testconfig
from itertools import product
allchars=set("0123456789+-/*=")

class unknown:
    def __init__(self):
        self.pos={}
    def getallequations(self):
        eqs=[]
        for (i,j),val in self.pos.items():
            for eqtest in val["equations"]:
                if eqtest not in eqs:
                    eqs.append(eqtest)
        return eqs
    def getpositions(self,equation):
        positions=[]
        for (i,j),val in self.pos.items():
            if ((i,j) not in positions) and (any(eqtest==equation for eqtest in val["equations"])):
                #print((i,j),val,"\n",[eqtest for eqtest in val["equations"] if eqtest==equation],"\n\n" )
                positions.append((i,j))
        return positions
                


def getunknows():
    tab=get_table()
    L=len(tab)
    l=len(tab[0])
    unknowns=unknown()
    for i in range(L):
        for j in range(l):
            if tab[i][j]=="?":
                eqs=[]
                eq=[tab[i][j]]
                for iplus in range(1,L-i):
                    if tab[i+iplus][j]!="X":
                        eq.append(tab[i+iplus][j])
                    else:
                        break
                for iminus in range(1,i+1):
                    if tab[i-iminus][j]!="X":
                        eq.insert(0,tab[i-iminus][j])
                    else:
                        break
                
                if len(eq)>2:
                    eqs.append(eq)
                eq=[tab[i][j]]
                for jplus in range(1,l-j):
                    if tab[i][j+jplus]!="X":
                        eq.append(tab[i][j+jplus])
                    else:
                        break
                for jminus in range(1,j+1):
                    if tab[i][j-jminus]!="X":
                        eq.insert(0,tab[i][j-jminus])
                    else:
                        break

                if len(eq)>2:
                    eqs.append(eq)
                unknowns.pos[(i,j)]={"possibilities":allchars,"equations":eqs}
    return tab,unknowns

def reducepossibilities(unknowns:unknown):    
    for ei,eq in enumerate(unknowns.getallequations()):
        I=[(i,j) for (i,j) in unknowns.getpositions(eq)]
        X=tuple(unknowns.pos[(i,j)]["possibilities"] for (i,j) in I)
        possibilities=[[] for _ in range(len(I))]
        for XO in product(*X):
            if testconfig(eq,XO):
                for xi,(i,j) in enumerate(I):
                    possibilities[xi].append(XO[xi])
        
        for indij,(i,j) in enumerate(I):
            unknowns.pos[(i,j)]["possibilities"]=set(possibilities[indij])

    return unknowns

def getNpossibilties(unknowns):
    return sum(len(unknowns.pos[(i,j)]["possibilities"]) for (i,j),val in unknowns.pos.items())


    
