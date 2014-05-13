# Spodnji razredi predstavljajo strukturo za predstavitev Boolovih formul.
# Var() predstavlja spremenljivko
# Tru() in Fal() predstavljata konstanti True in False
# And() in Or() predstavljata logièna veznika /\ in \/
# Not() predstavlja negacijo

# Vsako izjavo lahko valuiramo z metodo .izracun(val), ki sprejme slovar
# valuacij spremenljivk, ki nastopajo v izjavi
# (npr: {'A':False,'B':True,'C':True}).

# Vsako izjavo lahko poenostavimo z metodo .poenostavi(), ki potisne vse
# negacije do spremenljivk, odstrani morebitne pojavitve Tru() in Fal()
# in odveène oklepaje.


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
        sez = []
        for v in self.izjave:
            vr = v.izracun(val)
            if vr == False:
                return False
            elif type(vr) == Var or type(vr) == Not:
                sez.append(vr)
            elif type(vr) == And or type(vr) == Or:
                vr_izjave = vr.vrni()
                if len(vr_izjave) == 1:
                    sez.append(vr_izjave[0])
                else:
                    sez.append(vr)
        if not sez:
            return True
        elif len(sez) == 1:
            return sez[0]
        else:
            return And(sez)

    def poenostavi(self): 
        #self.nastavi(list(set(self.izjave())))
        for i in self.izjave:
            if type(i) is Tru:
                self.izjave.remove(i)
                return self
            elif type(i) is Fal:
                return Fal()
            elif type(i) is And:
                self.nastavi(self.izjave[:self.izjave.index(i)]+i.vrni()+self.izjave[self.izjave.index(i)+1:])
        if len(self.izjave) == 1:
            return self.izjave[0].poenostavi()
        return And([i.poenostavi() for i in self.izjave])
    

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
        sez = []
        for v in self.izjave:
            vr = v.izracun(val)
            if vr == True:
                return True
            elif type(vr) == Var or type(vr) == Not:
                sez.append(vr)
            elif type(vr) == And or type(vr) == Or:
                vr_izjave = vr.vrni()
                if len(vr_izjave) == 1:
                    sez.append(vr_izjave[0])
                else:
                    sez.append(vr)
        if not sez:
            return True
        elif len(sez) == 1:
            return sez[0]
        else:
            return Or(sez)
                            
    def poenostavi(self):
        #self.nastavi(list(set(self.izjave())))
        for i in self.izjave:
            if type(i) is Fal:
                self.izjave.remove(i)
            elif type(i) is Tru:
                return Tru()
            elif type(i) is Or:
                 self.nastavi(self.izjave[:self.izjave.index(i)]+i.vrni()+self.izjave[self.izjave.index(i)+1:])
        if len(self.izjave) == 1:
            return self.izjave[0].poenostavi()
        return Or([i.poenostavi() for i in self.izjave])

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
def test():
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
   print('spremenljivke, ki nastopajo: ',iz.var())

def test1():
    a = Var('A')
    c = Var('C')
    b = Var('B')
    iz = And([a,And([c,b]),Or([Not(a),Not(c)])])
    val = {'A':True,'B':True}
    print(iz)
    print(iz.izracun(val))
    print(iz.var())

