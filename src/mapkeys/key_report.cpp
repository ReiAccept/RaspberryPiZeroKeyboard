#include "main.h"
#include "key_report.h"

int key_report(char report[8], char buf[BUF_LEN], int *hold)
{
    char *tok = strtok(buf, " ");
    int key = 0;
    int i = 0;

    for (; tok != NULL; tok = strtok(NULL, " "))
    {

        if (strncmp(tok, "--", 2) == 0)
            tok += 2;

        if (strcmp(tok, "quit") == 0)
            return -1;

        if (strcmp(tok, "hold") == 0)
        {
            *hold = 1;
            continue;
        }

        if (key < 6)
        {
            for (i = 0; kval[i].opt != NULL; i++)
                if (strcmp(tok, kval[i].opt) == 0)
                {
                    report[2 + key++] = kval[i].val;
                    break;
                }
            if (kval[i].opt != NULL)
                continue;
        }

        for (i = 0; kmod[i].opt != NULL; i++)
            if (strcmp(tok, kmod[i].opt) == 0)
            {
                report[0] = report[0] | kmod[i].val;
                break;
            }
        if (kmod[i].opt != NULL)
            continue;

        if (key < 6)
            fprintf(stderr, "unknown option: %s\n", tok);
    }
    return 8;
}