#!/bin/bash
git config --local user.name "Loïc Grobol"
git config --local user.email "loic.grobol@gmail.com"
if [ $TRAVIS_BRANCH == 'master' ]
then
    git tag -f latest
elif [ $TRAVIS_BRANCH == 'stableb' ]
then
    git tag -f stable
fi
