import math
class Vec:
    def __init__(self,labels,function):
        self.D = labels # Domain
        self.f = function # Non-zero Values

    def setitem(self,d,val):
        assert d in self.D
        if val !=0:
            self.f[d] = val
    def __setitem__(self,d,val):
        assert d in self.D
        if val !=0:
            self.f[d] = val

    def getitem(self,k):return self.f[k] if k in self.f else 0

    def __getitem__(self,k):return self.f[k] if k in self.f else 0

    def scale(self,r): self.f = {self.f[i] * r for i in self.f}

    def copy(self): return Vec(self.D,self.f.copy())

    def print(self): return [str(i) + " = " + str(self.getitem(i)) for i in sorted(self.D,key=hash)]

    def __str__(v):
        "pretty-printing"
        D_list = sorted(v.D, key=repr)
        numdec = 3
        wd = dict([(k,(1+max(len(str(k)), len('{0:.{1}G}'.format(v[k], numdec))))) if isinstance(v[k], int) or isinstance(v[k], float) else (k,(1+max(len(str(k)), len(str(v[k]))))) for k in D_list])
        s1 = ''.join(['{0:>{1}}'.format(str(k),wd[k]) for k in D_list])
        s2 = ''.join(['{0:>{1}.{2}G}'.format(v[k],wd[k],numdec) if isinstance(v[k], int) or isinstance(v[k], float) else '{0:>{1}}'.format(v[k], wd[k]) for k in D_list])
        return "\n" + s1 + "\n" + '-'*sum(wd.values()) +"\n" + s2

    def __hash__(self):
        "Here we pretend Vecs are immutable so we can form sets of them"
        h = hash(frozenset(self.D))
        for k,v in sorted(self.f.items(), key = lambda x:repr(x[0])):
            if v != 0:
                h = hash((h, hash(v)))
        return h

    def __repr__(self):
        return "Vec(" + str(self.D) + "," + str(self.f) + ")"
    
    def is_almost_zero(self):
        s = 0
        for x in self.f.values():
            if isinstance(x, int) or isinstance(x, float):
                s += x*x
            elif isinstance(x, complex):
                y = abs(x)
                s += y*y
            else: return False
        return s < 1e-20
    
    def equals(self,other): 
        #assert isinstance(other,Vector) or isinstance(other,Vec)
        assert isinstance(other,Vec)
        fs=dict()
        fb=dict()
        if len(self.f)>0:
            fs={a:v for (a,v) in self.f.items() if v!=0}
        if len(other.f)>0:
            fb={a:v for (a,v) in other.f.items() if v!=0}
        return fs==fb and set(self.D)==set(other.D)
    def length(self):
        s=0
        for x in self.f.values():
            if isinstance(x,complex):
                s+=x*(x.real - x.imag * 1j)
            else:
                s+=x*x
        return math.sqrt(s)
    def normalize(self):
        l=self.length()
        self.f={x:self[x]/l for x in self.f}

    def __mul__(self,other):
        if isinstance(other,Vec):
            return vecdot(self,other)
        elif(isinstance(other,int) or isinstance(other,float)):
            return scalar_mult(self,other)
        else:
            return NotImplemented

    def __radd__(self, other): 
        "Hack to allow sum(...) to work with vectors"
        if other == 0:
            return self
        else:
            if isinstance(other,Vec):
                return add(self,other)
            else:
                return NotImplemented


    def __eq__(a,b): return a.equals(b)
    
    def __add__(a,b):
        return add(a,b)
    
    def __sub__(a,b): return a+neg(b)

    def __iter__(self):
        raise TypeError('%r object is not iterable' % self.__class__.__name__)
    
    def apply(self, func=lambda x: x):
        self.f={a:func(self[a]) for a in self.f}

    def total(self):
        return sum(self.f.values())
        
    def freq(self):
        l=sum(self.f.values())
        v=self.copy()
        v.f={a:v[a]/l for a in v.f}
        return v

def dist(v1,v2):
    assert v1.D==v2.D
    return math.sqrt(sum({(v1[x]-v2[x])**2 for x in v1.D}))

def zero_vec(D): return Vec(D,{})  

def scale(a,r): a.f = {k:b * r for (k,b) in a.f.items()}

def scalar_mult(v,c): return Vec(v.D,{d:c*val for d,val in v.f.items()})

def setitem(self,d,val): self.f[d] = val

def getitem(self,k): return self.f[k] if k in self.f else 0
            
def add(a,b):
    v = zero_vec(a.D|b.D)
    v.f = {i:a.getitem(i) + b.getitem(i) for i in v.D}
    return v
    
def neg(v): return scalar_mult(v,-1)

def vecdot(a,b):
    assert a.D==b.D
    return sum([a.getitem(i)*b.getitem(i) for i in a.D])

def listdot(a,b): return sum([a*b for (a,b) in zip(a,b)])

def triangular_solve_n(rowlist,b): # for list of row vectors for an upper triangular with no diag entries = 0
    D = rowlist[0].D
    n = len(D)
    assert D == set(range(n))
    x = zero_vec(D)
    for i in reversed(range(n)):
        x.f[i]=(b[i]-vecdot(x,rowlist[i]))/rowlist[i].f[i]
    return x

def triangular_solve(rowlist,label_list,b): # for up-tri system for label_list vector/no zero diag 
    x = zero_vec(set(label_list))
    for i in reversed(range(len(b))):
        x.f[label_list[i]]=(b[i]-vecdot(x,rowlist[i]))/rowlist[i].f[i]
    return x



