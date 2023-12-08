# This program can be run as python2 or as python3
from __future__ import print_function

# Question 7 #########################################################
# tokens:
# Start with this tokens
EOI = 'EOI'  # end of input
Tr = 'Tr'  # Constant True - True
Fa = 'Fa'  # Constant False - False
Ze = 'Ze'  # Constant Zero - 0
Succ = 'Succ'  # Successor (succ term)
Pred = 'Pred'  # Predecessor (pred term)
IsZero = 'IsZero'  # Zero Test (isZero term)
IfThenElse = 'IfThenElse'  # Conditional Expression (if term then term else term)
# Add these tokens later
LP = 'LP'  # Character \(
RP = 'RP'  # Character \)
ERR = 'ERR'  # Showing Error
# Tokens that I add but not use
THEN = 'THEN'
ELSE = 'ELSE'
# end of Question 7 ##################################################

# Question 8 - Grammar ###############################################
# statment -> term | termTail
# termTail -> Succ term | Pred term | isZero term | ifThenElse term term term
# term -> Tr | Fa | Ze | (Add this later) LP statment RP
# end of Question 8 ##################################################


# Question 9 - recursive descent parser###############################
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


def EatWhiteSpace(s, spp):
    j = len(s)
    if spp >= j:
        return spp

    while s[spp] == ' ' or s[spp] == '\n':
        spp = spp + 1
        if spp >= j:
            break

    return spp


# end EatWhiteSpace


# prog -> VAR tail1 | NUM tail2 | MINUS {VAR NUM} tail2 | LP expr RP | epsilon
# function prog ------------------------------------------------------------
def Parse(s, indent):
    # show(indent, 'Parse', s, 0)
    # Starting index
    spp = 0
    # Keeping the tokens
    result = []

    indent1 = indent + ' '

    # Need to start reading the statments
    result, spp = statment(s, spp, result)

    return result, spp


def statment(s, spp, result):

    next_token = lookAhead(s, spp)

    if next_token == Tr or next_token == Fa or next_token == EOI or next_token == ERR or next_token == Ze:
        # Read the next token
        token, spp = NextToken(s, spp)
        # Add the token to the result
        result.append(token)
        return result, spp
    elif next_token == IfThenElse:
        # Read the next token
        token, spp = NextToken(s, spp)
        
        # Add the token to the list
        result.append(token)
        
        # Read the next token
        next_token = lookAhead(s, spp)
        
        # When it is going to be an error:
        if next_token == RP or next_token== IfThenElse or next_token == THEN or next_token == ELSE:
            result.append(ERR)
            return result, spp
        # If not read the rest of statement
        
        # Read the statement
        result, spp = statment(s, spp, result)
        # Read the next token
        
        next_token = lookAhead(s, spp)
        if next_token is not THEN:
            # This is an error
            result.append(ERR)
            return result, spp
        else:
            # Continue reading statments
            return statment(s, spp, result)
    
    elif next_token == THEN:
        # Read the next token
        token, spp = NextToken(s, spp)
        
        # We are not going to add anything
        next_token = lookAhead(s, spp)
        # When it is going to be an error:
        
        if next_token == RP or next_token==IfThenElse or next_token == THEN or next_token == ELSE:
            result.append(ERR)
            return result, spp

        # Read the statement
        result, spp = statment(s, spp, result)

        # Read the next token
        next_token = lookAhead(s, spp)
        
        if next_token is not ELSE:
            # This is an error
            result.append(ERR)
            return result, spp
        else:
            # If not read the rest of statement
            return statment(s, spp, result)
    
    elif next_token == ELSE:
    
        # Read the next token
        token, spp = NextToken(s, spp)
        # Nothing will be added to the results
    
        # Read the next token
        next_token = lookAhead(s, spp)
    
        # When it is going to be an error:
        if next_token == RP or next_token == IfThenElse or next_token == THEN or next_token == ELSE:
            result.append(ERR)
            return result, spp
    
        # If not read the rest of statement
        return statment(s, spp, result)
    elif next_token == LP:
    
        # Read the next token
        token, spp = NextToken(s, spp)
        # Add to the result
        result.append(token)
        # Check if you are not reading a RP after LP
        next_token = lookAhead(s, spp)
        if next_token == RP:
            result.append(ERR)
            return result, spp

        # read the terms
        result, spp = statment(s, spp, result)
    
        # Read the next token
        next_token = lookAhead(s, spp)
    
        if next_token == RP:
            # read the next token
            token, spp = NextToken(s, spp)
            result.append(token)
            return result, spp
        else:
            # it should be an error
            result.append(ERR)
            return result, spp
    
    elif next_token == RP:
        # This is an error
        result.append(ERR)
        return result, spp
    
    elif next_token == Pred or next_token == Succ or next_token == IsZero:
        token, spp = NextToken(s, spp)
        result.append(token)
        # Read the next token
        next_token = lookAhead(s, spp)
    
        if next_token == LP or next_token == Tr or next_token == Fa or next_token == EOI or next_token == ERR:
            # Read the statement
            return statment(s, spp, result)
        else:
            # It is an error
            result.append(ERR)
            return result, spp


def term(s, spp, result):
    next_token = lookAhead(s, spp)
    if next_token == Tr or next_token == Fa:
        token, spp = NextToken(s, spp)
        result.append(token)
        return result, spp
    elif next_token == Pred or next_token == Succ or next_token == IsZero:
        # read the next token
        token, spp = NextToken(s, spp)
        result.append(token)
        # Read the next token
        next_token = lookAhead(s, spp)
        if next_token == LP:
            # Read the statment
            return statment(s, spp, result)
        else:
            # It is an error
            result.append(ERR)
            return result, spp


def lookAhead(s, spp):
    spp1 = spp
    spp = EatWhiteSpace(s, spp)
    j = len(s)
    if spp >= j:
        return EOI
    elif s[spp: spp + 4] == 'pred':
        return Pred
    elif s[spp: spp + 4] == "succ":
        return Succ
    elif s[spp: spp + 6] == "isZero":
        return IsZero
    elif s[spp: spp + 2] == "if":
        return IfThenElse
    elif s[spp: spp + 4] == "then":
        return THEN
    elif s[spp: spp + 4] == "else":
        return ELSE
    elif s[spp] == "(":
        return LP
    elif s[spp] == ")":
        return RP
    elif s[spp] == "0":
        return Ze
    elif s[spp:spp + 4] == "true":
        return Tr
    elif s[spp:spp + 5] == "false":
        return Fa
    else:
        return ERR


# function NextToken ---------------------------------------------
def NextToken(s, spp):
    spp1 = spp
    spp = EatWhiteSpace(s, spp)
    j = len(s)
    if spp >= j:
        return EOI, spp
    elif s[spp: spp + 4] == 'pred':
        return Pred, spp + 4
    elif s[spp: spp + 4] == "succ":
        return Succ, spp + 4
    elif s[spp: spp + 6] == "isZero":
        return IsZero, spp + 6
    elif s[spp: spp + 2] == "if":
        return IfThenElse, spp + 2
    elif s[spp: spp + 4] == "then":
        return THEN, spp + 4
    elif s[spp: spp + 4] == "else":
        return ELSE, spp + 4
    elif s[spp] == "(":
        return LP, spp + 1
    elif s[spp] == ")":
        return RP, spp + 1
    elif s[spp] == "0":
        return Ze, spp + 1
    elif s[spp:spp + 4] == "true":
        return Tr, spp + 4
    elif s[spp:spp + 5] == "false":
        return Fa, spp + 5
    else:
        return ERR, spp1


# main section
s = "if isZero(true) then true else false"
# What we expect

# (t_1 -> term) and (t_2 -> term) and (t_3 -> term) => if t_1 then t_2 else t_3 is a conditional expression

# What this mean?
# ----------------
# Is this a conditional expression ? if if then true else false
# Is this a conditional expression ? if pred(succ(0)) then 0 else true
# Is thi a conditional expression ? if secc(0)) then if else then?


# What we need to do?
# ----------------------
# We need to figure out what happens when we pass `if`, `then`, `else` to the parser.
# Give me suggestions?


# How we should do this?
# ------------------------
# If we are able to look ahead and find what we need to do if we receive any of the `if`, `then` or `else`,
# then we would able to have a proper instruciton of what needed to happen.

expected_string = "ifThenElse PRED LP SUC LP Zr RP RP Tr Fa EOI"

# I need a variable that keeps to index value. This will help
# me to figure out where in the string I am.
spp = 0  # Initial value will be zero since we are at index zero.
# Let's define a list that is going to keep the tokens

final_tokens_list, spp = Parse(s, "")

# is there a leftover ?
if spp < len(s) - 1:
    print("parse Error")
    print(' '.join(final_tokens_list))
else:
    print("parsing OK")
    print(' '.join(final_tokens_list))
# end main section

# end of Question 9 ########################################################
