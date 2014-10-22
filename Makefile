SHELL = /bin/sh +x
export PATH := ./bin:$(PATH)
# `make SETUP_PY_TARGET=develop install` to install as "developer egg"
SETUP_PY_TARGET ?= install
VIRTUALENV_NAME ?= data-in-the-mines
INSTALL_ROOT ?= $(HOME)

# Each of your targets should be listed as .PHONY (unless you are actually
# compiling a C source file or similar)
# :r! grep '^[a-z-]\+:' % | cut -d: -f1 | sort | tr "\n" " "
.PHONY: config edit install install-crontab package-deps run-example test uninstall virtualenv 
# first target is default, let it be something harmless
config:


# dev-helper targets

edit:
	vim README.md Makefile requirements.txt `find ./data-in-the-mines ./exampleapp \( -path '*.egg-info' -o -path '*/build/*' -o -name 'jquery*' -o -name __init__.py -o -name '*.egg' -o -name '*.pyc' -o -name '*.swp' -o -name '*.swo' -o -iname '*.ico' -o -iname '*.png' -o -iname '*.gif' -o -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.pdf' -o -iname '*.doc' \) -prune  -o -type f  -print`

test:
	nosetests  -sv --with-doctest --logging-level=INFO --cover-branches --with-coverage --cover-erase --cover-package=data-in-the-mines data-in-the-mines

# runtime targets

run-exampleapp:
	. ./bin/activate && ./exampleapp/app.py --config=config --debug

# installation targets

install: package-deps virtualenv
	git pull origin master && . ./bin/activate && cd ./data-in-the-mines && ./setup.py $(SETUP_PY_TARGET)

install-crontab:
	git pull origin master && ./bin/install-crontab

package-deps:
	sudo aptitude update && sudo aptitude safe-upgrade && sudo aptitude install gawk git libfreetype6-dev python2.7 python-dev python-pip python-virtualenv r-recommended

uninstall:
	. ./bin/activate && yes | pip uninstall data-in-the-mines

virtualenv:
	virtualenv --python=/usr/bin/python2.7 --no-site-packages --setuptools --prompt="[$(VIRTUALENV_NAME)]" . && \
	. ./bin/activate && pip install -r requirements.txt

# make is notoriously picky about formatting, these settings should make it
# reasonably safe to edit it with vim.  You might also want to frequently do:
# :%s/\s\+$// to remove all trailing whitespace
# vim: set noexpandtab shiftwidth=8 softtabstop=8 tabstop=8:
