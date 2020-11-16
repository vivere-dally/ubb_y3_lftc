#ifndef _MY_LIST_H_
#define _MY_LIST_H_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "dict.h"

struct list_node /* list entry */
{
    struct list_node *next; /* next entry */
    char *token;            /* token */
    int tokenKey;           /* token's id */
};

struct list /* list */
{
    struct list_node *root; /* root element */
    int currentTokenKey;    /* token id */
};

struct list *new_list()
{
    struct list *list = (struct list *)malloc(sizeof(struct list));
    list->root = NULL;
    list->currentTokenKey = 1;
    return list;
}

struct list_node *lookup_list(struct list *list, char *s)
{
    struct list_node *current;
    for (current = list->root; current != NULL; current = current->next)
    {
        if (strcmp(s, current->token) == 0)
        {
            return current; /* found */
        }
    }

    return NULL; /* not found */
}

struct list_node *install_list(struct list *list, char *s)
{
    struct list_node *current = lookup_list(list, s); /* don't add duplicates */
    if (current == NULL)
    {
        current = (struct list_node *)malloc(sizeof(struct list_node));
        if (current == NULL || (current->token = my_strdup(s)) == NULL)
        {
            return NULL;
        }

        /* push_front */
        current->tokenKey = list->currentTokenKey++;
        current->next = list->root;
        list->root = current;
    }

    return current;
}

void print_list(struct list *list, char *s)
{
    printf("\n === %s === \n", s);
    for (struct list_node *current = list->root; current != NULL; current = current->next)
    {
        printf("%3d : %s\n", current->tokenKey, current->token);
    }
}

#endif
