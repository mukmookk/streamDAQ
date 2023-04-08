#!/bin/bash

function usage() {
    echo "Usage: $0 [-h] [-k <API_KEY>] [-d <DIRECTORY>]"
    echo "  -h: Display this help message"
    echo "  -k <API_KEY>: Set the API key"
    echo "  -d <DIRECTORY>: Set the DAQWD environment variable to the specified directory"
    exit 1
}

while getopts "hk:d:" opt; do
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
            source ~/.bashrc
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

if [[ -z "${DAQWD}" ]]; then
    echo "DAQWD is not set"
    usage
fi

echo "APIKEY is set to ${APIKEY}"
echo "DAQWD is set to ${DAQWD}"

# change directory to DAQWD
cd $DAQWD

# execute Python file
python your_python_file.py
