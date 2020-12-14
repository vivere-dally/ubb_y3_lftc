#ifndef _INT_VAL_DICT_H_
#define _INT_VAL_DICT_H_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct kvp
{                     /* table entry: */
    struct kvp *next; /* next entry in chain */
    char *key;        /* defined key */
    int value;        /* defined val */
};

#define HASHSIZE 101
static struct kvp *hashtab[HASHSIZE]; /* pointer table */

/* hash: form hash value for string s */
unsigned hash(char *s)
{
    unsigned hashval;
    for (hashval = 0; *s != '\0'; s++)
        hashval = *s + 31 * hashval;
    return hashval % HASHSIZE;
}

/* get_by_key: look for s in hashtab */
struct kvp *get_by_key(char *s)
{
    struct kvp *np;
    for (np = hashtab[hash(s)]; np != NULL; np = np->next)
        if (strcmp(s, np->key) == 0)
            return np; /* found */
    return NULL;       /* not found */
}

char *my_strdup(char *s) /* make a duplicate of s */
{
    char *p;
    p = (char *)malloc(strlen(s) + 1); /* +1 for ’\0’ */
    if (p != NULL)
        strcpy(p, s);
    return p;
}

/* add: put (key, value) in hashtab */
struct kvp *add(char *key, int value)
{
    struct kvp *np;
    unsigned hashval;
    if ((np = get_by_key(key)) == NULL)
    { /* not found */
        np = (struct kvp *)malloc(sizeof(*np));
        if (np == NULL || (np->key = my_strdup(key)) == NULL)
            return NULL;
        hashval = hash(key);
        np->next = hashtab[hashval];
        hashtab[hashval] = np;
    }
    else /* already there */
    {
        np->value = value;
    }
    return np;
}

#endif
