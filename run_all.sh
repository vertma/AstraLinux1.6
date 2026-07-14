#!/bin/bash
cd ~/project/server
python3 main.py &
SERVER_PID=$!
sleep 3
cd ~/project/client
python3 main.py
kill $SERVER_PID
