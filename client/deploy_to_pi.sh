#!/bin/bash

rsync -avzC  --exclude="env" --exclude=".*" ./* sgzmd@192.168.0.19:/home/sgzmd/apps/tempi/client/
