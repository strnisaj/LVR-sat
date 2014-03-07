import Izjave

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
