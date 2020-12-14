%{
    #include <stdio.h>
    #include "int_val_dict.h"

    void yyerror(char *s);
    int yylex();
    extern FILE *yyin;
    int has_errors;
%}

%error-verbose
%union {int constant; char id[8]; }
%start program
%token ASSIGNMENT_OPERATOR ASTERISK BAND BNOT BOR BXOR COMMA INT LSB MINUS MODULO PLUS READ_HOST RSB SEMICOLON SHL SHR SLASH WRITE_HOST
%token <id> ID
%token <constant> CONSTANT

%type <id> recursiveIds declaration

%%

program                        : statement                                                      {;}
                               | program statement                                              {;}
                               |
                               ;

statement                      : declarationStatement                                           {;}
                               | assignmentStatement                                            {;}
                               | ioStatement                                                    {;}
                               ;

declarationStatement           : declaration SEMICOLON                                          {;}
                               | declaration COMMA recursiveIds SEMICOLON                       {;}
                               ;

recursiveIds                   : ID                                                             { $$ = $1; }
                               | recursiveIds COMMA ID                                          { ; }
                               ;

declaration                    : LSB INT RSB ID                                                 { $$ = $4; }
                               ;

assignmentStatement            : lhs ASSIGNMENT_OPERATOR rhs SEMICOLON                          {
                                                                                                    struct *kvp = add($1, $3);
                                                                                                    if (kvp == NULL) {
                                                                                                        printf("ERROR> Couldn't save to dictionary!\n");
                                                                                                    }
                                                                                                }
                               ;

lhs                            : ID                                                             { $$ = $1; }
                               | declaration                                                    { $$ = $1; }
                               ;

rhs                            : operand                                                        { $$ = $1; }
                               | rhs PLUS operand                                               { $$ = $1 + $3; }
                               | rhs MINUS operand                                              { $$ = $1 - $3; }
                               | rhs ASTERISK operand                                           { $$ = $1 * $3; }
                               | rhs SLASH operand                                              { $$ = $1 / $3; }
                               | rhs MODULO operand                                             { $$ = $1 % $3; }
                               | rhs BAND operand                                               { $$ = $1 & $3; }
                               | BNOT rhs                                                       { $$ = ~$1; }
                               | rhs BOR operand                                                { $$ = $1 | $3; }
                               | rhs BXOR operand                                               { $$ = $1 ^ $3; }
                               | rhs SHL operand                                                { $$ = $1 << $3; }
                               | rhs SHR operand                                                { $$ = $1 >> $3; }
                               ;

operand                        : ID                                                             {
                                                                                                    struct *kvp = get_by_key($1);
                                                                                                    if (kvp == NULL) {
                                                                                                        printf("ERROR> Key not found %s!\n", $1);
                                                                                                        $$ = NULL;
                                                                                                    } else {
                                                                                                        $$ = kvp->value;
                                                                                                    }
                                                                                                }
                               | CONSTANT                                                       { $$ = $1; }
                               ;

ioStatement                    : read SEMICOLON                                                 {;}
                               | write SEMICOLON                                                {;}
                               ;

read                           : lhs ASSIGNMENT_OPERATOR READ_HOST                              { 
                                                                                                    int v;
                                                                                                    printf("Read-Host>%s = ", $1);
                                                                                                    scanf("%d", &v);
                                                                                                    struct *kvp = add($1, v);
                                                                                                    if (kvp == NULL) {
                                                                                                        printf("ERROR> Couldn't save to dictionary!\n");
                                                                                                    }
                                                                                                }
                               ;

write                          : WRITE_HOST operand                                             { 
                                                                                                    if ($2 == NULL) { 
                                                                                                        printf("ERROR> Trying to print NULL!\n"); 
                                                                                                    } else { 
                                                                                                        printf("Write-Host> %d\n", $2); 
                                                                                                    } 
                                                                                                }
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
