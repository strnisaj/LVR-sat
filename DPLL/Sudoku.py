﻿import time
import Izjave
import CNF

# funkcija sprejme dva seznama. Seznam sez predstavlja nerešen sudoku z nekaterimi že vpisanimi številkami,
# seznam sezR pa rešen sudoku, ki ga predstavlja sez. Funkcija vrne izjavo, ki je resnièna, èe je sezR res rešen
# sez in neresnièna, èe to ni res.
def sudoku(sez):
    n = len(sez)
    m = int(n**0.5)
    # Sestavimo seznam spremenljivk spremen. Spremenljivka X(i,j,k) je na mestu spremen[i][j][k-1] in po meni:
    # "V polju (i,j) je zapisano število k"
    # Sestavimo tudi seznam spremenljivk spremenK. V tem seznamu element spremenK[i][j] predstavlja kvadratek (i,j)
    # pri èemer gresta i,j od 0 do m-1, kjer je m = sqrt(n). V vsakem elementu spremenK[i][j] je n seznamov( toliko
    # kolikor je možnih števil. V k+1-em so spremenljivke X(i,j,k) za vse i,j med 0 in m-1.
    spremen = []
    spremenK = []
    for i in range(n):
        spremen.append([])
        if i<m:
            spremenK.append([])
        for j in range(n):
            spremen[i].append([])
            if j<m and i<m:
                spremenK[i].append([])
            for k in range(1,n+1):
                x = Izjave.Var('X({0},{1},{2})'.format(i,j,k))
                spremen[i][j].append(x)
                if len(spremenK[i//m][j//m]) < n:
                    spremenK[i//m][j//m].append([])
                spremenK[i//m][j//m][k-1].append(x)                      
    # Sestavimo izjavo: "V vsakem polju (i,j) je zapisano vsaj eno število k od 1 do n."
    seznam1 = []
    for i in range(n):
        for j in range(n):
            seznam1.append(Izjave.Or(spremen[i][j]))
    izjava1 = Izjave.And(seznam1)

    # Sestavimo izjavo: "V nobenem polju (i,j) nista zapisani dve števili."
    seznam2 = []
    for i in range(n):
        for j in range(n):
            seznam21 = []
            for k in range(1,n+1):
                for l in range(k+1,n+1):
                    seznam21.append(Izjave.Not(Izjave.And([spremen[i][j][k-1],spremen[i][j][l-1]])))
            seznam2.append(Izjave.And(seznam21))
    izjava2 = Izjave.And(seznam2)
    
    # Sestavimo izjavo: "rešen in nerešen sudoku imata se strinjata na mestih, kjer so
    #                     v nerešenm sudokuju že vpisana števila"  
    
    seznam3 = []
    for i in range(n):
        for j in range(n):
            if sez[i][j] != 0:
                seznam3.append(spremen[i][j][sez[i][j]-1])
    izjava3 = Izjave.And(seznam3)

    # Sestavimo izjavo: "V vsaki vrstici so sama razlièna števila"
    seznam4 = []
    for i in range(n):
        for j in range(n):
            for k in range(1,n+1):
                for l in range(j+1,n):
                    seznam4.append(Izjave.Not(Izjave.And([spremen[i][j][k-1],spremen[i][l][k-1]])))
    izjava4 = Izjave.And(seznam4)

    # Sestavimo izjavo: "V vsakem stolpcu so sama razlièna števila"
    seznam5 = []
    for j in range(n):
        for i in range(n):
            for k in range(1,n+1):
                for l in range(i+1,n):
                    seznam5.append(Izjave.Not(Izjave.And([spremen[i][j][k-1],spremen[l][j][k-1]])))
    izjava5 = Izjave.And(seznam5)

    # Sestavimo izjavo: "V vsakem m*m kvadratku se vsako število pojavi natanko enkrat"
    seznam6 = []
    for i in range(m):
        for j in range(m):
            for k in range(1,n+1):
                for s in range(n):
                    for r in range(s+1,n): 
                        seznam6.append(Izjave.Not(Izjave.And([spremenK[i][j][k-1][s],spremenK[i][j][k-1][r]])))
    izjava6 = Izjave.And(seznam6)

    return Izjave.And([izjava1,izjava2,izjava3,izjava4,izjava5,izjava6])




def testS():
   a = sudoku([[1,2,0,0],[3,0,1,0],[0,1,0,3],[0,0,2,1]])
   b = sudoku([[5,3,0,0,7,0,0,0,0],[6,0,0,1,9,5,0,0,0],[0,9,8,0,0,0,0,6,0],[8,0,0,0,6,0,0,0,3],[4,0,0,8,0,3,0,0,1],[7,0,0,0,2,0,0,0,6],[0,6,0,0,0,0,2,8,0],[0,0,0,4,1,9,0,0,5],[0,0,0,0,8,0,0,7,9]])
   print('Izjava za sudoku:')
   t0 = time.clock()
   print(b)
   print('pretekel èas: ',time.clock()-t0)
   print('Izjava za sudoku v CNF obliki:')
   t0 = time.clock()
   print(CNF.CNF(b))
   print('pretekel èas: ',time.clock()-t0)


def valuacija():
    s = [[5,3,0,0,7,0,0,0,0],[6,0,0,1,9,5,0,0,0],[0,9,8,0,0,0,0,6,0],[8,0,0,0,6,0,0,0,3],[4,0,0,8,0,3,0,0,1],[7,0,0,0,2,0,0,0,6],[0,6,0,0,0,0,2,8,0],[0,0,0,4,1,9,0,0,5],[0,0,0,0,8,0,0,7,9]]
    s_r = [[5,3,4,6,7,8,9,1,2],[6,7,2,1,9,5,3,4,8],[1,9,8,3,4,2,5,6,7],[8,5,9,7,6,1,4,2,3],[4,2,6,8,5,3,7,9,1],[7,1,3,9,2,4,8,5,6],[9,6,1,5,3,7,2,8,4],[2,8,7,4,1,9,6,3,5],[3,4,5,2,8,6,1,7,9]]
##    s = [[1,2,0,0],[3,0,1,0],[0,1,0,3],[0,0,2,1]]
##    s_r = [[1,2,3,4],[3,4,1,2],[2,1,4,3],[4,3,2,1]]
    sud = sudoku(s)
    spremen = sud.var()
    val = {}
    for x in spremen:
        ime = x.vrni_ime()
        i = int(ime[2])
        j = int(ime[4])
        n = int(ime[6])
        if s_r[i][j]==n:
            val[x]= True
        else:
            val[x]= False
    return sud.izracun(val)
        
        



















    



    