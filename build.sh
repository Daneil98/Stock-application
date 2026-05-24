#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip setuptools wheel
pip install pybind11

# Compile and install C++ transaction engine
pip install . -v

# Install Python deps
pip install -r requirements.txt

# Django commands
python manage.py collectstatic --noinput    
python manage.py migrate
