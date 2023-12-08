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
LP = 'LP'  # Character (
RP = 'RP'  # Character )
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
    result, spp = statment(s, spp, indent, result)

    return result, spp

def statment(s, spp, indent, result):
    #show(indent, 'statment', s, spp)
    indent1 = indent + ' '

    # Keep the previous position saved
    previous_spp = spp

    # Let's read a token
    token, spp = NextToken(s, spp)

    if token == EOI or token == ERR:
        # Statement is a True term
        # Add the term to the list of tokens and return the statement
        result.append(token)
        return result, spp
    elif token == THEN or token == ELSE:
        return statment(s, spp, indent, result)
    else:
        # token == LP or token == IfThenElse or token == RP or token == Succ or token == Pred or token == IsZero
        # or token == IfThenElse:
        # We are going to either read another statement
        # Add the term and read another statement
        result.append(token)
        return statment(s, spp, indent, result)

    # # We have a special case. If term | statement then term | statement else term | else
    # if token == Succ or token == Pred or token == IsZero:
    #     # We need to read another token and repeat what we did above
    #     # Add the token to the list of the tokens
    #     result.append(token)
    #     # We need to read the next token
    #     token, spp = NextToken(s, spp)
    # # Two special case are `Then` and `Else` tokens
    # if token == THEN or token == ELSE:
    #     # We do not add the tokens to the token list
    #     # Just read the next token
    #     token, spp = NextToken(s, spp)
    #
    # # A token could be either a term or termTail.
    # # If it is a term then it is either 'Tr' or 'Fa' or 'Ze' or LP statment RP
    # if token == Tr or token == Fa or token == Ze or token == RP:
    #     # Statement is a True term
    #     # Add the term to the list of tokens and return the statement
    #     result.append(token)
    #     return result, spp
    # elif token == LP:
    #     # We are going to either read another statment
    #     # Add the term and read another statement
    #     result.append(token)
    #     return statment(s, spp, indent, result)


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
# end NUM


# main section
s = "if isZero(pred(succ(0))) then true else false"
# What we expect
expected_string = "ifThenElse PRED LP SUC LP Zr RP RP Tr Fa EOI"

# I need a variable that keeps to index value. This will help
# me to figure out where in the string I am.
spp = 0  # Initial value will be zero since we are at index zero.
# Let's define a list that is going to keep the tokens

final_tokens_list, spp = Parse(s, "")


# is there a leftover ?
if spp < len(s) - 1:
    print("parse Error")
else:
    print("parsing OK")
    print(' '.join(final_tokens_list))
# end main section

# end of Question 9 ########################################################
