%{
    #include <stdio.h>

    void yyerror(char *s);
    int yylex();
    extern FILE *yyin;
%}

%union {char constat[100]; char string_constant[500]; char id[8];}
%start program
%token AND ARRAY ASSIGNMENT_OPERATOR ASTERISK BOOL COMMA CONSTANT EQ GE GT ID IF INT LCB LE LRB LSB LT MINUS MODULO NE OR PARAM PLUS RCB READ_HOST RRB RSB SEMICOLON SLASH SPACE STRING STRING_CONSTANT WHILE WRITE_HOST
%type <id> ID
%type <constat> CONSTANT
%type <string_constant> STRING_CONSTANT

%%

program                                               : statementList                                                     { ; }
                                                      | PARAM LRB functionDeclarationList RRB statementList               { ; }

statementList                                         : statement                                                         { ; }
                                                      | statement SEMICOLON statementList                                 { ; }

statement                                             : operationList                                                     { ; }
                                                      | ioStatement                                                       { ; }
                                                      | ifStatement                                                       { ; }
                                                      | whileStatement                                                    { ; }

operationList                                         : operation SEMICOLON                                               { ; }
                                                      | operation SEMICOLON operationList                                 { ; }

operation                                             : assignment                                                        { ; }
                                                      | simpleOperation                                                   { ; }

simpleOperation                                       : operand arithmeticOperator operand SEMICOLON                      { ; }
                                                      | operand arithmeticOperator simpleOperation SEMICOLON              { ; }

operand                                               : ID                                                                { ; }
                                                      | CONSTANT                                                             { ; }

assignment                                            : lhs ASSIGNMENT_OPERATOR rhs SEMICOLON
                                                      | readStatement

lhs                                                   : ID
                                                      | declaration

rhs                                                   : operand
                                                      | simpleOperation

declarationList                                       : declaration SEMICOLON
                                                      | declaration SEMICOLON declarationList

functionDeclarationList                               : declaration
                                                      | declaration COMMA functionDeclarationList

declaration                                           : LSB type RSB ID

type                                                  : INT
                                                      | STRING
                                                      | BOOL
                                                      | ARRAY

ioStatement                                           : readStatement
                                                      | writeStatement

readStatement                                         : lhs ASSIGNMENT_OPERATOR READ_HOST SEMICOLON

writeStatement                                        : WRITE_HOST SPACE operand SEMICOLON
                                                      | WRITE_HOST SPACE STRING_CONSTANT SEMICOLON

ifStatement                                           : IF LRB compoundCondition RRB LCB statementList RCB

whileStatement                                        : WHILE LRB compoundCondition RRB LCB statementList RCB

compoundCondition                                     : condition
                                                      | LRB compoundCondition RRB SPACE logicalOperator SPACE LRB compoundCondition RRB

condition                                             : operand equalityOperator operand

equalityOperator                                      : LT
                                                      | LE
                                                      | EQ
                                                      | NE
                                                      | GT
                                                      | GE

logicalOperator                                       : AND
                                                      | OR

arithmeticOperator                                    : PLUS
                                                      | MINUS
                                                      | ASTERISK
                                                      | SLASH
                                                      | MODULO

%%

void yyerror(char *s)
{
	printf("%s\n", s);
}

int main(int argc, char** argv) {
    if (argc > 0) {
        yyin = fopen(argv[0], "r");
    }
    else {
        yyin = stdin;
    }

    yyparse();
    return 0;
}
