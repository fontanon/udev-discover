#!/usr/bin/make -f

PROJECT = udevdiscover

GETTEXT = /usr/bin/xgettext
MSGMERGE = /usr/bin/msgmerge

PO = $(shell find . -name '*.po' -print | sed -e 's!./!!g')

update-po:
	$(GETTEXT) -f POTFILES -L python -d $(PROJECT) -o $(PROJECT).pot
	$(GETTEXT) -j -f POTFILESUI -L glade -d $(PROJECT) -o $(PROJECT).pot
	for lang in $(PO); do $(MSGMERGE) -U $$lang $(PROJECT).pot; done 
