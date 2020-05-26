-- Data Definition Queries

DROP TABLE IF EXISTS people_plots;
DROP TABLE IF EXISTS plants;
DROP TABLE IF EXISTS tools;
DROP TABLE IF EXISTS people;
DROP TABLE IF EXISTS plots;
DROP TABLE IF EXISTS varieties;

CREATE TABLE people (
	person_id INTEGER PRIMARY KEY AUTOINCREMENT,
	first_name VARCHAR(100) NOT NULL,
	last_name VARCHAR(100) NOT NULL,
	email VARCHAR(100) NOT NULL,
	UNIQUE (first_name, last_name)
);

CREATE TABLE plots (
	plot_id INTEGER PRIMARY KEY AUTOINCREMENT,
	length FLOAT NOT NULL,
	width FLOAT NOT NULL,
	location VARCHAR(100) NOT NULL,
	UNIQUE (location)
);

CREATE TABLE varieties (
	variety_id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(100) NOT NULL,
	season VARCHAR(100) NOT NULL,
	UNIQUE (name)
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
	name VARCHAR(100) NOT NULL,
	checked_out BOOLEAN NOT NULL DEFAULT (FALSE),
	`condition` INTEGER NOT NULL DEFAULT (1), -- condition is reserved word
	/* condition enum:
		1 -> New
		2 -> Great
		3 -> Good
		4 -> Fair
		5 -> Poor
		6 -> Broken
       (not using MariaDB enum b/c final impl will be in SQLite)
	*/
	person_id INTEGER, -- not null b/c can be not checked out
	FOREIGN KEY (person_id) REFERENCES people (person_id)
);

CREATE TABLE people_plots (
	people_plot_id INTEGER PRIMARY KEY AUTOINCREMENT,
	person_id INTEGER NOT NULL,
	plot_id INTEGER NOT NULL,
	FOREIGN KEY (person_id) REFERENCES people (person_id),
	FOREIGN KEY (plot_id) REFERENCES plots (plot_id)
);
