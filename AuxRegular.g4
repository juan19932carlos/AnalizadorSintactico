grammar AuxRegular;

or_exp: cat_exp '|' cat_exp | cat_exp ;

cat_exp: kleene ':' cat_exp | kleene | ;

kleene: parent '+' | parent'*' | parent;

parent: '(' or_exp ')' | CARACTER;

CARACTER: [A-Za-z]+;

BASURA: [\n\r\t' '] -> skip;
