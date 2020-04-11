#include "main.h"

int main(int argc, const char *argv[])
{
    const char *filename = NULL;
    int fd = 0;
    char buf[BUF_LEN];
    int cmd_len;
    char report[8];
    int to_send = 8;
    int hold = 0;
    fd_set rfds;
    int retval, i;

    if (argc < 2)
    {
        fprintf(stderr, "Usage: %s devname\n",argv[0]);
        return 1;
    }

    filename = argv[1];

    if ((fd = open(filename, O_RDWR, 0666)) == -1)
    {
        perror(filename);
        return 3;
    }

    while (42)
    {

        FD_ZERO(&rfds);
        FD_SET(STDIN_FILENO, &rfds);
        FD_SET(fd, &rfds);

        retval = select(fd + 1, &rfds, NULL, NULL, NULL);
        if (retval == -1 && errno == EINTR)
            continue;
        if (retval < 0)
        {
            perror("select()");
            return 4;
        }

        if (FD_ISSET(fd, &rfds))
        {
            cmd_len = read(fd, buf, BUF_LEN - 1);
            printf("recv report:");
            for (i = 0; i < cmd_len; i++)
                printf(" %02x", buf[i]);
            printf("\n");
        }

        if (FD_ISSET(STDIN_FILENO, &rfds))
        {
            memset(report, 0x0, sizeof(report));
            cmd_len = read(STDIN_FILENO, buf, BUF_LEN - 1);

            if (cmd_len == 0)
                break;

            buf[cmd_len - 1] = '\0';
            hold = 0;

            memset(report, 0x0, sizeof(report));
            to_send = key_report(report, buf, &hold);

            if (to_send == -1)
                break;

            if (write(fd, report, to_send) != to_send)
            {
                perror(filename);
                return 5;
            }
            if (!hold)
            {
                memset(report, 0x0, sizeof(report));
                if (write(fd, report, to_send) != to_send)
                {
                    perror(filename);
                    return 6;
                }
            }
        }
    }

    close(fd);
    return 0;
}
