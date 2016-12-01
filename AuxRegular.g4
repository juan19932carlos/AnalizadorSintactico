grammar AuxRegular;

or_exp: cat_exp '|' cat_exp | cat_exp ;

cat_exp: kleene cat_exp | kleene | ;

kleene: parent '+' | parent'*' | parent;

parent: '(' or_exp ')' | CARACTER;

CARACTER: [A-Za-z0-9];

BASURA: [\n\r\t' '] -> skip;
