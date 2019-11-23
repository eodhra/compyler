import re
from Dyad import Dyad
import Types as Tp
from Quad import Quad
import Elements as El

opName = {Tp.EQUAL:'E', Tp.GR:'G', Tp.GRE:'GE', Tp.LE:'L', Tp.LEE:'LE', Tp.NE:'NE'}

class MidCoder:
    def __init__(self, idHolder):
        self.s = [0]
        self.c = [Dyad(Tp.EOF, None)]
        self.q = [Quad(None, None, None, None)]
        self.seq = None
        self.cptr = None
        self.idx = -1
        self.flag = Tp.NONE
        self.quadNum = 1
        self.idHolder = idHolder
    
    def Init(self):
        self.s = [0]
        self.c = [Dyad(Tp.EOF, None)]
        self.q = [Quad(None, None, None, None)]
        self.seq = None
        self.cptr = None
        self.idx = -1
        self.flag = Tp.NONE
        self.quadNum = 1
    
    def SetSeq(self, seq):
        self.seq = seq
        self.cptr = None
        self.idx = -1
    
    def GetNext(self):
        if self.flag != Tp.NONE:
            return
            
        self.idx += 1
        if self.idx >= len(self.seq):
            self.idx = -1
            self.cptr = None
            self.flag = Tp.SEQENDS
        else:
            self.cptr = self.seq[self.idx]
    
    def ShowState(self):
        if self.cptr == None:
            print('cptr : null')
        else:
            print('cptr : %d'%self.cptr.head)
        self.PrintStacks()
        print()
    
    def GetQuads(self):
        return self.q[1:]
    
    def PrintStacks(self):
        print('s : ', end = '')
        for e in self.s:
            print(e, end = ' ')
        print()
        print('c : ', end = '')
        for e in self.c:
            print(e.head, end = ' ')
        print()
    
    def Do(self, ds):
        if ds == None or ds == []:
            return self.flag
        if self.flag > Tp.SEQENDS:
            return self.flag
        self.flag = Tp.NONE
        self.SetSeq(ds)
        self.GetNext()
        while True:
            self.Act()
            self.Goto()
            #self.ShowState()
            if self.flag != Tp.NONE:
                return self.flag
        return self.flag
    
    def NewQuad(self, op, o1, o2, o3):
        self.q.append(Quad(op, o1, o2, o3))
        self.quadNum += 1
    
    def NewTemp(self):
        return self.idHolder.AddID('')
    
    def BackPatch(self, l, value):
        for e in l:
            self.q[e].o3 = value
    
    def Goto(self):
        if self.flag > Tp.SEQENDS:
            return
            
        elif self.s[-1] == 0 and self.c[-1].head == Tp.INT:
            self.s.append(2)

        elif self.s[-1] == 0 and self.c[-1].head == Tp.VOID:
            self.s.append(3)

        elif self.s[-1] == 2 and self.c[-1].head == Tp.ID:
            self.s.append(4)

        elif self.s[-1] == 3 and self.c[-1].head == Tp.ID:
            self.s.append(5)

        elif self.s[-1] == 4 and self.c[-1].head == Tp.LPAR:
            self.s.append(6)

        elif self.s[-1] == 5 and self.c[-1].head == Tp.LPAR:
            self.s.append(7)

        elif self.s[-1] == 6 and self.c[-1].head == Tp.RPAR:
            self.s.append(8)

        elif self.s[-1] == 7 and self.c[-1].head == Tp.RPAR:
            self.s.append(9)

        elif self.s[-1] == 8 and self.c[-1].head == Tp.LBR:
            self.s.append(11)

        elif self.s[-1] == 9 and self.c[-1].head == Tp.LBR:
            self.s.append(11)

        elif self.s[-1] == 11 and self.c[-1].head == Tp.INT:
            self.s.append(13)

        elif self.s[-1] == 11 and self.c[-1].head == Tp.ID:
            self.s.append(14)

        elif self.s[-1] == 11 and self.c[-1].head == Tp.RETURN:
            self.s.append(18)

        elif self.s[-1] == 11 and self.c[-1].head == Tp.WHILE:
            self.s.append(19)

        elif self.s[-1] == 11 and self.c[-1].head == Tp.IF:
            self.s.append(20)

        elif self.s[-1] == 13 and self.c[-1].head == Tp.ID:
            self.s.append(21)

        elif self.s[-1] == 14 and self.c[-1].head == Tp.ASSIGN:
            self.s.append(22)

        elif self.s[-1] == 15 and self.c[-1].head == Tp.RBR:
            self.s.append(23)

        elif self.s[-1] == 16 and self.c[-1].head == Tp.ID:
            self.s.append(14)

        elif self.s[-1] == 16 and self.c[-1].head == Tp.RETURN:
            self.s.append(18)

        elif self.s[-1] == 16 and self.c[-1].head == Tp.WHILE:
            self.s.append(19)

        elif self.s[-1] == 16 and self.c[-1].head == Tp.IF:
            self.s.append(20)

        elif self.s[-1] == 18 and self.c[-1].head == Tp.ID:
            self.s.append(26)

        elif self.s[-1] == 18 and self.c[-1].head == Tp.LPAR:
            self.s.append(27)

        elif self.s[-1] == 18 and self.c[-1].head == Tp.SEMICOL:
            self.s.append(28)

        elif self.s[-1] == 18 and self.c[-1].head == Tp.VALUE:
            self.s.append(33)

        elif self.s[-1] == 20 and self.c[-1].head == Tp.LPAR:
            self.s.append(35)

        elif self.s[-1] == 21 and self.c[-1].head == Tp.SEMICOL:
            self.s.append(36)

        elif self.s[-1] == 22 and self.c[-1].head == Tp.ID:
            self.s.append(26)

        elif self.s[-1] == 22 and self.c[-1].head == Tp.LPAR:
            self.s.append(27)

        elif self.s[-1] == 22 and self.c[-1].head == Tp.VALUE:
            self.s.append(33)

        elif self.s[-1] == 24 and self.c[-1].head == Tp.RBR:
            self.s.append(38)

        elif self.s[-1] == 25 and self.c[-1].head == Tp.ID:
            self.s.append(14)

        elif self.s[-1] == 25 and self.c[-1].head == Tp.RETURN:
            self.s.append(18)

        elif self.s[-1] == 25 and self.c[-1].head == Tp.WHILE:
            self.s.append(19)

        elif self.s[-1] == 25 and self.c[-1].head == Tp.IF:
            self.s.append(20)

        elif self.s[-1] == 27 and self.c[-1].head == Tp.ID:
            self.s.append(26)

        elif self.s[-1] == 27 and self.c[-1].head == Tp.LPAR:
            self.s.append(27)

        elif self.s[-1] == 27 and self.c[-1].head == Tp.VALUE:
            self.s.append(33)

        elif self.s[-1] == 29 and self.c[-1].head == Tp.SEMICOL:
            self.s.append(41)

        elif self.s[-1] == 30 and self.c[-1].head == Tp.RELOP:
            self.s.append(42)

        elif self.s[-1] == 31 and self.c[-1].head == Tp.ADD:
            self.s.append(43)

        elif self.s[-1] == 31 and self.c[-1].head == Tp.SUB:
            self.s.append(44)

        elif self.s[-1] == 32 and self.c[-1].head == Tp.MULT:
            self.s.append(45)

        elif self.s[-1] == 32 and self.c[-1].head == Tp.DIV:
            self.s.append(46)

        elif self.s[-1] == 34 and self.c[-1].head == Tp.LPAR:
            self.s.append(47)

        elif self.s[-1] == 35 and self.c[-1].head == Tp.ID:
            self.s.append(26)

        elif self.s[-1] == 35 and self.c[-1].head == Tp.LPAR:
            self.s.append(27)

        elif self.s[-1] == 35 and self.c[-1].head == Tp.VALUE:
            self.s.append(33)

        elif self.s[-1] == 36 and self.c[-1].head == Tp.INT:
            self.s.append(13)

        elif self.s[-1] == 37 and self.c[-1].head == Tp.SEMICOL:
            self.s.append(51)

        elif self.s[-1] == 40 and self.c[-1].head == Tp.RPAR:
            self.s.append(52)

        elif self.s[-1] == 42 and self.c[-1].head == Tp.ID:
            self.s.append(26)

        elif self.s[-1] == 42 and self.c[-1].head == Tp.LPAR:
            self.s.append(27)

        elif self.s[-1] == 42 and self.c[-1].head == Tp.VALUE:
            self.s.append(33)

        elif self.s[-1] == 43 and self.c[-1].head == Tp.ID:
            self.s.append(26)

        elif self.s[-1] == 43 and self.c[-1].head == Tp.LPAR:
            self.s.append(27)

        elif self.s[-1] == 43 and self.c[-1].head == Tp.VALUE:
            self.s.append(33)

        elif self.s[-1] == 44 and self.c[-1].head == Tp.ID:
            self.s.append(26)

        elif self.s[-1] == 44 and self.c[-1].head == Tp.LPAR:
            self.s.append(27)

        elif self.s[-1] == 44 and self.c[-1].head == Tp.VALUE:
            self.s.append(33)

        elif self.s[-1] == 45 and self.c[-1].head == Tp.ID:
            self.s.append(26)

        elif self.s[-1] == 45 and self.c[-1].head == Tp.LPAR:
            self.s.append(27)

        elif self.s[-1] == 45 and self.c[-1].head == Tp.VALUE:
            self.s.append(33)

        elif self.s[-1] == 46 and self.c[-1].head == Tp.ID:
            self.s.append(26)

        elif self.s[-1] == 46 and self.c[-1].head == Tp.LPAR:
            self.s.append(27)

        elif self.s[-1] == 46 and self.c[-1].head == Tp.VALUE:
            self.s.append(33)

        elif self.s[-1] == 47 and self.c[-1].head == Tp.ID:
            self.s.append(26)

        elif self.s[-1] == 47 and self.c[-1].head == Tp.LPAR:
            self.s.append(27)

        elif self.s[-1] == 47 and self.c[-1].head == Tp.VALUE:
            self.s.append(33)

        elif self.s[-1] == 49 and self.c[-1].head == Tp.RPAR:
            self.s.append(59)

        elif self.s[-1] == 58 and self.c[-1].head == Tp.RPAR:
            self.s.append(60)

        elif self.s[-1] == 61 and self.c[-1].head == Tp.LBR:
            self.s.append(11)

        elif self.s[-1] == 62 and self.c[-1].head == Tp.LBR:
            self.s.append(11)

        elif self.s[-1] == 65 and self.c[-1].head == Tp.ELSE:
            self.s.append(66)

        elif self.s[-1] == 67 and self.c[-1].head == Tp.LBR:
            self.s.append(11)

        elif self.s[-1] == 0 and self.c[-1].head == Tp.P:
            self.s.append(1)

        elif self.s[-1] == 8 and self.c[-1].head == Tp.B:
            self.s.append(10)

        elif self.s[-1] == 9 and self.c[-1].head == Tp.B:
            self.s.append(12)

        elif self.s[-1] == 11 and self.c[-1].head == Tp.S:
            self.s.append(15)

        elif self.s[-1] == 11 and self.c[-1].head == Tp.D:
            self.s.append(16)

        elif self.s[-1] == 11 and self.c[-1].head == Tp.L:
            self.s.append(17)

        elif self.s[-1] == 16 and self.c[-1].head == Tp.S:
            self.s.append(24)

        elif self.s[-1] == 16 and self.c[-1].head == Tp.L:
            self.s.append(17)

        elif self.s[-1] == 17 and self.c[-1].head == Tp.M:
            self.s.append(25)

        elif self.s[-1] == 18 and self.c[-1].head == Tp.E:
            self.s.append(29)

        elif self.s[-1] == 18 and self.c[-1].head == Tp.A:
            self.s.append(30)

        elif self.s[-1] == 18 and self.c[-1].head == Tp.I:
            self.s.append(31)

        elif self.s[-1] == 18 and self.c[-1].head == Tp.F:
            self.s.append(32)

        elif self.s[-1] == 19 and self.c[-1].head == Tp.M:
            self.s.append(34)

        elif self.s[-1] == 22 and self.c[-1].head == Tp.E:
            self.s.append(37)

        elif self.s[-1] == 22 and self.c[-1].head == Tp.A:
            self.s.append(30)

        elif self.s[-1] == 22 and self.c[-1].head == Tp.I:
            self.s.append(31)

        elif self.s[-1] == 22 and self.c[-1].head == Tp.F:
            self.s.append(32)

        elif self.s[-1] == 25 and self.c[-1].head == Tp.S:
            self.s.append(39)

        elif self.s[-1] == 25 and self.c[-1].head == Tp.L:
            self.s.append(17)

        elif self.s[-1] == 27 and self.c[-1].head == Tp.E:
            self.s.append(40)

        elif self.s[-1] == 27 and self.c[-1].head == Tp.A:
            self.s.append(30)

        elif self.s[-1] == 27 and self.c[-1].head == Tp.I:
            self.s.append(31)

        elif self.s[-1] == 27 and self.c[-1].head == Tp.F:
            self.s.append(32)

        elif self.s[-1] == 35 and self.c[-1].head == Tp.E:
            self.s.append(48)

        elif self.s[-1] == 35 and self.c[-1].head == Tp.C:
            self.s.append(49)

        elif self.s[-1] == 35 and self.c[-1].head == Tp.A:
            self.s.append(30)

        elif self.s[-1] == 35 and self.c[-1].head == Tp.I:
            self.s.append(31)

        elif self.s[-1] == 35 and self.c[-1].head == Tp.F:
            self.s.append(32)

        elif self.s[-1] == 36 and self.c[-1].head == Tp.D:
            self.s.append(50)

        elif self.s[-1] == 42 and self.c[-1].head == Tp.E:
            self.s.append(53)

        elif self.s[-1] == 42 and self.c[-1].head == Tp.A:
            self.s.append(30)

        elif self.s[-1] == 42 and self.c[-1].head == Tp.I:
            self.s.append(31)

        elif self.s[-1] == 42 and self.c[-1].head == Tp.F:
            self.s.append(32)

        elif self.s[-1] == 43 and self.c[-1].head == Tp.A:
            self.s.append(54)

        elif self.s[-1] == 43 and self.c[-1].head == Tp.I:
            self.s.append(31)

        elif self.s[-1] == 43 and self.c[-1].head == Tp.F:
            self.s.append(32)

        elif self.s[-1] == 44 and self.c[-1].head == Tp.A:
            self.s.append(55)

        elif self.s[-1] == 44 and self.c[-1].head == Tp.I:
            self.s.append(31)

        elif self.s[-1] == 44 and self.c[-1].head == Tp.F:
            self.s.append(32)

        elif self.s[-1] == 45 and self.c[-1].head == Tp.I:
            self.s.append(56)

        elif self.s[-1] == 45 and self.c[-1].head == Tp.F:
            self.s.append(32)

        elif self.s[-1] == 46 and self.c[-1].head == Tp.I:
            self.s.append(57)

        elif self.s[-1] == 46 and self.c[-1].head == Tp.F:
            self.s.append(32)

        elif self.s[-1] == 47 and self.c[-1].head == Tp.E:
            self.s.append(48)

        elif self.s[-1] == 47 and self.c[-1].head == Tp.C:
            self.s.append(58)

        elif self.s[-1] == 47 and self.c[-1].head == Tp.A:
            self.s.append(30)

        elif self.s[-1] == 47 and self.c[-1].head == Tp.I:
            self.s.append(31)

        elif self.s[-1] == 47 and self.c[-1].head == Tp.F:
            self.s.append(32)

        elif self.s[-1] == 59 and self.c[-1].head == Tp.M:
            self.s.append(61)

        elif self.s[-1] == 60 and self.c[-1].head == Tp.M:
            self.s.append(62)

        elif self.s[-1] == 61 and self.c[-1].head == Tp.B:
            self.s.append(63)

        elif self.s[-1] == 62 and self.c[-1].head == Tp.B:
            self.s.append(64)

        elif self.s[-1] == 63 and self.c[-1].head == Tp.N:
            self.s.append(65)

        elif self.s[-1] == 66 and self.c[-1].head == Tp.M:
            self.s.append(67)

        elif self.s[-1] == 67 and self.c[-1].head == Tp.B:
            self.s.append(68)
            
    def Act(self):       
        if self.flag != Tp.NONE:
            return
            
        elif self.s[-1] == 0 and self.cptr.head == Tp.INT:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 0 and self.cptr.head == Tp.VOID:
            self.c.append(self.cptr)
            self.GetNext()
            
        elif self.s[-1] == 0 and self.cptr.head == Tp.EOF:
            self.flag = Tp.ACC
            
        elif self.s[-1] == 1 and self.cptr.head == Tp.EOF:
            self.flag = Tp.ACC

        elif self.s[-1] == 2 and self.cptr.head == Tp.ID:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 3 and self.cptr.head == Tp.ID:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 4 and self.cptr.head == Tp.LPAR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 5 and self.cptr.head == Tp.LPAR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 6 and self.cptr.head == Tp.RPAR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 7 and self.cptr.head == Tp.RPAR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 8 and self.cptr.head == Tp.LBR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 9 and self.cptr.head == Tp.LBR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 10 and self.cptr.head == Tp.EOF:
            pops = []
            for i in range(5):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.P, None))

        elif self.s[-1] == 11 and self.cptr.head == Tp.INT:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 11 and self.cptr.head == Tp.ID:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 11 and self.cptr.head == Tp.RETURN:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 11 and self.cptr.head == Tp.WHILE:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 11 and self.cptr.head == Tp.IF:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 12 and self.cptr.head == Tp.EOF:
            pops = []
            for i in range(5):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.P, None))

        elif self.s[-1] == 13 and self.cptr.head == Tp.ID:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 14 and self.cptr.head == Tp.ASSIGN:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 15 and self.cptr.head == Tp.RBR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 16 and self.cptr.head == Tp.ID:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 16 and self.cptr.head == Tp.RETURN:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 16 and self.cptr.head == Tp.WHILE:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 16 and self.cptr.head == Tp.IF:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 17 and self.cptr.head == Tp.RBR:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.S, El.S(pops[0].body.nList)))

        elif self.s[-1] == 17 and self.cptr.head == Tp.ID:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 17 and self.cptr.head == Tp.RETURN:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 17 and self.cptr.head == Tp.WHILE:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 17 and self.cptr.head == Tp.IF:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 17 and self.cptr.head == Tp.VALUE:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 17 and self.cptr.head == Tp.LPAR:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 17 and self.cptr.head == Tp.LBR:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 18 and self.cptr.head == Tp.ID:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 18 and self.cptr.head == Tp.LPAR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 18 and self.cptr.head == Tp.SEMICOL:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 18 and self.cptr.head == Tp.VALUE:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 19 and self.cptr.head == Tp.ID:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 19 and self.cptr.head == Tp.RETURN:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 19 and self.cptr.head == Tp.WHILE:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 19 and self.cptr.head == Tp.IF:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 19 and self.cptr.head == Tp.VALUE:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 19 and self.cptr.head == Tp.LPAR:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 19 and self.cptr.head == Tp.LBR:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 20 and self.cptr.head == Tp.LPAR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 21 and self.cptr.head == Tp.SEMICOL:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 22 and self.cptr.head == Tp.ID:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 22 and self.cptr.head == Tp.LPAR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 22 and self.cptr.head == Tp.VALUE:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 23 and self.cptr.head == Tp.EOF:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.B, El.B(pops[1].body.nList)))

        elif self.s[-1] == 23 and self.cptr.head == Tp.ELSE:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.B, El.B(pops[1].body.nList)))

        elif self.s[-1] == 23 and self.cptr.head == Tp.RBR:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.B, El.B(pops[1].body.nList)))

        elif self.s[-1] == 23 and self.cptr.head == Tp.ID:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.B, El.B(pops[1].body.nList)))

        elif self.s[-1] == 23 and self.cptr.head == Tp.RETURN:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.B, El.B(pops[1].body.nList)))

        elif self.s[-1] == 23 and self.cptr.head == Tp.WHILE:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.B, El.B(pops[1].body.nList)))

        elif self.s[-1] == 23 and self.cptr.head == Tp.IF:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.B, El.B(pops[1].body.nList)))

        elif self.s[-1] == 24 and self.cptr.head == Tp.RBR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 25 and self.cptr.head == Tp.ID:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 25 and self.cptr.head == Tp.RETURN:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 25 and self.cptr.head == Tp.WHILE:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 25 and self.cptr.head == Tp.IF:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 26 and self.cptr.head == Tp.SEMICOL:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.F, El.F(El.Place(Tp.ID, pops[0].body))))

        elif self.s[-1] == 26 and self.cptr.head == Tp.RPAR:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.F, El.F(El.Place(Tp.ID, pops[0].body))))

        elif self.s[-1] == 26 and self.cptr.head == Tp.RELOP:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.F, El.F(El.Place(Tp.ID, pops[0].body))))

        elif self.s[-1] == 26 and self.cptr.head == Tp.ADD:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.F, El.F(El.Place(Tp.ID, pops[0].body))))

        elif self.s[-1] == 26 and self.cptr.head == Tp.SUB:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.F, El.F(El.Place(Tp.ID, pops[0].body))))

        elif self.s[-1] == 26 and self.cptr.head == Tp.MULT:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.F, El.F(El.Place(Tp.ID, pops[0].body))))

        elif self.s[-1] == 26 and self.cptr.head == Tp.DIV:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.F, El.F(El.Place(Tp.ID, pops[0].body))))

        elif self.s[-1] == 27 and self.cptr.head == Tp.ID:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 27 and self.cptr.head == Tp.LPAR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 27 and self.cptr.head == Tp.VALUE:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 28 and self.cptr.head == Tp.RBR:
            pops = []
            for i in range(2):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.L, El.L([])))
            self.NewQuad('RET', None, None, None)

        elif self.s[-1] == 28 and self.cptr.head == Tp.ID:
            pops = []
            for i in range(2):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.L, El.L([])))
            self.NewQuad('RET', None, None, None)

        elif self.s[-1] == 28 and self.cptr.head == Tp.RETURN:
            pops = []
            for i in range(2):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.L, El.L([])))
            self.NewQuad('RET', None, None, None)

        elif self.s[-1] == 28 and self.cptr.head == Tp.WHILE:
            pops = []
            for i in range(2):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.L, El.L([])))
            self.NewQuad('RET', None, None, None)

        elif self.s[-1] == 28 and self.cptr.head == Tp.IF:
            pops = []
            for i in range(2):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.L, El.L([])))
            self.NewQuad('RET', None, None, None)

        elif self.s[-1] == 29 and self.cptr.head == Tp.SEMICOL:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 30 and self.cptr.head == Tp.RELOP:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 30 and self.cptr.head == Tp.SEMICOL:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.E, El.E(pops[0].body.place)))

        elif self.s[-1] == 30 and self.cptr.head == Tp.RPAR:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.E, El.E(pops[0].body.place)))

        elif self.s[-1] == 31 and self.cptr.head == Tp.ADD:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 31 and self.cptr.head == Tp.SUB:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 31 and self.cptr.head == Tp.SEMICOL:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.A, El.A(pops[0].body.place)))

        elif self.s[-1] == 31 and self.cptr.head == Tp.RPAR:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.A, El.A(pops[0].body.place)))

        elif self.s[-1] == 31 and self.cptr.head == Tp.RELOP:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.A, El.A(pops[0].body.place)))

        elif self.s[-1] == 32 and self.cptr.head == Tp.MULT:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 32 and self.cptr.head == Tp.DIV:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 32 and self.cptr.head == Tp.SEMICOL:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.I, El.I(pops[0].body.place)))

        elif self.s[-1] == 32 and self.cptr.head == Tp.RPAR:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.I, El.I(pops[0].body.place)))

        elif self.s[-1] == 32 and self.cptr.head == Tp.RELOP:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.I, El.I(pops[0].body.place)))

        elif self.s[-1] == 32 and self.cptr.head == Tp.ADD:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.I, El.I(pops[0].body.place)))

        elif self.s[-1] == 32 and self.cptr.head == Tp.SUB:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.I, El.I(pops[0].body.place)))

        elif self.s[-1] == 33 and self.cptr.head == Tp.SEMICOL:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.F, El.F(El.Place(Tp.VALUE, pops[0].body))))

        elif self.s[-1] == 33 and self.cptr.head == Tp.RPAR:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.F, El.F(El.Place(Tp.VALUE, pops[0].body))))

        elif self.s[-1] == 33 and self.cptr.head == Tp.RELOP:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.F, El.F(El.Place(Tp.VALUE, pops[0].body))))

        elif self.s[-1] == 33 and self.cptr.head == Tp.ADD:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.F, El.F(El.Place(Tp.VALUE, pops[0].body))))

        elif self.s[-1] == 33 and self.cptr.head == Tp.SUB:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.F, El.F(El.Place(Tp.VALUE, pops[0].body))))

        elif self.s[-1] == 33 and self.cptr.head == Tp.MULT:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.F, El.F(El.Place(Tp.VALUE, pops[0].body))))

        elif self.s[-1] == 33 and self.cptr.head == Tp.DIV:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.F, El.F(El.Place(Tp.VALUE, pops[0].body))))

        elif self.s[-1] == 34 and self.cptr.head == Tp.LPAR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 35 and self.cptr.head == Tp.ID:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 35 and self.cptr.head == Tp.LPAR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 35 and self.cptr.head == Tp.VALUE:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 36 and self.cptr.head == Tp.INT:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 36 and self.cptr.head == Tp.ID:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.D, None))

        elif self.s[-1] == 36 and self.cptr.head == Tp.RETURN:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.D, None))

        elif self.s[-1] == 36 and self.cptr.head == Tp.WHILE:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.D, None))

        elif self.s[-1] == 36 and self.cptr.head == Tp.IF:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.D, None))

        elif self.s[-1] == 37 and self.cptr.head == Tp.SEMICOL:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 38 and self.cptr.head == Tp.EOF:
            pops = []
            for i in range(4):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.B, El.B(pops[1].body.nList)))

        elif self.s[-1] == 38 and self.cptr.head == Tp.ELSE:
            pops = []
            for i in range(4):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.B, El.B(pops[1].body.nList)))

        elif self.s[-1] == 38 and self.cptr.head == Tp.RBR:
            pops = []
            for i in range(4):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.B, El.B(pops[1].body.nList)))

        elif self.s[-1] == 38 and self.cptr.head == Tp.ID:
            pops = []
            for i in range(4):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.B, El.B(pops[1].body.nList)))

        elif self.s[-1] == 38 and self.cptr.head == Tp.RETURN:
            pops = []
            for i in range(4):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.B, El.B(pops[1].body.nList)))

        elif self.s[-1] == 38 and self.cptr.head == Tp.WHILE:
            pops = []
            for i in range(4):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.B, El.B(pops[1].body.nList)))

        elif self.s[-1] == 38 and self.cptr.head == Tp.IF:
            pops = []
            for i in range(4):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.B, El.B(pops[1].body.nList)))

        elif self.s[-1] == 39 and self.cptr.head == Tp.RBR:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            self.BackPatch(pops[2].body.nList, pops[1].body.quad)
            self.c.append(Dyad(Tp.S, El.S(pops[0].body.nList)))

        elif self.s[-1] == 40 and self.cptr.head == Tp.RPAR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 41 and self.cptr.head == Tp.RBR:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            self.NewQuad('RET', pops[1].body.place, None, None)
            self.c.append(Dyad(Tp.L, El.L([])))

        elif self.s[-1] == 41 and self.cptr.head == Tp.ID:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            self.NewQuad('RET', pops[1].body.place, None, None)
            self.c.append(Dyad(Tp.L, El.L([])))

        elif self.s[-1] == 41 and self.cptr.head == Tp.RETURN:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            self.NewQuad('RET', pops[1].body.place, None, None)
            self.c.append(Dyad(Tp.L, El.L([])))

        elif self.s[-1] == 41 and self.cptr.head == Tp.WHILE:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            self.NewQuad('RET', pops[1].body.place, None, None)
            self.c.append(Dyad(Tp.L, El.L([])))

        elif self.s[-1] == 41 and self.cptr.head == Tp.IF:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            self.NewQuad('RET', pops[1].body.place, None, None)
            self.c.append(Dyad(Tp.L, El.L([])))

        elif self.s[-1] == 42 and self.cptr.head == Tp.ID:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 42 and self.cptr.head == Tp.LPAR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 42 and self.cptr.head == Tp.VALUE:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 43 and self.cptr.head == Tp.ID:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 43 and self.cptr.head == Tp.LPAR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 43 and self.cptr.head == Tp.VALUE:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 44 and self.cptr.head == Tp.ID:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 44 and self.cptr.head == Tp.LPAR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 44 and self.cptr.head == Tp.VALUE:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 45 and self.cptr.head == Tp.ID:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 45 and self.cptr.head == Tp.LPAR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 45 and self.cptr.head == Tp.VALUE:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 46 and self.cptr.head == Tp.ID:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 46 and self.cptr.head == Tp.LPAR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 46 and self.cptr.head == Tp.VALUE:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 47 and self.cptr.head == Tp.ID:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 47 and self.cptr.head == Tp.LPAR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 47 and self.cptr.head == Tp.VALUE:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 48 and self.cptr.head == Tp.RPAR:
            pops = []
            for i in range(1):
                self.s.pop()
                pops.append(self.c.pop())
            c = El.C()
            c.tList = [self.quadNum]
            c.fList = [self.quadNum + 1]
            self.c.append(Dyad(Tp.C, c))
            self.NewQuad('JNZ', pops[0].body.place, None, 0)
            self.NewQuad('J', None, None, 0)

        elif self.s[-1] == 49 and self.cptr.head == Tp.RPAR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 50 and self.cptr.head == Tp.ID:
            pops = []
            for i in range(4):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.D, None))

        elif self.s[-1] == 50 and self.cptr.head == Tp.RETURN:
            pops = []
            for i in range(4):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.D, None))

        elif self.s[-1] == 50 and self.cptr.head == Tp.WHILE:
            pops = []
            for i in range(4):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.D, None))

        elif self.s[-1] == 50 and self.cptr.head == Tp.IF:
            pops = []
            for i in range(4):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.D, None))

        elif self.s[-1] == 51 and self.cptr.head == Tp.RBR:
            pops = []
            for i in range(4):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.L, El.L([])))
            self.NewQuad('ASSIGN', pops[1].body.place, None, pops[3].body)

        elif self.s[-1] == 51 and self.cptr.head == Tp.ID:
            pops = []
            for i in range(4):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.L, El.L([])))
            self.NewQuad('ASSIGN', pops[1].body.place, None, pops[3].body)

        elif self.s[-1] == 51 and self.cptr.head == Tp.RETURN:
            pops = []
            for i in range(4):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.L, El.L([])))
            self.NewQuad('ASSIGN', pops[1].body.place, None, pops[3].body)

        elif self.s[-1] == 51 and self.cptr.head == Tp.WHILE:
            pops = []
            for i in range(4):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.L, El.L([])))
            self.NewQuad('ASSIGN', pops[1].body.place, None, pops[3].body)

        elif self.s[-1] == 51 and self.cptr.head == Tp.IF:
            pops = []
            for i in range(4):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.L, El.L([])))
            self.NewQuad('ASSIGN', pops[1].body.place, None, pops[3].body)

        elif self.s[-1] == 52 and self.cptr.head == Tp.SEMICOL:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.F, El.F(pops[1].body.place)))

        elif self.s[-1] == 52 and self.cptr.head == Tp.RPAR:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.F, El.F(pops[1].body.place)))

        elif self.s[-1] == 52 and self.cptr.head == Tp.RELOP:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.F, El.F(pops[1].body.place)))

        elif self.s[-1] == 52 and self.cptr.head == Tp.ADD:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.F, El.F(pops[1].body.place)))

        elif self.s[-1] == 52 and self.cptr.head == Tp.SUB:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.F, El.F(pops[1].body.place)))

        elif self.s[-1] == 52 and self.cptr.head == Tp.MULT:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.F, El.F(pops[1].body.place)))

        elif self.s[-1] == 52 and self.cptr.head == Tp.DIV:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            self.c.append(Dyad(Tp.F, El.F(pops[1].body.place)))

        elif self.s[-1] == 53 and self.cptr.head == Tp.SEMICOL:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            t = self.NewTemp()
            self.NewQuad('J%s'%opName[pops[1].body], pops[2].body.place, pops[0].body.place, self.quadNum + 3)
            self.NewQuad('ASSIGN', El.Place(Tp.VALUE, 0), None, t)
            self.NewQuad('J', None, None, self.quadNum + 2)
            self.NewQuad('ASSIGN', El.Place(Tp.VALUE, 1), None, t)
            self.c.append(Dyad(Tp.E, El.E(El.Place(Tp.ID, t))))

        elif self.s[-1] == 53 and self.cptr.head == Tp.RPAR:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            t = self.NewTemp()
            self.NewQuad('J%s'%opName[pops[1].body], pops[2].body.place, pops[0].body.place, self.quadNum + 3)
            self.NewQuad('ASSIGN', El.Place(Tp.VALUE, 0), None, t)
            self.NewQuad('J', None, None, self.quadNum + 2)
            self.NewQuad('ASSIGN', El.Place(Tp.VALUE, 1), None, t)
            self.c.append(Dyad(Tp.E, El.E(El.Place(Tp.ID, t))))

        elif self.s[-1] == 54 and self.cptr.head == Tp.SEMICOL:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            t = self.NewTemp()
            self.c.append(Dyad(Tp.A, El.A(El.Place(Tp.ID, t))))
            self.NewQuad('ADD', pops[2].body.place, pops[0].body.place, t)

        elif self.s[-1] == 54 and self.cptr.head == Tp.RPAR:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            t = self.NewTemp()
            self.c.append(Dyad(Tp.A, El.A(El.Place(Tp.ID, t))))
            self.NewQuad('ADD', pops[2].body.place, pops[0].body.place, t)

        elif self.s[-1] == 54 and self.cptr.head == Tp.RELOP:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            t = self.NewTemp()
            self.c.append(Dyad(Tp.A, El.A(El.Place(Tp.ID, t))))
            self.NewQuad('ADD', pops[2].body.place, pops[0].body.place, t)

        elif self.s[-1] == 55 and self.cptr.head == Tp.SEMICOL:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            t = self.NewTemp()
            self.c.append(Dyad(Tp.A, El.A(El.Place(Tp.ID, t))))
            self.NewQuad('SUB', pops[2].body.place, pops[0].body.place, t)

        elif self.s[-1] == 55 and self.cptr.head == Tp.RPAR:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            t = self.NewTemp()
            self.c.append(Dyad(Tp.A, El.A(El.Place(Tp.ID, t))))
            self.NewQuad('SUB', pops[2].body.place, pops[0].body.place, t)

        elif self.s[-1] == 55 and self.cptr.head == Tp.RELOP:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            t = self.NewTemp()
            self.c.append(Dyad(Tp.A, El.A(El.Place(Tp.ID, t))))
            self.NewQuad('SUB', pops[2].body.place, pops[0].body.place, t)

        elif self.s[-1] == 56 and self.cptr.head == Tp.SEMICOL:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            t = self.NewTemp()
            self.c.append(Dyad(Tp.I, El.I(El.Place(Tp.ID, t))))
            self.NewQuad('MULT', pops[2].body.place, pops[0].body.place, t)

        elif self.s[-1] == 56 and self.cptr.head == Tp.RPAR:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            t = self.NewTemp()
            self.c.append(Dyad(Tp.I, El.I(El.Place(Tp.ID, t))))
            self.NewQuad('MULT', pops[2].body.place, pops[0].body.place, t)

        elif self.s[-1] == 56 and self.cptr.head == Tp.RELOP:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            t = self.NewTemp()
            self.c.append(Dyad(Tp.I, El.I(El.Place(Tp.ID, t))))
            self.NewQuad('MULT', pops[2].body.place, pops[0].body.place, t)

        elif self.s[-1] == 56 and self.cptr.head == Tp.ADD:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            t = self.NewTemp()
            self.c.append(Dyad(Tp.I, El.I(El.Place(Tp.ID, t))))
            self.NewQuad('MULT', pops[2].body.place, pops[0].body.place, t)

        elif self.s[-1] == 56 and self.cptr.head == Tp.SUB:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            t = self.NewTemp()
            self.c.append(Dyad(Tp.I, El.I(El.Place(Tp.ID, t))))
            self.NewQuad('MULT', pops[2].body.place, pops[0].body.place, t)

        elif self.s[-1] == 57 and self.cptr.head == Tp.SEMICOL:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            t = self.NewTemp()
            self.c.append(Dyad(Tp.I, El.I(El.Place(Tp.ID, t))))
            self.NewQuad('DIV', pops[2].body.place, pops[0].body.place, t)

        elif self.s[-1] == 57 and self.cptr.head == Tp.RPAR:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            t = self.NewTemp()
            self.c.append(Dyad(Tp.I, El.I(El.Place(Tp.ID, t))))
            self.NewQuad('DIV', pops[2].body.place, pops[0].body.place, t)

        elif self.s[-1] == 57 and self.cptr.head == Tp.RELOP:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            t = self.NewTemp()
            self.c.append(Dyad(Tp.I, El.I(El.Place(Tp.ID, t))))
            self.NewQuad('DIV', pops[2].body.place, pops[0].body.place, t)

        elif self.s[-1] == 57 and self.cptr.head == Tp.ADD:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            t = self.NewTemp()
            self.c.append(Dyad(Tp.I, El.I(El.Place(Tp.ID, t))))
            self.NewQuad('DIV', pops[2].body.place, pops[0].body.place, t)

        elif self.s[-1] == 57 and self.cptr.head == Tp.SUB:
            pops = []
            for i in range(3):
                self.s.pop()
                pops.append(self.c.pop())
            t = self.NewTemp()
            self.c.append(Dyad(Tp.I, El.I(El.Place(Tp.ID, t))))
            self.NewQuad('DIV', pops[2].body.place, pops[0].body.place, t)

        elif self.s[-1] == 58 and self.cptr.head == Tp.RPAR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 59 and self.cptr.head == Tp.ID:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 59 and self.cptr.head == Tp.RETURN:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 59 and self.cptr.head == Tp.WHILE:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 59 and self.cptr.head == Tp.IF:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 59 and self.cptr.head == Tp.VALUE:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 59 and self.cptr.head == Tp.LPAR:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 59 and self.cptr.head == Tp.LBR:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 60 and self.cptr.head == Tp.ID:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 60 and self.cptr.head == Tp.RETURN:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 60 and self.cptr.head == Tp.WHILE:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 60 and self.cptr.head == Tp.IF:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 60 and self.cptr.head == Tp.VALUE:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 60 and self.cptr.head == Tp.LPAR:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 60 and self.cptr.head == Tp.LBR:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 61 and self.cptr.head == Tp.LBR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 62 and self.cptr.head == Tp.LBR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 63 and self.cptr.head == Tp.RBR:
            pops = []
            for i in range(6):
                self.s.pop()
                pops.append(self.c.pop())
            self.BackPatch(pops[3].body.tList, pop[1].body.quad)
            self.c.append(Dyad(Tp.L, El.L(pops[3].body.fList + pops[0].body.nList)))

        elif self.s[-1] == 63 and self.cptr.head == Tp.ID:
            pops = []
            for i in range(6):
                self.s.pop()
                pops.append(self.c.pop())
            self.BackPatch(pops[3].body.tList, pop[1].body.quad)
            self.c.append(Dyad(Tp.L, El.L(pops[3].body.fList + pops[0].body.nList)))

        elif self.s[-1] == 63 and self.cptr.head == Tp.RETURN:
            pops = []
            for i in range(6):
                self.s.pop()
                pops.append(self.c.pop())
            self.BackPatch(pops[3].body.tList, pop[1].body.quad)
            self.c.append(Dyad(Tp.L, El.L(pops[3].body.fList + pops[0].body.nList)))

        elif self.s[-1] == 63 and self.cptr.head == Tp.WHILE:
            pops = []
            for i in range(6):
                self.s.pop()
                pops.append(self.c.pop())
            self.BackPatch(pops[3].body.tList, pop[1].body.quad)
            self.c.append(Dyad(Tp.L, El.L(pops[3].body.fList + pops[0].body.nList)))

        elif self.s[-1] == 63 and self.cptr.head == Tp.IF:
            pops = []
            for i in range(6):
                self.s.pop()
                pops.append(self.c.pop())
            self.BackPatch(pops[3].body.tList, pop[1].body.quad)
            self.c.append(Dyad(Tp.L, El.L(pops[3].body.fList + pops[0].body.nList)))

        elif self.s[-1] == 63 and self.cptr.head == Tp.ELSE:
            self.c.append(Dyad(Tp.N, El.N([self.quadNum])))
            self.NewQuad('J', None, None, 0)

        elif self.s[-1] == 64 and self.cptr.head == Tp.RBR:
            pops = []
            for i in range(7):
                self.s.pop()
                pops.append(self.c.pop())
            self.BackPatch(pops[0].body.nList, pops[5].body.quad)
            self.BackPatch(pops[3].body.tList, pops[1].body.quad)
            self.c.append(Dyad(Tp.L, El.L(pops[3].body.fList)))
            self.NewQuad('J', None, None, pops[5].body.quad)

        elif self.s[-1] == 64 and self.cptr.head == Tp.ID:
            pops = []
            for i in range(7):
                self.s.pop()
                pops.append(self.c.pop())
            self.BackPatch(pops[0].body.nList, pops[5].body.quad)
            self.BackPatch(pops[3].body.tList, pops[1].body.quad)
            self.c.append(Dyad(Tp.L, El.L(pops[3].body.fList)))
            self.NewQuad('J', None, None, pops[5].body.quad)

        elif self.s[-1] == 64 and self.cptr.head == Tp.RETURN:
            pops = []
            for i in range(7):
                self.s.pop()
                pops.append(self.c.pop())
            self.BackPatch(pops[0].body.nList, pops[5].body.quad)
            self.BackPatch(pops[3].body.tList, pops[1].body.quad)
            self.c.append(Dyad(Tp.L, El.L(pops[3].body.fList)))
            self.NewQuad('J', None, None, pops[5].body.quad)

        elif self.s[-1] == 64 and self.cptr.head == Tp.WHILE:
            pops = []
            for i in range(7):
                self.s.pop()
                pops.append(self.c.pop())
            self.BackPatch(pops[0].body.nList, pops[5].body.quad)
            self.BackPatch(pops[3].body.tList, pops[1].body.quad)
            self.c.append(Dyad(Tp.L, El.L(pops[3].body.fList)))
            self.NewQuad('J', None, None, pops[5].body.quad)

        elif self.s[-1] == 64 and self.cptr.head == Tp.IF:
            pops = []
            for i in range(7):
                self.s.pop()
                pops.append(self.c.pop())
            self.BackPatch(pops[0].body.nList, pops[5].body.quad)
            self.BackPatch(pops[3].body.tList, pops[1].body.quad)
            self.c.append(Dyad(Tp.L, El.L(pops[3].body.fList)))
            self.NewQuad('J', None, None, pops[5].body.quad)

        elif self.s[-1] == 65 and self.cptr.head == Tp.ELSE:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 66 and self.cptr.head == Tp.ID:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 66 and self.cptr.head == Tp.RETURN:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 66 and self.cptr.head == Tp.WHILE:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 66 and self.cptr.head == Tp.IF:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 66 and self.cptr.head == Tp.VALUE:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 66 and self.cptr.head == Tp.LPAR:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 66 and self.cptr.head == Tp.LBR:
            self.c.append(Dyad(Tp.M, El.M(self.quadNum)))

        elif self.s[-1] == 67 and self.cptr.head == Tp.LBR:
            self.c.append(self.cptr)
            self.GetNext()

        elif self.s[-1] == 68 and self.cptr.head == Tp.RBR:
            pops = []
            for i in range(10):
                self.s.pop()
                pops.append(self.c.pop())
            self.BackPatch(pops[7].body.tList, pops[5].body.quad)
            self.BackPatch(pops[7].body.fList, pops[1].body.quad)
            self.c.append(Dyad(Tp.L, El.L(pops[4].body.nList + pops[3].body.nList + pops[0].body.nList)))

        elif self.s[-1] == 68 and self.cptr.head == Tp.ID:
            pops = []
            for i in range(10):
                self.s.pop()
                pops.append(self.c.pop())
            self.BackPatch(pops[7].body.tList, pops[5].body.quad)
            self.BackPatch(pops[7].body.fList, pops[1].body.quad)
            self.c.append(Dyad(Tp.L, El.L(pops[4].body.nList + pops[3].body.nList + pops[0].body.nList)))

        elif self.s[-1] == 68 and self.cptr.head == Tp.RETURN:
            pops = []
            for i in range(10):
                self.s.pop()
                pops.append(self.c.pop())
            self.BackPatch(pops[7].body.tList, pops[5].body.quad)
            self.BackPatch(pops[7].body.fList, pops[1].body.quad)
            self.c.append(Dyad(Tp.L, El.L(pops[4].body.nList + pops[3].body.nList + pops[0].body.nList)))

        elif self.s[-1] == 68 and self.cptr.head == Tp.WHILE:
            pops = []
            for i in range(10):
                self.s.pop()
                pops.append(self.c.pop())
            self.BackPatch(pops[7].body.tList, pops[5].body.quad)
            self.BackPatch(pops[7].body.fList, pops[1].body.quad)
            self.c.append(Dyad(Tp.L, El.L(pops[4].body.nList + pops[3].body.nList + pops[0].body.nList)))

        elif self.s[-1] == 68 and self.cptr.head == Tp.IF:
            pops = []
            for i in range(10):
                self.s.pop()
                pops.append(self.c.pop())
            self.BackPatch(pops[7].body.tList, pops[5].body.quad)
            self.BackPatch(pops[7].body.fList, pops[1].body.quad)
            self.c.append(Dyad(Tp.L, El.L(pops[4].body.nList + pops[3].body.nList + pops[0].body.nList)))
            
        else:
            self.flag = Tp.ERR
