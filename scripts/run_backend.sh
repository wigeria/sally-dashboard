#!/bin/bash

cd /code/

pip install -r /code/requirements.txt

# Starting the tasks service
(while true; do
    # This line halts execution inside the loop until a crash/exit
    /scripts/spawn_worker.sh tasks.jobs
done) &

# Starting the backend service
python -m backend.__init__
