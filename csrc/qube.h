#ifndef QBE_DEF
#define QBE_DEF

#define MAX_QBES 16

/*
  To articulate this for a moment:
      we are going to be treating these things as indexes as long as we have them.
      so newQbe returns the index to the qbe
*/
int newQbe(int d, int dimensions[]);
int* getQbe(int idx);
void clearQbe(int idx);

/*
  These will be used to apply the rules, and draw
*/
int* qbeAt(int d, int dimensions[], int* flattened_array, int coordinates[]);
void qbeSetAt(int d, int dimensions[], int* flattened_array, int coordinates[], int value);

/* Allocates a new Qube, leveraged by newQbe */
int* createQbe(int d, int dimensions[]);
#endif
