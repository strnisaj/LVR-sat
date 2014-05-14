# Primeri uporabe
# -*- encoding: utf-8 -*-
from time import *
from Izjave import *
from Sudoku import *
from Hadamard import *
from CNF import *
from DPLL import *

# Primer uporabe za Izjave
def primerIzjave():
   a = Var('A')
   b = Var('B')
   c = Var('C')

   #primer za OR
   or1 = Or([a,b,c]);
   or2 = Or([a, Or([a,b]),b,Or([b,c])]);

   #primer za AND
   and1 = And([a,b,c]);
   and2 = And([a,b,And([a,c])]);

   #primer za NOT
   not1 = Not(a);
   not2 = Not(or2);
   not3 = Not(and2);

   #primeri za NNF
   nnf1 = not2.poenostavi();
   nnf2 = not3.poenostavi();

   #primer za CNF
   izjava1 = Not(And([Or([Not(a),b]),Not(And([c,a])),Not(Or([Not(b),a,Not(c)]))]))
   cnf1 = CNF(izjava1)

   #primeri za izracun
   #za izracun nastavimo spremenljivkam vrednosti
   val = {'A':False,'B':True,'C':True}   
   #izracun izjave, ki ni poenostavljena
   izracun1 = izjava1.izracun(val)
   #izracun poenostavljene izjave
   izracun2 = izjava1.poenostavi().izracun(val)

   #izpis
   print('Primer za OR: ',or2)
   print('Primer za AND: ',and2)
   print('Primer za NNF: ',nnf2)
   print('Primer za CNF: ',cnf1)
   print('Primer za izracun - izjava: ', izjava1)
   print('Primer za izracun: ', izracun1)
   print('Primer za izracun poenostavljene izjave: ', izracun2)
   
	
# Primer uporabe za Sudoku
def primerSudoku():
    # Sudoku podamo kot dvodimenzionalno tabelo (nxn) stevil. Podana tabela vsebuje stevila od 0 do 9,
    # kjer 0 oznacuje prazno (se nereseno) polje sudokuja.
    # Lazji primer za sudoku
    t0 = time.clock()
    a = sudoku([[1,2,0,0],[3,0,1,0],[0,1,0,3],[0,0,2,1]])
    t1 = time.clock() - t0
    print('Sudoku a: ', a)
    print('Cas za sudoku a: ', t1)
    # Malo tezji primer za sudoku
    t0 = time.clock()
    b = sudoku([[5,3,0,0,7,0,0,0,0],[6,0,0,1,9,5,0,0,0],[0,9,8,0,0,0,0,6,0],[8,0,0,0,6,0,0,0,3],[4,0,0,8,0,3,0,0,1],[7,0,0,0,2,0,0,0,6],[0,6,0,0,0,0,2,8,0],[0,0,0,4,1,9,0,0,5],[0,0,0,0,8,0,0,7,9]])
    t1 = time.clock() - t0
    print('Sudoku b: ',b)
    print('Cas za sudoku b: ')
    c = b.poenostavi();
    print('Poenostavljena izjava za sudoku b: ', c)
   
# Primer uporabe za Hadamardove matrike
def primerHadamard():
    #Hadamardovo matriko podamo kot dvodimenzionalno tabelo sestavljeno iz 1 in -1.
    # Lazji primer za Hadamardovo matriko
    t0 = time.clock()
    a = hadamard([[1,1],[-1,1]])
    t1 = time.clock() - t0
    print('Cas za Hadamardovo matriko a: ',t1)
    # Malo tezji primer za Hadamardovo matriko
    t0 = time.clock()
    b = hadamard([[1,1,1,1],[-1,1,-1,1],[-1,-1,1,1],[1,-1,-1,-1]])
    t1 = time.clock() - t0
    print('Izjava za Hadamardovo matriko b: ', b)
    print('Cas za Hadamardovo matriko b: ', t1);
    c = CNF(b)
    print('Izjava za Hadamardovo matriko v CNF obliki: ', c)

# Primer uporabe za DPLL algoritem
def primerDPLL():
    y = Var('y')
	q = Var('q')
	z = Var('z')
	x = Var('x')
	izjava1 = And([Or([y, Not(q)]), Or([y, Not(z)]), Or([x, Not(y)]), Or([y,z,q]), Or([x,Not(z)]), Or([x,Not(q)])])
	print('1. Izjava: ', izjava1)
	t0 = time.clock()
	a = DPLL(izjava1)
	t01 = time.clock() - t0
	print('Cas za resevanje izjave z DPLL: ', t01)
	izjava2 = sudoku([[5,3,0,0,7,0,0,0,0],[6,0,0,1,9,5,0,0,0],[0,9,8,0,0,0,0,6,0],[8,0,0,0,6,0,0,0,3],[4,0,0,8,0,3,0,0,1],[7,0,0,0,2,0,0,0,6],[0,6,0,0,0,0,2,8,0],[0,0,0,4,1,9,0,0,5],[0,0,0,0,8,0,0,7,9]])
	print('2. Sudoku: ')
	t1 = time.clock()
	b = DPLL(izjava2)
	t11 = time.clock() - t1
	print('Cas za resevanje sudoku z DPLL: ', t11)
	
print('IZJAVE')
primerIzjave()
print('SUDOKU')
primerSudoku()
print('HADAMARD')
primerHadamard()
print('DPLL')
primerDPLL()
	