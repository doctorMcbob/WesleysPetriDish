#ifndef RULES_DEF
#define RULES_DEF

#include <stdint.h>

uint8_t* makeRuleSegment(int d);
int* applyRule(int qbeIdx, unsigned int* rule, int d);

#endif
