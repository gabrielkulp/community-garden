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