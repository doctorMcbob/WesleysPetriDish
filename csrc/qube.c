#include <stdio.h>
#include <stdint.h>
#include <math.h>
#include <stdlib.h>
#include "log.h"
#include "qube.h"
#include "rules.h"

static int* QBES[MAX_QBES] = {NULL};
static int CLEARED_QBES[MAX_QBES] = {-1};
int total_qubes = 0;
int cleared_qubes = 0;

// returns the index value of the qube
int newQbe(int d, int dimensions[]) {
  if (total_qubes >= MAX_QBES || cleared_qubes <= 0) {
    char buffer[100];
    snprintf(buffer, sizeof(buffer), "[Error Creating Qube]: Only allow %i Qubes", MAX_QBES);
    logText(buffer);
    
    return -1;
  }
  int* qbe = createQbe(d, dimensions);

  if (cleared_qubes > 0) {
    int idx = CLEARED_QBES[cleared_qubes--];
    QBES[idx] = qbe;
    return idx;
  }

  QBES[total_qubes] = qbe;
  return total_qubes++;
}

int* getQbe(int idx) {
  if (total_qubes >= MAX_QBES || total_qubes < 0) {
    char buffer[100];
    snprintf(buffer, sizeof(buffer), "[Error Getting Qube]: Attempted to get Qube outside of our narrow bounds. %i", idx);
    logText(buffer);
    
    return NULL;
  }
  return QBES[idx];
}

void clearQbe(int idx) {
  if (total_qubes >= MAX_QBES || total_qubes < 0) {
    char buffer[100];
    snprintf(buffer, sizeof(buffer), "[Error Clearing Qube]: Attempted to clear Qube outside of our narrow bounds. %i", idx);
    logText(buffer);

    return;
  }
  free(QBES[idx]);
  CLEARED_QBES[cleared_qubes++] = idx;
}
// Function to access an element in the flattened array based on multi-dimensional coordinates
int* qbeAt(int d, int dimensions[], int* flattened_array, int coordinates[]) {
    // Calculate the index in the flattened array corresponding to the coordinates
    int index = 0;
    int multiplier = 1;
    for (int i = d - 1; i >= 0; i--) {
        if (coordinates[i] < 0 || coordinates[i] >= dimensions[i]) {
            char buffer[100];
            snprintf(buffer, sizeof(buffer), "[Error Indexing Qube] Coordinates out of bounds: [%d] for dimension %d.\n", coordinates[i], i+1);
            logText(buffer);
            return NULL;
        }
        index += coordinates[i] * multiplier;
        multiplier *= dimensions[i];
    }

    // Return a pointer to the element at the calculated index
    return &flattened_array[index];
}

// Function to set an element in the flattened array based on multi-dimensional coordinates
void qbeSetAt(int d, int dimensions[], int* flattened_array, int coordinates[], int value) {
    // Calculate the index in the flattened array corresponding to the coordinates
    int index = 0;
    int multiplier = 1;
    for (int i = d - 1; i >= 0; i--) {
        if (coordinates[i] < 0 || coordinates[i] >= dimensions[i]) {
            char buffer[100];
            snprintf(buffer, sizeof(buffer), "[Error Indexing Qube] Coordinates out of bounds: [%d] for dimension %d.\n", coordinates[i], i+1);
            logText(buffer);
            return; // Exit the function if coordinates are out of bounds
        }
        index += coordinates[i] * multiplier;
        multiplier *= dimensions[i];
    }

    // Set the value at the calculated index
    flattened_array[index] = value;
}

int* createQbe(int d, int dimensions[]) {
    if (d <= 0) {
        logText("[Error Creating Qube] Dimension must be greater than 0.\n");
        return NULL;
    }

    int total_elements = 1;
    for (int i = 0; i < d; i++) {
        if (dimensions[i] <= 0) {
            logText("[Error Creating Qube] Dimension sizes must be positive integers.\n");
            return NULL;
        }
        total_elements *= dimensions[i];
    }

    int* flattened_array = (int*)malloc(total_elements * sizeof(int));
    
    if (flattened_array == NULL) {
        logText("[Error Creating Qube] Memory allocation failed.\n");
        return NULL;
    }

    for (int i = 0; i < total_elements; i++) {
        flattened_array[i] = 0;
    }

    return flattened_array;
}

void findNeighborsRecursively(int *point, int **result, int *temp, int dim, int N, int idx, int *counter) {
    if (idx == N) { // Base case: If current index equals dimension, save the temp array to result.
        for (int i = 0; i < N; i++) {
            result[*counter][i] = temp[i];
        }
        (*counter)++;
        return;
    }

    for (int i = -1; i <= 1; i++) {
        temp[idx] = point[idx] + i; // Set current dimension
        findNeighborsRecursively(point, result, temp, dim, N, idx + 1, counter); // Recurse for next dimension
    }
}

int **findNeighbors(int *point, int N, int *size) {
    int totalNeighbors = pow(3, N); // Calculate total neighbors including the point itself
    *size = totalNeighbors; // Update the size for the caller

    // Dynamically allocate memory for result
    int **result = (int **)malloc(totalNeighbors * sizeof(int *));
    for (int i = 0; i < totalNeighbors; i++) {
        result[i] = (int *)malloc(N * sizeof(int));
    }

    // Temporary array to hold a combination of neighbor coordinates
    int *temp = (int *)malloc(N * sizeof(int));
    int counter = 0; // Counter to keep track of filled positions in result

    // Recursively find neighbors
    findNeighborsRecursively(point, result, temp, totalNeighbors, N, 0, &counter);

    free(temp); // Cleanup

    return result;
}

uint8_t* nbrsOf(int* qbe, int* position, int* dimensions, int d) {
  uint8_t *seg = makeRuleSegment(d);

  int size;
  int **nbrs = findNeighbors(position, d, &size);

  for (int i = 0; i < size; i++) {
    int *pos = nbrs[i];

    int *v = qbeAt(d, dimensions, qbe, pos);
    // Calculate the index in the array (byte position)
    int idx = i / 8; // Each uint8_t holds 8 bits
    // Calculate the bit position within the byte
    int bit = i % 8;
    // Set the bit
    if (*v == 1)  seg[idx] |=   1U << bit;
    else          seg[idx] &= ~(1U << bit);
  }

  free(nbrs);
  return seg;
}

