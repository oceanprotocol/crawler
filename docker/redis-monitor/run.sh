#!/bin/bash
mkdir -p logs && touch logs/redis_monitor.log
python redis_monitor.py &
tail -f logs/redis_monitor.log
