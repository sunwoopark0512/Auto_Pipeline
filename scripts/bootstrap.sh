#!/bin/bash

# 가상환경 설정
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

echo "Bootstrap completed."
