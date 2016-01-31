#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""

    return psycopg2.connect("dbname=tournament")


def delete_matches():
    """Remove all the match records from the database."""
    delete_matches_cursor = connect().cursor()

    delete_matches_query = "delete from matches"

    delete_matches_cursor.execute(delete_matches_query)
    delete_matches_cursor.execute("commit;")


def delete_players():
    """Remove all the player records from the database."""
    delete_players_cursor = connect().cursor()

    delete_players_query = "delete from players CASCADE"

    delete_players_cursor.execute(delete_players_query)
    delete_players_cursor.execute("commit;")


def count_players():
    """Returns the number of players currently registered."""
    count_players_cursor = connect().cursor()

    count_players_query = """select count(*) from players"""

    count_players_cursor.execute(count_players_query)

    fetchall = count_players_cursor.fetchall()

    count = fetchall[0][0]

    return count


def register_player(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    register_player_cursor = connect().cursor()

    register_player_query = """INSERT INTO players (name) values (%s);"""

    register_player_cursor.execute(register_player_query, (name,))
    register_player_cursor.execute("commit;")


def player_standings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    player_standings_cursor = connect().cursor()

    player_standings_query = """select players.id,
                                players.name,
                                count(matches.winner) as wins,
                                ((select count(*)
                                 from matches
                                 where players.id = matches.id1) +
                                 (select count(*)
                                 from matches
                                 where players.id = matches.id2)) as matches_played
                                from players
                                left join matches
                                on players.id = matches.winner
                                group by players.id;
                                """

    player_standings_cursor.execute(player_standings_query)

    standings = player_standings_cursor.fetchall()

    return standings


def report_match(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    report_match_cursor = connect().cursor()

    report_match_query = """insert into matches (id1, id2, winner) values (%s, %s, %s) """

    report_match_cursor.execute(report_match_query, (winner, loser, winner,))
    report_match_cursor.execute("commit;")


def swiss_pairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    swiss_pairing_cursor = connect().cursor()

    swiss_pairing_query = """ select player1.id, player1.name, player2.id, player2.name
                              from players player1
                              join (
                                 select id, name, count(matches.winner) countPlayer2
                                 from players
                                 left join matches on matches.winner = players.id
                                 group by players.id
                              ) as player2
                              on player2.countPlayer2 =
                                (select count(matches.winner)
                                 from matches
                                 where matches.winner = player1.id)
                              where player1.id < player2.id
                              group by player1.id, player2.id, player2.name;
                              """

    swiss_pairing_cursor.execute(swiss_pairing_query)

    pairing = swiss_pairing_cursor.fetchall()

    return pairing
