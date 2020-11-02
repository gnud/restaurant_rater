Implement voting REST API for choosing where to go to lunch.

Basic business rules/requirements

1. Everyone can add/remove/update restaurants

2. Every user gets X (hardcoded, but "configurable") votes per day.

	1st user vote on the same restaurant counts as 1
	2nd = 0.5
	3rd and all subsequent votes, as 0.25.

2.1. If a voting result is the same in a couple of restaurants, the
winner is the one who got more distinct users to vote on it.

3. Every day vote amounts are reset. Not used previous day votes are
lost.

4. Show the history of selected restaurants per time period

5. Do not forget, that frontend dev will need a way to show on what
restaurants users can vote and what restaurant is a winner.

6. Readme on how to use API, launch project etc

If the app would be wrapped in docker, it would be great, but not
mandatory.
Bonus points, API is deployed somewhere (For example, Heroku)`


# TODOS
- [x] django project
- [x] django app for API
- [x] documentations
- [x] django app routes
- [ ] requirements
    1. [x] Everyone can add/remove/up... 
    1. [x] Every user gets X (hardcod...
    1. [x] Every day vote amounts ar...
    1. [ ] Show the history of selec...
    1. [ ] Do not forget, that front... [WIP: vote done 1 of 2]
    1. [x] API routes dump in docs [WIP]
- [x] docker container + docker compose
- [x] production on Heroku or better


# Quick start

First we start by cloning the project's repo

```
git clone https://github.com/gnud/restaurant_rater.git
```

now, cd into our project

```
virtualenv -p python3 venv
source venv/bin/activate
```

Note: we can replace venv with ~/.venvs/restaurant_rater_venv or
any full path to some venvs directory

# Install packages

```
pip install -r requirements.txt
```

Note: make sure virtualenv is loaded.

# Migrations

Do initial migration first

```python 
./manage.py migrate
```

Now setup a cache table for the cache database backend 

```bash
./manage.py createcachetable
```

# Usage

## API Docs
A guest user can browse API docs via the Insomnia viewer web interface, provided
via http://127.0.0.1:8000/static/index.html

## Run server

### runserver

````bash
./manage.py runserver
````

### gunicorn (locally)

**Note**: Working directory must be the project's root

```bash
gunicorn -c restaurant_rater/gunicorn.conf.py restaurant_rater.wsgi:application --preload
```

### gunicorn (pycharm)

Create a new Python Run configuration, named Gunicorn or whatever.

Find path:
- Find the full gunicorn path, use ```which gunicorn``` in your projects path when virtualenv is loaded to find the
full path.
- Or find it by hand in myvenv/bin/gunicorn.

**Note**: if gunicorn is not found, make sure you install all packages from requirements.txt.

Apply full path in **Script path**.

In **Parameters** paste this '-c gunicorn.conf.py wsgi:application --preload'
- wsgi:application - means wsgi.py which is located in restaurant_rater/wsgi.py as python module and application is
variable an instance of WSGIHandler.

**Working directory** should be set as "restaurant_rater/restaurant_rater" using it's full path, not relative - where
restaurant_rater is the root project path, and restaurant_rater is the Django project's python package.

After saving the Run configuration try running it with run/debug

Expected to see:
```
... Random config verbose garbage
[2020-11-01 16:01:01 +0000] [29684] [INFO] Starting gunicorn 20.0.4
[2020-11-01 16:01:01 +0000] [29684] [DEBUG] Arbiter booted
[2020-11-01 16:01:01 +0000] [29684] [INFO] Listening at: http://0.0.0.0:8000 (29684)
[2020-11-01 16:01:01 +0000] [29684] [INFO] Using worker: sync
[2020-11-01 16:01:01 +0000] [29684] [DEBUG] 1 workers
[2020-11-01 16:01:01 +0000] [29694] [INFO] Booting worker with pid: 29694
```

## Admin

An admin user can login via the admin web interface, provided
via http://127.0.0.1/admin/

## Create a sample user

```bash
./manage.py createsuperuser --username='petko' --email='petko@example.com'
# <type a password>
```

### Login

Login with sample user
and the owner can see Menus admin page.

## API

The browsable API located at
http://127.0.0.1:8000/api/v1/restaurant/

## Testing

To run RestaurantTests

```bash
./manage.py test api.tests.RestaurantTests
```

To run VotingTests

```bash
./manage.py test api.tests.VotingTests
```

# Docker

This Dockerfile is based on the official Python image and it's full version including and OS, vim and less.

Docker-compose is being added to manage the services.

**Note**: for less complexity no database server was chosen, there for we have mounted the "docker/data/db.sqlite3"
for the database to the root path of the django project

Building

```bash
docker-compose build
docker-compose up -d
```

Logs

```bash
docker-compose logs -f
```

**NOTE**: Control the log level via the env var APP_GUNICORN_LOGLEVEL: info, debug see gunicorn docs for more. 

### Start API service

```bash
docker-compose up -d
```

### Stop API service

```bash
docker-compose stop dj-api
```

### API exec manage.py

```bash
docker-compose exec dj-api python manage.py
```

Now we can use:
- manage.py migrate
- manage.py collectstatic
- manage.py createsuperuser
when needed.

To access the shell in the container:

```bash
docker-compose exec dj-api bash
```

### First time

1. Migrate database

```bash
docker-compose exec dj-api python manage.py createcachetable
```

2. collectstatic

```bash
docker-compose exec dj-api python manage.py collectstatic
```

3. Cache table for the cache database backend 

```bash
docker-compose exec dj-api python manage.py createcachetable
```

### Container structure

Our Django project root is located in /app/
Contains only the minimum required files to run Django, controlled via .dockerignore.