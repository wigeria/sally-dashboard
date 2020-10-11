#!/bin/bash

cd /code/

# Starting the tasks service
/scripts/spawn_worker.sh tasks.jobs &

# Starting the backend service
python -m backend.__init__
