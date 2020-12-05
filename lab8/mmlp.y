%{
    #include <stdio.h>

    void yyerror(char *s);
    int yylex();
    extern FILE *yyin;
    int has_errors;
%}

%error-verbose
%union {char constat[100]; char id[8];}
%start program
%token ASSIGNMENT_OPERATOR ASTERISK BAND BNOT BOR BXOR COMMA CONSTANT ID INT LSB MINUS MODULO PLUS READ_HOST RSB SEMICOLON SHL SHR SLASH WRITE_HOST
%type <id> ID
%type <constat> CONSTANT

%%

program                        : statement
                               | program statement
                               |
                               ;

statement                      : declarationStatement
                               | assignmentStatement
                               | ioStatement
                               ;

declarationStatement           : declaration SEMICOLON
                               | declaration COMMA recursiveIds SEMICOLON
                               ;

recursiveIds                   : ID
                               | recursiveIds COMMA ID
                               ;

declaration                    : LSB INT RSB ID
                               ;

assignmentStatement            : lhs ASSIGNMENT_OPERATOR rhs SEMICOLON
                               ;

lhs                            : ID
                               | declaration
                               ;

rhs                            : operand
                               | rhs arithmeticOperator operand
                               ;

operand                        : ID
                               | CONSTANT
                               ;

ioStatement                    : read SEMICOLON
                               | write SEMICOLON
                               ;

read                           : lhs ASSIGNMENT_OPERATOR READ_HOST
                               ;

write                          : WRITE_HOST rhs
                               ;

arithmeticOperator             : PLUS
                               | MINUS
                               | ASTERISK
                               | SLASH
                               | MODULO
                               | BAND
                               | BNOT
                               | BOR
                               | BXOR
                               | SHL
                               | SHR
                               ;

%%

void yyerror(char *s)
{
    has_errors = 1;
	printf("%s\n", s);
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
