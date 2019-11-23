import Status
import Types

class LexAnalyzer:
    def __init__(self, idHolder):
        self.keyWordList = {'int':Types.INT, 'void':Types.VOID, 'if':Types.IF, 'else':Types.ELSE, 'while':Types.WHILE, 'return':Types.RETURN}
        self.noPush = False
        self.idHolder = idHolder
    
    def Init(self):
        self.noPush = False
    
    def PopScope(self):
        self.idHolder.BackScope()
        
    def PushScope(self):
        self.idHolder.EnterScope()
    
    def SearchID(self, id, curr = False):
        return self.idHolder.SearchID(id, curr = curr)
    
    def NewID(self, id):
        return self.idHolder.AddID(id)
    
    def IsKeyWord(self, token):
        if token in self.keyWordList:
            return self.keyWordList[token]
        return 0
        
    def Do(self, line):
        lex = []
        l = len(line)
        i = 0
        status = Status.START
        #preLex = None
        token = ''
        ch = line[0]
        
        while True:
            if status == Status.START:
                if ch == '\n':
                    break
                if ch.isdigit():
                    token += ch
                    status = Status.INT
                elif ch.isalpha():
                    token += ch
                    status = Status.ID
                elif ch == '=':
                    token += ch
                    status = Status.ASSIGN
                elif ch == '+':
                    token += ch
                    status = Status.ADD
                elif ch == '-':
                    token += ch
                    status = Status.SUB
                elif ch == '*':
                    token += ch
                    status = Status.MULT
                elif ch == '/':
                    token += ch
                    status = Status.DIV
                elif ch == ',':
                    token += ch
                    status = Status.COMMA
                elif ch == '(':
                    token += ch
                    status = Status.LPAR
                elif ch == ')':
                    token += ch
                    status = Status.RPAR
                elif ch == '{':
                    token += ch
                    status = Status.LBRACE
                elif ch == '}':
                    token += ch
                    status = Status.RBRACE
                elif ch == ';':
                    token += ch
                    status = Status.SEMICOLON
                elif ch == '>':
                    token += ch
                    status = Status.GREATER
                elif ch == '<':
                    token += ch
                    status = Status.LESS
                else:
                    token += ch
                    status = Status.OTHER
                    
            elif status == Status.INT:
                i += 1
                ch = line[i]
                if ch.isdigit():
                    token += ch
                elif ch.isalpha():
                    token += ch
                    status = Status.ID
                else:
                    status = Status.INTENDS
            elif status == Status.INTENDS:
                lex.append([Types.VALUE, token])
                status = Status.START
                #preLex = token
                token = ''
                
            elif status == Status.ID:
                i += 1
                ch = line[i]
                if ch.isalnum():
                    token += ch
                elif ch == '(':
                    status = Status.PROC
                else:
                    status = Status.VAR
            elif status == Status.VAR:
                if token[0].isdigit():
                    lex.append([Types.ELEX, token])
                else:
                    k = self.IsKeyWord(token)
                    if k == 0:
                        if lex == [] or (lex[-1][0] != Types.INT and lex[-1][0] != Types.VOID):
                            j = self.SearchID(token)
                            if j == -1:
                                lex.append([Types.EUNDEF, token])
                            else:
                                lex.append([Types.ID, j])
                        else:
                            j = self.SearchID(token, curr = True)
                            if j != -1:
                                lex.append([Types.EREDEF, token])
                            else:
                                lex.append([Types.ID, self.NewID(token)])
                    else:
                        lex.append([k])
                status = Status.START
                #preLex = token
                token = ''
            elif status == Status.PROC:
                if token[0].isdigit():
                    lex.append([Types.ELEX, token])
                else:
                    k = self.IsKeyWord(token)
                    if k == 0:
                        j = self.SearchID(token)
                        if lex == [] or (lex[-1][0] != Types.INT and lex[-1][0] != Types.VOID):
                            if j == -1:
                                lex.append([Types.EUNDEF, token])
                            else:
                                lex.append([Types.ID, j])
                        else:
                            if j == -1:
                                lex.append([Types.ID, self.NewID(token)])
                                self.PushScope()
                                #print('PushScope for new proc')
                                self.noPush = True
                            else:
                                lex.append([Types.EREDEF, token])
                    else:
                        lex.append([k])
                status = Status.START
                #preLex = token
                token = ''
                
            elif status == Status.ASSIGN:
                i += 1
                ch = line[i]
                if ch == '=':
                    status = Status.EQUAL
                else:
                    status = Status.ASSIGNENDS
            elif status == Status.EQUAL:
                lex.append([Types.EQUAL])
                i += 1
                ch = line[i]
                status = Status.START
                #preLex = token
                token = ''
            elif status == Status.ASSIGNENDS:
                lex.append([Types.ASSIGN])
                status = Status.START
                #preLex = token
                token = ''
            
            elif status == Status.ADD:
                lex.append([Types.ADD])
                i += 1
                ch = line[i]
                status = Status.START
                #preLex = token
                token = ''
                
            elif status == Status.SUB:
                lex.append([Types.SUB])
                i += 1
                ch = line[i]
                status = Status.START
                #preLex = token
                token = ''
                
            elif status == Status.COMMA:
                lex.append([Types.COMM])
                i += 1
                ch = line[i]
                status = Status.START
                #preLex = token
                token = ''
                
            elif status == Status.LPAR:
                lex.append([Types.LPAR])
                i += 1
                ch = line[i]
                status = Status.START
                #preLex = token
                token = ''
                
            elif status == Status.RPAR:
                lex.append([Types.RPAR])
                i += 1
                ch = line[i]
                status = Status.START
                #preLex = token
                token = ''
                
            elif status == Status.MULT:
                lex.append([Types.MULT])
                i += 1
                ch = line[i]
                status = Status.START
                #preLex = token
                token = ''
                
            elif status == Status.DIV:
                lex.append([Types.DIV])
                i += 1
                ch = line[i]
                status = Status.START
                #preLex = token
                token = ''
                
            elif status == Status.GREATER:
                i += 1
                ch = line[i]
                if ch == '=':
                    status = Status.GE
                else:
                    status = Status.GENDS
            elif status == Status.GE:
                lex.append([Types.GRE])
                i += 1
                ch = line[i]
                status = Status.START
                #preLex = token
                token = ''
            elif status == Status.GENDS:
                lex.append([Types.GR])
                status = Status.START
                #preLex = token
                token = ''
                
            elif status == Status.LESS:
                i += 1
                ch = line[i]
                if ch == '=':
                    status = Status.LE
                else:
                    status = Status.LENDS
            elif status == Status.LE:
                lex.append([Types.LEE])
                i += 1
                ch = line[i]
                status = Status.START
                #preLex = token
                token = ''
            elif status == Status.LENDS:
                lex.append([Types.LE])
                status = Status.START
                #preLex = token
                token = ''
            
            elif status == Status.LBRACE:
                lex.append([Types.LBR])
                if self.noPush == False:
                    #print('PushScope for new block')
                    self.PushScope()
                else:
                    self.noPush = False
                i += 1
                ch = line[i]
                status = Status.START
                #preLex = token
                token = ''           
            elif status == Status.RBRACE:
                lex.append([Types.RBR])
                self.PopScope()
                i += 1
                ch = line[i]
                status = Status.START
                #preLex = token
                token = ''
                
            elif status == Status.SEMICOLON:
                lex.append([Types.SEMICOL])
                i += 1
                ch = line[i]
                status = Status.START
                #preLex = token
                token = ''
                
            elif status == Status.NEQUAL:
                lex.append([Types.NE])
                i += 1
                ch = line[i]
                status = Status.START
                #preLex = token
                token = ''
                
            elif status == Status.OTHER:
                if ch == '!':
                    i += 1
                    ch = line[i]
                    if ch == '=':
                        status = Status.NEQUAL
                    else:
                        lex.append([Types.ELEX, '!'])
                        status = Status.START
                        #preLex = token
                        token = ''
                else:
                    if ch != ' ':
                        lex.append([Types.ELEX, ch])
                    i += 1
                    ch = line[i]
                    status = Status.START
                    #preLex = token
                    token = ''
        return lex