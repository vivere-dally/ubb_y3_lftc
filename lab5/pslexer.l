%{

#include "dict.h"

void print(char* atom, char* token) {
	struct nlist *np = lookup(token);
	printf("%10s : %2s : %s\n", atom, np->defn, token);
}

void print_special(char* atom, char* token, char* special) {
	struct nlist *np = lookup(token);
	printf("%10s : %2s : %s\n", atom, np->defn, special);
}

%}

%option noyywrap
%option yylineno

DIGIT									[0-9]
CONST									(\+|-)?[0-9]*(kb|mb|gb|tb|pb)?
LETTER									[a-zA-Z]
CONST_STRING							\"[^\"]*\"
ID										$[a-zA-Z]([a-zA-Z]|[0-9]){0,7}

%%
param									{ print("PARAM", yytext); }
int|string|bool|array					{ print("TYPE", yytext); }
if|while								{ print("STATEMENT", yytext); }
Write-Host|Read-Host					{ print("IO", yytext); }
-lt|-le|-eq|-ne|-gt|-ge					{ print("EQ OPERATOR", yytext); }
-and|-or								{ print("LO OPERATOR", yytext); }
"+"|"-"|"*"|"/"|"%"						{ print("AR OPERATOR", yytext); }
"="										{ print("AS OPERATOR", yytext); }
"("|")"|"["|"]"|"{"|"}"|","|";"			{ print("SEPARATOR", yytext); }
{ID}									{ print_special("ID", "ID", yytext); }
{CONST}									{ print_special("CONST", "CONST", yytext); }
{CONST_STRING}							{ print_special("STR CONST", "STRING_CONST", yytext); }
" "|"\n"|"\t"							{ printf(""); }
.										{ printf("ERROR: unrecognized token on line %d.\n", yylineno); }

%%
int main( argc, argv ) 
int argc; 
char **argv; 
	{ 	++argv, --argc; 
		if ( argc > 0 ) 
			yyin = fopen( argv[0], "r" ); 
		else 
			yyin = stdin; 

		install("STRING_CONST", "1");
		install("ID", "2");
		install("CONST", "3");
		install(";", "4");
		install("(", "5");
		install(")", "6");
		install("[", "7");
		install("]", "8");
		install("{", "9");
		install("}", "10");
		install(",", "11");
		install("int", "12");
		install("string", "13");
		install("bool", "14");
		install("array", "15");
		install("+", "16");
		install("-", "17");
		install("*", "18");
		install("/", "19");
		install("%", "20");
		install("=", "21");
		install("-lt", "22");
		install("-le", "23");
		install("-eq", "24");
		install("-ne", "25");
		install("-gt", "26");
		install("-ge", "27");
		install("-and", "28");
		install("-or", "29");
		install("if", "30");
		install("while", "31");
		install("Read-Host", "32");
		install("Write-Host", "33");
		install(" ", "34");
		install("param", "35");
		yylex();
		return 0;
	} 
