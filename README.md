# honk-api

Upon pushes to master, the app is automatically deployed to Heroku pending Continuous Integration approval from Travis CI.

## Development on Honk API
Please use make use of Python's virtual environment tools in dependency/package management.

1. Clone the repository and set your current directory to the project root.
2. Activate and provision your virtual environment ([see here](#venv))
3. Initalize the database on your development machine. ([see here](#database))
4. Run the flask application on the development server with `flask run`. It will be available on the local IP address `127.0.0.1`.

<a name=database></a>
### Dev Database Initialization & Migration
The Honk API implements a local SQLite database to reap the efficiencies of local data
storage for development and for its convenience in our database server/client model.

We use [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/), a wrapper
for the [SQLAlchemy](https://www.sqlalchemy.org) object relational mapper, to manage
tables in our database using classes. Mappings from database tables to classes
are defined in [models.py](https://github.com/benvandenbosch/honk-api/blob/master/app/models.py)

**Set up a Local Database for Development**

While within the project's virtual environment and in the root directory, run the command `flask db upgrade`. This will apply the most recent migration script from the [migrations](https://github.com/benvandenbosch/honk-api/tree/master/migrations) directory, making any additions/changes not in the local database.

**Add or Edit Tables in the Database**

Migrations are handled using [Flask-Migrate](https://github.com/miguelgrinberg/flask-migrate), a wrapper for the [Alembic](https://alembic.sqlalchemy.org/en/latest/) database migration tool for SQLAlchemy.


Table schemas are contained in [models.py](https://github.com/benvandenbosch/honk-api/blob/master/app/models.py). To edit a table, edit its class in this file. For a new table, add a new class.

Run `flask db migrate` to create a migration script that can apply these changes.

Finally, run `flask db upgrade` to apply the migration script locally.

**Downgrade the Database**
If you need to downgrade to a previous version of the database, the command `flask db downgrade` will revert the last migration.

<a name=venv></a>
### Virtual Environment
**Dependencies**

All of the dependencies for honk-api will live in `requirements.txt` within the root directory for the project.


Developers on Honk API will use Python's `venv` package to manage dependencies within the application. Developers must be running Python 3.4 or newer to use this tool. In our application, this directory will be called `honkenv`.

**Creating the Environment**

Developers on Honk's API will use Python's `venv` package to manage dependencies within the application on their local machine. Developers must be running Python 3.4 or newer to use this tool. In our root project directory, this directory will be called `honkenv`, though it will be included in the gitignore to prevent matriculation to production.

To create the environment, run this command in the root directory: `python3 -m venv honkenv`.

**Activating the Environment**

Activating the virtual environment will cause the application to run with the dependencies specified by the virtual environment.

To activate the virtual environment, from the project root directory, run the command: `source honkenv/bin/activate`

**Provisioning the environment**

To install all dependencies within your virtual environment, run the command: `pip install -r requirements.txt`. This command will also work to make sure you are up to date with

**Adding a Dependency**

To add a dependency to the virtual environment, first install the package within your local virtual environment: `pip install <name_of_dependency>`


Then, run `pip install -r requirements.txt` to make sure your virtual environment is up to date.

Finally, add it to `requirements.txt` so other developers can include it too: `pip freeze > requirements.txt`

**Deactivate the virtual environment**

Run the command `deactivate` while within the virtual environment
