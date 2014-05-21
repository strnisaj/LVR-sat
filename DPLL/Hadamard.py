from Izjave import *
from CNF import *
from time import *

# Funkcija dobi seznam izjav in stevilo m, vrne pa izjavo, ki je resnicna natanko tedaj,
# ko je v seznamu natanko m izjav resnicnih.
def stetje(m,sez):
    k = len(sez)
    if k == 1 and m == 0:
        return Not(sez[0])
    elif k == 1 and  m == 1:
        return sez[0]
    elif m == 0:
        return And([stetje(0,sez[:k-1]),Not(sez[k-1])])
    else:
        if k == m:
            return And([sez[k-1],stetje(m-1,sez[:k-1])])
        else:
            return Or([And([sez[k-1],stetje(m-1,sez[:k-1])]),And([Not(sez[k-1]),stetje(m,sez[:k-1])])])

#Funkcija potenca2 preveri, ce je podano stevilo potenca stevila 2
def potenca2(n):
	tmp = 2
	while tmp < n:
		tmp = tmp * 2
	return tmp == n
			
# Funkcija sprejme seznam seznamov, ki predstavlja n x n matriko (podseznami predstavljajo vrstice v matriki)
# in vrne izjavo, ki je resnicna, natanko tedaj, ko je matrika Hadamardova.
def hadamard(n):
    if not potenca2(n):
        print('Podana velikost matrike mora biti potenca stevila 2!')
        return n
    spremen = []
    for i in range(n):
        spremen.append([])
        for j in range(n):
            spremen[i].append([])
            spremen[i][j].append(Var('X({0},{1},{2})'.format(i,j,1)))
            spremen[i][j].append(Var('X({0},{1},{2})'.format(i,j,-1)))
    
    # Sestavimo izjavo: "Na vsakem mestu v matriki je bodisi 1 bodisi -1
    seznam1 = []
    for i in range(n):
        for j in range(n):
            seznam1.append(Or([spremen[i][j][0],spremen[i][j][1]]))
    izjava1 = And(seznam1)

    #Sestavimo izjavo: "Poljubni dve vrstici se strinjata na polovici mest "
    seznam2 = []
    for i in range(n-1):
        for s in range(i+1,n):
            seznam21 = []
            for j in range(n):
                seznam21.append(Or([And([spremen[i][j][0],spremen[s][j][0]]),And([spremen[i][j][1],spremen[s][j][1]])]))
            seznam2.append(stetje(n/2,seznam21))
    izjava2 = And(seznam2)
    
    return And([izjava1,izjava2])
    
# Test za hadamard()
def testH():
    a = hadamard([[1,1,1,1],[-1,1,-1,1],[-1,-1,1,1],[1,-1,-1,-1]])
    print('1. Izjava za Hadamardovo matriko:')
    t0 = time.clock()
    b = hadamard([[1,1],[-1,1]])
    t01 = time.clock() - t0
    print('Pretekel cas: ', t01)
    print(b)
    print('2. Izjava za Hadamardovo matriko v CNF obliki:')
    t1 = time.clock()
    c = CNF(hadamard([[1,1],[-1,1]]))
    t11 = time.clock() - t1
    print('Pretekel cas: ', t11)
    print('Razlika med 1. in 2.: ', t01 - t11)
	#print(CNF.CNF(b).poenostavi())

#  Test za stetje()
def testS():
    a = Var('A')
    b = Var('B')
    c = Var('C')
    iz1 = And([a,c])
    iz2 = Or([Not(a),b])
    iz3 = Not(And([b,c]))
    sez = [iz1,iz2,iz3]
    print(sez)
    print([i.izracun({'A':True,'B':False,'C':True}) for i in sez])
    print(stetje(2,sez))
    print(stetje(2,sez).izracun({'A':True,'B':False,'C':True}))

# Preveri, ce je izjava resnicna natanko tedaj, ko je dana matrika h res hadamardova.
def valuacija():
    #h = [[1,1],[1,-1]]
    h = 2
    had = hadamard(h)
    hadCNF = CNF(had)
    hadCNFp = hadCNF.poenostavi()
    spremen = had.var()
    val = {}
    for x in spremen:
        ime = x.vrni_ime()
        i = int(ime[2])
        j = int(ime[4])
        if len(ime) == 9:
            n = int(ime[6]+ime[7])
        else:
            n = int(ime[6])
        if h[i][j]==n:
            val[x]= True
        else:
            val[x]= False
    print(had.izracun(val))
    print(hadCNF.izracun(val))
    print(hadCNFp.izracun(val))
