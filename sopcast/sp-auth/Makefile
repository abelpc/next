#!/usr/bin/make -f

PACKAGE ?= sp-auth
NAME ?= sp-sc-auth
PREFIX ?= /usr
DATADIR ?= $(PREFIX)/share
DOCDIR ?= $(DATADIR)/doc/$(PACKAGE)
INSTALLDIR ?= $(DATADIR)/$(PACKAGE)
BINDIR ?= $(PREFIX)/bin
INSTALL ?= install -p
EXECUTABLE ?= sp-sc
VERSION ?= 3.2.6

build:

install:
	$(INSTALL) -dm 0755 $(DESTDIR)$(INSTALLDIR)
	$(INSTALL) -dm 0755 $(DESTDIR)$(DOCDIR)
	$(INSTALL) -dm 0755 $(DESTDIR)$(BINDIR)
	$(INSTALL) -m 0755 $(NAME) $(DESTDIR)$(BINDIR)/$(EXECUTABLE)
	$(INSTALL) -m 0644 Readme $(DESTDIR)$(DOCDIR)

uninstall:
	rm -fr $(DESTDIR)$(INSTALLDIR)
	rm -fr $(DESTDIR)$(DOCDIR)
	rm $(DESTDIR)$(INSTALLDIR)/$(NAME)


