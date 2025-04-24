from getcrossdata import get_table
from validate import testconfig
from itertools import product
allchars=set("0123456789+-/*=")

class Unknownmanager:
    """Manages the information about unknowns and simplifies acquiring the data in different 
    """
    def __init__(self):
        """Initializes the UnknownManager with an empty position dictionary."""
        self.pos={}
    def getallequations(self):
        """Get all equations in the problem

        Returns:
            list[list[str]]: list of equations, each being a list of characters 
        """
        eqs=[]
        for (i,j),val in self.pos.items():
            for eqtest in val["equations"]:
                if eqtest not in eqs:
                    eqs.append(eqtest)
        return eqs
    def getpositions(self,equation):
        """Get the positions of all variables present in a given equation

        Args:
            equation (list[str]): equation represented by a list of characters 

        Returns:
            list[tuple[int,int]]: list of positions, each position being a tuple of two integers
        """
        positions=[]
        for (i,j),val in self.pos.items():
            if ((i,j) not in positions) and (any(eqtest==equation for eqtest in val["equations"])):
                positions.append((i,j))
        return positions
                


def getunknows():
    """extract unknown variables from get_table() using Unknownmanager and return it as well as the table

    Returns:
        tuple[list,Unknownmanager]: table:L*l list of strings and unknown variables info :Unknownmanager
    """
    tab=get_table()
    L=len(tab)
    l=len(tab[0])
    unknowns=Unknownmanager()
    for i in range(L):
        for j in range(l):
            if tab[i][j]=="?":
                eqs=[]
                eq=[tab[i][j]]
                for iplus in range(1,L-i):
                    if tab[i+iplus][j]!="■":
                        eq.append(tab[i+iplus][j])
                    else:
                        break
                for iminus in range(1,i+1):
                    if tab[i-iminus][j]!="■":
                        eq.insert(0,tab[i-iminus][j])
                    else:
                        break
                
                if len(eq)>2:
                    eqs.append(eq)
                eq=[tab[i][j]]
                for jplus in range(1,l-j):
                    if tab[i][j+jplus]!="■":
                        eq.append(tab[i][j+jplus])
                    else:
                        break
                for jminus in range(1,j+1):
                    if tab[i][j-jminus]!="■":
                        eq.insert(0,tab[i][j-jminus])
                    else:
                        break

                if len(eq)>2:
                    eqs.append(eq)
                unknowns.pos[(i,j)]={"possibilities":allchars,"equations":eqs}
    return tab,unknowns

def reducepossibilities(unknowns:Unknownmanager): 
    """reduce number of possibilities of each unknown by only keeping those present in valid equations

    Args:
        unknowns (Unknownmanager): unknown variables info 

    Returns:
        unknowns (Unknownmanager): unknown variables info with less (or equal) number of possible configurations than at the start
    """
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
    """sum together the number of possibilities. 
    If equal to the number of unknowns then that means the puzzle has been solved

    Args:
        unknowns (_type_): unknown variables info

    Returns:
        int: number of possible configurations
    """
    return sum(len(unknowns.pos[(i,j)]["possibilities"]) for (i,j),val in unknowns.pos.items())


    
