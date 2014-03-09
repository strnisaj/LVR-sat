import Izjave

# funkcija vrne izjavo, ki je resnièna natanko tedaj ko je v seznamu sez m izjav
# resniènih. stevilo k mora biti enako dolžini seznama sez.
def stetje(k,m,sez):
    n = len(sez)-1
    if k == 1 and m == 0:
        return Izjave.Not(sez[0])
    elif k == 1 and  m == 1:
        return sez[0]
    elif m == 0:
        return Izjave.And([stetje(k-1,0,sez[:n]),Izjave.Not(sez[k-1])])
    else:
        if k == m:
            return Izjave.And([sez[k-1],stetje(k-1,m-1,sez[:n])])
        else:
            return Izjave.Or([Izjave.And([sez[k-1],stetje(k-1,m-1,sez[:n])]),Izjave.And([Izjave.Not(sez[k-1]),stetje(k-1,m,sez[:n])])])

def hadamard(sez):
    n = len(sez)
    spremen = []
    for i in range(n):
        spremen.append([])
        for j in range(n):
            spremen[i].append([])
            spremen[i][j].append(Izjave.Var('X({0},{1},{2})'.format(i,j,1)))
            spremen[i][j].append(Izjave.Var('X({0},{1},{2})'.format(i,j,-1)))

    seznam1 = []
    for i in range(n):
        for j in range(n):
            seznam1.append(Izjave.Or([spremen[i][j][0],spremen[i][j][1]]))
    izjava1 = Izjave.And(seznam1)
    return izjava1

def test():
    a = Izjave.Var('A',True)
    b = Izjave.Var('B',False)
    c = Izjave.Var('C',False)
    iz1 = Izjave.And([a,c])
    iz2 = Izjave.Or([Izjave.Not(a),b])
    iz3 = Izjave.Not(Izjave.And([b,c]))
    sez = [iz1,iz2,iz3]
    print(sez)
    print([i.izracun() for i in sez])
    print(stetje(3,2,sez))
    print(stetje(3,2,sez).izracun())






    
