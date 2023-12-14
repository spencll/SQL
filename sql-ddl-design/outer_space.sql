-- from the terminal run:
-- psql < outer_space.sql

DROP DATABASE IF EXISTS outer_space;

CREATE DATABASE outer_space;

\c outer_space

CREATE TABLE galaxy
(
id SERIAL PRIMARY KEY,
name TEXT
);

INSERT INTO galaxy
  (name)
VALUES 
 ('Milky Way');

CREATE TABLE orbits
(
id SERIAL PRIMARY KEY,
name TEXT
);

INSERT INTO orbits 
  (name)
VALUES 
 ('The Sun'),
 ('Proxima Centauri'),
 ('Gliese 876');

CREATE TABLE planets
(
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  orbital_period_in_years FLOAT NOT NULL,
  orbits_id INTEGER REFERENCES orbits,
  galaxy_id INTEGER REFERENCES galaxy,
  moons TEXT []
);

INSERT INTO planets
  (name, orbital_period_in_years, moons)
VALUES
  ('Earth', 1.00, '{"The Moon"}'),
  ('Mars', 1.88,  '{"Phobos", "Deimos"}'),
  ('Venus', 0.62, '{}'),
  ('Neptune', 164.8, '{"Naiad", "Thalassa", "Despina", "Galatea", "Larissa", "S/2004 N 1", "Proteus", "Triton", "Nereid", "Halimede", "Sao", "Laomedeia", "Psamathe", "Neso"}'),
  ('Proxima Centauri b', 0.03, '{}'),
  ('Gliese 876 b', 0.23, '{}');