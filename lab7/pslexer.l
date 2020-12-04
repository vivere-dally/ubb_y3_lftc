%{
    #include <stdio.h>
    #include "y.tab.h"

    void yyerror (char *s);
%}

%option yylineno

DIGIT									[0-9]
CONST									(\+|-)?[0-9]*(kb|mb|gb|tb|pb)?
LETTER									[a-zA-Z]
CONST_STRING							\"[^\"]*\"
ID										$[a-zA-Z]([a-zA-Z]|[0-9]){0,7}

%%
"param"                             { return PARAM; }
"int"                               { return INT; }
"string"                            { return STRING; }
"bool"                              { return BOOL; }
"array"                             { return ARRAY; }
"if"                                { return IF; }
"while"                             { return WHILE; }
"Read-Host"                         { return READ_HOST; }
"Write-Host "                       { return WRITE_HOST; }
" -and "                            { return AND; }
" -or "                             { return OR; }
" -lt "                             { return LT; }
" -le "                             { return LE; }
" -eq "                             { return EQ; }
" -ne "                             { return NE; }
" -ge "                             { return GE; }
" -gt "                             { return GT; }
"="                                 { return ASSIGNMENT_OPERATOR; }
"*"                                 { return ASTERISK; }
","                                 { return COMMA; }
";"                                 { return SEMICOLON; }
"{"                                 { return LCB; }
"("                                 { return LRB; }
"["                                 { return LSB; }
"-"                                 { return MINUS; }
"%"                                 { return MODULO; }
"+"                                 { return PLUS; }
"}"                                 { return RCB; }
")"                                 { return RRB; }
"]"                                 { return RSB; }
"/"                                 { return SLASH; }
{ID}                                { sscanf(yytext, "%s", yylval.id); return ID; }
{CONST}                             { sscanf(yytext, "%s", yylval.constat); return CONSTANT; }
{CONST_STRING}                      { sscanf(yytext, "%s", yylval.string_constant); return STRING_CONSTANT; }
[ \t\n]                             { ; }
.                                   { printf("ERROR: unrecognized token on line %d.\n", yylineno); }

%%

int yywrap(void) { return 1; }
