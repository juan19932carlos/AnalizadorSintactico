grammar AuxRegularFactorizado;

or_exp: cat_exp or_exp_p;
or_exp_p: '|' cat_exp or_exp_p | ;

cat_exp: kleene cat_exp_p ;
cat_exp_p: ':' kleene cat_exp_p | ;

kleene: parent kleene_p ;
kleene_p: '+' | '*' | ;

parent: '(' or_exp ')' | CARACTER;

CARACTER: [A-Za-z]+;

BASURA: [\n\r\t' '] -> skip;
