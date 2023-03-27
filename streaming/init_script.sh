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
            if grep -q '^export APIKEY=' ~/.bashrc; then
                sed -i "s/^export APIKEY=.*/export APIKEY=${OPTARG}/" ~/.bashrc
            else
                echo "export APIKEY=${OPTARG}" >> ~/.bashrc
            fi
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