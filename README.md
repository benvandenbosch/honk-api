# honk-api

## Development on Honk API
Please use make use of Python's virtual environment tools in dependency/package management.

1. Clone the repository and set your current directory to the project root.
2. Activate and provision your virtual environment ([see here](#venv))
3. Run the flask application on the development server with `flask run`. It will be available on the local IP address `127.0.0.1`.


### Virtual Environment
<a name=venv></a>
**Dependencies**

All of the dependencies for honk-api will live in `dependencies.txt` within the root directory for the project.


Developers on Honk API will use Python's `venv` package to manage dependencies within the application. Developers must be running Python 3.4 or newer to use this tool. In our application, this directory will be called `honkenv`.

**Creating the Environment**

Developers on Honk's API will use Python's `venv` package to manage dependencies within the application on their local machine. Developers must be running Python 3.4 or newer to use this tool. In our root project directory, this directory will be called `honkenv`, though it will be included in the gitignore to prevent matriculation to production.

To create the environment, run this command in the root directory: `python3 -m venv honkenv`.

**Activating the Environment**

Activating the virtual environment will cause the application to run with the dependencies specified by the virtual environment.

To activate the virtual environment, from the project root directory, run the command: `source honkenv/bin/activate`

**Provisioning the environment**

To install all dependencies within your virtual environment, run the command: `pip install -r dependencies.txt`. This command will also work to make sure you are up to date with

**Adding a Dependency**

To add a dependency to the virtual environment, first install the package within your local virtual environment: `pip install <name_of_dependency`


Then, run `pip install -r dependencies.txt` to make sure your virtual environment is up to date.

Finally, add it to `dependencies.txt` so other developers can include it too: `pip freeze > dependencies.txt`

**Deactivate the virtual environment**

Run the command `deactivate` while within the virtual environment
