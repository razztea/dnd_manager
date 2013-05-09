"""
This module handles any player-side functions
like generating a character.
"""
import MySQLdb
import simplejson

connection = MySQLdb.connect(user='rpg_root', passwd='rpg_root', host='localhost', db='rpg_manager')
db_cursor = connection.cursor(MySQLdb.cursors.DictCursor)

def save_character(json_data):
    json_dict = simplejson.loads(json_data)
    username = MySQLdb.escape_string(json_dict['username'])
    world_id = MySQLdb.escape_string(json_dict['world_id'])

    # TODO save the character
    return simplejson.dumps({"success": "true"})

def retrieve_world_list(json_data):
    # retrive all worlds to show player the list to choose from

    with connection:
        db_cursor.execute("SELECT * FROM worlds")
        result = db_cursor.fetchall()

        if result:
            return simplejson.dumps({"success": "true", "worlds": result})
        else:
            return simplejson.dumps({"success": "false", "message": "Error pulling user's worlds."})

def retrieve_world_info(json_data):
    # try to sign on with the given credentials
    json_dict = simplejson.loads(json_data)
    world_id = MySQLdb.escape_string(json_dict['world_id'])

    with connection:
        db_cursor.execute("SELECT * FROM races WHERE world_id = '%s'" % (world_id))
        races = db_cursor.fetchall()

        db_cursor.execute("SELECT * FROM classes WHERE world_id = '%s'" % (world_id))
        classes = db_cursor.fetchall()

        db_cursor.execute("SELECT * FROM attributes WHERE world_id = '%s'" % (world_id))
        attributes = db_cursor.fetchall()

        db_cursor.execute("SELECT * FROM alignments WHERE world_id = '%s'" % (world_id))
        alignments = db_cursor.fetchall()

        return simplejson.dumps({"success": "true", "races": races, "classes": classes, "attributes": attributes, "alignments": alignments})
