%{

#include "dict.h"
#include "list.h"

struct list *id_list, *const_list, *str_const_list;

void print(char* atom, char* token) {
	struct nlist *np = lookup(token);
	printf("%10s : %2s : %s\n", atom, np->defn, token);
}

void print_special(char* atom, char* token, char* special, struct list* list) {
	struct nlist *np = lookup(token);
	printf("%10s : %2s : %s\n", atom, np->defn, special);
	install_list(list, special);
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
cattimp|executa|sfcattimp				{ print("EXT STMT", yytext); }
param									{ print("PARAM", yytext); }
int|string|bool|array					{ print("TYPE", yytext); }
if|while								{ print("STATEMENT", yytext); }
Write-Host|Read-Host					{ print("IO", yytext); }
-lt|-le|-eq|-ne|-gt|-ge					{ print("EQ OPERATOR", yytext); }
-and|-or								{ print("LO OPERATOR", yytext); }
"+"|"-"|"*"|"/"|"%"						{ print("AR OPERATOR", yytext); }
"="										{ print("AS OPERATOR", yytext); }
"("|")"|"["|"]"|"{"|"}"|","|";"			{ print("SEPARATOR", yytext); }
{ID}									{ print_special("ID", "ID", yytext, id_list); }
{CONST}									{ print_special("CONST", "CONST", yytext, const_list); }
{CONST_STRING}							{ print_special("STR CONST", "STRING_CONST", yytext, str_const_list); }
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
		install("cattimp", "36");
		install("executa", "37");
		install("sfcattimp", "38");

		id_list = new_list();
		const_list = new_list();
		str_const_list = new_list();

		yylex();

		print_list(id_list, "ID");
		print_list(const_list, "CONST");
		print_list(str_const_list, "STR CONST");

		return 0;
	} 
