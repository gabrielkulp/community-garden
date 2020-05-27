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
		return render_template("people.html")
	
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


@bp.route("/admin/plot")
def plot():
	return render_template("plot.html")


@bp.route("/admin/plots", methods=["GET", "POST"])
def plots():
	db = get_db()

	if request.method == "GET":
		return render_template("plots.html")
	
	action = request.form.get("action")

	if action not in ["add"]:
		abort(400) # client error: invalid action

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

	db.commit()
	return redirect(url_for("pages.plots"))


@bp.route("/admin/tools", methods=["GET", "POST"])
def tools():
	db = get_db()

	if request.method == "GET":
		return render_template("tools.html")
	
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
		return render_template("varieties.html")
	
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

# Database usage examples
#
#@bp.route("/bookshelf", methods=["GET", "POST"])
#@login_required
#def bookshelf():
#	db = get_db()
#	if (request.method == "GET"):
#		book_ids = db.execute(
#			"SELECT book_id FROM bookshelf WHERE user_id = ?",
#			(g.user["id"],)
#		).fetchall()
#		books = [catalog.get_info(b["book_id"]) for b in book_ids]
#		return render_template("bookshelf.html", books=books)
#
#	action = request.form.get("action")
#	book_id = request.form.get("book_id")
#	user_id = g.user["id"]
#
#	if not (action in ["add", "delete"] and book_id and user_id):
#		abort(400) # client error: bad request
#
#	prev_bookmark =  db.execute(
#		"SELECT book_id FROM bookshelf WHERE book_id = ? AND user_id = ?",
#		(book_id, user_id)
#	).fetchone()
#
#	if action == "delete" and prev_bookmark is not None:
#		db.execute(
#			"DELETE FROM bookshelf WHERE book_id = ? AND user_id = ?",
#			(book_id, user_id)
#		)
#
#	if action == "add" and prev_bookmark is None:
#		db.execute(
#			"INSERT INTO bookshelf (book_id, user_id) VALUES (?, ?)",
#			(book_id, user_id)
#		)
#
#	db.commit()
#	return redirect(url_for("books.bookshelf"))
#
#
#@bp.route("/book/<int:id>")
#def info(id):
#	db = get_db()
#	res = catalog.get_info(id)
#	logged_in = g.user and g.user["id"]
#	bookmarked = None
#
#	if (logged_in): # if logged in, check if the user has a bookmark already
#		bookmarked =  db.execute(
#			"SELECT book_id FROM bookshelf WHERE book_id = ? AND user_id = ?",
#			(id, g.user["id"])
#		).fetchone() is not None
#	else:
#		bookmarked = False
#
#	return render_template("bookInfo.html", book=res, bookmarked=bookmarked)
