#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """
    Connect to the PostgreSQL database.
    Returns a database connection.
    """

    try:
        return psycopg2.connect("dbname=tournament")
    except psycopg2.DatabaseError:
        print "Was unable to connect to the database"


def delete_matches():
    """
    Remove all the match records from the database.
    """

    # get a cursor to our database
    delete_matches_cursor = connect().cursor()

    # put our delete statement in string form
    delete_matches_query = "delete from matches"

    # execute and commit our query, then close our cursor
    delete_matches_cursor.execute(delete_matches_query)
    delete_matches_cursor.execute("commit;")
    delete_matches_cursor.close()


def delete_players():
    """
    Remove all the player records from the database.
    """
    # get a cursor to our database
    delete_players_cursor = connect().cursor()

    # put our delete statement in string form
    # CASCADE our delete because if we have no players we should have no matches
    delete_players_query = "delete from players CASCADE"

    # execute and commit our query, then close our cursor
    delete_players_cursor.execute(delete_players_query)
    delete_players_cursor.execute("commit;")
    delete_players_cursor.close()


def count_players():
    """Returns the number of players currently registered."""
    # get a cursor to our database
    count_players_cursor = connect().cursor()

    # put our query in a string
    count_players_query = """select count(*) from players"""

    # execute our query
    # get all results
    # parse our information from the result set
    # close our cursor
    count_players_cursor.execute(count_players_query)
    fetchall = count_players_cursor.fetchall()
    count = fetchall[0][0]
    count_players_cursor.close()

    return count


def register_player(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    # get a cursor to our database
    register_player_cursor = connect().cursor()

    # our insert string
    register_player_query = """INSERT INTO players (name) values (%s);"""

    # execute our insert statement with the name parameter
    # commit the insert and close our cursor
    register_player_cursor.execute(register_player_query, (name,))
    register_player_cursor.execute("commit;")
    register_player_cursor.close()


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
    # get a cursor to our database
    player_standings_cursor = connect().cursor()

    # create a string to query our view
    player_standings_query = "select * from player_standings_view;"

    # execute our query
    # get all results
    # close our cursor
    player_standings_cursor.execute(player_standings_query)
    standings = player_standings_cursor.fetchall()
    player_standings_cursor.close()

    return standings


def report_match(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # get a cursor to our database
    report_match_cursor = connect().cursor()

    # create our query string
    # winner will be listed first and in the winner column
    # loser will be listed second
    report_match_query = """insert into matches (id1, id2, winner) values (%s, %s, %s) """

    # execute our query
    # commit our changes
    # close our cursor
    report_match_cursor.execute(report_match_query, (winner, loser, winner,))
    report_match_cursor.execute("commit;")
    report_match_cursor.close()


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
    # get a cursor to our database
    swiss_pairing_cursor = connect().cursor()

    # create our query string
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

    # execute our query
    # get all results
    # close our cursor
    swiss_pairing_cursor.execute(swiss_pairing_query)
    pairing = swiss_pairing_cursor.fetchall()
    swiss_pairing_cursor.close()
    return pairing
