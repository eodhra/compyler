import Types as Tp
from Dyad import Dyad

def lex2dyads(leces):
    dyads = []
    for l in leces:
        if l[0] in Tp.relopList:
            d = Dyad(Tp.RELOP, l[0])
        elif l[0] in Tp.errorList:
            d = Dyad(l[0], l[1])
        elif l[0] == Tp.ID or l[0] == Tp.VALUE:
            d = Dyad(l[0], int(l[1]))
        else:
            d = Dyad(l[0], None)
        dyads.append(d)
    return dyads