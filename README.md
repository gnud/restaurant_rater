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
- django project                    []
- django app for API                []
- documentations                    []
- docker container + docker compose []
- production on Heroku              []