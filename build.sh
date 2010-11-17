#!/bin/sh
set +x

VERSION=0.0.1
PYTHON=python2.5
PACKNAME=localbox
APPNAME=Localbox
CAPBLS=NetworkServices+LocalServices+ReadUserData+WriteUserData+UserEnvironment
PYS60DIR=/home/ignatov/src/symbian/S60
BUILDDIR=target

rm -rf ./ensymble.py
cp -R $PYS60DIR/ensymble.py .

rm -rf ./module-repo
cp -R $PYS60DIR/module-repo .

rm -rf ./templates
cp -R $PYS60DIR/templates .

rm -rf ./$BUILDDIR
mkdir -p ./$BUILDDIR/root/data/python/lib/$PACKNAME
cp ./src/$PACKNAME/*.py ./$BUILDDIR/root/data/python/lib/$PACKNAME
cp ./src/default.py ./$BUILDDIR

# copy libraries to build dir
cp -R ./lib/* ./$BUILDDIR/root/data/python/lib

$PYTHON ./ensymble.py py2sis \
    --version="$VERSION" \
    --appname="$APPNAME" \
    --caps="$CAPBLS" \
    --extrasdir=root $BUILDDIR \
    "$APPNAME.sis"