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
- django project                    [x]
- django app for API                [x]
- documentations                    [x]
- django app routes                 [x]
- requirements
    1. Everyone can add/remove/up...[] 
    1. Every user gets X (hardcod...[]
    1. Every day vote amounts ar... []
    1. Show the history of selec... []
    1. Do not forget, that front... []
    1. API routes dump in docs      []
- docker container + docker compose []
- production on Heroku              []


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

# Usage

## Admin

An admin user can login via the admin web interface, provide
via http://127.0.0.1/admin/

## Create a sample user

```bash
./manage.py createsuperuser --username='petko' --email='petko@example.com'
# <type a password>
```

### Login

Login with sample user
and the owner can see Menus admin page.

The admin page for the menu has one field called company, which has also company admin, to be
able to use the popup in place for creating companies

## API

The browsable API located at
http://127.0.0.1:8000/api/v1/orders/ 

