LVR-sat
=======

Prevajanje na SAT
=================

Ta modul vsebuje ogrodje za delo z logičnimi izrazi (datoteka Izjave.py), primera prevedbe znanih problemov (Hadamardove matrike in sudoku) na SAT ter testno okolje (datoteka Primeri.py).

Datoteke
========

V modulu se nahajajo datoteke:
+ <b>CNF.py</b> (metode za pretvarjanje izrazov v konjuktivno normalno obliko)
+ <b>Hadamard.py</b> (prevedba Hadamardove matrike na SAT problem)
+ <b>Izjave.py</b> (osnovno ogrodje za delo z logičnimi izrazi)
+ <b>Primeri.py</b> (testno okolje)
+ <b>Sudoku.py</b> (prevedba sudoku na SAT problem)

Uporaba
=======

CNF
---
CNF.py datoteka vsebuje le funkcijo <b>CNF(p)</b>, kjer je p izjava, katero želimo prevesti v CNF obliko. 

Hadamard
--------
Hadamard.py je sestavljen iz dveh funkcij in sicer <b>stetje(m, sez)</b> in <b>hadamard(sez)</b>.
Funkcija <b>stetje</b> sprejme seznam izjav sez in število m, vrne pa izjavo, ki je resnična natanko tedaj, ko je v seznamu izjav sez resničnih natanko m izjav.
<b>Hadamard</b> funkcija pa sprejme nxn matriko in vrne izjavo, ki je resnična natanko tedaj, ko je matrika Hadamardova.

Izjave
------
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

Sudoku
------
Sudoku.py vsebuje fukncijo <b>sudoku(sez)</b>. Ta sprejme dvodimenzionalno tabelo (nxn matrika), ki predstavlja nerešen sudoku. Kot rezultat nam vrne izjavo, ki je resnična natanko tedaj, ko za dani sudoku obstaja rešitev.

Primeri
-------
Tu se nahajajo testi za Izjave.py, Hadamard.py, Sudoku.py in CNF.py.
