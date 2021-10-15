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
long global_b;

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
        int condition;
        klee_make_symbolic(&condition, sizeof(int), "condition");
        struct Type2* var_struct = (struct Type2*) malloc(sizeof(struct Type2));
        var_struct->status = 0;
        printf ("..........exploiting path is taken. \n");
        *gvar.obj2->ptr = 0x1234; // But we modify it (e.g., to badFunc)

        if (condition){
            global_b = var_struct->status + 100;
        }

        global_a = 100;

        if (condition + 100){
            handler = global_a - 100;
        }else {
            handler = global_b - 100;
        }

        handler = handler + 1000;

    }
    handler(gvar.obj2->ptr);
    return res;
}
