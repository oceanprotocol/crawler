#!/bin/bash
mkdir -p logs && touch logs/rest_service.log
python rest_service.py &
tail -F logs/rest_service.log
