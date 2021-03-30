SDIR  = ./
IDIR  = ./
LDIR  = ./

MAKEFLAGS = --no-print-directory -r -s
INCLUDE = $(shell root-config --cflags)
LIBS    = $(shell root-config --libs) -lTMVA -lMLP -lTreePlayer -lMinuit
CFLAGS +=-g

BINS7 = roo
OBJS = 
all: $(BINS7) $(BINS9)

$(BINS7): % : main.C
	@echo -n "Building $@ ... "
	$(CXX) $(CCFLAGS) $(CFLAGS) $< -I$(IDIR) $(INCLUDE) $(LIBS) TH1Fs/TH1Fs.C main/EventLoop.C utilis/NeutrinoBuilder.C utilis/Chi2_minimization.C utilis/configparser.h -o execute
	@echo "Done"

clean:
	rm -f $(BINS)
