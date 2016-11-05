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
            elif c == '|':
                state = 11
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
            return (index-1, "PO" )
        elif state == 2:
            return (index-1, "PC" )
        elif state == 3:
            if c == '-':
                state = 4
                return_aux = (index-1,"SIMBOLO")
            else:
                index-=1
                state = 15
        elif state == 4:
            if c.isalpha():
                state = 5
            elif return_aux is not None:
                return return_aux
            else:
                index-=1
                state = 14
        elif state == 5:
            return (index-1,"CUALQUIER LETRA")
        elif state == 6:
            if c == '-':
                state = 7
                return_aux = (index-1,"SIMBOLO")
            else:
                index-=1
                state = 15
        elif state == 7:
            if c.isdigit():
                state = 8
            elif return_aux is not None:
                return return_aux
            else:
                index-=1
                state = 14
        elif state == 8:
            return (index-1,"CUALQUIER NUMERO")
        elif state == 9:
            return (index-1,"+")
        elif state == 10:
            return (index-1,"KLEENE")
        elif state == 11:
            return (index-1,"OR")
        elif state == 12:
            return (index-1,"ASIGNACION")
        elif state == 13:
            return (index-1,"CUALQUIERCOSA")
        elif state == 14:  #TODO: testing
            return (index-1,"SIMBOLO")
        elif state == 15:
            return (index-1,"SIMBOLO")
        elif state == 16:
            if c == '=':
                state = 12
        elif state == 17:
            return (index-1,"OPER ?")
        elif state == 18:
            if c == '\t' or c == '\n' or c == ' ':
                state = 18
            else:
                return (index-1,"BLANCO")
        else:
            return (index, "DESCONOCIDO")

index = 0
while index < len(input)-1:
    t = token(input,index)
    if t[1] is not "BLANCO":
        print input[index:t[0]], "\t", t
    index = t[0]
