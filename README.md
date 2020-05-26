# Tomato Boundary Community Garden

An open-source garden manager written in Python 3.

## Installation

For the simplest method (might require sudo), just do this:

```bash
pip3 install flask
flask db-init
flask db-example # optional to load example data
```

For an isolated installation, the process is a bit more involved:

```bash
# First install the isolated package environment
# manager if it isn't already available.
pip3 install virtualenv

# Next create a new virtual environment
virtualenv --python=python3 venv

# Activate the virtual environment in Bash.
# There are other scripts for other shells, like activate.fish and .ps1
source venv/bin/activate

# Once inside venv, pip will install packages isolated from your system
pip install flask

# Then setup your local state
flask db-init

# Optionally, load example data
flask db-example

# When you're done with flask, exit the virtual environment
deactivate
```

## Usage

If you're using `virtualenv`, then first run `source venv/bin/activate`. Run `deactivate` or exit the shell to leave the virtual environment.

### Commands

* `flask run` starts the server. Visit http://127.0.0.1:5000 in your browser.

* `flask db-init` creates or clears the database that stores garden information.

* `flask db-example` loads example data (additive) for testing.

## Contributor Info

* Tabs, not spaces. That's what the tab key is for.

* Use quotes for strings, not apostrophes. The exception is in templates, where it messes up the syntax highlighting to use real quotes.

* Don't commit (even locally) if there are errors or warnings.

* Flask has a built-in development server that supports auto-reload on source change and shows an interactive debugger on errors. Run it with `FLASK_ENV=development flask run`.

* Flask also has a shell that's useful for debugging. Use `flask shell`, then access modules after importing them: `import garden.books as books`.
