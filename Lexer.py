import sys


class Nodo:
    def __init__(self):
        self.isCaracter = None  # Booleano que define si es operacion o simbolos
        self.Dato = None  # Caracter o Operacion padre
        self.izquierdo = None
        self.derecho = None
        self.padre = None
        self.etiqueta = None
class LexicoLexer:
    def __init__(self, entrada):
        self.input = entrada
        self.TokenList = []
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
                return (ind - 1, "CONCATENACION")
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
                if token[1] != "BLANCO":
                    txt = self.input[bandera:token[0]]
                    (self.TokenList).append( token + tuple(txt) )
                bandera = token[0]
        return self.TokenList
class LexicoParser:
    def __init__(self,tokens):
        if type(tokens) != type(list()):
            raise Exception("Debe ingresar una lista de tokens.")
            return
        #Lista de primeras en
        self.D = {}
        self.tokens = tokens
        self.tokens.append((None, None, None))
        self.index = 0  # index para el contador de los tokens
        self.etiqueta = 0  #Etiquetas para los nodos
        self.aux = 0
        # Funciones de linkeo

    def make_link(self, N_actual, N_destino, etiqueta):
        if not N_actual in self.D:
            self.D[N_actual] = {}
        if not N_destino in self.D:
            self.D[N_destino] = {}
        self.D[N_actual][etiqueta] = N_destino

    # Funciones que majean el arbol sintactico
    def inicio(self):
        self.root = self.or_exp()

    def preOrden(self, nodo, h=0):
        print("\t" * h, nodo.Dato)
        if not nodo.isCaracter:
            if nodo.izquierdo != None:
                self.preOrden(nodo.izquierdo, h + 1)
            if nodo.derecho != None:
                self.preOrden(nodo.derecho, h + 1)

    def anulable(self, nodo):
        if nodo.Dato[1] == "KLEENE":
            return True
        else:
            return False

    def primerapos(self, nodo):
        token = nodo.Dato[1]
        if token == "OR":
            return self.primerapos(nodo.izquierdo) + self.primerapos(nodo.derecho)
        elif token == "CONCATENACION":
            return self.primerapos(nodo.izquierdo)
        elif token == "KLEENE" or token == "+":
            return self.primerapos(nodo.derecho) + self.siguientepos(nodo)
        else:
            return [("".join(nodo.Dato[2:]), nodo.etiqueta, nodo)]

    def ultimapos(self, nodo):
        token = nodo.Dato[1]
        if token == "OR":
            return self.primerapos(nodo.izquierdo) + self.primerapos(nodo.derecho)
        elif token == "CONCATENACION":
            return self.primerapos(nodo.derecho)
        elif token == "KLEENE" or token == "+":
            return self.primerapos(nodo.derecho)
        else:
            return [("".join(nodo.Dato[2:]), nodo.etiqueta, nodo)]

    def siguientepos(self, nodo):
        return self.primerapos(nodo.padre.derecho)

    # Construir el automata
    def construir_automata(self):
        estado = []
        marcados = {}
        simbolos = []
        nodos = []
        for (a, b, c) in self.primerapos(self.root):
            estado.append(b)
            if a not in simbolos:
                simbolos.append(a)
            if c not in nodos:
                nodos.append(c)

        marcados[estado] = "blanco"
        for b in marcados:
            marcados[b] = "negro"
            U = []
            for c in simbolos:
                for nodo in nodos:
                    if c == "".join(nodo.Dato[3:]):
                        U.append(nodo.etiqueta)
                if U not in marcados:
                    marcados[U] = "blanco"
                self.make_link(b, U, c)

    #recursiones que contruyen el arbol sintactico
    def or_exp(self):
        # print"or_exp"
        hijo = self.cat_exp()
        return self.or_exp_p(hijo)

    def or_exp_p(self, izquierdo):
        nodo = Nodo();
        self.etiqueta += 1
        nodo.etiqueta = self.etiqueta
        if self.tokens[self.index][1] == "OR":
            izquierdo.padre = nodo
            nodo.isCaracter = False
            nodo.Dato = self.tokens[self.index]
            self.index += 1
            hijo = self.cat_exp()
            derecho = self.or_exp_p(hijo)
            derecho.padre = nodo
            nodo.izquierdo = izquierdo
            nodo.derecho = derecho
            return nodo
        else:
            return izquierdo

    def cat_exp(self):
        hijo = self.kleene()
        return self.cat_exp_p(hijo)

    def cat_exp_p(self, izquierdo):
        nodo = Nodo();
        self.etiqueta += 1
        nodo.etiqueta = self.etiqueta
        if self.tokens[self.index][1] == "CONCATENACION" and self.index < len(self.tokens):
            izquierdo.padre = nodo
            nodo.isCaracter = False
            nodo.Dato = self.tokens[self.index]
            self.index += 1
            hijo = self.kleene()
            derecho = self.cat_exp_p(hijo)
            derecho.padre = nodo
            nodo.derecho = derecho
            nodo.izquierdo = izquierdo
            return nodo
        else:
            return izquierdo

    def kleene(self):
        hijo = self.parent()
        return self.kleene_p(hijo)

    def kleene_p(self, hijo):
        nodo = Nodo();
        self.etiqueta += 1
        nodo.etiqueta = self.etiqueta  # Estrella de kleene solo genera hijos derechos
        if self.tokens[self.index][1] == "+" and self.index < len(self.tokens):
            hijo.padre = nodo
            nodo.isCaracter = False
            nodo.Dato = self.tokens[self.index]
            nodo.derecho = hijo
            self.index += 1
            return nodo
        elif self.tokens[self.index][1] == "KLEENE" and self.index < len(self.tokens):
            hijo.padre = nodo
            nodo.isCaracter = False
            nodo.Dato = self.tokens[self.index]
            nodo.derecho = hijo
            self.index += 1
            return nodo
        else:
            return hijo
    def parent(self):
        if self.tokens[self.index][1] == "PO" and self.index < len(self.tokens):
            self.index += 1
            hijo = self.or_exp()
            if self.tokens[self.index][1] != "PC" and self.index < len(self.tokens):
                raise Exception("No hay equilibrio de parentecis", self.tokens[self.index][0])
            else:
                self.index += 1
                return hijo
        elif self.tokens[self.index][1] == "SIMBOLO" and self.index < len(self.tokens):
            self.index += 1
            nodo = Nodo();
            self.etiqueta += 1
            nodo.etiqueta = self.etiqueta
            nodo.isCaracter = True
            nodo.Dato = self.tokens[self.index - 1]
            return nodo
        elif self.tokens[self.index][1] == "CUALQUIER NUMERO" and self.index < len(self.tokens):
            self.index += 1
            nodo = Nodo();
            self.etiqueta += 1
            nodo.etiqueta = self.etiqueta
            nodo.isCaracter = True
            nodo.Dato = self.tokens[self.index - 1]
            return nodo
        elif self.tokens[self.index][1] == "CUALQUIER LETRA" and self.index < len(self.tokens):
            self.index += 1
            nodo = Nodo();
            self.etiqueta += 1
            nodo.etiqueta = self.etiqueta
            nodo.isCaracter = True
            nodo.Dato = self.tokens[self.index - 1]
            return nodo
        elif self.tokens[self.index][1] == "CUALQUIERCOSA" and self.index < len(self.tokens):
            self.index += 1
            nodo = Nodo();
            self.etiqueta += 1
            nodo.etiqueta = self.etiqueta
            nodo.isCaracter = True
            nodo.Dato = self.tokens[self.index - 1]
            return nodo


#para el lexer y definicion de tokens
archivo = open ( sys.argv[1]+".lx")
texto = archivo.readlines()
for expresiones in texto:
    print("-------------------------------------")
    aux = expresiones.split("=>")
    if len(aux) < 2:
        raise Exception("Hay una regla sin nombre")
    name = aux[0]
    lexer = LexicoLexer(aux[1])
    tokens = lexer.getTokenList()
    parser = LexicoParser(tokens)
    parser.inicio()
    parser.preOrden(parser.root)
    #parser.construir_automata()
