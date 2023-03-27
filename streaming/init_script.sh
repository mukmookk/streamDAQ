#!/bin/bash

function usage() {
    echo "Usage: $0 [-h] [-k <API_KEY>]"
    echo "  -h: Display this help message"
    echo "  -k <API_KEY>: Set the API key"
    exit 1
}

while getopts "hk:" opt; do
    case ${opt} in
        h)
            usage
            ;;
        k)
            export APIKEY="${OPTARG}"
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

echo "APIKEY is set to ${APIKEY}"