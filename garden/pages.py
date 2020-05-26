from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for, abort
)
import urllib

from garden.db import get_db

bp = Blueprint("pages", __name__, static_folder="static")

@bp.route("/")
def index():
	return render_template("index.html")


# Database usage examles
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
