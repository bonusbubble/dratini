#!/usr/bin/env bash

PROJECT_ROOT=$(pwd)

BGC_ROOT=$(realpath ../bgc)
RAYLIB_ROOT=$(realpath ../raylib)

LINKING_ROOT=$PROJECT_ROOT/dratini/linking

INCLUDE_DIR=$LINKING_ROOT/include
LIB_DIR=$LINKING_ROOT/lib/$DRATINI_PLATFORM

function build_bgc() {
    cd $BGC_ROOT
    make cleanall
    make
    cp include/* $INCLUDE_DIR
    cp dist/lib/* $LIB_DIR
    cd $PROJECT_ROOT
}

function build_raylib() {
    cd $RAYLIB_ROOT/src
    make clean
    make
    cd $RAYLIB_ROOT
    cp src/raylib.h $INCLUDE_DIR
    cp src/libraylib.a $LIB_DIR
    cd $PROJECT_ROOT
}

function build_all() {
    build_bgc
    build_raylib
}

build_all
