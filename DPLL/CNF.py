from Izjave import *
from time import *

# CNF(p) sprejme izjavo p in jo preoblikuje v CNF obliko.
def CNF(p):
    p = p.poenostavi()
    if type(p) is Var or type(p) is Tru or type(p) is Fal or type(p) is Not:
        return p
    if type(p) is And:
        return And([CNF(i) for i in p.vrni()])
    if type(p) is Or:
        izjave = p.vrni()
        if len(izjave) == 1:
            return CNF(izjave[0])
        else:
            i = 0
            while i < len(izjave):                  
                if type(izjave[i]) is And:
                    sez = []
                    if i == 0:
                        for j in izjave[i].vrni():
                            sez.append(Or([j,izjave[i+1]]))
                        return CNF(Or([And(sez)]+izjave[2:]))
                    else:
                        for j in izjave[i].vrni():
                            sez.append(Or([izjave[i-1],j]))
                        return CNF(Or(izjave[:i-1]+[And(sez)]+izjave[i+1:]))
                if type(izjave[i]) is Or:
                    return CNF(Or(izjave[:i]+izjave[i].vrni()+izjave[i+1:]))
                i+=1
            return p

# testni primeri:
#	izbiramo lahko med 4 izjavami: iz, iz1, iz2 in izjava
def test():
    a = izjave.var('a')
    b = izjave.var('b')
    c = izjave.var('c')
    d = izjave.var('d')
    # val = {'A':True,'B':False,'C':True,'D':False}
    # iz = Izjave.Or([Izjave.And([a,b]),Izjave.And([c,d]),d])
    # iz1 = Izjave.Not(Izjave.And([Izjave.Or([Izjave.Not(a),b]),c]))
    # iz2 = Izjave.Or([Izjave.Or([a,Izjave.And([c,d])]),d])
    izjava = Not(And([Or([Not(a),b]),Not(And([c,a])),Not(Or([Not(b),a,Not(c)]))]))
    print('Izjava: ', izjava)
    t0 = time.clock()
    izcnf = CNF(izjava)
    t01 = time.clock() - t0
    print('Izjava v CNF obliki: ', izcnf)
    print('Pretekel cas: ', t01)
