#!/bin/bash

DEFAULT_BOOTSTRAP_SERVER="localhost:9092"
DEFAULT_DAQWD="./"

function usage() {
    echo "Usage: $0 [-h] [-k <API_KEY>] [-b <BOOTSTRAP_SERVER>] [-t <TOPIC>] [-d <DIRECTORY>] <ACTION>"
    echo "  -h: Display this help message"
    echo "  -k <API_KEY>: Set the API key"
    echo "  -b <BOOTSTRAP_SERVER>: Set the bootstrap server"
    echo "  -t <TOPIC>: Set the topic"
    echo "  -d <DIRECTORY>: Set the DAQWD environment variable to the specified directory"
    echo "  <ACTION>: Specify 'produce' to execute the Kafka producer or 'test' to execute the Kafka consumer"
    exit 1
}

while getopts "hk:b:t:d:" opt; do
    case ${opt} in
        h)
            usage
            ;;
        k)
            export APIKEY="${OPTARG}"
            ;;
        b)
            export BOOTSTRAP_SERVER="${OPTARG}"
            ;;
        t)
            export TOPIC="${OPTARG}"
            ;;
        d)
            export DAQWD="${OPTARG}"
            ;;
        \?)
            usage
            ;;
    esac
done

if [[ -z "${APIKEY}" ]]; then
    echo "APIKEY is not set"
    usage
fi

# Set default value for BOOTSTRAP_SERVER
export BOOTSTRAP_SERVER="${BOOTSTRAP_SERVER:-$DEFAULT_BOOTSTRAP_SERVER}"
echo "BOOTSTRAP_SERVER is set to ${BOOTSTRAP_SERVER}"

# Set default value for DAQWD
export DAQWD="${DAQWD:-$DEFAULT_DAQWD}"
echo "DAQWD is set to ${DAQWD}"

ACTION="${@:$OPTIND:1}"

if [[ "$ACTION" == "produce" ]]; then
    # execute Kafka producer Python file
    python kafka_producer.py --bootstrap-server "${BOOTSTRAP_SERVER}" --topic "${TOPIC}" --api-key "${APIKEY}"
elif [[ "$ACTION" == "test" ]]; then
    # execute Kafka consumer Python file
    python kafka_consumer.py --bootstrap-server "${BOOTSTRAP_SERVER}" --topic "${TOPIC}" --api-key "${APIKEY}"
else
    usage
fi
