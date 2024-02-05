#include <stdint.h>
#include <stdlib.h>
#include <math.h>

#include "qube.h"

uint8_t* makeRuleSegment(int d) {
  // Calculate the total number of bits needed
  // Power of three. Number of neighbors is d^3
  // 1d is 3   left, self, right
  // 2d is 9   top left ...  bottom right
  // 3d is 27  above top left ... below bottom right
  
  int totalBits = pow(3, d);
  
  // Calculate the number of uint8_t elements needed to store totalBits
  int arraySize = ceil(totalBits / 8.0);
  
  // Allocate memory for the binary unit
  uint8_t *binaryUnit = (uint8_t*)calloc(arraySize, sizeof(uint8_t));
  return binaryUnit;
}

int* applyRule(int qbeIdx, unsigned int* rule, int d) {
  int* qbe  = getQbe(qbeIdx);

  
}

