
grammar GramaticaAyuda;

init: CLASE ENDL (lineas ENDL)+;
lineas: NO_TERMINAL '=>' expresion          #exp_noterminal
      //| TERMINAL '=>' expresion_regular     #exp_terminal
;
expresion: expresion OP = ( OP_KLEENE | OP_UNICO | OP_POSITIVO )    #operacion
         | expresion '|' expresion                                  #or
         | '(' expresion ')'                                        #parentecis
         | (TERMINAL | NO_TERMINAL)                                 #terminal
;

CLASE: 'lexer' | 'parser';
OP_POSITIVO: '+';
OP_UNICO: '?';
OP_KLEENE: '*';
NO_TERMINAL: [A-Z]+;
TERMINAL: [a-z]+;
ENDL: [\n]+;
BASURA: [\t' '\r]+ -> skip;
