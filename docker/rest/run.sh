#!/bin/bash
mkdir -p logs && touch logs/rest_service.log
python rest_service.py &
tail -f logs/rest_service.log
