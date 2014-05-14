from Izjave import *
from Sudoku import *
#from Hadamard import *
from CNF import *
import time

newPureValFound = True
solutionVals = {}
lockSolutionVals = False

def DPLL(izjava):
    # Metoda dobi izjavo, ki jo obdela s pomocjo funkcije prepareStatement(izjava)
    # Ce izjava ni na zacetku False (zaradi praznega protislovja), potem klicemo rekurzivno metodo rec_DPLL(izjava, varValues)
    # FIXME: prepareStatement naj preveri se, ce ni izjava False zaradi kaksnega praznega OR-a

    global solutionVals
    solution = False
    
    startTime = time.time()
    dataForDPLL = prepareStatement(izjava)      # Pripravimo izjavo. Metoda vrne [izjava, varValues], kjer so vrednosti 100% pravilne
    
    if (dataForDPLL != False):
        izjava = dataForDPLL[0]
        varValues = dataForDPLL[1]
        
        print('####### BEFORE REC ########')
        print('Izjava: ', izjava)
        print('VarValues: ', varValues)
        print('_________________________________')
        solution = rec_DPLL(izjava, varValues)  # klic rekurzivne metode
        
    print('Vrnjena resitev: ', solution)
    print('Vrednosti: ' , solutionVals)

    endTime = time.time()
    timePassed = endTime - startTime
    print('Time: ', timePassed)

def prepareStatement(izjava):
    # Metoda sprejme izjavo in jo pripravi takole:
    #   - izjavo pretvori v CNF obliko
    #   - izjavo pretvori v seznam seznamov oblike [ ... [ ... ] ...]
    #   - odstrani vse proste spremenljivke
    #   - preveri, da se ne zgodi primer (X and notX)
    #   - pobrise vse True izjave oblike (X or notX)
    #   - najde vse proste spremenljivke
    # Metoda vrne seznam, v katerem je izjava in vrednosti spremenljivk
    # Ce je primer na osnovi zgornjih ugotovitev neresljiv, potem metoda vrne False

    # poresetiram prejsno resitev
    global solutionVals
    global lockSolutionVals
    global newPureValFound
    solutionVals = {}
    lockSolutionVals = False
    newPureValFound = True

    izjava = CNF(izjava)                                    # pretvori izjavo v CNF
    izjava = izjava.poenostavi().vrni()                     # dobim [ ... (...) ...]
    #print('IZJAVA: ' ,izjava)
    izjava = get_2D_list(izjava)                            # dobim [ ... [...] ...]
    varValues = {}                                          # Zacetne vrednosti spremenljivk
    izjava = removeTrueSantences(izjava)                    # metoda odstrani podizjave tipa (X or notX)
    #print('IZJAVA: ' ,izjava)
  
    # PONOVNO PREVERJAMO PROSTE SPREMENLJIVKE, DOKLER JE KAKŠNA SE PROSTA!!
    while (True):
        #print('________________________')
        #print('Izjava: ' , izjava)
        changes = 0                                             # stevec za ustavitveni pogoj
        getInfo = removeSingleVars(izjava)                      # metoda vrne [sprmenjenaIzjava, slovarProstihSpremenljivk]
        if getInfo[1] == False:
            print('ERROR: getInfo[1] == False ..... returning False!!!')
            return False
        else:
            izjava = getInfo[0]                                 # izjava brez prostih spremenljivk
            singleVarValues = getInfo[1]                        # slovar vrednosti prostih spremenljivk. Lahko je False, ce je bila oblika (X and notX)
            varValues = concatDicts(varValues, singleVarValues) # metoda zdruzi seznama obstojecih in novih vrednosti spremenljivk (sicer vrne false)
            if varValues == False:                              # ce je prislo do protislovja (X and notX) potem ni resitve in vrnemo False
                print('ERROR: varValues == False ..... returning False!!!')
                return False
            
            #print('New vals: ' , varValues)
            izjava = processStatement(izjava, varValues)        # metoda odstrani OR-e, ki so True in spremenljivke znotraj OR-ov, ki so False
            #print('New izjava: ', izjava)
        if (getInfo[1] != {}):
            changes = changes + 1
        if (changes == 0):
            #print('breaking.....')
            break

    # testni izpis stevila prostih in cistih spremenljivk, ki smo jih nasli
    #steviloSpremenljivk = 0
    #for keys in varValues:
    #    steviloSpremenljivk = steviloSpremenljivk + 1
    #print('___najdenih cistih/prostih spremenljivk: ', steviloSpremenljivk)
       
    # PREVERIMO CISTE SPREMENLJIVKE
    # Spodnja while zanka pridobiva ciste spremenljivke, poenostavlja izjavo in to ponavalja, dokler je kaksna spremenljivka cista
    while (newPureValFound == True):
        #print('.................')
        pureVals = getPureVals(izjava)                  # pridobim slovar cistih spremenljivk
        varValues = concatDicts(varValues, pureVals)    # zdruzim obstojece spremenljivke s cistimi

        #preverimo, da nismo prisli do protislovja:
        if varValues == False:
            print('################## WARNING :::: pureVals is returning FALSE!!!')
            return False
        izjava = processStatement(izjava, varValues)    # metoda odstrani OR-e, ki so True in spremenljivke znotraj OR-ov, ki so False
        #print('in while izjava: ', izjava)
    #print('Izjava 2D: ' , izjava)
    #print('vals after pure: ', varValues)
    #test = isThereAnySingleVar(izjava)
    #print('any single var left: ', test)
    izjava = sortByLength(izjava)                       # sortiranje izjave po dolzini podizjav (narascajoce)

    # testni izpis stevila prostih in cistih spremenljivk, ki smo jih nasli
    #steviloSpremenljivk = 0
    #for keys in varValues:
    #    steviloSpremenljivk = steviloSpremenljivk + 1
    #print('___najdenih cistih/prostih spremenljivk: ', steviloSpremenljivk)

    izjava = sortByLength(izjava)

    # vrnemo seznam, ki vsebuje na rekurzijo pripravljeno izjavo in slovar vrednosti spremenljivk (te niso vec zastopane v izjavi)
    return [izjava, varValues]

def isThereAnySingleVar(izjava):
    for subizjava in izjava:
        if len(subizjava) == 1:
            return True


def rec_DPLL(izjava, varValues):
    # Metoda najprej preveri, ce je kaksna spremenljivka cista. Nato poenostavi izjavo in naredi dve kopiji izjave
    # Vzame se prva spremenljivka iz izjave in se nastavi na True. Sprocesira se kopija_1 izjave z novo vrednostjo spremenljivke True
    # Vzame se prva spremenljivka iz izjave in se nastavi na False. Sprocesira se kopija_2 izjave z novo vrednostjo spremenljivke False

    #print('Break point 1')
    print('')
    print('_______rec_DPLL()____________')
    print('Recived izjava: ' , izjava)
    print('Recived varValues: ' , varValues)
    
    # Ce smo dobili ze resitev, potem ne potrebujemo vec preverjanja
    global lockSolutionVals
    if lockSolutionVals == True:
        print('LOCK = LOCKED')
        return True
    #print('Values before getting pureVals: ', varValues)

    # Preverimo, ce smo prisli do resitve=true
    if is_AND_empty(izjava):
        global solutionVals
        if lockSolutionVals == False:
            #print('NASTAVLJAM GLOBALNO RESITEV')
            lockSolutionVals = True
            solutionVals = copyVarValues(varValues)
        return True

    # Preverimo, ce smo prisli do resitve=false
    if is_OR_empty(izjava):
        return False
    #print('Break point 5')
    firstVar = getFirstVar(izjava)      # pridobimo prvo spremenljivko
    izjava_1 = copyStatement(izjava)    # prekopiramo izjavo
    izjava_2 = copyStatement(izjava)    # prekopiramo izjavo
    vals_1 = copyVarValues(varValues)   # prekopiramo vrednosti
    vals_2 = copyVarValues(varValues)   # prekopiramo vrednosti
    vals_1[firstVar] = True             # enkrat vrednost prve spremenljivke nastavimo na True

    print('')
    print('Vals_1: ' , vals_1)
    print('Izjava_1: ' , izjava_1)
    izjava_1 = processStatement(izjava_1, vals_1)
    print('Sprocesirana: ' , izjava_1)

    if (rec_DPLL(izjava_1, vals_1) != False):  # rekurzivni klic
        return True

    print('GREM NA FALSE')
    vals_2[firstVar] = False
    print('')
    print('Vals_2: ' , vals_2)
    print('Izjava_2: ', izjava_2)
    izjava_2 = processStatement(izjava_2, vals_2)
    print('Sprocesirana: ' , izjava_2)
    
    if (rec_DPLL(izjava_2, vals_2) != False):  # rekurzivni klic
        return True
    return False

def getPureVals(izjava):
    # Metoda se sprehodi cez izjavo in poisce ciste spremenljivke.
    # Metoda vrne slovar cistih spremenljivk, ki jih nastavi na true (x) oz. false (not x)

    #print('WELCOME TO GET-PURE-VALS-FUNCTION')
    #print('received izjava: ', izjava)
    pureVals = {}
    varsInStatement = {}
    global newPureValFound
    newPureValFound = False

    #print('Welcome to getPureVars...................... ')
    #napolnim slovar zastopanosti spremenljivk: 1: X .... 2: notX ..... 3: (X and notX)
    for subIzjava in izjava:
        for var in subIzjava:
            #ce ni spremenljivke v seznamu, jo dodamo
            #print('thisVar == ', var)
            if ((var.vrni() in varsInStatement) == False):
                #print('VAR IS NOT INSIDE VARS-IN-STATEMENT!!!! ', varsInStatement )
                #if var.poenostavi() == var.vrni(): #XXX
                if isinstance(var, Var):
                    varsInStatement[var.vrni()] = 1
                else:
                    varsInStatement[var.vrni()] = 2
            #ce je spremenljivka ze v seznamu, preverimo katero vrednost ima
            else:
                #print('VAR IS INSIDE VARS-IN-STATEMENT!!! ', varsInStatement)
                vrednost = varsInStatement[var.vrni()]
                #if var.poenostavi() == var.vrni() and vrednost == 2: #XXX
                if ((vrednost == 2) and (isinstance(var, Var))):
                    varsInStatement[var.vrni()] = 3
                #elif var.poenostavi() != var.vrni() and vrednost == 1: #XXX
                elif ( (vrednost == 1) and (isinstance(var, Not)) ):
                    varsInStatement[var.vrni()] = 3
                else:
                    #print('XXXX: this should not have happened!!! (getPureVars function)')
                    pass
    
    #ugotovimo, katere key-e je potrebno odstraniti
    keysToBeRemoved = []
    for key in varsInStatement:
        if (varsInStatement[key] == 3):
            keysToBeRemoved.append(key)

    #odstranimo key-e
    for i in keysToBeRemoved:
        varsInStatement.pop(i)

    #napolnimo slovar cistih spremenljivk
    for key in varsInStatement:
        newPureValFound = True
        if varsInStatement[key] == 1:
            pureVals[key] = True
        else:
            pureVals[key] = False
    return pureVals

def processStatement(izjava, vals):
    # Metoda prejme izjavo in vrednsoti spremenljik.
    # Metoda odstrani OR stavek, ce je ta zaradi ene izmed sprmeenljivk ze True
    # Metoda odstrani spremenljivko iz OR stavka, ce je njena vrednost False
    # Kadar odstranimo spremenljivko iz OR stavka, preverimo, da OR ni prazen .... to bi lahko klicov uno drugo metodo
    # XXX: pazi, ker je razlika, ali odstranis True spremenljivko iz OR stavka, ali odstranis False spremenljivko iz Or stavka!!!!
    toBeRemoved_OR = []
    toBeRemoved_AND = []
    indexAND = -1

    #print('__________________________________________________________________________')
    #print('*************** Welcome to processStatement(izjava, vals) ***************')
    #print('Received izjava: ', izjava)
    #print('Received vals: ' , vals)
    #print('@@@@@@@@@@@@@@@@@@@@@')
    for subIzjava in izjava:
        indexAND = indexAND + 1
        indexOR = -1
        toBeRemoved_OR = []
        #grem cez vse podizjave
        for i in subIzjava:
            indexOR = indexOR + 1
            if i.vrni() in vals:
                #print('i = ', i)
                vrednost = vals[i.vrni()]   #dobim vrednost shranjene spremenljivke
                #ce je v podizjavi VAR
                if isinstance(i.poenostavi(), Var):
                    if vrednost == True:
                        toBeRemoved_AND.append(indexAND)
                        break
                    elif vrednost == False:
                        toBeRemoved_OR.append(indexOR)
                    else:
                        pass
                #ce je v podizjavi NOT
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
                    
            # ce je kaksno spr. potrebno odstraniti iz OR-a, jo odstranim tukaj
            if len(toBeRemoved_OR) != 0:
                toBeRemoved_OR.reverse()
                for i in range(0, len(toBeRemoved_OR)):
                    del subIzjava[toBeRemoved_OR[i]]
            # preverim, ce je prazn OR
            if len(subIzjava) == 0:
                #print('TODO: return FALSE')
                #return False
                pass
            
    # ce je kaksen AND true, potem ga odstranimo iz izjava
    toBeRemoved_AND.reverse()
    for i in range(0, len(toBeRemoved_AND)):
        del izjava[toBeRemoved_AND[i]]

    #print('Returned izjava: ' , izjava)
    #print('Returned vals: ', vals)
    #print('__________________________________________________________________________')

    '''
    #TESTIRAM:
    for subIzjava in izjava:
        for i in subIzjava:
            if i in vals:
                print('ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR')
    '''
    
    return izjava

def getFirstVar(izjava): 
    x = izjava[0][0].vrni()
    return x

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
    # Metoda preveri, ce je izjava = []. V tem primeru imamo resitev in vrnemo True, sicer vrnemo False
    if len(izjava) == 0:
        return True
    else:
        return False

def is_OR_empty(izjava):
    # Metoda preveri, ce je izjava = [ ... [] ... ].
    # Ce je katerikoli OR prazen, potem ni resitve in vrnemo True, sicer vrnemo False
    for subIzjava in izjava:
        if len(subIzjava) == 0:
            return True
    return False

def concatDicts(oldValues, newValues):
    # Metoda zdruzi stare in nove spremenljivke v slovarjih
    # Metoda preme 2 slovarja starih in novi vrednosti spremenljivk in jih zdruzi
    # Metoda vrne slovar zdruzenih spremenljivk ali False, ce jih ne more zdruziti (ker pride do protislovja)
    '''
    print('WELCOME TO CONCAT-DICTS')
    print('')
    print('OLD-VALUES')
    print('')
    print(oldValues)
    print('NEW-VALUES')
    print(newValues)
    print('')
    '''
    for key in newValues:
        #ce je ze vsebovan
        if key in oldValues:
            #ce se stara in nova vrednost razlikujeta
            if oldValues[key] != newValues[key]:
                #print('tuki pride do errorja......')
                #print('oldValues[' , key, '] = ', oldValues[key])
                #print('newValues[' , key, '] = ', newValues[key])
                return False
        #ce ni vsebovan, dodamo novo vrednost med stare vrednosti
        else:
            oldValues[key] = newValues[key]
    return oldValues

def removeSingleVars(izjava):
    # Metoda gre cez izjavo in iz nje odstrani vse 'proste' spremenljivke, ter jih nastavi na True
    # Metoda vrne spremenljeno izjavo in slovar prostih spremenljivk, ki so nastavljene na ustrezno vrednost
    # Metoda iz izjave izbrise te proste podizjave
    # Metoda hkrati preveri, da ni prislo do protislovja oblike (X and notX)
    toBeRemoved = []
    singleVars = []

    #proste spremenljivke shranimo v singleVars in pridobimo indexe teh prostih spremenljivk, da jih bomo pobrisali iz izjave
    for i in range (0, len(izjava)):
        # ce je samo ena spremenljivka v podizjavi
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

    # preverimo, da ni prislo do protislovja oblike (X and notX)
    for i in range(0, len(singleVars)-1):
        if singleVarsDict == False:
            break
        for j in range((i+1), len(singleVars)):
            #ce se pojavi x and notx
            #if (singleVars[i].vrni() == singleVars[j].vrni()) and (singleVars[i].poenostavi() != singleVars[j].poenostavi()):
            if ( (isinstance(singleVars[i], Var) and isinstance(singleVars[j], Not)) or (isinstance(singleVars[i],Not) and isinstance(singleVars[j], Var))):
                print('Tukaj nastane problem: ')
                print('singleVars[i].poenostavi() == ', singleVars[i].poenostavi())
                print('singleVars[j].poenostavi() == ', singleVars[j].poenostavi())
                print('singleVars[i].vrni() == ', singleVars[i].vrni())
                print('singleVars[j].vrni() == ', singleVars[j].vrni())
                print('i = ', i)
                print('j = ',j)
                singleVarsDict = False
                break

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
    # Metoda sortira podizjave v izjavi glede na njihovo dolzino (narascajoce). Vrne sortirano izjavo
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
    a = Var('A')

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
    elif caseNumber == 666:
        i = And([ Not(x), Or([x,z]) ])
    elif caseNumber == 777:
        i = And([ Not(x), Or([Not(x), z, Not(y)]) , Or([x,z]) , Or([Not(z), y]), Or([q,a]) , Or([Not(q), a]) , Or([q, Not(a)]) , Or([Not(q),Not(a)]) ])
    else:
        i = or_4
        i = And([Or([x,Not(y),Not(z)]) , Or([Not(x),Not(y)]) , Or([x,z]) , Or([Not(x),Not(q)])])
    return i
    
def pozdravnaMetoda():
    print('************************************************************************************************************')
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
    print('************************************************************************************************************')

    izjava = sudoku([[1,2,0,0],[3,0,1,0],[0,1,0,3],[0,0,2,1]])
    #izjava = sudoku([[5,3,0,0,7,0,0,0,0],[6,0,0,1,9,5,0,0,0],[0,9,8,0,0,0,0,6,0],[8,0,0,0,6,0,0,0,3],[4,0,0,8,0,3,0,0,1],[7,0,0,0,2,0,0,0,6],[0,6,0,0,0,0,2,8,0],[0,0,0,4,1,9,0,0,5],[0,0,0,0,8,0,0,7,9]])
    #izjava = getTestIzjava(777)
    DPLL(izjava)

pozdravnaMetoda()





