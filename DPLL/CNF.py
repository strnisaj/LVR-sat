import Izjave

def CNF(p):
    p = p.poenostavi()
    if type(p) is Izjave.Var or type(p) is Izjave.Tru or type(p) is Izjave.Fal or type(p) is Izjave.Not:
        return p
    if type(p) is Izjave.And:
        return Izjave.And([CNF(i) for i in p.vrni()])
    if type(p) is Izjave.Or:
        izjave = p.vrni()
        if len(izjave) == 1:
            return CNF(izjave[0])
        else:
            i = 0
            while i<len(izjave):                  
                if type(izjave[i]) is Izjave.And:
                    sez = []
                    if i == 0:
                        for j in izjave[i].vrni():
                            sez.append(Izjave.Or([j,izjave[i+1]]))
                        return CNF(Izjave.Or([Izjave.And(sez)]+izjave[2:]))
                    else:
                        for j in izjave[i].vrni():
                            sez.append(Izjave.Or([izjave[i-1],j]))
                        return CNF(Izjave.Or(izjave[:i-1]+[Izjave.And(sez)]+izjave[i+1:]))
                if type(izjave[i]) is Izjave.Or:
                    return CNF(Izjave.Or(izjave[:i]+izjave[i].vrni()+izjave[i+1:]))
        
                i+=1
            return p
                

def test():
    a = Izjave.Var('A')
    b = Izjave.Var('B')
    c = Izjave.Var('C')
    d = Izjave.Var('D')
    val = {'A':True,'B':False,'C':True,'D':False}
    iz = Izjave.Or([Izjave.And([a,b]),Izjave.And([c,d]),d])
    iz1 = Izjave.Not(Izjave.And([Izjave.Or([Izjave.Not(a),b]),c]))
    iz2 = Izjave.Or([Izjave.Or([a,Izjave.And([c,d])]),d])
    return iz

    
                   

