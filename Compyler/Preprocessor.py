class Preprocessor:
    def __init__(self):
        self.tail = ''
        self.isAnno = False
        self.tList = ['+', '-', '*', '/', '=', '>', '<', '!', '(', ')', ',', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ';', '{', '}']
        
    def Init(self):
        self.tail = ''
        self.isAnno = False

    def Compress(self, s):
        l = len(s)
        i = 0
        while i < l:
            if s[i] in self.tList:
                if i > 0 and s[i - 1] == ' ':
                    s = s[:i - 1] + s[i:]
                    i -= 1
                    l -= 1
                    
                if i < l - 1 and s[i + 1] == ' ':
                    if i + 2 < l:
                        s = s[:i + 1] + s[i + 2:]
                    else:
                        s = s[:i + 1]
                    l -= 1
            i += 1
        return s
                    
        
    def Do(self, line):
        #line = ' '.join(line.split())
        sentences = []
        noCompleteSent = True
        sEnd = -1
        aStart = 0
        preC = ' '
        
        i = 0
        l = len(line)
        tl = len(self.tail)
        while i < l:
            ch = line[i]
            if self.isAnno == False:
                if ch == ';':
                    if noCompleteSent == True:
                        if len(self.tail) == 0:
                            s = line[sEnd + 1:i + 1]
                        else:
                            s = self.tail + ' ' + line[sEnd + 1:i + 1]
                    else:
                        s = line[sEnd + 1:i + 1]
                    s = ' '.join(s.split())
                    #print(s)
                    if s != '':
                        sentences.append(self.Compress(s) + '\n')
                    sEnd = i
                    noCompleteSent = False
                    
                elif ch == '{' or ch == '}':
                    if noCompleteSent == True:
                        if len(self.tail) == 0:
                            s = line[sEnd + 1:i]
                        else:
                            s = self.tail + ' ' + line[sEnd + 1:i]
                    else:
                        s = line[sEnd + 1:i]
                    s = ' '.join(s.split())
                    #print(s)
                    if s != '':
                        sentences.append(self.Compress(s) + '\n')
                    sentences.append(ch + '\n')
                    sEnd = i
                    noCompleteSent = False
                elif ch == '/' and preC == '/':
                    line = line[:i - 1]
                    l = len(line)
                elif ch == '*' and preC == '/':
                    self.isAnno = True
                    aStart = i - 1
            else:
                if ch == '/' and preC == '*':
                    self.isAnno = False
                    if i < l - 1:
                        line = line[:aStart] + line[i + 1:]
                    else:
                        line = line[:aStart]
                    i = aStart - 1
                    l = len(line)
            i += 1
            preC = ch
        
        if self.isAnno == True:
            line = line[:aStart]
            
        if noCompleteSent == True:
            self.tail = self.tail + ' ' + line
        elif sEnd < l - 1:
            self.tail = line[sEnd + 1:]
        else:
            self.tail = ''
            
        return sentences
        
    def GetTail(self):
        return self.Compress(' '.join(self.tail.split()) + '\n')
