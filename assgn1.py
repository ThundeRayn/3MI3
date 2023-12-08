from __future__ import print_function
import re

'''

        3MI3 ASSGN1

        ShirongTang, 400309194, Due 10.27th

'''

#---------------------Q7-----------------------#
#regular expression description of all tokens you will be using in Question 8

F = '^False$' #False constant value
T = '^True$' #True constant value
NOT = '^not$' #unary not operation
AND = '^and$' #and operation
EQUAL = '^=$'  #equal operation
OR = '^or$' #or operation
LP = "^\($"  #LPAREN
RP = "^\)$"  #RPAREN
VAR = '^[$]([a-zA-Z0-9]*)' #boolean name variable
ERR = '^ERR$'  # Showing Error
EOI = '^EOI$' #end of input


#---------------------Q8------------------------#
# BNF grammar

# FINALEXPR -> VAR EQU | EXPR
# EQU -> EQUAL EXPR EQU | epsilon
# EXPR -> CONTRI COMBINE
# COMBINE -> {AND OR} CONTRI COMBINE| epsilon
# CONTRI -> TERM | NOT CONTRI
# TERM -> T | F | VAR | LP FINALEXPR RP

#---------------------Q9------------------------#

debug = False

def show(indent, name, s, spp):
    if debug:
        print(indent + name + '("', end='');
        j = len(s)
        for i in range(spp, j):
            print(s[i], sep="", end="")
        print('")', end='\n')
        return
    else:
        return
#end show


def EatWhiteSpace(s, spp):
    j = len(s)
    if spp >= j:
        return spp

    while s[spp] == ' ' or s[spp] == '\n':
        spp = spp + 1
        if spp >= j:
            break
    return spp
    #end eating white space


# function Parse ---------------------------------------------
def Parse(s,indent):
    show(indent,'Parse',s,0)
    
    spp = 0;
    indent1 = indent+' '
    res,spp = FINALEXPR(s,spp,indent1)
    if debug:
        print(indent+"back to Parse from FINALEXPR")
    if not res:
        return False
    
    token = LookAhead(s,spp)
    if token != EOI:
        return False
    else:
        return True
#end Parse


# FINALEXPR -> VAR EQU | EXPR
# function FINALEXPR ---------------------------------------
def FINALEXPR(s,spp,indent):
    show(indent,'FINALEXPR',s,spp)
    indent1 = indent+' '
    spp1 = spp #save position

    token = LookAhead(s,spp)
    if token == VAR:
        token,spp = NextToken(s,spp)
        res,spp = EQU(s,spp,indent1)
        if res:
            print("FINALEXPR return true")
            return True,spp
        else:
            print("FINALEXPR return false,equation failed!")
            return False,spp1
    else:
        res,spp = EXPR(s,spp,indent1)
        if res:
            print("FINALEXPR return true")
            return True,spp
        else:
            print("FINALEXPR return false,expr failed!")
            return False,spp1
#end FINALEXPR


# EQU -> EQUAL EXPR EQU | epsilon
# function EQU ------------------------------------------ good
def EQU(s,spp,indent):
    show(indent,'EQU',s,spp)
    indent1 = indent + ' '
    spp1 =spp

    token = LookAhead(s,spp)
    if token == EQUAL:
        token,spp = NextToken(s,spp)
        res,spp = EXPR(s,spp,indent)
        if res:
            print("EQU return true")
            pass
        else:
            print("EQU return false,expr failed!")
            return False,spp1
        res,spp=EQU(s,spp,indent)
        if res:
            print("EQU followed return true")
            return True,spp
        else:
            print("EQU followed return false!")
            return False,spp1
    else:
        print("EQU return true, epsilon")
        return True, spp
#end EQU

# EXPR -> CONTRI COMBINE
# function EXPR ------------------------------------------- good
def EXPR(s,spp,indent):
    show(indent,'EXPR',s,spp)
    indent1 = indent + ' '
    spp1=spp

    res,spp = CONTRI(s,spp,indent1)
    if not res:
        print("EXPR return false,contri failed!")
        return False,spp1
    res,spp = COMBINE(s,spp,indent1)
    if res:
        print("EXPR return true")
        return True,spp
    else:
        print("EXPR eturn false,combine failed!")
        return False,spp1 

# COMBINE -> {AND OR} CONTRI COMBINE| epsilon
# function COMBINE ----------------------------------------- good
def COMBINE(s,spp,indent):
    show(indent,'COMBINE',s,spp)
    indent1 = indent + ' '
    spp1 =spp

    token = LookAhead(s,spp)
    if token == AND or token == OR:
        token,spp = NextToken(s,spp)
        res,spp = CONTRI(s,spp,indent1)
        if res:
            print("COMBINE's CONTRI return true")
            pass
        else:
            print("COMBINE return false,CONTRI failed!")
            return False,spp1
        res,spp = COMBINE(s,spp,indent1)
        if res:
            print("COMBINE return true")
            return True,spp
        else:
            print("COMBINE return false,combine followed by contri failed!")
            return False,spp1 
    else:
        print("COMBINE return epsilon true")
        return True,spp1 #epsilon
 

# CONTRI -> TERM | NOT CONTRI
# function CONTRI ----------------------------------------- good
def CONTRI(s,spp,indent):
    show(indent,'CONTRI',s,spp)
    indent1 = indent + ' '
    spp1 =spp

    token = LookAhead(s,spp)
    if token == NOT:
        token,spp = NextToken(s,spp)
        res,spp = CONTRI(s,spp,indent1)
        if res:
            print("CONTRI return true")
            return True,spp
        else:
            print("CONTRI return false, CONTRI followed by not failed")
            return False,spp1
    else: 
        res,spp = TERM(s,spp,indent1)
        if res:
            print("CONTRI:TERM return true")
            return True,spp
        else:
            print("CONTRI return false, TERM failed")
            return False,spp1

# end CONTRI

# TERM -> T | F | VAR | LP FINALEXPR RP
# function TERM ----------------------------------------- half good
def TERM(s,spp,indent):
    show(indent,'TERM',s,spp)
    indent1 = indent + ' '
    spp1 =spp

    token = LookAhead(s,spp)
    if (token == T) or (token == F)  or (token == VAR):
        token,spp = NextToken(s,spp)
        print("Term True with T,F,VAR")
        return True,spp
    elif token == LP:
        token,spp = NextToken(s,spp)
        res,spp = FINALEXPR(s,spp,indent1)
        if not res:
            print("Term False for finalexpr")
            return False,spp1
        token,spp = NextToken(s,spp)
        if token == RP:
            return True,spp
        else:
            print("Term False for RP")
            return False,spp1
    else:
        return False,spp1

# the scanner ######################################################
# function LookAhead ------------------------------------------- 
def LookAhead(s,spp):
    j = len(s);
    i = spp
    if i >= j:
        return EOI
    while s[i]==" " or s[i]=="\n":
        i = i+1
        if i >= j:
            return EOI
    if s[i]=='=':
        return EQUAL
    elif s[i]=='F':
        return F
    elif s[i]=='T':
        return T
    elif s[i]=='n':
        return NOT
    elif s[i]=='a':
        return AND
    elif s[i]=='o':
        return OR
    elif s[i]=='(':
        return LP
    elif s[i]==')':
        return RP
    elif s[i]=='$':
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
    elif s[spp]=='T':
        return T,spp+4
    elif s[spp] == "F":
        return F,spp+5
    elif s[spp] == "a":
        return AND,spp+3
    elif s[spp] == "o":
        return OR,spp+2
    elif s[spp] == "n":
        return NOT,spp+3
    elif s[spp] == "(":
        return LP,spp+1
    elif s[spp] == ")":
        return RP,spp+1
    elif s[spp] == "=":
        return EQUAL,spp+1
    elif s[spp] == "$":
        return VAR, spp+2 ##should modify this later when name could be longer!
    else:
        return ERR,spp1
#end NUM


#main section-----------------------
s = "True = $C"
show('','main',s,0)
indent = ' '
res = Parse(s,indent);


# is there a leftover?
if res:
    print("parsing OK")
else:
    print("parse Error!")
#end main section
