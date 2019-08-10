#!/bin/bash

export FILES=$(ls bin/*)
for FILE in $FILES; do 
    export NAME=$(basename $FILE .py)
    if [ -z $TRAVIS_TAG ]; then 
        export NEW_NAME="${NAME}-build${TRAVIS_BUILD_NUMBER}_${TRAVIS_OS_NAME}"
    else 
        export NEW_NAME="${NAME}-${TRAVIS_TAG}_${TRAVIS_OS_NAME}"
    fi

    pyinstaller -F "$FILE" -n "$NEW_NAME"
done