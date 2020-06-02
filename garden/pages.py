from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for, abort
)
import urllib

from garden.db import get_db

bp = Blueprint("pages", __name__, static_folder="static")


@bp.route("/")
def index():
	return render_template("index.html")


@bp.route("/user")
def user():
	return render_template("user.html")


@bp.route("/admin")
def admin():
	return render_template("admin.html")


@bp.route("/admin/people", methods=["GET", "POST"])
def people():
	db = get_db()

	if request.method == "GET":
		people = db.execute(
			"SELECT * FROM people;"
		).fetchall()
		return render_template("people.html", people=people)
	
	action = request.form.get("action")

	if action not in ["add"]:
		abort(400) # client error: invalid action

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

	db.commit()
	return redirect(url_for("pages.people"))


@bp.route("/admin/plot/<int:id>")
def plot(id):
	db = get_db()
	plants = db.execute("""SELECT * FROM plants
						   INNER JOIN plots ON plants.plot_id = plots.plot_id
						   INNER JOIN varieties ON plants.variety_id = varieties.variety_id
						   WHERE plots.plot_id = ?""", (str(id))).fetchall()

	return render_template("plot.html", plants=plants)


@bp.route("/admin/plots", methods=["GET", "POST"])
def plots():
	db = get_db()

	if request.method == "GET":
		query = request.args.get("query", default="")
		plots = db.execute("""SELECT * FROM plots
							  INNER JOIN people_plots ON plots.plot_id = people_plots.plot_id
							  INNER JOIN people ON people_plots.person_id = people.person_id
							  ORDER BY plot_id ASC""").fetchall()

		people = db.execute("SELECT * FROM people").fetchall()

		if query is not "":
			plots = [x for x in plots if query in x["location"]]

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

		return render_template("plots.html", plots=plots, people=people, plot_owners=people_for_plot, query=query)

	# handle POST request

	action = request.form.get("action")

	if action == "add":
		location = request.form.get("location")
		length   = request.form.get("length")
		width    = request.form.get("width")
	
		if not (location and length and width):
			abort(400) # client error: missing data
	
		db.execute(
			"INSERT INTO plots (length, width, location) VALUES (?, ?, ?)",
			(length, width, location)
		)
	elif action == "changelocation":
		location = request.form.get("location")
		plot_id = request.form.get("plot_id")
		if not location:
			abort(400)

		db.execute("UPDATE plots SET location = ? WHERE plot_id = ?", (location, plot_id))
	elif action == "changesize":
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
	elif action == "changeowners":
		owners = request.form.getlist("owners")
		plot_id = request.form.get("plot_id")

		db.execute("DELETE FROM people_plots WHERE plot_id = ?", (plot_id))

		for o in owners:
			db.execute("INSERT INTO people_plots (plot_id, person_id) VALUES (?, ?)", (plot_id, o))

	else:
		abort(400) # client error: invalid action

	db.commit()
	return redirect(url_for("pages.plots"))


@bp.route("/admin/tools", methods=["GET", "POST"])
def tools():
	db = get_db()

	if request.method == "GET":
		tools = db.execute("SELECT * FROM tools LEFT JOIN people ON tools.person_id = people.person_id").fetchall()
		people = db.execute("SELECT * FROM people").fetchall()
		return render_template("tools.html", tools=tools, people=people)
	
	action = request.form.get("action")

	if action not in ["add"]:
		abort(400) # client error: invalid action

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

	db.commit()
	return redirect(url_for("pages.tools"))


@bp.route("/admin/varieties", methods=["GET", "POST"])
def varieties():
	db = get_db()

	if request.method == "GET":
		varieties = db.execute(
			"SELECT * FROM varieties;"
		).fetchall()
		return render_template("varieties.html", varieties=varieties)
	
	action = request.form.get("action")

	if action not in ["add"]:
		abort(400) # client error: invalid action

	if action == "add":
		name   = request.form.get("name")
		season = request.form.get("season")
	
		if not (name and season):
			abort(400) # client error: missing data
		
		db.execute(
			"INSERT INTO varieties (name, season) VALUES (?, ?)",
			(name, season)
		)

	db.commit()
	return redirect(url_for("pages.varieties"))
