#!/usr/bin/env bash
docker exec -it spark-master bash /spark/mysql_setup.sh
docker exec -it spark-worker bash /spark/mysql_setup.sh
sleep 10
docker exec -it spark-master bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/sparkjob.py