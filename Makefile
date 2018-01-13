SUBDIRS := trivialities
CLEANSUBDIRS = $(addprefix clean_,$(SUBDIRS))

all: $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@

$(CLEANSUBDIRS):
	$(MAKE) -C $(patsubst clean_%,%,$@) clean

clean: $(CLEANSUBDIRS)

.PHONY: all $(SUBDIRS) $(CLEANSUBDIRS) clean
