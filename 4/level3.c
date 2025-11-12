#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void ___syscall_malloc()
{
    puts("Nope.");
    exit(1);
}

void ____syscall_malloc()
{
    puts("Good job.");
}

int main()
{
    char input[24];
    char buffer[9];
    char temp[4];
    int ret;
    long long i;
    int j;
    int cmp_result;

    printf("Please enter key: ");
    ret = scanf("%23s", input);

    // Check that scanf succeeded
    if (ret != 1)
        ___syscall_malloc();

    // Check second character is '2' (0x32)
    if (input[1] != '2')
        ___syscall_malloc();

    // Check first character is '4' (0x34)
    if (input[0] != '4')
        ___syscall_malloc();

    fflush(stdin);

    // Initialize buffer with '*' at first position
    memset(buffer, 0, 9);
    buffer[0] = '*';

    // Parse input in groups of 3 digits
    i = 2;  // start at position 2
    j = 1;  // buffer index starts at 1

    while (strlen(buffer) < 8 && i < strlen(input)) {
        // Extract 3 characters
        temp[0] = input[i];
        temp[1] = input[i + 1];
        temp[2] = input[i + 2];
        temp[3] = '\0';

        // Convert to integer and store as char
        buffer[j] = (char)atoi(temp);

        i += 3;
        j++;
    }

    buffer[j] = '\0';

    // Compare with "********" and handle different results
    cmp_result = strcmp(buffer, "********");

    switch (cmp_result) {
        case 0:
            ____syscall_malloc();
            break;
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
        case -1:
        case -2:
        case 115:  // 0x73
            ___syscall_malloc();
            break;
        default:
            ___syscall_malloc();
            break;
    }

    return 0;
}
