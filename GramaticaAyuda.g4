/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

grammar GramaticaAyuda;

init: (lineas)+;
lineas: TERM = (NO_TERMINAL | TERMINAL) '=>' expresion ;

expresion: palabra                              #terminal
         | expresion OP = ( '*' | '?' | '+' )   #operacion
         | expresion '|' expresion              #or
         | '(' expresion ')'                    #parentecis
         ;

palabra: TERMINAL
       ;

NO_TERMINAL: [A-Z]+;
TERMINAL: [a-z]+;
BASURA: [\t\n' '\r]+ -> skip;
