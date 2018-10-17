LIBS_ORIG := $(patsubst %/,%, $(dir $(wildcard libs/*/Makefile)))
LIBS_CLEAN := $(addsuffix -clean,$(LIBS_ORIG))

.PHONY: $(LIBS_CLEAN)

all: build-shared

build-libs: $(LIBS_ORIG)

$(LIBS_ORIG):
	$(MAKE) -C $@

build-shared:
	$(MAKE) -C project

test:
	@echo $(LIBS_ORIG)

# clean:$(LIBS_CLEAN)
clean:
	$(MAKE) -C project clean
	$(MAKE) -C bin clean
	$(RM) -rf  logs/*.log
	$(RM) -rf  tmp

cleanall:$(LIBS_CLEAN) clean

install:
	$(MAKE) -C project install

$(LIBS_CLEAN):
	$(MAKE) -C $(@:-clean=) clean
