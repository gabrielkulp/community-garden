from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for, abort
)
import urllib

from garden.db import get_db

bp = Blueprint("pages", __name__, static_folder="static")


@bp.route("/")
def index():
	return render_template("index.html")

@bp.route("/people", methods=["GET", "POST"])
def people():
	db = get_db()

	if request.method == "GET":
		people = db.execute(
			"SELECT * FROM people;"
		).fetchall()
		return render_template("people.html", people=people)
	
	action = request.form.get("action")

	if action == "add":
		first_name = request.form.get("first_name")
		last_name  = request.form.get("last_name")
		email      = request.form.get("email")
	
		if not (first_name and last_name and email):
			abort(400) # client error: missing data
	
		db.execute(
			"INSERT INTO people (first_name, last_name, email) VALUES (?, ?, ?)",
			(first_name, last_name, email)
		)

	elif action == "first_name":
		first_name = request.form.get("name")
		person_id = request.form.get("person_id")

		if not first_name:
			abort(400)

		db.execute("UPDATE people SET first_name = ? WHERE person_id = ?", (first_name, person_id))
	elif action == "last_name":
		last_name = request.form.get("name")
		person_id = request.form.get("person_id")

		if not last_name:
			abort(400)

		db.execute("UPDATE people SET last_name = ? WHERE person_id = ?", (last_name, person_id))
	elif action == "email":
		email = request.form.get("email")
		person_id = request.form.get("person_id")

		if not email:
			abort(400)

		db.execute("UPDATE people SET email = ? WHERE person_id = ?", (email, person_id))
	elif action == "delete":
		person_id = request.form.get("person_id")

		if not person_id:
			abort(400) # client error: missing data

		db.execute(
			"DELETE FROM people WHERE person_id = ?",
			(person_id,)
		)
	else:
		abort(400)

	db.commit()
	return redirect(url_for("pages.people"))


@bp.route("/plot/<int:id>", methods=["GET", "POST"])
def plot(id):
	db = get_db()

	if request.method == "GET":
		plants = db.execute("""SELECT * FROM plants
							   INNER JOIN plots ON plants.plot_id = plots.plot_id
							   INNER JOIN varieties ON plants.variety_id = varieties.variety_id
							   WHERE plots.plot_id = ?""",
			(str(id))
		).fetchall()
		varieties = db.execute("SELECT * FROM varieties").fetchall()
		return render_template("plot.html", plants=plants, varieties=varieties)

	action = request.form.get("action")

	if action not in ["add", "delete"]:
		abort(400) # client error: invalid action
	
	if action == "add":
		variety_id = request.form.get("variety_id")

		if not variety_id:
			abort(400) # client error: missing data
		
		db.execute("INSERT INTO plants (variety_id, plot_id) VALUES (?, ?)",
			(variety_id, id)
		)
	elif action == "delete":
		plant_id = request.form.get("plant_id")

		if not plant_id:
			abort(400) # client error: missing data

		db.execute("DELETE FROM plants WHERE plant_id = ?", (plant_id,))
	
	db.commit()
	return redirect(url_for("pages.plot", id=id))


@bp.route("/plots", methods=["GET", "POST"])
def plots():
	db = get_db()

	if request.method == "GET":
		query = request.args.get("query", default="%")
		if query != "%":
			query = "%" + query + "%"

		plots = db.execute("""SELECT * FROM plots
							  LEFT JOIN people_plots ON plots.plot_id = people_plots.plot_id
							  LEFT JOIN people ON people_plots.person_id = people.person_id
							  WHERE location LIKE ?
							  ORDER BY plot_id ASC""", (query,)).fetchall()

		people = db.execute("SELECT * FROM people").fetchall()

		people_for_plot = {}
		for p in plots:
			if p['plot_id'] not in people_for_plot.keys():
				people_for_plot[p['plot_id']] = []
			people_for_plot[p['plot_id']].append(p['person_id'])

		# dedup
		dedup = []
		for p in plots:
			if [x for x in dedup if x['plot_id'] == p['plot_id']] == []:
				dedup.append(p)
		plots = dedup

		return render_template("plots.html", plots=plots, people=people, plot_owners=people_for_plot, query=query[1:-1])

	# handle POST request

	action = request.form.get("action")

	if action == "add":
		location = request.form.get("location")
		length   = request.form.get("length")
		width    = request.form.get("width")
		owners = request.form.getlist("owners")
	
		if not (location and length and width):
			abort(400) # client error: missing data

		cursor = db.cursor()	
		cursor.execute(
			"INSERT INTO plots (length, width, location) VALUES (?, ?, ?)",
			(length, width, location)
		)

		plot_id = cursor.lastrowid
		
		for o in owners:
			db.execute("INSERT INTO people_plots (plot_id, person_id) VALUES (?, ?)", (plot_id, o))
	elif action == "location":
		location = request.form.get("location")
		plot_id = request.form.get("plot_id")
		if not location:
			abort(400)

		db.execute("UPDATE plots SET location = ? WHERE plot_id = ?", (location, plot_id))
	elif action == "size":
		length   = request.form.get("length")
		width    = request.form.get("width")
		plot_id = request.form.get("plot_id")
		
		if not (length and width and plot_id):
			abort(400)

		try:
			length = float(length)
			width = float(width)
			assert(length > 0)
			assert(width > 0)
		except Exception as e:
			print(e)
			abort(400)
		
		db.execute("UPDATE plots SET width = ?, length = ? WHERE plot_id = ?", (width, length, plot_id))
	elif action == "owners":
		owners = request.form.getlist("owners")
		plot_id = request.form.get("plot_id")

		db.execute("DELETE FROM people_plots WHERE plot_id = ?", (plot_id))

		for o in owners:
			db.execute("INSERT INTO people_plots (plot_id, person_id) VALUES (?, ?)", (plot_id, o))
	elif action == "delete":
		plot_id = request.form.get("plot_id")

		if not plot_id:
			abort(400) # client error: missing data

		db.execute(
			"DELETE FROM plots WHERE plot_id = ?",
			(plot_id,)
		)
	else:
		abort(400) # client error: invalid action

	db.commit()
	return redirect(url_for("pages.plots"))


@bp.route("/tools", methods=["GET", "POST"])
def tools():
	db = get_db()

	if request.method == "GET":
		tools = db.execute("SELECT * FROM tools LEFT JOIN people ON tools.person_id = people.person_id").fetchall()
		people = db.execute("SELECT * FROM people").fetchall()
		return render_template("tools.html", tools=tools, people=people)
	
	action = request.form.get("action")

	if action == "add":
		name      = request.form.get("name")
		condition = request.form.get("condition")
		person    = request.form.get("person")
	
		if not (name and condition and person):
			abort(400) # client error: missing data
		
		if int(person) < 0:
			person = None
	
		# TODO: extra query to validate person id
		db.execute(
			"INSERT INTO tools (name, `condition`, person_id) VALUES (?, ?, ?)",
			(name, condition, person)
		)

	elif action == "name":
		name = request.form.get("name")
		tool_id = request.form.get("tool_id")

		if not (name and tool_id):
			abort(400)

		db.execute("UPDATE tools SET name = ? WHERE tool_id = ?", (name, tool_id))
	elif action == "check_out":
		person = request.form.get("person_id")
		tool_id = request.form.get("tool_id")

		if not (person and tool_id):
			abort(400)

		# null the fk
		if person == "checked_in":
			person = ""

		db.execute("UPDATE tools SET person_id = ? WHERE tool_id = ?", (person, tool_id))
	elif action == "condition":
		condition = request.form.get("condition")
		tool_id = request.form.get("tool_id")

		if not (condition and tool_id):
			abort(400)

		db.execute("UPDATE tools SET condition = ? WHERE tool_id = ?", (condition, tool_id))
	elif action == "delete":
		tool_id = request.form.get("tool_id")

		if not tool_id:
			abort(400) # client error: missing data
		
		db.execute("DELETE FROM tools WHERE tool_id = ?", (tool_id,))
	else:
		abort(400)

	db.commit()
	return redirect(url_for("pages.tools"))


@bp.route("/varieties", methods=["GET", "POST"])
def varieties():
	db = get_db()

	if request.method == "GET":
		varieties = db.execute(
			"SELECT * FROM varieties;"
		).fetchall()
		return render_template("varieties.html", varieties=varieties)
	
	action = request.form.get("action")

	if action == "add":
		name   = request.form.get("name")
		season = request.form.get("season")
	
		if not (name and season):
			abort(400) # client error: missing data
		
		db.execute(
			"INSERT INTO varieties (name, season) VALUES (?, ?)",
			(name, season)
		)
	elif action == "name":
		name = request.form.get("name")
		variety_id = request.form.get("variety_id")

		if not (name and variety_id):
			abort(400)

		db.execute("UPDATE varieties SET name = ? WHERE variety_id = ?", (name, variety_id))
	elif action == "season":
		season = request.form.get("season")
		variety_id = request.form.get("variety_id")

		if not (season and variety_id):
			abort(400)

		db.execute("UPDATE varieties SET season = ? WHERE variety_id = ?", (season, variety_id))
	elif action == "delete":
		variety_id = request.form.get("variety_id")

		if not variety_id:
			abort(400)

		db.execute("DELETE FROM plants WHERE variety_id = ?", (variety_id))
		db.execute("DELETE FROM varieties WHERE variety_id = ?", (variety_id))
	else:
		abort(400)

	db.commit()
	return redirect(url_for("pages.varieties"))
