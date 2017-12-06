#!/usr/bin/env bash
apt-get update &&
apt-get install python3-dev libmysqlclient-dev -y &&
apt-get install python-pip -y &&
pip install mysqlclient &&
apt-get install python-mysqldb
