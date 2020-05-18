DROP TABLE IF EXISTS people;
DROP TABLE IF EXISTS plots;
DROP TABLE IF EXISTS varieties;
DROP TABLE IF EXISTS plants;
DROP TABLE IF EXISTS tools;
DROP TABLE IF EXISTS people_plots;

CREATE TABLE people (
	person_id INTEGER PRIMARY KEY AUTOINCREMENT,
	first_name VARCHAR NOT NULL,
	last_name VARCHAR NOT NULL,
	email VARCHAR NOT NULL,
	UNIQUE (first_name, last_name)
);

CREATE TABLE plots (
	plot_id INTEGER PRIMARY KEY AUTOINCREMENT,
	length FLOAT NOT NULL,
	width FLOAT NOT NULL,
	location VARCHAR NOT NULL
);

CREATE TABLE varieties (
	variety_id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR NOT NULL,
	season VARCHAR NOT NULL
);

CREATE TABLE plants (
	plant_id INTEGER PRIMARY KEY AUTOINCREMENT,
	variety_id INTEGER NOT NULL,
	plot_id INTEGER NOT NULL,
	FOREIGN KEY (variety_id) REFERENCES varieties (variety_id),
	FOREIGN KEY (plot_id) REFERENCES plots (plot_id)
);

CREATE TABLE tools (
	tool_id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR NOT NULL,
	checked_out BOOLEAN NOT NULL,
	condition INTEGER NOT NULL,
	person_id INTEGER NOT NULL,
	FOREIGN KEY (person_id) REFERENCES people (person_id)
);

CREATE TABLE people_plots (
	people_plot_id INTEGER PRIMARY KEY AUTOINCREMENT,
	person_id INTEGER NOT NULL,
	plot_id INTEGER NOT NULL,
	FOREIGN KEY (person_id) REFERENCES people (person_id),
	FOREIGN KEY (plot_id) REFERENCES plots (plot_id)
);
