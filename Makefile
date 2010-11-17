BUILDDIR=target
DEVPYTHON=python2.5
help:
	@echo "Use:"
	@echo "  build"
	@echo "  dev-run"
	@echo "  clean"

dev-run:
	$(DEVPYTHON) ./src/dev.py

build:
	./build.sh

clean:
	rm -rf ./debug.txt
	rm -rf ./ensymble.py
	rm -rf ./module-repo
	rm -rf ./templates
	rm -rf ./$(BUILDDIR)
	rm -rf ./*.sis
	rm -rf ./.dropbox
	rm -rf ./.localbox
	rm -rf ./.localbox.log
