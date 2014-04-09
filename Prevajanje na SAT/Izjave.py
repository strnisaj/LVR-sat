
class Var():
    def __init__(self,ime):
        self.ime = ime

    def __repr__(self):
        return str(self.ime)

    def vrni(self):
        return self

    def izracun(self,val):
        for k,v in val.items():
            if k == self.ime:
                return v

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
        for i in self.izjave:
            if self.izjave.index(i)== 0:
                ime = ime + i.ime
            else:
               ime = ime + ' and {0}'.format(i.ime) 
        self.ime = ime + ')'  

    def __repr__(self):
        return self.ime

    def vrni(self):
        return self.izjave

    def izracun(self,val):
        for v in self.izjave:
            if v.izracun(val) == False:
                return False
        return True

    def poenostavi(self):
        for i in self.izjave:
            if type(i) is Tru:
                self.izjave.remove(i)
            elif type(i) is Fal:
                return Fal()
        if len(self.izjave) == 1:
            return self.izjave[0].poenostavi()
        return And([i.poenostavi() for i in self.izjave])
    

class Or():
    def __init__(self, izjave):
        self.izjave = izjave
        ime = '('
        for i in self.izjave:
            if self.izjave.index(i)== 0:
                ime = ime + i.ime
            else:
               ime = ime + ' or {0}'.format(i.ime) 
        self.ime = ime + ')'

    def __repr__(self):
        return self.ime

    def vrni(self):
        return self.izjave

    def izracun(self,val):
        for v in self.izjave:
            if v.izracun(val)== True:
                return True
        return False
                            
    def poenostavi(self):
        for i in self.izjave:
            if type(i) is Fal:
                self.izjave.remove(i)
            elif type(i) is Tru:
                return Tru()
        if len(self.izjave) == 1:
            return self.izjave[0].poenostavi()
        return Or([i.poenostavi() for i in self.izjave])

class Not():
    def __init__(self,A):
        self.A = A
        self.ime = 'not{0}'.format(self.A.ime)

    def __repr__(self):
        return self.ime

    def vrni(self):
        return self.A

    def izracun(self,val):
        return not self.A.izracun(val)

    def poenostavi(self):
        if type(self.A) is Var:
            return self
        elif type(self.A) is And:
            return Or([Not(i).poenostavi() for i in self.A.vrni()])
        elif type(self.A) is Or:
            return And([Not(i).poenostavi() for i in self.A.vrni()])
        elif type(self.A) is Not:
            return self.A.vrni().poenostavi()



def test():
   a = Var('A')
   b = Var('B')
   c = Var('C')
   iz = Not(And([Or([Not(a),b]),Not(And([c,a])),Not(Or([Not(b),a,Not(c)]))]))
   val = {'A':False,'B':True,'C':True}
   print(iz)
   print(iz.poenostavi())
   print(iz.izracun(val))

    
