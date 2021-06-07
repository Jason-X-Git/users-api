# Users DRF API

User API with List, Create, Delete and Search functions.

## Getting Started

```bash
$ git clone git@github.com:Jason-X-Git/users-api.git
$ cd users-api

# Setup virtual environment.
$ virtualenv project-env
$ source project-env/bin/activate
$ pip install -r requirements.txt

# Start web server.
$ python manage.py makemigrations authentication
$ python manage.py migrate
$ python manage.py runserver
```
Navigate to http://localhost:8000/api
```bash
# Testing
$ python manage.py test
```