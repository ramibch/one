git pull
uv run manage.py migrate
sudo systemctl restart huey.service
sudo systemctl restart gunicorn.service
