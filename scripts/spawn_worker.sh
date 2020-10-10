#!/bin/bash

# Meant to be used as ./spawn_workers <module containing actors>; ex: spawn_workers tasks.jobs
dramatiq $1 --watch.sh
