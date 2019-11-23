import Types as Tp

class Quad:
    def __init__(self, op, o1, o2, o3):
        self.op = op;
        self.o1 = o1;
        self.o2 = o2;
        self.o3 = o3;
        
    def ToStr(self):
        o1 = '\\' if self.o1 is None else 'id(%d)'%self.o1.value if self.o1.type == Tp.ID else 'va(%d)'%self.o1.value
        o2 = '\\' if self.o2 is None else 'id(%d)'%self.o2.value if self.o2.type == Tp.ID else 'va(%d)'%self.o2.value
        o3 = '\\' if self.o3 is None else '%d'%self.o3
        return "[%s,%s,%s,%s]"%(self.op, o1, o2, o3)