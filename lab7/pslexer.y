%{
    #include <stdio.h>

    void yyerror(char *s);
    int yylex();
    extern FILE *yyin;
    int has_errors;
%}

%error-verbose
%union {char constat[100]; char string_constant[500]; char id[8];}
%start program
%token AND ARRAY ASSIGNMENT_OPERATOR ASTERISK BOOL COMMA CONSTANT EQ GE GT ID IF INT LCB LE LRB LSB LT MINUS MODULO NE OR PARAM PLUS RCB READ_HOST RRB RSB SEMICOLON SLASH STRING STRING_CONSTANT WHILE WRITE_HOST
%type <id> ID
%type <constat> CONSTANT
%type <string_constant> STRING_CONSTANT

%%

program                                               : statementList                                                                   { ; }
                                                      | PARAM LRB functionDeclarationList RRB statementList                             { ; }
                                                      |                                                                                 { ; }
                                                      ;

statementList                                         : statement                                                                       { ; }
                                                      | statementList statement                                                         { ; }
                                                      ;

statement                                             : operationList                                                                   { ; }
                                                      | declarationList                                                                 { ; }
                                                      | ioStatement                                                                     { ; }
                                                      | ifStatement                                                                     { ; }
                                                      | whileStatement                                                                  { ; }
                                                      ;

operationList                                         : operation                                                                       { ; }
                                                      | operationList operation                                                         { ; }
                                                      ;

operation                                             : assignment                                                                      { ; }
                                                      | simpleOperation                                                                 { ; }
                                                      ;

simpleOperation                                       : operand arithmeticOperator operand SEMICOLON                                    { ; }
                                                      | operand arithmeticOperator simpleOperation                                      { ; }
                                                      ;

operand                                               : ID                                                                              { ; }
                                                      | CONSTANT                                                                        { ; }
                                                      ;

assignment                                            : lhs ASSIGNMENT_OPERATOR rhs                                                     { ; }
                                                      | readStatement                                                                   { ; }
                                                      ;

lhs                                                   : ID                                                                              { ; }
                                                      | declaration                                                                     { ; }
                                                      ;

rhs                                                   : operand SEMICOLON                                                               { ; }
                                                      | simpleOperation                                                                 { ; }
                                                      ;

declarationList                                       : declaration SEMICOLON                                                           { ; }
                                                      | declarationList declaration SEMICOLON                                           { ; }
                                                      ;

functionDeclarationList                               : declaration                                                                     { ; }
                                                      | functionDeclarationList COMMA declaration                                       { ; }
                                                      ;

declaration                                           : LSB type RSB ID                                                                 { ; }
                                                      ;

type                                                  : INT                                                                             { ; }
                                                      | STRING                                                                          { ; }
                                                      | BOOL                                                                            { ; }
                                                      | ARRAY                                                                           { ; }
                                                      ;

ioStatement                                           : readStatement                                                                   { ; }
                                                      | writeStatement                                                                  { ; }
                                                      ;

readStatement                                         : lhs ASSIGNMENT_OPERATOR READ_HOST SEMICOLON                                     { ; }
                                                      ;

writeStatement                                        : WRITE_HOST operand SEMICOLON                                                    { ; }
                                                      | WRITE_HOST STRING_CONSTANT SEMICOLON                                            { ; }
                                                      ; 

ifStatement                                           : IF LRB compoundCondition RRB LCB statementList RCB                              { ; }
                                                      ;

whileStatement                                        : WHILE LRB compoundCondition RRB LCB statementList RCB                           { ; }
                                                      ;

compoundCondition                                     : condition
                                                      | LRB compoundCondition RRB logicalOperator LRB compoundCondition RRB { ; }
                                                      ;

condition                                             : operand equalityOperator operand                                                { ; }
                                                      ;

equalityOperator                                      : LT                                                                              { ; }
                                                      | LE                                                                              { ; }
                                                      | EQ                                                                              { ; }
                                                      | NE                                                                              { ; }
                                                      | GT                                                                              { ; }
                                                      | GE                                                                              { ; }
                                                      ;

logicalOperator                                       : AND                                                                             { ; }
                                                      | OR                                                                              { ; }
                                                      ;

arithmeticOperator                                    : PLUS                                                                            { ; }
                                                      | MINUS                                                                           { ; }
                                                      | ASTERISK                                                                        { ; }
                                                      | SLASH                                                                           { ; }
                                                      | MODULO                                                                          { ; }
                                                      ;

%%

void yyerror(char *s)
{
    has_errors = 1;
	fprintf(stderr, "%s\n", s);
}

int main(int argc, char** argv) {
    if (argc == 2) {
        yyin = fopen(argv[1], "r");
    }
    else {
        yyin = stdin;
    }

    has_errors = 0;
    yyparse();
    if (!has_errors) {
        printf("The input is valid!\n");
    }

    return 0;
}
