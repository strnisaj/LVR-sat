import time
# Spodnji razredi predstavljajo strukturo za predstavitev Boolovih formul.
# Var() predstavlja spremenljivko
# Tru() in Fal() predstavljata konstanti True in False
# And() in Or() predstavljata logicna veznika 
# Not() predstavlja negacijo

# Vsako izjavo lahko valuiramo z metodo .izracun(val), ki sprejme slovar
# valuacij spremenljivk, ki nastopajo v izjavi
# (npr: {'A':False,'B':True,'C':True}).

# Vsako izjavo lahko poenostavimo z metodo .poenostavi(), ki potisne vse
# negacije do spremenljivk, odstrani morebitne pojavitve Tru() in Fal()
# in odvecne oklepaje.

class Var():
    def __init__(self,ime):
        self.ime = ime

    def __repr__(self):
        return str(self.ime)

    def vrni(self):
        return self

    def vrni_ime(self):
        return self.ime
    
    def var(self):
        return [self]

    def nastavi(self,ime):
        self.ime = ime

    def izracun(self,val):
        for k,v in val.items():
            if k == self:
                return v
        return self

    def poenostavi(self):
        return self

class Tru(Var):
    def __init__(self):
        Var.__init__(self,'T')
        
    def izracun(self,val):
        return True

class Fal(Var):
    def __init__(self):
        Var.__init__(self,'F')

    def izracun(self,val):
        return False

class And():
    def __init__(self, izjave):
        self.izjave = izjave
        ime = '('
        for i in range(len(izjave)):
            if i == 0:
                ime = ime + str(izjave[i].ime)
            else:
               ime = ime + ' and {0}'.format(str(izjave[i].ime)) 
        self.ime = ime + ')'  

    def __repr__(self):
        return self.ime

    def vrni(self):
        return self.izjave

    def var(self):
        spr = set()
        for i in self.izjave:
            spr = spr.union(set(i.var()))
        return list(spr)
            

    def nastavi(self,izjave):
        self.izjave = izjave

    def izracun(self,val):
        izjave = self.izjave
        length = len(izjave)
        i=0
        while i < length:
            vr = izjave[i].izracun(val)
            if type(vr) is bool:
                if not vr:
                    return False
                else:
                    izjave.remove(izjave[i])
                    length -= 1
                    continue
            else:
                izjave[i]=vr
            i+=1
        if not izjave:
            return True
        elif len(izjave) == 1:
            return izjave[0]
        return And(izjave)
                

    def poenostavi(self): 
        if len(self.izjave) == 1:
            return self.izjave[0].poenostavi()
        self.izjave = [i.poenostavi() for i in self.izjave] 
        for i in self.izjave:
            if type(i) is Tru:
                self.izjave.remove(i)
                return self
            elif type(i) is Fal:
                return Fal()
            elif type(i) is And:
                self.izjave = self.izjave[:self.izjave.index(i)]+i.vrni()+self.izjave[self.izjave.index(i)+1:]
        return And(self.izjave)

class Or():
    def __init__(self, izjave):
        self.izjave = izjave
        ime = '('
        for i in range(len(izjave)):
            if i == 0:
                ime = ime + str(izjave[i].ime)
            else:
               ime = ime + ' or {0}'.format(str(izjave[i].ime)) 
        self.ime = ime + ')' 

    def __repr__(self):
        return self.ime

    def vrni(self):
        return self.izjave

    def var(self):
        spr = set()
        for i in self.izjave:
            spr = spr.union(set(i.var()))
        return list(spr)

    def nastavi(self,izjave):
        self.izjave = izjave

    def izracun(self,val):
        izjave = self.izjave
        length = len(izjave)
        i=0
        while i < length:
            vr = izjave[i].izracun(val)
            if type(vr) is bool:
                if vr:
                    return True
                else:
                    izjave.remove(izjave[i])
                    length -= 1
                    continue
            else:
                izjave[i]=vr
            i+=1
        if not izjave:
            return False
        elif len(izjave) == 1:
            return izjave[0]
        return Or(izjave)
                            
    def poenostavi(self):
        if len(self.izjave) == 1:
            return self.izjave[0].poenostavi()
        self.izjave = [i.poenostavi() for i in self.izjave] 
        for i in self.izjave:
            if type(i) is Fal:
                self.izjave.remove(i)
                return self
            elif type(i) is Tru:
                return Fal()
            elif type(i) is Or:
                self.izjave = self.izjave[:self.izjave.index(i)]+i.vrni()+self.izjave[self.izjave.index(i)+1:]
        return Or(self.izjave)

class Not():
    def __init__(self,A):
        self.A = A
        self.ime = 'not{0}'.format(str(self.A.ime))

    def __repr__(self):
        return self.ime

    def vrni(self):
        return self.A

    def var(self):
        return self.A.var()

    def nastavi(self,A):
        self.A = A

    def izracun(self,val):
        vr = self.A.izracun(val)
        if type(vr) == bool:
            return not vr
        else:
            return Not(vr)

    def poenostavi(self):
        if type(self.A) is Var:
            return self
        elif type(self.A) is And:
            return Or([Not(i).poenostavi() for i in self.A.vrni()])
        elif type(self.A) is Or:
            return And([Not(i).poenostavi() for i in self.A.vrni()])
        elif type(self.A) is Not:
            return self.A.vrni().poenostavi()


# Test za izjave
# Imamo dva primera izjav: iz in iz1. Nad izjavo delamo sledece operacije:
# 		- poenostavljanje izjave (pretvorba v NNF obliko)
# 		- racunanje vrednosti izjave (za dan nabor vrednosti spremenljivk izracunamo izjavo)
#		- izpis nastopajocih spremenljivk (za dano izjavo vrnemo vse spremenljivke)
def test():
    a = Var('A')
    b = Var('B')
    c = Var('C')
    iz = Not(And([Or([Not(a),b]),Not(And([c,a])),Not(Or([Not(b),a,Not(c)]))]))
    iz1 = And([a,And([c,b]),Or([Not(a),Not(c)])])
    print('Poenostavitev izjave: ')
    print('izjava: ',iz)
    t0 = time.clock()
    i = iz.poenostavi()
    print('Pretekel cas: ', time.clock() - t0)
    print('Poenostavljena izjava: ', i)
    print('###############################')

    print('Vrednost izjave: ')
    val = {a:False,b:True,c:True}
    val1 = {a:False,b:True}
    t0 = time.clock()
    j = iz.izracun(val)
    print('Pretekel cas: ', time.clock() - t0)
    print('Vrednost: ', j)
    print('###############################')

    print('Nastopajoce spremenljivke: ', iz.var())
