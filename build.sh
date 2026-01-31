set -o errexit

pip install pybind11
pip install -r Requirement.txt && python manage.py collectstatic --no-input
pip install .

python manage.py makemigrations
python manage.py migrate
