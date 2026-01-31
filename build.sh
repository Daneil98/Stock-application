

set -o errexit

pip install --upgrade pip setuptools wheel
pip install pybind11

pwd
ls -la

# Install native extension FIRST
pip install . -v

#  Install Python deps
pip install -r requirements.txt

# Django commands (safe now)
python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
