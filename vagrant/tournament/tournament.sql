-- noinspection SqlNoDataSourceInspectionForFile
-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--drop table players if it exists
drop table if exists players cascade;

--create the players table
create table players(
	id serial primary key,
	name varchar(50));

--drop table matches if it exists
drop table if exists matches;

--create the matches table
create table matches(
	id1 integer references players(id),
	id2 integer references players(id),
	winner integer,
	primary key(id1, id2));
