%{
    #include <stdio.h>
    #include "y.tab.h"

    void yyerror (char *s);
%}

%option yylineno

CONST									(\+|-)?[0-9]*(kb|mb|gb|tb|pb)?
ID										$[a-zA-Z]([a-zA-Z]|[0-9]){0,7}

%%
"int"                               { return INT; }
"Read-Host"                         { return READ_HOST; }
"Write-Host "                       { return WRITE_HOST; }
"="                                 { return ASSIGNMENT_OPERATOR; }
"+"                                 { return PLUS; }
"-"                                 { return MINUS; }
"*"                                 { return ASTERISK; }
"/"                                 { return SLASH; }
"%"                                 { return MODULO; }
"-band"                             { return BAND; }
"-bnot"                             { return BNOT; }
"-bor"                              { return BOR; }
"-bxor"                             { return BXOR; }
"-shl"                              { return SHL; }
"-shr"                              { return SHR; }
"["                                 { return LSB; }
"]"                                 { return RSB; }
","                                 { return COMMA; }
";"                                 { return SEMICOLON; }
{ID}                                { sscanf(yytext, "%s", yylval.id); return ID; }
{CONST}                             { yylval.constant = atoi(yytext); return CONSTANT; }
[ \t\n]                             { ; }
.                                   { printf("ERROR: unrecognized token on line %d.\n", yylineno); }
%%

int yywrap(void) { return 1; }
