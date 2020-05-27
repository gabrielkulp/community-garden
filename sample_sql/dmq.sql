-- A lot of these queries can be easily changed for different fields to filter on, i.e. id vs name vs email, etc.

------------
-- PEOPLE --
------------

-- Add a Person
INSERT INTO people (first_name, last_name, email) VALUES (:fname, :lname, :email);

-- Get a Person(s)
SELECT * FROM people;
SELECT * FROM people WHERE person_id = :id;

-- Change a Person
UPDATE people SET email = :email WHERE person_id = :id;

-- Delete a Person
DELETE FROM people_plots WHERE person_id = :id; -- and the second query
DELETE FROM people WHERE person_id = :id;

-----------
-- PLOTS --
-----------

-- Add a Plot
INSERT INTO plots (length, width, location) VALUES (:length, :width, :location);
INSERT INTO people_plots (person_id, plot_id) VALUES (:person, :plot);

-- Get a Plot(s)
SELECT * FROM plots
INNER JOIN people ON plots.person_id = people.person_id
WHERE plots.plot_id = :id;
SELECT * FROM plots
INNER JOIN people ON plots.person_id = people.person_id;

-- Change a Plot
UPDATE plots SET width = :width WHERE plot_id = :id;

-- Delete a Plot
DELETE FROM people_plots WHERE plot_id = :id; -- and the second query
DELETE FROM plots WHERE plot_id = :id;

-----------
-- TOOLS --
-----------

-- Add a Tool
INSERT INTO tools (name, `condition`) VALUES (:name, :condition);
INSERT INTO tools (name, checked_out, `condition`, person_id) VALUES (:name, TRUE, :condition, :person);

-- Get a Tool
SELECT * FROM tools
INNER JOIN people ON tools.person_id = people.people_id
WHERE tools.tool_id = :id;
SELECT * FROM tools
INNER JOIN people ON tools.person_id = people.people_id;

-- Change a Tool
UPDATE tools SET checked_out = FALSE, person_id = NULL WHERE tool_id = :id;

-- Delete a Tool
DELETE FROM tools WHERE tool_id = :id;

---------------
-- VARIETIES --
---------------

-- Add a Variety
INSERT INTO varieties (name, season) VALUES (:name, :season);

-- Get a Variety(s)
SELECT * FROM varieties;
SELECT * FROM varieties WHERE variety_id = :id;

-- Change a Variety
UPDATE varieties SET season = :season WHERE variety_id = :id;

-- Delete a Variety
DELETE FROM plants WHERE variety_id = :id; -- and the second query
DELETE FROM varieties WHERE variety_id = :id;

------------
-- PLANTS --
------------

-- Add a Plant
INSERT INTO plants (variety_id, plot_id) VALUES (:variety, :plot);

-- Get a Plant(s)
SELECT * FROM plants
INNER JOIN plots ON plants.plot_id = plots.plot_id
INNER JOIN varieties ON plants.variety_id = varieties.variety_id
WHERE plants.id = :id;
SELECT * FROM plants
INNER JOIN plots ON plants.plot_id = plots.plot_id
INNER JOIN varieties ON plants.variety_id = varieties.variety_id;

-- Change a Plant
UPDATE plants SET plot_id = :plot WHERE plant_id = :id;

-- Delete a Plant
DELETE FROM plants WHERE plant_id = :id;
