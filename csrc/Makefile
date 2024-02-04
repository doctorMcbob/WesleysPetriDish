CC := gcc
CFLAGS := -I/usr/include/SDL2 -D_REENTRANT
LDFLAGS := -lSDL2 -lSDL2_ttf -lSDL2_image
# CFLAGS += -H

# Collect all .c files in the directory
SRC := $(wildcard *.c)
# Substitute .c files with .o files
OBJ := $(SRC:.c=.o)

all: wxpd

wxpd: $(OBJ)
	$(CC) $(OBJ) -o wxpd $(LDFLAGS)

# Generic rule for building objects
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ)
