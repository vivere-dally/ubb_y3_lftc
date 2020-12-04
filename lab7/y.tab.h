
/* A Bison parser, made by GNU Bison 2.4.1.  */

/* Skeleton interface for Bison's Yacc-like parsers in C
   
      Copyright (C) 1984, 1989, 1990, 2000, 2001, 2002, 2003, 2004, 2005, 2006
   Free Software Foundation, Inc.
   
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
   
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.
   
   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */


/* Tokens.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
   /* Put the tokens into the symbol table, so that GDB and other debuggers
      know about them.  */
   enum yytokentype {
     AND = 258,
     ARRAY = 259,
     ASSIGNMENT_OPERATOR = 260,
     ASTERISK = 261,
     BOOL = 262,
     COMMA = 263,
     CONSTANT = 264,
     EQ = 265,
     GE = 266,
     GT = 267,
     ID = 268,
     IF = 269,
     INT = 270,
     LCB = 271,
     LE = 272,
     LRB = 273,
     LSB = 274,
     LT = 275,
     MINUS = 276,
     MODULO = 277,
     NE = 278,
     OR = 279,
     PARAM = 280,
     PLUS = 281,
     RCB = 282,
     READ_HOST = 283,
     RRB = 284,
     RSB = 285,
     SEMICOLON = 286,
     SLASH = 287,
     SPACE = 288,
     STRING = 289,
     STRING_CONSTANT = 290,
     WHILE = 291,
     WRITE_HOST = 292
   };
#endif
/* Tokens.  */
#define AND 258
#define ARRAY 259
#define ASSIGNMENT_OPERATOR 260
#define ASTERISK 261
#define BOOL 262
#define COMMA 263
#define CONSTANT 264
#define EQ 265
#define GE 266
#define GT 267
#define ID 268
#define IF 269
#define INT 270
#define LCB 271
#define LE 272
#define LRB 273
#define LSB 274
#define LT 275
#define MINUS 276
#define MODULO 277
#define NE 278
#define OR 279
#define PARAM 280
#define PLUS 281
#define RCB 282
#define READ_HOST 283
#define RRB 284
#define RSB 285
#define SEMICOLON 286
#define SLASH 287
#define SPACE 288
#define STRING 289
#define STRING_CONSTANT 290
#define WHILE 291
#define WRITE_HOST 292




#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef union YYSTYPE
{

/* Line 1676 of yacc.c  */
#line 9 ".\\pslexer.y"
char constat[100]; char string_constant[500]; char id[8];


/* Line 1676 of yacc.c  */
#line 130 "y.tab.h"
} YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
#endif

extern YYSTYPE yylval;


