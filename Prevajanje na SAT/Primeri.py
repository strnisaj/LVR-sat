# Primeri uporabe
# -*- encoding: utf-8 -*-

from Izjave import *
from Sudoku import *
from Hadamard import *
from CNF import *

# Testi za Izjave
def testIzjave1():
   a = Var('A')
   b = Var('B')
   c = Var('C')
   iz = Not(And([Or([Not(a),b]),Not(And([c,a])),Not(Or([Not(b),a,Not(c)]))]))
   val = {'A':False,'B':True,'C':True}
   print('valuacija spremenljivk: ',str(val))
   print('izjava: ',iz)
   print('poenostavljena izjava: ',iz.poenostavi())
   print('vrednost izjave: ',iz.izracun(val))
   print('vrednost poenostavljene izjave: ',iz.poenostavi().izracun(val))
   
def testIzjave2():
    a = Var('A')
    c = Var('C')
    b = Var('B')
    iz = And([a,b,Not(c)])
    val = {'A':True,'B':True}
    print(iz.izracun(val))
	
# Test za Sudoku
def testSudoku():
   a = sudoku([[1,2,0,0],[3,0,1,0],[0,1,0,3],[0,0,2,1]])
   print(a)
   
# Testi za Hadamardove matrike
"""def testHadamardStetje():
    a = Izjave.Var('A')
    b = Izjave.Var('B')
    c = Izjave.Var('C')
    iz1 = Izjave.And([a,c])
    iz2 = Izjave.Or([Izjave.Not(a),b])
    iz3 = Izjave.Not(Izjave.And([b,c]))
    sez = [iz1,iz2,iz3]
    print(sez)
    print([i.izracun({'A':True,'B':False,'C':True}) for i in sez])
    print(stetje(2,sez))
    print(stetje(2,sez).izracun({'A':True,'B':False,'C':True}))"""

def testHadamard():
    a = hadamard([[1,1,1,1],[-1,1,-1,1],[-1,-1,1,1],[1,-1,-1,-1]])
    b = hadamard([[1,1],[-1,1]])
    print('Izjava za Hadamardovo matriko:')
    print(b)
    print('Izjava za Hadamardovo matriko v CNF obliki:')
    print(CNF.CNF(b).poenostavi())
	
# Test za CNF
def testCNF():
    a = Izjave.Var('A')
    b = Izjave.Var('B')
    c = Izjave.Var('C')
    d = Izjave.Var('D')
    val = {'A':True,'B':False,'C':True,'D':False}
    iz = Izjave.Or([Izjave.And([a,b]),Izjave.And([c,d]),d])
    iz1 = Izjave.Not(Izjave.And([Izjave.Or([Izjave.Not(a),b]),c]))
    iz2 = Izjave.Or([Izjave.Or([a,Izjave.And([c,d])]),d])
    return iz