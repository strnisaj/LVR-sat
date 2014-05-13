from Izjave import *
from Sudoku import *
from Hadamard import *
from CNF import *
import time

newPureValFound = True
solutionVals = {}
lockSolutionVals = False

def DPLL(izjava):

    # poresetiram prejšno rešitev
    global solutionVals
    global lockSolutionVals
    solutionVals = {}
    lockSolutionVals = False

    startTime = time.time()

    izjava = CNF(izjava)
    izjava = izjava.poenostavi().vrni()     #dobim [ ... (...) ...]
    izjava = get_2D_list(izjava)            #dobim [ ... [...] ...]
    print('Izjava: ', izjava)

    izjava = removeTrueSantences(izjava)
    izjava = sortByLength(izjava)
    varValues = {}                          # Začetne vrednosti spremenljivk
    solution = rec_DPLL(izjava, varValues) # Klic rekurzivne metode
    print('Vrnjena rešitev: ', solution)
    print('Vrednosti: ' , solutionVals)

    endTime = time.time()
    timePassed = endTime - startTime
    print('Time: ', timePassed)

def rec_DPLL(izjava, varValues):

    # Metoda najprej preveri, če je kakšna spremenljivka čista. Nato poenostavi izjavo in naredi dve kopiji izjave
    # Vzame se prva spremenljivka iz izjave in se nastavi na True. Sprocesira se kopija_1 izjave z novo vrednostjo spremenljivke True
    # Vzame se prva spremenljivka iz izjave in se nastavi na False. Sprocesira se kopija_2 izjave z novo vrednostjo spremenljivke False


    # Če smo dobili že rešitev, potem ne potrebujemo več preverjanja
    global lockSolutionVals
    if lockSolutionVals == True:
        return True

    # Spodnja while zanka pridobiva čiste spremenljivke, poenostavlja izjavo in to ponavalja, dokler je kakšna spremenljivka čista
    # Če pride do protislovja v vrednostih, potem vrne False #zaenkrat še ne, ampak naj....
    global newPureValFound
    while (newPureValFound == True):
        pureVals = getPureVals(izjava)                  # pridobim slovar čistih spremenljivk
        varValues = concatDicts(varValues, pureVals)    # združim obstoječe spremenljivke s čistimi

        #preverimo, da nismo prišli do protislovja:
        if varValues == False:
            return False
        izjava = processStatement(izjava, varValues)    # metoda odstrani OR-e, ki so True in spremenljivke znotraj OR-ov, ki so False

    # Preverimo, če smo prišli do rešitv=true
    if is_AND_empty(izjava):
        global solutionVals
        if lockSolutionVals == False:
            #print('NASTAVLJAM GLOBALNO REŠITEV')
            lockSolutionVals = True
            solutionVals = copyVarValues(varValues)
        return True

    # Preverimo, če smo prišli do rešitev=false
    if is_OR_empty(izjava):
        return False


    firstVar = getFirstVar(izjava)      # pridobimo prvo spremenljivko
    izjava_1 = copyStatement(izjava)    # prekopiramo izjavo
    izjava_2 = copyStatement(izjava)    # prekopiramo izjavo
    vals_1 = copyVarValues(varValues)   # prekopiramo vrednosti
    vals_2 = copyVarValues(varValues)   # prekopiramo vrednosti
    vals_1[firstVar] = True             # enkrat vrednost prve spremenljivke nastavimo na True
    vals_2[firstVar] = False            # enkrat vrednost prve spremenljivke nastavimo na False

    izjava_1 = processStatement(izjava_1, vals_1)
    izjava_2 = processStatement(izjava_2, vals_2)


    if (rec_DPLL(izjava_1, vals_1) != False):  # rekurzivni klic
        return True
    if (rec_DPLL(izjava_2, vals_2) != False):  # rekurzivni klic
        return True

    return False

def getFirstVar(izjava): 
    x = izjava[0][0].vrni()
    return x

def processStatement(izjava, vals):

    # Metoda prejme izjavo in vrednsoti spremenljik.
    # Metoda odstrani OR stavek, če je ta zaradi ene izmed sprmeenljivk že True
    # Metoda odstrani spremenljivko iz OR stavka, če je njena vrednost False
    # Kadar odstranimo spremenljivko iz OR stavka, preverimo, da OR ni prazen .... to bi lahko klicov uno drugo metodo
    # XXX: pazi, ker je razlika, ali odstraniš True spremenljivko iz OR stavka, ali odstraniš False spremenljivko iz Or stavka!!!!

    toBeRemoved_OR = []
    toBeRemoved_AND = []
    indexAND = -1

    for subIzjava in izjava:
        indexAND = indexAND + 1
        indexOR = -1
        toBeRemoved_OR = []
        #grem čez vse podizjave
        for i in subIzjava:
            indexOR = indexOR + 1
            if i.vrni() in vals:
                #print('i = ', i)
                vrednost = vals[i.vrni()]   #dobim vrednost shranjene spremenljivke
                #če je v podizjavi VAR
                if isinstance(i.poenostavi(), Var):
                    if vrednost == True:
                        toBeRemoved_AND.append(indexAND)
                        break
                    elif vrednost == False:
                        toBeRemoved_OR.append(indexOR)
                    else:
                        pass
                #če je v podizjavi NOT
                elif isinstance(i.poenostavi(), Not):
                    if vrednost == True:
                        toBeRemoved_OR.append(indexOR)
                    elif vrednost == False:
                        toBeRemoved_AND.append(indexAND)
                        break
                    else:
                        pass
                else:
                    pass
                    
            # če je kakšno spr. potrebno odstraniti iz OR-a, jo odstranim tukaj
            if len(toBeRemoved_OR) != 0:
                toBeRemoved_OR.reverse()
                for i in range(0, len(toBeRemoved_OR)):
                    del subIzjava[toBeRemoved_OR[i]]
            # preverim, če je prazn OR
            if len(subIzjava) == 0:
                #print('TODO: return FALSE')
                #return False
                pass
            
    # če je kakšen AND true, potem ga odstranimo iz izjava
    toBeRemoved_AND.reverse()
    for i in range(0, len(toBeRemoved_AND)):
        del izjava[toBeRemoved_AND[i]]

    return izjava

def copyStatement(izjava):

    # Metoda skopira izjavo in vrne njeno kopijo

    copy = []
    for subIzjava in izjava:
        subCopy = []
        for i in subIzjava:
            subCopy.append(i)
        copy.append(subCopy)

    return copy

def copyVarValues(varValues):

    # Metoda skopira vrednosti spremenljivk in vrne njihovo kopijo

    copy = {}
    for keys in varValues:
        copy[keys] = varValues[keys]

    return copy

def getPureVals(izjava):

    # Metoda se sprehodi čez izjavo in poišče čiste spremenljivke.
    # Metoda vrne slovar čistih spremenljivk, ki jih nastavi na true (x) oz. false (not x)

    pureVals = {}
    varsInStatement = {}
    global newPureValFound
    newPureValFound = False

    #napolnim slovar zastopanosti spremenljivk: 1: X .... 2: notX ..... 3: (X and notX)
    for subIzjava in izjava:
        for var in subIzjava:
            #če ni spremenljivke v seznamu, jo dodamo
            if (var.vrni() in varsInStatement) == False:
                if var.poenostavi() == var.vrni():
                    varsInStatement[var.vrni()] = 1
                else:
                    varsInStatement[var.vrni()] = 2
            #če je spremenljivka že v seznamu, preverimo katero vrednost ima
            else:
                vrednost = varsInStatement[var.vrni()]
                if var.poenostavi() == var.vrni() and vrednost == 2:
                    varsInStatement[var.vrni()] = 3
                elif var.poenostavi() != var.vrni() and vrednost == 1:
                    varsInStatement[var.vrni()] = 3
                else:
                    pass

    
    #ugotovimo, kate key-e je potrebno odstraniti
    keysToBeRemoved = []
    for key in varsInStatement:
        if (varsInStatement[key] == 3):
            keysToBeRemoved.append(key)

    #odstranimo key-e
    for i in keysToBeRemoved:
        varsInStatement.pop(i)

    #napolnimo slovar čistih spremenljivk
    for key in varsInStatement:
        newPureValFound = True
        if varsInStatement[key] == 1:
            pureVals[key] = True
        else:
            pureVals[key] = False

    return pureVals

def get_2D_list(izjava):

    # Metoda sprejme list oblike [ ... (...) ...] in vrne list oblike [ ... [] ...].
    # Proste spremenljivke so v listu dolzine 1
    
    allList = []
    subList = []

    # if preveri, da ni samo ene spremenljivke v izjavi znotraj ANDa
    if isinstance(izjava, Var) or isinstance(izjava, Not):
        subList.append(izjava)
        allList.append(subList)
        return allList
    
    for i in range(0, len(izjava)):
        subList = []
        if isinstance(izjava[i], Not) or isinstance(izjava[i], Var):
            subList.append(izjava[i])
        else:
            for var in izjava[i].vrni():
                subList.append(var)
        allList.append(subList)

    return allList
    
def is_AND_empty(izjava):

    # Metoda preveri, če je izjava = []. V tem primeru imamo rešitev in vrnemo True, sicer vrnemo False

    if len(izjava) == 0:
        return True
    else:
        return False

def is_OR_empty(izjava):

    # Metoda preveri, če je izjava = [ ... [] ... ].
    # Če je katerikoli OR prazen, potem ni rešitve in vrnemo True, sicer vrnemo False

    for subIzjava in izjava:
        if len(subIzjava) == 0:
            return True

    return False

def concatDicts(oldValues, newValues):

    # Metoda združi stare in nove spremenljivke v slovarjih
    # Metoda preme 2 slovarja starih in novi vrednosti spremenljivk in jih združi
    # Metoda vrne slovar združenih spremenljivk ali False, če jih ne more združiti (ker pride do protislovja)

    for key in newValues:
        #če je že vsebovan
        if key in oldValues:
            #če se stara in nova vrednost razlikujeta
            if oldValues[key] != newValues[key]:
                return False
        #če ni vsebovan, dodamo novo vrednost med stare vrednosti
        else:
            oldValues[key] = newValues[key]

    return oldValues

def removeSingleVars(izjava):

    # Metoda gre čez izjavo in iz nje odstrani vse 'proste' spremenljivke, ter jih nastavi na True
    # Metoda vrne spremenljeno izjavo in slovar prostih spremenljivk, ki so nastavljene na ustrezno vrednost
    # Metoda iz izjave izbriše te proste podizjave
    
    toBeRemoved = []
    singleVars = []

    #proste spremenljivke shranimo v singleVars in pridobimo indexe teh prostih spremenljivk, da jih bomo pobrisali iz izjave
    for i in range (0, len(izjava)):
        # če je samo ena spremenljivka v podizjavi
        if len(izjava[i]) == 1:
            singleVars.append(izjava[i][0])
            toBeRemoved.append(i)

    #odstranimo proste spremenljivke iz izjave
    toBeRemoved.reverse()
    for i in range(0, len(toBeRemoved)):
        del izjava[toBeRemoved[i]]

    # zgradimo dictionary prostih spremenljivk
    singleVarsDict = {}

    for i in singleVars:
        if isinstance(i, Var):
            singleVarsDict[i.vrni()] = True
        if isinstance(i, Not):
            singleVarsDict[i.vrni()] = False

    return [izjava, singleVarsDict]

def removeTrueSantences(izjava):

    # Metoda odstrani podizjave tipa (X or notX)

    toBeRemoved = [] #indexi podizjav, ki jih bomo odstranili
    indexCounter = -1
    
    for subIzjava in izjava:
        indexCounter = indexCounter + 1
        for i in range(0, len(subIzjava)-1):
            for j in range((i+1), len(subIzjava)):
                #preverim ali se zgodi (X or notX)
                if ( subIzjava[i].vrni() == subIzjava[j].vrni() ) and ( subIzjava[i].poenostavi() != subIzjava[j].poenostavi() ):
                    toBeRemoved.append(indexCounter)

    # odstranim iz izjav podizjave oblike (X or notX)
    toBeRemoved.reverse()
    for i in range (0, len(toBeRemoved)):
        del izjava[toBeRemoved[i]]

    return izjava

def sortByLength(izjava):

    # Metoda sortira podizjave v izjavi glede na njihovo dolžino (naraščajoče). Vrne sortirano izjavo

    for i in range(0, len(izjava)-1):
        for j in range((i+1), len(izjava)):
            if len(izjava[i]) > len(izjava[j]):
                tempIzjava = izjava[j]
                izjava[j] = izjava[i]
                izjava[i] = tempIzjava

    return izjava
         

def getTestIzjava(caseNumber): 

    x = Var('X')
    y = Var('Y')
    z = Var('Z')
    q = Var('Q')

    or_1 = Or([x,Not(Not(y)),Not(z)])
    or_2 = Or([Not(x),Not(y)])
    or_3 = Or([x,z])
    or_4 = x
    or_5 = Or( [  z , y, Not(q) ] )
    or_6 = Or([Not(x)])

    if caseNumber == 1:
        i = And([])   
    elif caseNumber == 2:
        i = And([x]) 
    elif caseNumber == 3:
        i = And([x, Or([])]) 
    elif caseNumber == 4:
        i = And([Or([]),Or([x])])
    elif caseNumber == 5:
        i = or_4
        i = And([Or([x,Not(y),Not(z)]) , Or([Not(x),Not(y)]) , Or([x,z]) , Or([Not(x),Not(q)])])
    elif caseNumber == 6:
        i = And([or_1 , or_2 , or_3, or_4, or_5])
    elif caseNumber == 7:
        i = And([x, Or([x,y]), Or([Not(y), z]), Or([Not(x)])])
    elif caseNumber == 8:
        i = And([x, Not(x), Or([x, q])]) #test (x AND notx)
    elif caseNumber == 9:
        i = And([Or([x, y, Not(x)]), Or([q,z])]) #test (x or notX)
    elif caseNumber == 10:
        #testiranje za pureValues ker sta tuki 2xpure, ostalo vse odpade
        i = And([ Or([y, Not(q)]) , Or([y, Not(z)]) , Or([x, Not(y)]) , Or([y,z,q]) , Or([x,Not(z)]) , Or([x,Not(q)]) ])
    else:
        i = or_4
        i = And([Or([x,Not(y),Not(z)]) , Or([Not(x),Not(y)]) , Or([x,z]) , Or([Not(x),Not(q)])])

    return i
    
def pozdravnaMetoda():
    print('******************************************************')
    print('Pozdravljeni v algoritmu DPLL')
    print('Za zagon algoritma poklicite funkcijo: DPLL(izjava), ki ji podate izjavo')
    print('Primer izjave: ((X or Y) and (Y or notZ)) := And( [ Or([ X, Y ]) , Or([ Y, Not(Z) ]) ] )')
    print('Za preverjanje pravilnosti delovanja sta spodaj prilozena copy/paste testna primera')
    
    print('izjava=getTestIzjava(0) -----> ((X or notY or notZ) and (notX or notY) and (X or Z) and (notX or notQ))')
    print('izjava=getTestIzjava(1) -----> ()')
    print('izjava=getTestIzjava(2) -----> ((X))')
    print('izjava=getTestIzjava(3) -----> ((X) and ())')
    print('izjava=getTestIzjava(4) -----> (() and (X))')
    print('izjava=getTestIzjava(5) -----> ((X or notY or notZ) and (notX or notY) and (X or Z) and (notX or notQ))')
    print('izjava=getTestIzjava(6) -----> ((X or Y or notZ) and (notX or notY) and (X or Z) and (X) and (Z or Y or notQ))')
    print('izjava=getTestIzjava(7) -----> ((X) and (X or Y) and (notY or Z) and (notX))')
    print('izjava=getTestIzjava(8) -----> ((X) and (notX) and (X or Q))')
    print('izjava=getTestIzjava(9) -----> ((X or Y or notX) and (Q or Z))')
    print('izjava=getTestIzjava(10) -----> ((Y or notQ) and (Y or notZ) and (X or notY) and (Y or Z or Q) and (X or notZ) and (X or notQ))')
    print('')
    print('Primer za sudoku: izjava = sudoku([[1,2,0,0],[3,0,1,0],[0,1,0,3],[0,0,2,1]])')
    print('Izjavo lahko zgradite tudi sami, vendar je potrebno ustvariti vsako spremenljivko, ki jo boste uporabljali (glej Izjave.py)')
    print('******************************************************')

pozdravnaMetoda()





