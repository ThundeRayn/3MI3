# This program can be run as a python2 or as a python3 program
from __future__ import print_function

# A recursive descent parser in C for simple arithemic expressions.
# The scanner is not separated from the parser. Each nonterminal corresponds
# to a function, the correspoding productions are shown as a comment at the
# header of the function. 

# tokens and corresponding values as returned by the scanner
EOI = 0    #end of input
NUM = 1    #an unsigned decimal number with at most 4 digits after . , at most
           #9 significant digits and no leading zeroes
VAR = 2    #a 1 character identifier of upper case letters A to Z
EQ = 3     #character =
MINUS = 4  #character -
PLUS = 5   #character +
MULT = 6   #character *
DIVI = 7   #character /
LP = 8     #character (
RP = 9     #character )
SEMI = 10  #character ;
ERR = 11   #error

# Grammar
# prog: sts expr | sts
# sts: st sts | epsilon
# st: VAR EQ expr SEMI 
# expr: MINUS NUM | MINUS VAR | term expr1
# expr1: PLUS term expr1 | MINUS term expr1 | epsilon 
# term: factor term1
# term1: MULT factor term1 | DIVI factor term1 | epsilon
# factor: NUM | VAR | LP expr RP | epsilon

import sys
debug = True

def show(indent,name,s,spp):
    if debug:
        print(indent+name+'("',end='');
        j = len(s)
        for i in range(spp,j):
            print(s[i],sep="",end="")
        print('")',end='\n')
        return
    else:
        return
#end show



def EatWhiteSpace(s,spp):
    j = len(s)
    if spp >= j:
        return spp

    while s[spp] == ' ' or s[spp] == '\n':
        spp=spp+1
        if spp >= j:
            break
    return spp
#end EatWhiteSpace


# function Parse ---------------------------------------------
def Parse(s,indent):
    show(indent,'Parse',s,0)
    
    spp = 0;
    indent1 = indent+' '
    res,spp = prog(s,spp,indent1)
    if debug:
        print(indent+"back to Parse from prog")
    if not res:
        return False
    
    token = LookAhead(s,spp)
    if token != EOI:
        return False
    else:
        return True
#end Parse


# prog: sts expr | sts 
# function prog --------------------------------------------- 
def prog(s,spp,indent):
    show(indent,'prog',s,spp)
    indent1 = indent+' '
    spp1 = spp #save position

    res,spp = sts(s,spp,indent1)
    if debug:
        print(indent+"back to prog from sts")
    if not res:
        return False,spp1

    token = LookAhead(s,spp)
    if token == EOI:
        return True,spp
 
    res,spp = expr(s,spp,indent1)
    if debug:
        print(indent+"back to prog from expr")
    if res:
        return True,spp
    else:
        return False,spp1
#end prog



# sts: st sts | epsilon
# function sts --------------------------------------------- 
def sts(s,spp,indent):
    show(indent,'sts',s,spp)
    indent1 = indent+' '
    spp1 = spp # save position

    res,spp = st(s,spp,indent1)
    if debug:
        print(indent+"back to sts from st")
    if not res:
        return True,spp1  # epsilon
    res,spp = sts(s,spp,indent1)
    if debug:
        print(indent+"back to sts from sts")
    if res:
        return True,spp
    else:
        return True,spp1  # epsilon
#end sts



# st: VAR EQ expr SEMI 
# function st ---------------------------------------------- 
def st(s,spp,indent):
    show(indent,'st',s,spp)
    indent1 = indent+' '
    spp1 = spp # save position

    j = len(s)

    token,spp = NextToken(s,spp)     
    if token != VAR:
        return False,spp1

    token,spp = NextToken(s,spp)
    if token != EQ:
        return False,spp1

    res,spp = expr(s,spp,indent1)
    if debug:
        print(indent+"back to st from expr")
    if not res:
        return False,spp1

    token,spp = NextToken(s,spp)
    if token == SEMI:
        return True,spp
    else:
        return False,spp1 
#end st


# expr: MINUS NUM | MINUS VAR | term expr1 
# function expr --------------------------------------------- 
def expr(s,spp, indent):
    show(indent,'expr',s,spp)
    indent1 = indent+' '
    spp1 = spp # save position

    token = LookAhead(s,spp)
    if token == MINUS:
        token,spp = NextToken(s,spp)
        token,spp = NextToken(s,spp)
        if token == NUM or token == VAR:
            return True,spp
        else:
            return False,spp1
    else:   
        res,spp = term(s,spp,indent1)
        if debug:
            print(indent+"back to expr from term")
        if not res:
            return False,spp1
        res,spp = expr1(s,spp,indent1)
        if debug:
            print(indent+"back to expr from expr1")
        if res:
            return True,spp
        else:
            return False,spp1
#end expr



# expr1: PLUS term expr1 | MINUS term expr1 | epsilon 
# function expr1 ------------------------------------------- 
def expr1(s,spp,indent):
    show(indent,'expr1',s,spp)
    indent1 = indent+' '
    spp1 = spp  # save position

    token = LookAhead(s,spp)
    if token == PLUS or token == MINUS:
        token,spp = NextToken(s,spp)
        res,spp = term(s,spp,indent1)
        if debug:
            print(indent+"back to expr1 from term")
        if not res:  
            return False,spp1
        res,spp = expr1(s,spp,indent1)
        if debug:
            print(indent+"back to expr1 from expr1")
        if not res:
            return False,spp1
        return True,spp
    else:
        return True,spp1  # epsilon
#end expr1


# term: factor term1 
# function term ------------------------------------------- 
def term(s,spp,indent):
    show(indent,'term',s,spp)
    indent1 = indent+' '
    spp1 = spp  # save position
    
    res,spp = factor(s,spp,indent1)
    if debug:
        print(indent+"back to term from factor")
    if not res: 
        return False,spp1
    res,spp = term1(s,spp,indent1)
    if debug:
        print(indent+"back to term from term1")
    if res:
        return True,spp
    else:
        return False,spp1
#end term


# term1: MULT factor term1 | DIVI factor term1 | epsilon 
# function term1 ------------------------------------------- 
def term1(s,spp,indent):
    show(indent,'term1',s,spp)
    indent1 = indent+' '
    spp1 = spp # save position

    token = LookAhead(s,spp)
    if token == MULT or token == DIVI:
        token,spp = NextToken(s,spp)
        res,spp = factor(s,spp,indent1)
        if debug:
            print(indent+"back to term1 from factor")
        if not res:
            return False,spp1
        res,spp = term1(s,spp,indent1)
        if debug:
            print(indent+"back to term1 from term1")
        if res:
            return True,spp
        else:
            return False,spp1
    else:
        return True,spp1  # epsilon
#end term1


# factor: NUM | VAR | LP expr RP | epsilon
# function factor ----------------------------------------- 
def factor(s,spp,indent):
    show(indent,'factor',s,spp)
    indent1 = indent+' '
    spp1 = spp  # save position

    token = LookAhead(s,spp)
    if token == NUM or token == VAR:
        token,spp = NextToken(s,spp)
        return True,spp
    elif token == LP:
        token,spp = NextToken(s,spp)
        res,spp = expr(s,spp,indent1)
        if debug:
            print(indent+"back to factor from expr")
        if not res:
            return False,spp1
        token,spp = NextToken(s,spp)
        if token == RP:
            return True,spp
        else:
            return False,spp1
    else:
        return True,spp1
#end factor

# the scanner ####################################################

# function LookAhead ------------------------------------------- 
def LookAhead(s,spp):
    j = len(s);
    i = spp
    if i >= j:
        return EOI
    while s[i]==" " or s[i]=="\n":
        if i >= j:
            return EOI

    if s[i] == '=':
        return EQ
    elif s[i] == "-":
        return MINUS
    elif s[i] == "+":
        return PLUS
    elif s[i] == "*":
        return MULT
    elif s[i] == "/":
        return DIVI
    elif s[i] == "(":
        return LP
    elif s[i] == ")":
        return RP
    elif s[i] == ";":
        return SEMI
    elif (ord(s[i]) >= ord('0') and ord(s[i]) <= ord('9')):
        return NUM
    elif (ord(s[i]) >= ord('A') and ord(s[i]) <= ord('Z')):
        return VAR
    else:
        return ERR
#end LookAhead


# function NextToken --------------------------------------------- 
def NextToken(s,spp):
    spp1 = spp
    spp = EatWhiteSpace(s,spp)
    j = len(s)
    if spp >= j:
        return ERR,spp1

    if spp >= j:
        return EOI,spp+1
    elif s[spp] == '=':
        return EQ,spp+1
    elif s[spp] == "-":
        return MINUS,spp+1
    elif s[spp] == "+":
        return PLUS,spp+1
    elif s[spp] == "*":
        return MULT,spp+1
    elif s[spp] == "/":
        return DIVI,spp+1
    elif s[spp] == "(":
        return LP,spp+1
    elif s[spp] == ")":
        return RP,spp+1
    elif s[spp] == ";":
        return SEMI,spp+1
    elif (ord(s[spp])>=ord('0') and ord(s[spp])<=ord('9')):
        res,spp = Lnum(s,spp)
        if not res:
            return ERR,spp1
        if spp >= j:
            return True,spp
        if s[spp] != '.':
            return NUM,spp
        spp = spp+1  # eat .
        if spp >= j:
            return ERR,spp1
        res,spp = Rnum(s,spp);
        if not res:
            return ERR,spp1
        return NUM,spp
    elif (ord(s[spp])>=ord('A') and ord(s[spp])<=ord('Z')):
        return VAR,spp+1
    else:
        return ERR,spp1
#end NUM


# function Rnum -------------------------------------------- 
def Rnum(s,spp):
    spp1 = spp # save position
    j = len(s)

    found = False
    i = 0
    while i<4 :
        if spp < j and ord(s[spp]) >= ord('0') and ord(s[spp]) <= ord('9'):
            found = True
            spp = spp+1
            if spp >= j:
                break
            i = i+1
        else:
            break
    #endwhile

    if found:
        return True,spp
    else:
        return False,spp1
#end Rnum


# function Lnum -------------------------------------------- 
def Lnum(s,spp):
    spp1 = spp # save position
    j = len(s)
    if spp >= j:
        return False,spp1

    if s[spp] == '0':
        spp = spp+1  # eat 0
        return True,spp

    i = 0
    found = False
    while i<4 :
        if spp < j and ord(s[spp]) >= ord('0') and ord(s[spp]) <= ord('9'):
            found = True
            spp = spp+1
            i = i+1
        else:
            break
    #endwhile

    if found:
        return True,spp
    else:
        return False,spp1
#end Lnum


#main section
s = "A=2;2"
show('','main',s,0)
indent = ' '
res = Parse(s,indent);
if res:
    print("parsing OK")
else:
    print("parse Error")
#end main section
                


