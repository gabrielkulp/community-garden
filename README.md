# Tomato Boundary Community Garden

An open-source garden manager written in Python 3.

## Installation

For the simplest method, just do this:

```bash
pip install flask # or use pip3 if Python 2 is your system default
flask init-db
```

For an isolated installation, the process is a bit more involved:

```bash
# First install the isolated package environment
# manager if it isn't already available
pip install virtualenv

# Next create a new virtual environment
virtualenv --python=python3 venv

# Activate the virtual environment in Bash.
# There are other scripts for other shells, like activate.fish and .ps1
source venv/bin/activate

# Once inside venv, pip will install packages isolated from your system
pip install flask

# Then setup your local state
flask init-db

# When you're done with flask, exit the virtual environment
deactivate
```

## Usage

If you're using `virtualenv`, then first run `source venv/bin/activate`. Run `deactivate` or exit the shell to leave the virtual environment.

Execute `flask run`, then visit http://127.0.0.1:5000 in your browser.

### Comtributors

Flask has a built-in development server that supports auto-reload on source change and shows an interactive debugger on errors. Run it with `FLASK_ENV=development flask run`.
