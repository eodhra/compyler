import copy
from TerList import terList

gens = []
items = []
v = []
vt = []
vn = []
states = []
go = {}
follow = {}
action = {}
goto = {}

class Item:
    def __init__(self, head, content):
        self.head = head
        self.content = content

class Go:
    def __init__(self, s, d, by):
        self.s = s
        self.d = d
        self.by = by

class Gen:
    def __init__(self, l, r):
        self.r = r
        self.l = l
        
    def toStr(self):
        string = '%s\t:=\t'%self.l
        for m in self.r:
            string  += '%s '%m
        return string

def printFollow():
    for f in follow:
        string = '%s\t'%f
        for p in follow[f]:
            string += '%s '%p
        print(string)

def addState(c):
    for s in states:
        if sameClosure(s, c):
            return s, False
    states.append(c)
    return c, True

def sameClosure(c1, c2):
    for c in c1:
        if c not in c2:
            return False
    for c in c2:
        if c not in c1:
            return False
    return True

def buildClosure(closure):  
    x = True
    while(x):
        x = False
        for i in closure:
            idx = i.content.index('/')
            if idx == len(i.content) - 1:
                continue
            else:
                for it in items:
                    if it.head == i.content[idx + 1] and it not in closure and it.content[0] == '/':
                        closure.append(it)
                        x = True
    return closure

def printItem(item):
    print('%s\t:=\t'%item.head, end = '')
    for i in item.content:
        print('%s '%i, end = '')
    print()

def printClosure(closure):
    for i in closure:
        printItem(i)

def writeItem(file, item):
    file.write('%s   :=  '%item.head)
    for c in item.content:
        file.write('%s '%c)
    file.write('\n')

def writeClosure(file, closure):
    for item in closure:
        writeItem(file, item)

def searchItem(item):
    for it in items:
        if it.head != item.head:
            continue
        l = len(item.content)
        if len(it.content) != l:
            continue
        equa = True
        idx = 0
        while idx < l:
            if item.content[idx] != it.content[idx]:
                equa = False
                break
            idx += 1
        if equa:
            return it
    return None

def getSucc(closure, by):
    succ = []
    for item in closure:
        idx = item.content.index('/')
        if idx == len(item.content) - 1:
            continue
        if item.content[idx + 1] != by:
            continue
        it = copy.deepcopy(item)
        (it.content[idx], it.content[idx + 1]) = (it.content[idx + 1], it.content[idx])
        d = searchItem(it)
        if d is not None:
            succ.append(d)
    return succ

def detectContra(go):
    for g in go:
        if g.by == go.by and g.s == go.s and g.d != go.d:
            print('Contradiction!')
            print('%d\t%d\t%s'%(g.s, g.d, g.by))
            print('%d\t%d\t%s'%(go.s, go.d, go.by))
            return True
    return False

def buildGo():
    global states
    global go
    states = []
    go = {}
    
    states.append(buildClosure([items[0]]))
    x = True
    while x:
        x = False
        for s in states:
            go.setdefault(states.index(s), {})
            for by in v:
                succ = getSucc(s, by)
                if succ == []:
                    continue
                c = buildClosure(succ)
                c, x = addState(c)
                go[states.index(s)][by] = states.index(c)
                
                
def printGo():
    for s in go:
        for by in go[s]:
            print('%d\t%d\t%s'%(s, go[s][by], by))

def writeGo(file):
    for s in go:
        for by in go[s]:
            file.write('%d\t%d\t%s\n'%(s, go[s][by], by))

def getGen(item):
    l = item.head
    r = copy.deepcopy(item.content)
    r.remove('/')
    if r == []:
        r = ['none']
    for g in gens:
        if g.l != l:
            continue
        if len(r) != len(g.r):
            continue
        e = True
        for a, b in zip(r, g.r):
            if a != b:
                e = False
                break
        if e:
            return g
    return None

def buildSLR():
    for s in go:
        action.setdefault(s, {})
        for by in go[s]:
            if by in vt:
                action.setdefault(s, {})
                action[s][by] = go[s][by]
            elif by in vn:
                goto.setdefault(s, {})
                goto[s][by] = go[s][by]
                
    for s in states:
        action.setdefault(states.index(s), {})
        for i in s:
            if i.content[-1] == '/':
                for f in follow[i.head]:
                    g = getGen(i)
                    t = action[states.index(s)].setdefault(f, g)
                    if t != g:
                        print('Contradiction!')
            
def printSLR():
    for a in action:
        for by in action[a]:
            print('action\t%d\t%s\t'%(a, by), end = '')
            if a == 1 and by == 'EOF':
                print('acc')
            elif type(action[a][by]) == Gen:
                print(action[a][by].toStr())
            else:
                print('%d'%action[a][by])
    for s in goto:
        for by in goto[s]:
            print('goto\t%d\t%s\t%d'%(s, by, goto[s][by]))

def writeSLR(file):
    for a in action:
        for by in action[a]:
            file.write('action\t%d\t%s\t'%(a, by))
            if a == 1 and by == 'EOF':
                file.write('acc\n')
            elif type(action[a][by]) == Gen:
                file.write('%s\n'%action[a][by].toStr())
            else:
                file.write('%d\n'%action[a][by])
    for s in goto:
        for by in goto[s]:
            file.write('goto\t%d\t%s\t%d\n'%(s, by, goto[s][by]))
    

if __name__ == "__main__":
    f = open('Grammar.txt')
    for line in f:
        line = line.strip()
        pars = line.split()
        pars.remove(':=')
        for p in pars:
            if p not in v:
                v.append(p)
                if p in terList:
                    vt.append(p)
                else:
                    vn.append(p)
        gens.append(Gen(pars[0], pars[1:]))
        if pars[1] == 'none':
            item = Item(pars[0], ['/'])
            items.append(item)
        else:
            rs = pars[1:]
            l = len(rs)
            i = 0
            while i <= l:
                content = rs[:i] + ['/'] + rs[i:]
                item = Item(pars[0], content)
                items.append(item)
                i += 1
    f.close()
    v.append('EOF')
    vt.append('EOF')
    
    f = open('Follow.txt')
    for line in f:
        pars = line.split()
        follow.setdefault(pars[0], [])
        for p in pars[1:]:
            follow[pars[0]].append(p)
    f.close()
    printFollow()

    f = open('Items.txt', 'w')
    for i in items:
        writeItem(f, i)
    f.close()
    
    print('Generators')
    for g in gens:
        print(g.toStr())

    if buildGo() == -1:
        print('Unprocessable grammar.')
    printGo()
    
    buildSLR()
    printSLR()
    
    f = open('States.txt', 'w')
    count = 0
    for c in states:
        f.write('State %d\n'%count)
        writeClosure(f, c)
        f.write('\n')
        count += 1
    f.close()

    f = open('Go.txt', 'w')
    writeGo(f)
    f.close()
    
    f = open('SLR1.txt', 'w')
    writeSLR(f)
    f.close()