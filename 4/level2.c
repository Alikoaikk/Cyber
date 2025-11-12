#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void no()
{
    puts("Nope.");
    exit(1);
}

void ok()
{
    puts("Good job.");
}

int main()
{
    char input[24];
    char buffer[9];
    char temp[4];
    int ret;
    int i, j;

    printf("Please enter key: ");
    ret = scanf("%23s", input);

    // Check that scanf succeeded
    if (ret != 1)
        no();

    // Check second character is '0'
    if (input[1] != '0')
        no();

    // Check first character is '0'
    if (input[0] != '0')
        no();

    fflush(stdin);

    // Initialize buffer with 'd' at first position
    memset(buffer, 0, 9);
    buffer[0] = 'd';

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

    // Compare with "delabere"
    if (strcmp(buffer, "delabere") == 0) {
        ok();
    } else {
        no();
    }

    return 0;
}
