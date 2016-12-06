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
            while bandera < len(self.input):
                token = self.getNextToken(bandera)
                print(token)
                if token[1] != "BLANCO" and token != None:
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
        self.tokens.append((float("inf"), "END", "\0"))  # poner caracter de fin
        self.index = 0  # index para el contador de los tokens
    def make_link(self, N_actual, N_destino, etiqueta):
        if not N_actual in self.D:
            self.D[N_actual] = {}
        if not N_destino in self.D:
            self.D[N_destino] = {}
        self.D[N_actual][etiqueta] = N_destino
    # Funciones que majean el arbol sintactico
    def inicio(self):
        print(self.tokens)
        self.root = self.or_exp()
    def preOrden(self, nodo, h=0):
        print("\t" * h, nodo.Dato)
        if not nodo.isCaracter:
            if nodo.izquierdo != None:
                self.preOrden(nodo.izquierdo, h + 1)
            if nodo.derecho != None:
                self.preOrden(nodo.derecho, h +1)
    def anulable(self, nodo):
        if nodo.isCaracter:
            return False
        elif nodo.Dato[1] is "OR":
            return self.anulable(nodo.derecho) or self.anulable(nodo.izquierdo)
        elif nodo.Dato[1] is "CONCATENACION":
            return self.anulable(nodo.derecho) and self.anulable(nodo.izquierdo)
        elif nodo.Dato[1] is "KLEENE":
            return True
        elif nodo.Dato[1] is "END":
            return True
        elif nodo.Dato[1] is "+":
            return self.anulable(nodo.derecho)
    def primerapos(self, nodo):
        if nodo.isCaracter:
            return [nodo]
        elif nodo.Dato[1] is "OR":
            return self.primerapos(nodo.izquierdo) + self.primerapos(nodo.derecho)
        elif nodo.Dato[1] is "CONCATENACION":
            if self.anulable(nodo.izquierdo):
                return self.primerapos(nodo.izquierdo) + self.primerapos(nodo.derecho)
            else:
                return self.primerapos(nodo.izquierdo)
        elif nodo.Dato[1] is "KLEENE" or nodo.Dato[1] is "+":
            return self.primerapos(nodo.derecho)
    def ultimapos(self, nodo):
        if nodo.isCaracter:
            return [nodo]
        elif nodo.Dato[1] is "OR":
            return self.ultimapos(nodo.izquierdo) + self.ultimapos(nodo.derecho)
        elif nodo.Dato[1] is "CONCATENACION":
            if self.anulable(nodo.derecho):
                return self.ultimapos(nodo.izquierdo) + self.ultimapos(nodo.derecho)
            else:
                return self.ultimapos(nodo.derecho)
        elif nodo.Dato[1] is "KLEENE" or nodo.Dato[1] is "+":
            return self.ultimapos(nodo.derecho)
    def siguientepos(self, nodo):
        if nodo is self.root:
            return []
        padre = nodo.padre
        if padre.izquierdo is nodo:
            if padre.Dato[1] is "CONCATENACION":
                return self.primerapos(padre.derecho)
            elif padre.Dato[1] is "OR":
                return self.siguientepos(padre)
        else:
            if padre.Dato[1] is "CONCATENACION":
                return self.siguientepos(padre)
            elif padre.Dato[1] is "OR":
                return self.siguientepos(padre)
            elif padre.Dato[1] is "+" or padre.Dato[1] is "KLEENE":
                return self.siguientepos(padre) + self.primerapos(padre)
    # Construir el automata
    def construir_automata(self):
        aux = sort_nodos(self.primerapos(parser.root))
        cola = [aux]
        lista_full = [aux]
        for estado in cola:
            # separar y clasificar los distintos tipos de simbolos en el estado actual y guardarlo en simbolos
            simbolos = {}
            for simbol in estado:
                s = ""
                if type(simbol) == Nodo:
                    # hacer asociacion de simbolos en el diccionario simbolos
                    s = s.join(simbol.Dato[2:])
                    if s not in simbolos:
                        simbolos[s] = []
                    simbolos[s].append(simbol)  # Agrega el nodo correspondiente al simbolo

            # Para cada simbolo de entrada 'a' en el diccionario, dejar que U sea la union de siguientepos(p) para
            # todas las 'p'=nodos actuales que correspondan con el simbolo 'a'
            for simbolo in simbolos:
                U = []
                for nodo in simbolos[simbolo]:  # union
                    U += self.siguientepos(nodo)
                U = sort_nodos(U)
                if U not in lista_full:
                    cola += [U]
                    lista_full += [U]

                self.make_link(lista_full.index(estado), \
                               lista_full.index(U), \
                               simbolo)
    #recursiones que contruyen el arbol sintactico
    def or_exp(self, h=0):
        # print"or_exp"
        print("  " * h, "or_exp")
        hijo = self.cat_exp(h + 1)
        return self.or_exp_p(hijo, h + 1)

    def or_exp_p(self, izquierdo, h):
        print("  " * h, "or_exp_p")
        nodo = Nodo();
        if self.tokens[self.index][1] == "OR":
            izquierdo.padre = nodo
            nodo.isCaracter = False
            nodo.Dato = self.tokens[self.index]
            self.index += 1
            hijo = self.cat_exp(h + 1)
            derecho = self.or_exp_p(hijo, h +1)
            derecho.padre = nodo
            nodo.izquierdo = izquierdo
            nodo.derecho = derecho
            return nodo
        else:
            return izquierdo

    def cat_exp(self, h):
        print("  " * h, "cat_exp")
        hijo = self.kleene(h + 1)
        return self.cat_exp_p(hijo, h + 1)

    def cat_exp_p(self, izquierdo, h):
        print("  " * h, "cat_exp_p")
        nodo = Nodo();
        if (self.tokens[self.index][1] == "SIMBOLO" or self.tokens[self.index][1] == "PO") \
                and self.index < len(self.tokens):
            izquierdo.padre = nodo
            nodo.isCaracter = False
            nodo.Dato = (self.tokens[self.index][0], "CONCATENACION", '')
            hijo = self.kleene(h + 1)
            derecho = self.cat_exp_p(hijo, h +1)
            derecho.padre = nodo
            nodo.derecho = derecho
            nodo.izquierdo = izquierdo
            return nodo
        else:
            return izquierdo

    def kleene(self, h):
        print("  " * h, "kleene")
        hijo = self.parent(h + 1)
        return self.kleene_p(hijo, h + 1)

    def kleene_p(self, hijo, h):
        nodo = Nodo();
        # Estrella de kleene solo genera hijos derechos
        print("  " * h, "kleene_p")
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

    def parent(self, h):
        print("  " * h, "parent")
        if self.tokens[self.index][1] == "PO" and self.index < len(self.tokens):
            self.index += 1
            hijo = self.or_exp(h +1)
            if self.tokens[self.index][1] != "PC" and self.index < len(self.tokens):
                raise Exception("No hay equilibrio de parentecis", self.tokens[self.index][0])
            else:
                self.index += 1
                return hijo
        elif self.tokens[self.index][1] == "SIMBOLO" and self.index < len(self.tokens):
            self.index += 1
            nodo = Nodo();
            nodo.isCaracter = True
            nodo.Dato = self.tokens[self.index - 1]
            return nodo
        elif self.tokens[self.index][1] == "CUALQUIER NUMERO" and self.index < len(self.tokens):
            self.index += 1
            nodo = Nodo();
            nodo.isCaracter = True
            nodo.Dato = self.tokens[self.index - 1]
            return nodo
        elif self.tokens[self.index][1] == "CUALQUIER LETRA" and self.index < len(self.tokens):
            self.index += 1
            nodo = Nodo();
            nodo.isCaracter = True
            nodo.Dato = self.tokens[self.index - 1]
            return nodo
        elif self.tokens[self.index][1] == "CUALQUIERCOSA" and self.index < len(self.tokens):
            self.index += 1
            nodo = Nodo();
            nodo.isCaracter = True
            nodo.Dato = self.tokens[self.index - 1]
            return nodo
        elif self.tokens[self.index][1] == "END" and self.index < len(self.tokens):
            self.index += 1
            nodo = Nodo();
            nodo.isCaracter = True
            nodo.Dato = self.tokens[self.index - 1]
            return nodo


def sort_nodos(U):
    '''
    :param U: Lista de nodos en cualquier orden
    :return: Lista de nodos ordenados por orden de la aparicion del toquen que contienen.
    '''
    if type(U) is not list:
        raise Exception("Esta funcion solo admite lsitas de nodos")
    return sorted(U, key=lambda nodo: nodo.Dato[0])

#para el lexer y definicion de tokens
archivo = open ( sys.argv[1]+".lx")
texto = archivo.readlines()

for expresiones in texto:
    print("-------------------------------------")
    aux = expresiones.split("=>")
    if len(aux) < 2:
        sys.stderr.write("\nHay una regla sin nombre")
        continue
    name = aux[0]
    lexer = LexicoLexer(aux[1])
    tokens = lexer.getTokenList()
    print(tokens)
    parser = LexicoParser(tokens)
    parser.inicio()
    print(parser.root.Dato)
    parser.preOrden(parser.root)
    # aux = (parser.siguientepos(parser.root.izquierdo.derecho.derecho))
    '''print("Testing ")
    for nodo in aux:
        print (nodo.Dato)'''

    print(parser.D)







#parser.construir_automata()
