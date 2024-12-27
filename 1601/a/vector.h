#pragma once


typedef struct Vector {
  int r;
  int c;
} Vector;
typedef Vector Position;
typedef Vector PositionDelta;


Vector add(Vector v1, Vector v2);

Vector add_weighted(Vector v1, int v2_weight, Vector v2);

void print_vector(Vector v, char* prefix);
