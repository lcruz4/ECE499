default: all

CFLAGS := -I./include -g --std=gnu99
CC := gcc

BINARIES := controller-c
all : $(BINARIES)

LIBS := -lach 

controller-c: src/controller-c.o
	gcc -o $@ $< $(LIBS)

%.o: %.c
	$(CC) $(CFLAGS) -o $@ -c $<

clean:
	rm -f $(BINARIES) src/*.o
