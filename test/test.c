#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "klee/klee.h"
struct Type1 {char data [8];};
struct Type2 {
    int status;
    int* ptr;
};
int (*handler1)(int);
int (*handler2)(int);
int (*handler)(const int*);
int goodFunc(const int* var){printf("/////This is a Good function\n");return 0;}
int badFunc(const int* var){printf("/////This is a Evil function\n");return 0;}
long global_a;
struct {struct Type1* obj1; struct Type2* obj2;} gvar = {};
int main(int argc, char* argv[]){
    gvar.obj1 = (struct Type1*)malloc(sizeof(struct Type1));
    gvar.obj2 = (struct Type2*)malloc(sizeof(struct Type2));
    int res;
    char temp[16];
    klee_make_symbolic(temp, 16, "temp");

    char* buf = temp;
    memcpy (&gvar.obj2->status, buf, 16);
    handler = goodFunc; //Here we should call a Good function
    if(gvar.obj2->status)
    {
        printf ("crashing path is taken. \n");
        res = *gvar.obj2->ptr;
    }
    else
    {
        long *b = malloc(sizeof(long));
        printf ("..........exploiting path is taken. \n");
        *gvar.obj2->ptr = 0x1234; // But we modify it (e.g., to badFunc)
        if (1){
            b = global_a - 100;
        }
        handler = *b - 100 + 1000;

    }
    handler = global_a;
    long array[10000];
    for (int i = 0; i < 10000; i++){
        handler = array[i];
    }
    //handler = 100;
    handler(gvar.obj2->ptr);
    return res;
}
