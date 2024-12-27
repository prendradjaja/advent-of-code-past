#pragma once


// Like fopen(), but exits on error
FILE *fopen_strict(char *path, char *mode);

// Like getc(), but skips whitespace
int getc_nonwhitespace(FILE *input);
