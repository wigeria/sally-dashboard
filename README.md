# Sally-Dashboard

A customizable UI for working with [Selenium-YAML](https://github.com/wigeria/selenium-yaml-core) bots. The UI can be customized by forking the repository and modifying the `frontend/` contents, while new `Steps` for the bots can be added via the Plugin functionality (needs better documentation).

## Running via Docker

After the `.env` file has been set up (see variables in `.env.example`), a simple `docker-compose up` will be enough to get the services running locally. The backend should be available on port 5000, and the frontend on 3000.

If you require network `host` to be used by the redis/backend containers (perhaps if you have a local database), use `docker-compose -f docker-compose.linux.yml` up.


### Running Tests

Tests can be run by getting into a docker bash shell, and using `pytest tests`.

Note that if you're using the included Redis service via docker-compose, you'll probably want to use `exec` to get into a running container, instead of `run` to spawn a new container.

## Documentation

The endpoints and file structure is partially documented under `docs/`. Note that this is currently not as comprehensive as it could be, but further documentation and improvements are planned.
