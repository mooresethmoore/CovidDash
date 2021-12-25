from vectors import Vec
from math import sqrt
class Vector:
    def __init__(self, domain, function={}):
        assert isinstance(domain,list)
        assert isinstance(function,dict)
        self.D=domain
        self.f=function
    def __getitem__(self,d):
        assert d in domain
        if d not in self.f: return 0
        else: return self.f[d]
    def __eq__(self,other):
        assert isinstance(other,Vector) or isinstance(other,Vec)
        fs=dict()
        fb=dict()
        if len(self.f)>0:
            fs={a:v for (a,v) in self.f.items() if v!=0}
        if len(other.f)>0:
            fb={a:v for (a,v) in other.f.items() if v!=0}
    def __add__(self,other):
        assert (isinstance(other,Vector) and other.D==self.D) or (isinstance(other,Vec) and set(other.D)==self.D)
        return Vector(self.D,{a:self.f[a] + other.f[a] for a in self.D})
    def __setitem__(self,d,val):
        assert d in self.D
        if val !=0:
            self.f[d] = val
    def __radd__(self, other): 
        "Hack to allow sum(...) to work with vectors"
        if other == 0:
            return self
        else:
            if isinstance(other,Vector) or isinstance(other,Vec):
                return add(self,other)
            else:
                return NotImplemented
    def __neg__(self):
        return Vector(self.D,{a:-b for (a,b) in self.items()})
    def __sub__(self,other):
        return add(-other,self)
    def __mul__(self,other):
        if isinstance(other,Vector) or isinstance(other,Vec):
            return vecdot(self,other)
        elif(isinstance(other,int) or isinstance(other,float)):
            return scalar_mult(self,other)
        else:
            return NotImplemented
    def scale(self,c):
        self.f={a:c*b for (a,b) in self.f.values()}
    def length(self):
        s=0
        for x in self.f.values():
            if isinstance(x,complex):
                s+=x*(x.real - x.imag * 1j)
            else:
                s+=x*x
        return sqrt(s)
    def normalize(self):
        l=self.length()
        self.f={x:self[x]/l for x in self.f}
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
    def __str__(v):
        "pretty-printing"
        D_list=v.D
        numdec = 3
        wd = dict([(k,(1+max(len(str(k)), len('{0:.{1}G}'.format(v[k], numdec))))) if isinstance(v[k], int) or isinstance(v[k], float) else (k,(1+max(len(str(k)), len(str(v[k]))))) for k in D_list])
        s1 = ''.join(['{0:>{1}}'.format(str(k),wd[k]) for k in D_list])
        s2 = ''.join(['{0:>{1}.{2}G}'.format(v[k],wd[k],numdec) if isinstance(v[k], int) or isinstance(v[k], float) else '{0:>{1}}'.format(v[k], wd[k]) for k in D_list])
        return "\n" + s1 + "\n" + '-'*sum(wd.values()) +"\n" + s2
    def __repr__(self):
        return "Vector(" + str(self.D) + "," + str(self.f) + ")"

    def __hash__(self):
        "Here we pretend Vecs are immutable so we can form sets of them"
        h = hash(frozenset(self.D))
        for k,v in sorted(self.f.items(), key = lambda x:repr(x[0])):
            if v != 0:
                h = hash((h, hash(v)))
        return h

    def copy(self):return Vector(self.D,self.f.copy())



def zero_vector(d): return Vector(d)

def add(v1,v2):
    assert isinstance(v1,Vector) and (isinstance(v2,Vector) and v2.D==v1.D) or (isinstance(v2,Vec) and set(v2.D)==v1.D)
    return Vector(self.D,{a:self.f[a] + other.f[a] for a in self.D})


def scalar_mult(v,c): return Vector(v.D,{d:c*val for d,val in v.f.items()})

def neg(v): return scalar_mult(v,-1)

def getitem(self,k):return self.f[k] if k in self.f else 0

def setitem(self,k,v): 
    assert k in self.D
    self.f[k]=v

def vecdot(v1,v2):
    assert v1.D==v2.D
    return sum([v1[x]*v2[x] for x in v1.D])

def triangular_solve(rowlist,b):
    x=zero_vector(rowlist[0].D)
    n=len(x.D)
    for i in reversed(range(n)):
        x.f[x.D[i]]=(b.f[b.D[i]]-vecdot(x,rowlist[i]))/rowlist[i].f[x.D[i]]
    return x
    


