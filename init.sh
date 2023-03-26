#!/bin/bash

python3 src/process_dataset.py

case "$1" in
  "dashboard")
    streamlit run src/app.py
  ;;
  "notebooks")
    jupyter notebook notebooks
  ;;
  *)
    echo "ERROR: Invalid option.
Valid options are: dashboard or notebook"
  exit 1
  ;;
esac
