Tema 1: Analizor lexical
Tema de laborator in lucru: 3 saptamani
Enunt general:
Scrierea unui ANALIZOR LEXICAL pentru un minilimbaj de programare (MLP),
ales ca subset al unui limbaj existent.
1. Specificarea minilimbajului de programare (MLP).
Limbajul trebuie sa contina cel putin anumite instructiuni si tipuri de
date:
- 2 tipuri de date simple si un tip de date definit de utilizator
- instructiuni:
- o instructiune de atribuire
- o instructiune de intrare/iesire
- o instructiune de selectie (conditionala)
- o instructiune de ciclare
Pe langa acestea, vor exista unele restrictii suplimentare referitoare la
identificatori si constante (vezi sectiunea 3.1).
Se cere ca specificarea sa fie suficient de generala astfel incat sa descrie
constructiile limbajului folosite pentru scrierea programelor de la pct.1
2. se cer textele sursa a 3 programe
(versiune electronica)
care respecta specificatiile MLP date si care rezolva trei dintre
urmatoarele probleme:
- calculeaza perimetrul si aria cercului de o raza data data
- calculeaza minimul si maximul a trei numere
- verifica daca un numar este prim
- determina cmmdc a 2 nr naturale
- calculeaza suma a n numere citite de la tastatura
3. Se cer textele sursa a doua programe care contin erori conform MLP-ului
definit:
- Unul dintre programe contine doua erori care sunt in acelasi timp
erori in limbajul original (pentru care MLP defineste un subset)
- Al doilea program contine doua erori conform MLP, dar care nu sunt
erori in limbajul original
4. Implementarea analizorului lexical
Analizorul lexical accepta la intrare un fisier text reprezentand un
program sursa si intocmeste ca date de iesire tabelele:
FIP - forma interna a programului sursa si
TS - tabelui de simboluri.
In plus, programul va trebui sa semnaleze erorile lexicale si locul in care
apar.
Analizoarele lexicale se vor diferentia dupa urmatoarele criterii:
 1. identificatori
 a. de lungime cel mult opt caractere
 b. de lungime oarecare nedepasind 250 caractere
 2. tabela de simboluri:
 a. unica pentru identificatori si constante
 b. separat pentru identificatori si constante
 3. organizarea tabelelor de simboluri:
 a. tabel ordonat lexicografic
 b. tabel arbore binar de cautare (ordine lexicografica)
 c. tabel de dispersie (hash)
Se cere, de asemenea, implementarea structurilor de date cerute
pentru tabela de simboluri. Se pot folosi implementarile facute la
materia structuri de date.
