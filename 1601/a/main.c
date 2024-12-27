#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <assert.h>

#include "vector.h"
#include "my_io.h"


const PositionDelta directions[] = { {-1, 0}, {0, 1}, {1, 0}, {0, -1} };
const int count_directions = sizeof(directions) / sizeof(directions[0]);

typedef struct {
  bool is_right_turn;
  int distance;
} Movement;


// Returns true if successful
bool get_next_movement(FILE *input, Movement *result) {
  char direction = getc_nonwhitespace(input);
  if (direction == EOF) {
    return false;
  }
  assert(direction == 'R' || direction == 'L');
  bool is_right_turn = direction == 'R';

  int distance;
  if (fscanf(input, "%d", &distance) != 1) {
    return false;
  }

  char comma = getc_nonwhitespace(input);
  assert(comma == ',' || comma == EOF);

  *result = (Movement) { is_right_turn, distance };
  return true;
}

int rotate(int direction_index, bool right_turn) {
  assert(0 <= direction_index && direction_index < 4);
  if (right_turn) {
    return (direction_index + 1) % 4;
  } else {
    return (direction_index + 3) % 4;
  }
}

void assert_valid_args(int argc, char **argv) {
  if (argc < 2) {
    fprintf(stderr, "Usage:\n");
    fprintf(stderr, " ./a ex\n");
    fprintf(stderr, " ./a in\n");
    exit(EXIT_FAILURE);
  }
}

int main(int argc, char **argv) {
  assert_valid_args(argc, argv);
  FILE *input = fopen_strict(argv[1], "r");

  Movement movement;
  Position pos = { 0, 0 };
  int direction = 0;
  PositionDelta direction_vector;
  while (get_next_movement(input, &movement)) {
    direction = rotate(direction, movement.is_right_turn);
    direction_vector = directions[direction];
    pos = add_weighted(pos, movement.distance, direction_vector);
  }

  int answer = abs(pos.r) + abs(pos.c);
  printf("%d\n", answer);
}
