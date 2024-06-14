#!/bin/bash
MODELS_DIR=$(pwd)/models

cd "$MODELS_DIR" || { echo "Failure"; exit 1; }

python models_to_local.py

fastapi run main.py --port 4300
