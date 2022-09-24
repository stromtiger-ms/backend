# Installation

Run the Container (see docker-compose.yml File) using docker-compose et al.

Initialize the DB with the following commands:

> docker compose exec app flask --app myapp db init

> docker compose exec app flask --app myapp db migrate

> docker compose exec app flask --app myapp db upgrade


## Curl Commands

Download all Verbraucher
> docker compose exec app curl localhost:5000/getallverbraucher

# TODOS
- Should probably version the migrations (so init & migrate is no longer necessary)