set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate --noinput
