#
# File:  Makefile for application
#
CC=gcc
CFLAGS=-I. -I./lib 

all: libovs ovs-controller ovs-ofctl 


ovs-controller:
	@echo compiling ovs-controller
	@$(CC) ovs-controller.c  -o ovs-controller  $(CFLAGS) -L./lib -Bstatic -lovs -Bdynamic -lrt -ggdb3




ovs-ofctl:
	@echo compiling ovs-ofctl
	@$(CC) ovs-ofctl.c -o ovs-ofctl $(CFLAGS) -L./lib -Bstatic -lovs -Bdynamic -lrt -ggdb3



include lib/Makefile

clean:
	rm -f lib/*.o
	rm -f libovs.a
	rm -f lib/libovs.a
	rm -f lib/coverage-counters.c
	rm -f *.o
	rm -f ovs-controller
	rm -f ovs-ofctl
