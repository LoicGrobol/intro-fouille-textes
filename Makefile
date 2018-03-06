SUBDIRS := syllabus slides
CLEANSUBDIRS = $(addprefix clean_,$(SUBDIRS))

all: $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@

$(CLEANSUBDIRS):
	$(MAKE) -C $(patsubst clean_%,%,$@) clean

test:
	$(MAKE) -C $@

clean: $(CLEANSUBDIRS)

.PHONY: all $(SUBDIRS) $(CLEANSUBDIRS) clean test
