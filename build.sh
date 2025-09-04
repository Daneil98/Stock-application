set -o errexit

pip install pybind11
pip install -r Requirement.txt
pip install .


python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
