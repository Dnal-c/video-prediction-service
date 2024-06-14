#!/bin/bash

ctrlc_received=0

function handle_ctrlc() {
    echo
    if [[ $ctrlc_received == 0 ]]
    then
        echo "Interrupted! Exit with code 0";
        ctrlc_received=1;
        exit 0
    fi
}

# trapping the SIGINT signal
trap handle_ctrlc SIGINT

# Checking ENV variables set
echo "-----------------Checking env variables-------------"
declare -a envs=(ELASTIC_HOST ELASTIC_LOGIN ELASTIC_PASSWORD MINIO_URL MINIO_BUCKET MINIO_KEY MINIO_SECRET_KEY)
for env in "${envs[@]}"
do
  if [[ -z "$(printf '%s\n' "${!env}")" ]]; then
    echo "Set the ${env} environment variable";
    exit 1;
  else 
    echo "${env} is set"
  fi
done

echo "-------------Generating huggingface models------------"
MODELS_DIR=$(pwd)/models
cd "$MODELS_DIR" || { echo "Failure"; exit 1; }
python models_to_local.py

echo "-------------Starting fastapi server------------------"
cd ..
fastapi run main.py --port 4300
