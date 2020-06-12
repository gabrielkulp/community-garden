-- A lot of these queries can be easily changed for different fields to filter on, i.e. id vs name vs email, etc.

------------
-- PEOPLE --
------------

-- Create a Person
INSERT INTO people (first_name, last_name, email) VALUES (:first_name, :last_name, :email);

-- Read a Person(s)
SELECT * FROM people;
SELECT * FROM people WHERE person_id = :id;

-- Update a Person
UPDATE people SET first_name = :first_name WHERE person_id = :id;
UPDATE people SET last_name = :last_name WHERE person_id = :id;
UPDATE people SET email = :email WHERE person_id = :id;

-- Delete a Person
DELETE FROM people_plots WHERE person_id = :id; -- and the second query
DELETE FROM people WHERE person_id = :id;

-----------
-- PLOTS --
-----------

-- Create a Plot
INSERT INTO plots (length, width, location) VALUES (:length, :width, :location);
INSERT INTO people_plots (person_id, plot_id) VALUES (:person, :plot);

-- READ a Plot(s)
SELECT * FROM plots
INNER JOIN people ON plots.person_id = people.person_id
WHERE plots.plot_id = :id;
SELECT * FROM plots
INNER JOIN people ON plots.person_id = people.person_id;

-- Update a Plot
UPDATE plots SET location = :location WHERE plot_id = :id;
UPDATE plots SET width = :width, length = :length WHERE plot_id = :id;


-- Delete a Plot
DELETE FROM people_plots WHERE plot_id = :id; -- and the second query
DELETE FROM plots WHERE plot_id = :id;

-----------
-- TOOLS --
-----------

-- Create a Tool
INSERT INTO tools (name, `condition`, person_id) VALUES (:name, :condition, NULL);
INSERT INTO tools (name, `condition`, person_id) VALUES (:name, :condition, :person);

-- Read a Tool
SELECT * FROM tools
INNER JOIN people ON tools.person_id = people.people_id
WHERE tools.tool_id = :id;
SELECT * FROM tools
INNER JOIN people ON tools.person_id = people.people_id;

-- Update a Tool
UPDATE tools SET name = :name WHERE tool_id = :id;
UPDATE tools SET person_id = :person_id WHERE tool_id = :id;
UPDATE tools SET condition = :condition WHERE tool_id = :id;

-- Delete a Tool
DELETE FROM tools WHERE tool_id = :id;

---------------
-- VARIETIES --
---------------

-- Create a Variety
INSERT INTO varieties (name, season) VALUES (:name, :season);

-- Read a Variety(s)
SELECT * FROM varieties;
SELECT * FROM varieties WHERE variety_id = :id;

-- Update a Variety
UPDATE varieties SET name = :name WHERE variety_id = :id;
UPDATE varieties SET season = :season WHERE variety_id = :id;

-- Delete a Variety
DELETE FROM plants WHERE variety_id = :id; -- and the second query
DELETE FROM varieties WHERE variety_id = :id;

------------
-- PLANTS --
------------

-- Create a Plant
INSERT INTO plants (variety_id, plot_id) VALUES (:variety, :plot);

-- Read a Plant(s)
SELECT * FROM plants
INNER JOIN plots ON plants.plot_id = plots.plot_id
INNER JOIN varieties ON plants.variety_id = varieties.variety_id
WHERE plants.id = :id;
SELECT * FROM plants
INNER JOIN plots ON plants.plot_id = plots.plot_id
INNER JOIN varieties ON plants.variety_id = varieties.variety_id;

-- Update not needed

-- Delete a Plant
DELETE FROM plants WHERE plant_id = :id;
