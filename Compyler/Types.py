INT     = 1
VOID    = 2
IF      = 3
ELSE    = 4
WHILE   = 5
RETURN  = 6
ID      = 7
VALUE   = 8
ASSIGN  = 9
ADD     = 10
SUB     = 11
MULT    = 12
DIV     = 13
EQUAL   = 14
GR      = 15
GRE     = 16
LE      = 17
LEE     = 18
NE      = 19
SEMICOL = 20
COMM    = 21
LPAR    = 22
RPAR    = 23
LBR     = 24
RBR     = 25

G       = 100
P       = 101
B       = 102
D       = 103
S       = 104
L       = 105
E       = 106
A       = 107
I       = 108
F       = 109
M       = 110
N       = 111
C       = 112

RELOP   = 30

ELEX    = -1
EUNDEF  = -2
EREDEF  = -3
ESYNT   = -4  

EOF     = 0

vList =     [
    INT     ,
    VOID    ,
    IF      ,
    ELSE    ,
    WHILE   ,
    RETURN  ,
    ID      ,
    VALUE   ,
    ASSIGN  ,
    ADD     ,
    SUB     ,
    MULT    ,
    DIV     ,
    EQUAL   ,
    GR      ,
    GRE     ,
    LE      ,
    LEE     ,
    NE      ,
    SEMICOL ,
    COMM    ,
    LPAR    ,
    RPAR    ,
    LBR     ,
    RBR     ,
    G       ,
    P       ,
    B       ,
    D       ,
    S       ,
    L       ,
    E       ,
    A       ,
    I       ,
    F       ,
    M       ,
    N       ,
    EOF     ]

vnList =    [
    G       ,
    P       ,
    B       ,
    D       ,
    S       ,
    L       ,
    E       ,
    A       ,
    I       ,
    F       ,
    M       ,
    N       ,
    C       ]

vtList =    [
    INT     ,
    VOID    ,
    IF      ,
    ELSE    ,
    WHILE   ,
    RETURN  ,
    ID      ,
    VALUE   ,  
    ASSIGN  , 
    ADD     ,
    SUB     ,
    MULT    ,
    DIV     ,
    EQUAL   ,
    GR      ,
    GRE     ,
    LE      ,
    LEE     ,
    NE      ,
    SEMICOL ,
    COMM    ,
    LPAR    ,
    RPAR    ,
    LBR     ,
    RBR     ,
    EOF     ]

relopList = [EQUAL, GR, GRE, LE, LEE, NE]

errorList = [ELEX, EUNDEF, EREDEF]

NONE = 0
SEQENDS = 1
ACC = 255
ERR = 254