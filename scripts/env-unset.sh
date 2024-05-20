#!/bin/sh

## Usage:
##   . ./env-unset.sh

unset $(grep -v '^#' .env | sed -E 's/OBJREC_(.*)=.*/\1/' | xargs)