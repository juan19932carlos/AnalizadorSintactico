import sys

class Lexer:
    def __init__(self, entrada):
        self.input = entrada
        self.TokenList = list()
        self.index = 0
    def getNextToken(self,ind = None):
        state = 0
        return_aux = None
        if ind == None:
            ind = self.index
        while ind < len(self.input):
            c = self.input[ind]
            ind += 1
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
                elif c == '"':
                    state = 19
                else:
                    state = 14
            elif state == 1:
                return (ind - 1, "PO")
            elif state == 2:
                return (ind - 1, "PC")
            elif state == 3:
                if c == '-':
                    state = 4
                    return_aux = (ind - 1, "SIMBOLO")
                else:
                    ind -= 1
                    state = 15
            elif state == 4:
                if c.isalpha():
                    state = 5
                elif return_aux is not None:
                    return return_aux
                else:
                    ind -= 1
                    state = 14
            elif state == 5:
                return (ind - 1, "CUALQUIER LETRA")
            elif state == 6:
                if c == '-':
                    state = 7
                    return_aux = (ind - 1, "SIMBOLO")
                else:
                    ind -= 1
                    state = 15
            elif state == 7:
                if c.isdigit():
                    state = 8
                elif return_aux is not None:
                    return return_aux
                else:
                    ind -= 1
                    state = 14
            elif state == 8:
                return (ind - 1, "CUALQUIER NUMERO")
            elif state == 9:
                return (ind - 1, "+")
            elif state == 10:
                return (ind - 1, "KLEENE")
            elif state == 11:
                return (ind - 1, "OR")
            elif state == 12:
                return (ind - 1, "ASIGNACION")
            elif state == 13:
                return (ind - 1, "CUALQUIERCOSA")
            elif state == 14:  # TODO: testing
                return (ind - 1, "NO REC")
            elif state == 15:
                return (ind - 1, "SIMBOLO")
            elif state == 16:
                if c == '=':
                    state = 12
            elif state == 17:
                return (ind - 1, "OPER ?")
            elif state == 18:
                if c == '\t' or c == '\n' or c == ' ':
                    state = 18
                else:
                    return (ind - 1, "BLANCO")
            elif state == 19:
                return (ind - 1, "COMILLA")
            else:
                return (ind, "DESCONOCIDO")
    def getTokenList(self,remake = False):
        bandera = 0
        if remake or len(self.TokenList) == 0:
            while bandera < len(self.input)-1:
                token = self.getNextToken(bandera)
                self.TokenList.append( token )
                bandera += token[0]
        return self.TokenList

class parser:
    def __init__(self,input):
        if type(input) != type(list()):
            raise Exception("Debe ingresar una lista de tokens.")
            return
        #Lista de primeras en
        self.primeras = {}
        self.primeras["init"]=[""]
        self.index = 0
        self.inicio(input)

    def inicio(self,input):



input = "".join( sys.stdin.readlines() )
lexer = Lexer(input)
print lexer.getTokenList()
