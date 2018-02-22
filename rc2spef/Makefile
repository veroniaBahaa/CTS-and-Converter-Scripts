#
# qflow project source compile makefile
#

# Main compiler arguments
CFLAGS = -g -O2
DEFS = -DPACKAGE_NAME=\"\" -DPACKAGE_TARNAME=\"\" -DPACKAGE_VERSION=\"\" -DPACKAGE_STRING=\"\" -DPACKAGE_BUGREPORT=\"\" -DPACKAGE_URL=\"\" -DSTDC_HEADERS=1 -DHAVE_SETENV=1 -DHAVE_PUTENV=1 -DTCLSH_PATH=\"/usr/bin/tclsh\"
LIBS = 
LDFLAGS = 
INSTALL = /usr/bin/install -c

OBJECTS = rc2spef.o
HASHLIB = hash.o
LIBERTYLIB = readliberty.o
SOURCES := $(patsubst %.o,%.c,$(OBJECTS))
TARGETS := $(patsubst %.o,%$(EXEEXT),$(OBJECTS))

BININSTALL = ${QFLOW_LIB_DIR}/bin

all: $(TARGETS)

rc2spef$(EXEEXT): rc2spef.o $(HASHLIB) $(LIBERTYLIB)
	$(CC) $(LDFLAGS) rc2spef.o $(HASHLIB) $(LIBERTYLIB) -o $@ $(LIBS)


clean:
	$(RM) -f $(OBJECTS) $(HASHLIB) $(LIBERTYLIB)
	$(RM) -f $(TARGETS)

veryclean:
	$(RM) -f $(OBJECTS) $(HASHLIB) $(LIBERTYLIB)
	$(RM) -f $(TARGETS)

.c.o:
	$(CC) $(CFLAGS) $(CPPFLAGS) $(DEFS) -c $< -o $@
