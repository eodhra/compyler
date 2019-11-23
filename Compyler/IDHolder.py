class Scope:
    def __init__(self):
        self.pScope = None
        self.cScopes = []
        self.idList = []
        
class IDHolder:
    def __init__(self):
        self.ids = []
        self.currScope = Scope()
        self.scopes = [self.currScope]
        self.idnum = 0
    
    def Init(self):
        self.ids = []
        self.currScope = Scope()
        self.scopes = [self.currScope]
        self.idnum = 0
    
    def AddID(self, id):
        self.ids.append(id)
        self.currScope.idList.append(self.idnum)
        self.idnum += 1
        return self.idnum - 1
        
    def SearchID(self, id, curr = False):
        if curr:
            for idx in self.currScope.idList:
                if self.ids[idx] == id:
                    return idx
            return -1
        else:
            s = self.currScope
            while s is not None:
                for idx in s.idList:
                    if self.ids[idx] == id:
                        return idx
                s = s.pScope
            return -1
        
    def EnterScope(self):
        s = Scope()
        s.pScope = self.currScope
        self.currScope.cScopes.append(s)
        self.scopes.append(s)
        self.currScope = s
        
    def BackScope(self):
        self.currScope = self.currScope.pScope