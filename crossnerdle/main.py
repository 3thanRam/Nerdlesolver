from getcrossdata import print_table
from getconfigs import getunknows,reducepossibilities,getNpossibilties


def main():
    table,unknowns=getunknows()
    
    Nvars=len(unknowns.pos.items())
    possibilities=None
    lastpossibilities=None 
    count=0   
    while (lastpossibilities!=Nvars):
        unknowns=reducepossibilities(unknowns)
        possibilities=getNpossibilties(unknowns)
        if (possibilities==lastpossibilities) or (count>10**3):
            break
        lastpossibilities=getNpossibilties(unknowns)
        count+=1
    print(f"Niter:{count}")
    print_table(table,unknowns)

if __name__ == '__main__': 
    main()