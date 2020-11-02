#!/bin/bash

python ./produce.py

git add -u
git commit -m "[AUTO] Automatic update ($(date +'%y%m%d%H%M'))."
git push
