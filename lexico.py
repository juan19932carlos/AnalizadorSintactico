import sys
input = "".join(sys.stdin.readlines())

def token(input,init):
    state = 0
    index = init
    return_aux = None
    while index < len(input):
        c = input[index]
        index+=1
        if state == 0:
            if c == '(' or c == '[':
                state = 1
            elif c == ')' or c == ']':
                state = 2
            elif c.isalpha():
                state = 3
            elif c.isdigit():
                state = 6
            elif c == '+':
                state = 9
            elif c == '*':
                state = 10
            elif c == ':':
                state = 16
            elif c == '=':
                state = 12
            elif c == '.':
                state == 13
            elif c == '?':
                state = 17
            elif c == '\t' or c == '\n' or c == ' ':
                state = 18
            else:
                state = 14
        elif state == 1:
            return [ index-1, "PO" ]
        elif state == 2:
            return [ index-1, "PC" ]
        elif state == 3:
            if c == '-':
                state = 4
            else:
                state = 15
        elif state == 18: #Espacios en blanco
            if c == '\t' or c == '\n' or c == ' ':
                state = 18
            else:
                return [index-1,"BLANCO"]
        else:
            return [index, "DESCONOCIDO"]

index = 0
print "input len:",len(input)
while index < len(input):
    t = token(input,index)
    print input[index:t[0]], "\t", t
    index = t[0]
