class Dyad:
    def __init__(self, head, body):
        self.head = head
        self.body = body

    def ToStr(self):
        if self.body is None:
            return '[%s]'%str(self.head)
        else:
            return '[%s,%s]'%(str(self.head), str(self.body))
