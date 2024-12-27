#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>


FILE *fopen_strict(char *path, char *mode) {
  FILE *file = fopen(path, mode);
  if (!file) {
    perror(NULL);
    exit(EXIT_FAILURE);
  }
  return file;
}

int getc_nonwhitespace(FILE *input) {
  int result = ' ';
  while (isspace(result = getc(input)));
  return result;
}
