#LVR-sat

LVR-sat vsebuje tri module: CNF, DPLL in Prevajanje na SAT. Od teh je glaven DPLL, ki je predstavljen v nadaljevanju tega dokumenta. 

##DPLL

Ta modul vsebuje ogrodje za delo z logičnimi izrazi (datoteka Izjave.py), primera prevedbe znanih problemov (Hadamardove matrike in sudoku) na SAT, SAT solverja (DPLL.py) ter primere uporabe (datoteka Primeri.py).

##Datoteke

V modulu se nahajajo datoteke:
+ <b>CNF.py</b> (metode za pretvarjanje izrazov v konjuktivno normalno obliko)
+ <b>Hadamard.py</b> (prevedba Hadamardove matrike na SAT problem)
+ <b>Izjave.py</b> (osnovno ogrodje za delo z logičnimi izrazi)
+ <b>Primeri.py</b> (primeri uporabe)
+ <b>Sudoku.py</b> (prevedba sudoku na SAT problem)
+ <b>DPLL.py</b> (SAT solver - DPLL algoritem)

##Uporaba
###Testno okolje
Za testiranje delovanja funkcij, so v vsaki datoteki temu namenjene metode.

###CNF

CNF.py datoteka vsebuje le funkcijo <b>CNF(p)</b>, kjer je p izjava, katero želimo prevesti v CNF obliko. 

V datoteki se nahaja tudi funkcija <b>test()</b>, ki testira delovanje CNF. Poženemo jo iz konzole.
Beležimo tudi čas izvajanja funkcije <b>CNF</b>.

###Hadamard

Hadamard.py je sestavljen iz dveh funkcij in sicer <b>stetje(m, sez)</b> in <b>hadamard(n)</b>.
Funkcija <b>stetje</b> sprejme seznam izjav sez in število m, vrne pa izjavo, ki je resnična natanko tedaj, ko je v seznamu izjav sez resničnih natanko m izjav.
<b>Hadamard</b> funkcija pa sprejme velikost matrike in vrne izjavo, ki je resnična natanko tedaj, ko je matrika Hadamardova.

Testiranje delovanje je izvedeno s pomočjo funkcij <b>testS()</b>, ki testira delovanje funkcije <b>stetje</b>, ter <b>testH()</b>, ki testira delovanje funkcije <b>hadamard</b>. Obe kličemo iz konzole.
<b>testH</b> beleži še hitrost delovanja za primer sestavljanja izjave za hadamardovo matriko in za primer sestavljanja izjave za hadamardovo matriko v CNF obliki, beleži se tudi razlika v hitrosti izvajanja med obema.

Opomba: Izvajanje programa za Hadamardovo matriko velikosti 4x4 je nekoliko počasnejše, zato prosimo za potrpežljivost.

###Izjave

Izjave.py datoteka je sestavljena iz sledečih razredov:
+ <b>Var()</b> (predstavlja spremenljivke)
+ <b>Tru()</b> (predstavlja konstanto True)
+ <b>Fal()</b> (predstavlja konstanto False)
+ <b>And()</b> (predstavlja logični veznik And)
+ <b>Or()</b> (predstavlja logični veznik Or)
+ <b>Not()</b> (predstavlja negacijo)

Vsak razred (razen <b>Tru()</b> in <b>Fal()</b>) vsebuje funkcije:
+ <b>vrni</b> (vrne objekt) 
+ <b>nastavi</b> (nastavimo vrednosti objektu; npr. v razredu <b>Var()</b> nastavimo ime spremenljivke)
+ <b>izracun</b> (sprejme slovar vrednosti spremenljivk (npr. {'A':False,'B':True,'C':True}) in vrne valuirano izjavo)
+ <b>poenostavi</b> (potisne vse negacije do spremenljivk, odstrani morebitne pojavitve <b>Tru()</b>, <b>Fal()</b> in odvečne oklepaje)

Razreda <b>Tru()</b> in <b>Fal()</b> vsebujeta le funkcijo <b>izracun</b>.

Izjave.py vsebujejo funkcijo za testiranje <b>test()</b>. V testu izvajamo poenostavljanje, računanje vrednosti izjave ter izpis nastopajočih spremenljivk. Za poenostavljanje in računanje vrednosti beležimo še čas izvajanja.

###Sudoku

Sudoku.py vsebuje fukncijo <b>sudoku(sez)</b>. Ta sprejme dvodimenzionalno tabelo (nxn matrika), ki predstavlja nerešen sudoku. Kot rezultat nam vrne izjavo, ki je resnična natanko tedaj, ko za dani sudoku obstaja rešitev.

Poleg <b>sudoku</b> funkcije vsebuje še <b>testS()</b>, s katero lahko testiramo delovanje. Beleži se tudi čas izvajanja za reševanje sudoku problema (sestavljanje izjave za sudoku), sestavljanje izjave v CNF obliki in razlika v hitrosti delovanja obeh.

###DPLL
Algoritem [DPLL](http://en.wikipedia.org/wiki/DPLL_algorithm) vsebuje glavne funkcije <b>pozdravnaMetoda()</b>, ki nam razloži način klica DPLL algoritma in primere klicev. Algoritem DPLL sicer kličemo z ukazom "DPLL(izjava)", kjer je izjava sestavljena iz And, Or in Not operatorjev in se sklada s terminologijo v datoteki Izjave.py.

Testni primeri se nahajajo v funkciji <b>getTestIzjava(N)</b>, kjer je N številka testnega primera in lahko zavzema vrednosti med 0 in 10.

###Primeri

Tu se nahajajo primeri uporabe za Izjave.py, Hadamard.py, Sudoku.py, CNF.py in DPLL.py. Ob zagonu datoteke, se izvedejo primeri uporabe za Izjave (primeri za And, Or, Not, CNF in NNF), Sudoku (primer za sudoku velikosti 4x4 in 9x9), Hadamardovo matriko (primer za velikost 2 in 4) ter DPLL (primer za neko izjavo, 9x9 sudoku, 2x2 in 4x4 Hadamardovo matriko). Za sudoku, Hadamardove matrike in DPLL se beleži še čas izvajanja programa.
