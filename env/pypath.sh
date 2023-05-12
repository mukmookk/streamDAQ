#!/bin/bash

CURRENT_DIR="$(pwd)"
SRC_DIR="$CURRENT_DIR/../srcs"

if [[ ":$PYTHONPATH:" == *":$SRC_DIR:"* ]]; then
  echo "SRC_DIR already in PYTHONPATH. Skipping."
else
  echo "export PYTHONPATH=$SRC_DIR" >> ~/.bashrc
  echo "SRC_DIR added to PYTHONPATH."
  source ~/.bashrc
fi
