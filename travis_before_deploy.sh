#!/bin/bash
if [ -z "$TRAVIS_TAG" ]
then
    git config --local user.name "Loïc Grobol"
    git config --local user.email "loic.grobol@gmail.com"
    export TRAVIS_TAG=latest
    git tag -f $TRAVIS_TAG
fi
