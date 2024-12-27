#include <stdio.h>
#include "vector.h"

Vector add(Vector v1, Vector v2) {
  return (Vector){
    v1.r + v2.r,
    v1.c + v2.c,
  };
}

Vector add_weighted(Vector v1, int v2_weight, Vector v2) {
  return (Vector){
    v1.r + v2_weight * v2.r,
    v1.c + v2_weight * v2.c,
  };
}

void print_vector(Vector v, char* prefix) {
  if (prefix == NULL) {
    prefix = "";
  }
  printf("%s%d, %d\n", prefix, v.r, v.c);
}
