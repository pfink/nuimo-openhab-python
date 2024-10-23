#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
source "./nuimo-python-venv/bin/activate"
python3 main.py
