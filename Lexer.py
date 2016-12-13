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
        self.input = entrada + '$'
        self.TokenList = []
        self.index = 0

    def getNextToken(self, index=0):
        '''
        :param ind: indice desde el cual empieza a buscar en el string de entrada
        :return: tupla generada por segun los estados de aceptacion.
        '''
        ind = index
        state = 0
        while (ind <= len(self.input)):
            if state is 0:
                c = self.input[ind]
                ind += 1
                if c.isalpha():
                    state = 1
                elif c.isnumeric():
                    state = 4
                elif c is '(' or c is '[':
                    state = 7
                elif c is ')' or c is ']':
                    state = 8
                elif c is '|':
                    state = 9
                elif c is '*':
                    state = 10
                elif c is '+':
                    state = 11
                elif c is ' ':
                    state = 13
                elif c is '$':
                    state = 15
                else:
                    self.fallo()
            elif state is 1:
                c = self.input[ind]
                ind += 1
                if c is '-':
                    state = 2
                else:
                    state = 12
            elif state is 2:
                c = self.input[ind]
                ind += 1
                if c.isalpha():
                    state = 3
                else:
                    self.fallo()
            elif state is 3:
                break
            elif state is 4:
                c = self.input[ind]
                ind += 1
                if c is '-':
                    state = 5
                else:
                    state = 12
            elif state is 5:
                c = self.input[ind]
                ind += 1
                if c.isnumeric():
                    state = 6
                else:
                    self.fallo()
            elif state is 6:
                break
            elif state is 7:
                break
            elif state is 8:
                break
            elif state is 9:
                break
            elif state is 10:
                break
            elif state is 11:
                break
            elif state is 12:
                ind -= 1
                break
            elif state is 13:
                c = self.input[ind]
                ind += 1
                if c is ' ':
                    state = 13
                else:
                    state = 14
            elif state is 14:
                ind -= 1
                break
            elif state is 15:
                break
            else:
                self.fallo()

        # Estados de aceptación
        if state is 3:
            return (ind, "CUALQUIER LETRA", "".join(self.input[index:ind]))
        elif state is 6:
            return (ind, "CUALQUIER NUMERO", "".join(self.input[index:ind]))
        elif state is 7:
            return (ind, "PO", "".join(self.input[index:ind]))
        elif state is 8:
            return (ind, "PC", "".join(self.input[index:ind]))
        elif state is 9:
            return (ind, "OR", "".join(self.input[index:ind]))
        elif state is 10:
            return (ind, "KLEENE", "".join(self.input[index:ind]))
        elif state is 11:
            return (ind, "+", "".join(self.input[index:ind]))
        elif state is 12:
            return (ind, "SIMBOLO", "".join(self.input[index:ind]))
        elif state is 14:
            return (ind, "BLANCO", "".join(self.input[index:ind]))
        elif state is 15:
            return (ind, "FIN", "".join(self.input[index:ind]))
        else:
            self.fallo()

    def getTokenList(self, remake=False):
        ind = 0
        lista_vacia = not self.TokenList or remake
        print("remake:", lista_vacia)
        while True or lista_vacia:
            token = self.getNextToken(ind)
            if token[1] is not "BLANCO":
                self.TokenList.append(token)
            ind = token[0]

            if token[1] is "FIN":
                break
        return self.TokenList.copy()

    def fallo(self):
        raise Exception("Error lexico");
class LexicoParser:
    def __init__(self,tokens):
        if type(tokens) != type(list()):
            raise Exception("Debe ingresar una lista de tokens.")
            return
        #Lista de primeras en
        self.D = {}
        self.tokens = tokens
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
        elif nodo.Dato[1] is "FIN":
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
        if self.index < len(self.tokens) and self.tokens[self.index][1] == "OR":
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
        if self.index < len(self.tokens) and (self.tokens[self.index][1] is "SIMBOLO" or \
                                                          self.tokens[self.index][1] is "CUALQUIER LETRA" or \
                                                          self.tokens[self.index][1] is "CUALQUIER NUMERO" or \
                                                          self.tokens[self.index][1] is "PO" or \
                                                          self.tokens[self.index][1] is "FIN"):

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
        if self.index < len(self.tokens) and self.tokens[self.index][1] is "+":
            hijo.padre = nodo
            nodo.isCaracter = False
            nodo.Dato = self.tokens[self.index]
            nodo.derecho = hijo
            self.index += 1
            return nodo
        elif self.index < len(self.tokens) and self.tokens[self.index][1] is "KLEENE":
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
        if self.index < len(self.tokens) and self.tokens[self.index][1] is "PO":
            self.index += 1
            hijo = self.or_exp(h + 1)

            # si la lista llego al final o el siguiente token es distinto a el parentecis que cierra
            if self.index >= len(self.tokens) or self.tokens[self.index][1] != "PC":
                raise Exception("No hay equilibrio de parentecis", self.tokens[self.index][0])
            else:
                self.index += 1
                return hijo

        elif self.index < len(self.tokens) and self.tokens[self.index][1] is "SIMBOLO":
            self.index += 1
            nodo = Nodo();
            nodo.isCaracter = True
            nodo.Dato = self.tokens[self.index - 1]
            return nodo
        elif self.index < len(self.tokens) and self.tokens[self.index][1] is "CUALQUIER NUMERO":
            self.index += 1
            nodo = Nodo();
            nodo.isCaracter = True
            nodo.Dato = self.tokens[self.index - 1]
            return nodo
        elif self.index < len(self.tokens) and self.tokens[self.index][1] is "CUALQUIER LETRA":
            self.index += 1
            nodo = Nodo();
            nodo.isCaracter = True
            nodo.Dato = self.tokens[self.index - 1]
            return nodo
        elif self.index < len(self.tokens) and self.tokens[self.index][1] is "FIN":
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
    nombre, exprecion = expresiones.split("=>")
    if not exprecion:
        sys.stderr.write("\nHay una regla sin nombre")
        continue
    lexer = LexicoLexer(exprecion)
    tokens = lexer.getTokenList()
    parser = LexicoParser(tokens)
    parser.inicio()
    # aux = (parser.siguientepos(parser.root.izquierdo.derecho.derecho))
    parser.construir_automata()
    print(parser.D)
