#!/bin/bash

cd /code/

pip install -r /code/requirements.txt

# Starting the tasks service
/scripts/spawn_worker.sh tasks.jobs &

# Starting the backend service
python -m backend.__init__
