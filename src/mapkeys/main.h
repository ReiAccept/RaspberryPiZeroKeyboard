#include <string.h>
#include <stdio.h>
#include <ctype.h>
#include <fcntl.h>
#include <errno.h>
#include <stdlib.h>
#include <unistd.h>

#define BUF_LEN 512

int key_report(char report[8], char buf[BUF_LEN], int *hold);