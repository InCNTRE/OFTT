#
# File:  Makefile (for library)
#
LIB=lib/libovs.a
LIBDEST=./

# source files.
LIBSRC =  \
        lib/backtrace.c \
        lib/bitmap.c \
        lib/command-line.c \
        lib/coverage.c \
	lib/coverage-counters.c \
	lib/csum.c \
        lib/daemon.c \
	lib/dpif.c \
	lib/dpif-linux.c \
	lib/dpif-netdev.c \
	lib/dirs.c \
        lib/dynamic-string.c \
        lib/entropy.c \
        lib/fatal-signal.c \
        lib/flow.c \
        lib/hash.c \
        lib/hmap.c \
        lib/leak-checker.c \
        lib/learning-switch.c \
        lib/list.c \
        lib/lockfile.c \
        lib/mac-learning.c \
        lib/netdev.c \
	lib/netdev-linux.c \
	lib/netdev-patch.c \
	lib/netdev-tunnel.c \
	lib/netdev-vport.c \
	lib/netlink.c \
	lib/odp-util.c \
        lib/ofpbuf.c \
        lib/ofp-print.c \
        lib/ofp-parse.c \
        lib/ofp-util.c \
        lib/packets.c \
        lib/pcap.c \
        lib/poll-loop.c \
	lib/port-array.c \
        lib/process.c \
	lib/rtnetlink.c \
        lib/queue.c \
        lib/random.c \
        lib/rconn.c \
        lib/shash.c \
        lib/socket-util.c \
        lib/svec.c \
	lib/stream-fd.c \
	lib/stream-tcp.c \
	lib/stream-unix.c \
	lib/stream.c \
        lib/tag.c \
        lib/timeval.c \
        lib/unixctl.c \
        lib/util.c \
        lib/vconn.c \
	lib/vconn-stream.c \
        lib/vlog.c \

LIBOBJ=$(LIBSRC:.c=.o)

libovs: lib/coverage-counters.c $(LIB) 
#	@echo lib Makefile - installing $(LIB)
#	@install -m 444 $(LIB) $(LIBDEST)

$(LIB): $(LIBOBJ)
	@echo lib Makefile - archiving $(LIB)
	@$(AR) r $(LIB) $(LIBOBJ)


PERL = /usr/bin/perl
COVERAGE_FILES = \
	lib/dpif.c \
	lib/flow.c \
	lib/hmap.c \
	lib/lockfile.c \
	lib/mac-learning.c \
	lib/netdev.c \
	lib/poll-loop.c \
        lib/process.c \
        lib/rconn.c \
	lib/rtnetlink.c \
	lib/netdev-linux.c \
	lib/netlink.c \
	lib/stream.c \
        lib/timeval.c \
        lib/unixctl.c \
        lib/util.c \
        lib/vconn.c 

lib/coverage-counters.c: ${COVERAGE_FILES} lib/coverage-scan.pl
	( $(PERL) lib/coverage-scan.pl $(COVERAGE_FILES)) > $@.tmp
	mv $@.tmp $@

