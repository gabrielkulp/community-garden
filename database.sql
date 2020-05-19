DROP TABLE IF EXISTS people_plots;
DROP TABLE IF EXISTS plants;
DROP TABLE IF EXISTS tools;
DROP TABLE IF EXISTS people;
DROP TABLE IF EXISTS plots;
DROP TABLE IF EXISTS varieties;

-- DDQs
CREATE TABLE people (
	person_id INTEGER PRIMARY KEY AUTO_INCREMENT,
	first_name VARCHAR(100) NOT NULL,
	last_name VARCHAR(100) NOT NULL,
	email VARCHAR(100) NOT NULL,
	UNIQUE (first_name, last_name)
);

CREATE TABLE plots (
	plot_id INTEGER PRIMARY KEY AUTO_INCREMENT,
	length FLOAT NOT NULL,
	width FLOAT NOT NULL,
	location VARCHAR(100) NOT NULL,
	UNIQUE (location)
);

CREATE TABLE varieties (
	variety_id INTEGER PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(100) NOT NULL,
	season VARCHAR(100) NOT NULL,
	UNIQUE (name)
);

CREATE TABLE plants (
	plant_id INTEGER PRIMARY KEY AUTO_INCREMENT,
	variety_id INTEGER NOT NULL,
	plot_id INTEGER NOT NULL,
	FOREIGN KEY (variety_id) REFERENCES varieties (variety_id),
	FOREIGN KEY (plot_id) REFERENCES plots (plot_id)
);

CREATE TABLE tools (
	tool_id INTEGER PRIMARY KEY AUTO_INCREMENT,
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
	people_plot_id INTEGER PRIMARY KEY AUTO_INCREMENT,
	person_id INTEGER NOT NULL,
	plot_id INTEGER NOT NULL,
	FOREIGN KEY (person_id) REFERENCES people (person_id),
	FOREIGN KEY (plot_id) REFERENCES plots (plot_id)
);

-- Default Data

-- Add People
INSERT INTO people (first_name, last_name, email) VALUES ('Harold', 'Miller', 'harold.miller@email.corp');
INSERT INTO people (first_name, last_name, email) VALUES ('Nancy', 'Mulligan', 'nancy.mulligan@email.corp');

-- Add Plots
INSERT INTO plots (length, width, location) VALUES (9.0, 5.0, 'Near shed');
INSERT INTO plots (length, width, location) VALUES (3.0, 3.0, 'North of gate');

-- Add Varieties
INSERT INTO varieties (name, season) VALUES ('Argentina Cherry Tomato', 'Late Summer');
INSERT INTO varieties (name, season) VALUES ('Esterina Tomato', 'Early Fall');
INSERT INTO varieties (name, season) VALUES ('Emerald Evergreen Tomato', 'Late Spring');
INSERT INTO varieties (name, season) VALUES ('Virginia Sweets Tomato', 'Late Summer');
INSERT INTO varieties (name, season) VALUES ('Rosella Tomato', 'Late Fall');
INSERT INTO varieties (name, season) VALUES ('Ace Tomato', 'Early Fall');
INSERT INTO varieties (name, season) VALUES ('Maya Tomato', 'Early Fall');
INSERT INTO varieties (name, season) VALUES ('Miroma Tomato', 'Early Fall');

-- Add Plants (M:M People/Plots)
INSERT INTO plants (variety_id, plot_id) VALUES ((
	SELECT variety_id FROM varieties WHERE name = 'Ace Tomato'
), (
	SELECT plot_id FROM plots WHERE location = 'Near shed'
));
INSERT INTO plants (variety_id, plot_id) VALUES ((
	SELECT variety_id FROM varieties WHERE name = 'Maya Tomato'
), (
	SELECT plot_id FROM plots WHERE location = 'Near shed'
));
INSERT INTO plants (variety_id, plot_id) VALUES ((
	SELECT variety_id FROM varieties WHERE name = 'Miroma Tomato'
), (
	SELECT plot_id FROM plots WHERE location = 'Near shed'
));

-- Add Tools (M:1 with People)
INSERT INTO tools (name, `condition`) VALUES ('Trowel', 3);
INSERT INTO tools (name, checked_out, `condition`, person_id) VALUES ('Watering can', TRUE, 4, (
	SELECT person_id FROM people WHERE first_name = 'Harold' and last_name = 'Miller'
));
INSERT INTO tools (name, checked_out, `condition`, person_id) VALUES ('Shears', TRUE, 1, (
	SELECT person_id FROM people WHERE first_name = 'Nancy' and last_name = 'Mulligan'
));