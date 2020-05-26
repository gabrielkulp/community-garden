import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def init_app(app):
	app.teardown_appcontext(_close_db)
	app.cli.add_command(_db_init_command)
	app.cli.add_command(_db_example_command)


def get_db():
	if "db" not in g:
		g.db = sqlite3.connect(
			current_app.config["DATABASE"],
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row
	
	return g.db


def _close_db(e=None):
	db = g.pop("db", None)

	if db is not None:
		db.close()


def _init():
	db = get_db()

	with current_app.open_resource("schema.sql") as s:
		db.executescript(s.read().decode("utf8"))


def _load_example():
	db = get_db()
	with current_app.open_resource("example.sql") as s:
		db.executescript(s.read().decode("utf-8"))


@click.command("db-init")
@with_appcontext
def _db_init_command():
	"""Clear the existing data and create new tables."""
	_init()
	click.echo("Initialized the database.")


@click.command("db-example")
@with_appcontext
def _db_example_command():
	"""Load example data into database."""
	_load_example()
	click.echo("Loaded example data.")
