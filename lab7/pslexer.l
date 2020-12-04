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
"-and"                              { return AND; }
"array"                             { return ARRAY; }
"="                                 { return ASSIGNMENT_OPERATOR; }
"*"                                 { return ASTERISK; }
"bool"                              { return BOOL; }
","                                 { return COMMA; }
{CONST}                             { sscanf(yytext, "%s", yylval.constat); return CONSTANT; }
"-eq"                               { return EQ; }
"-ge"                               { return GE; }
"-gt"                               { return GT; }
{ID}                                { sscanf(yytext, "%s", yylval.id); return ID; }
"if"                                { return IF; }
"int"                               { return INT; }
"{"                                 { return LCB; }
"-le"                               { return LE; }
"("                                 { return LRB; }
"["                                 { return LSB; }
"-lt"                               { return LT; }
"-"                                 { return MINUS; }
"%"                                 { return MODULO; }
"-ne"                               { return NE; }
"-or"                               { return OR; }
"param"                             { return PARAM; }
"+"                                 { return PLUS; }
"}"                                 { return RCB; }
"Read-Host"                         { return READ_HOST; }
")"                                 { return RRB; }
"]"                                 { return RSB; }
";"                                 { return SEMICOLON; }
"/"                                 { return SLASH; }
" "                                 { return SPACE; }
"string"                            { return STRING; }
{CONST_STRING}                      { sscanf(yytext, "%s", yylval.string_constant); return STRING_CONSTANT; }
"while"                             { return WHILE; }
"Write-Host"                        { return WRITE_HOST; }
.                                   { ECHO; char buffer[50]; sprintf(buffer, "Syntax ERROR on line %d!\n", yylineno); yyerror(buffer); }

%%

int yywrap(void) { return 1; }
