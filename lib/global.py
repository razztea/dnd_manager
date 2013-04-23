"""
This module handles any global functions
like user registration.
"""
import MySQLdb
import simplejson

connection = MySQLdb.connect(user='dnd_root', passwd='dnd_root', host='localhost', db='dnd_manager')
db_cursor = connection.cursor(MySQLdb.cursors.DictCursor)

def register(json_data):
    # check to see if username exists
    json_dict = simplejson.loads(json_data)
    username = MySQLdb.escape_string(json_dict['username'])
    password = MySQLdb.escape_string(json_dict['password'])
    master = "TRUE" if json_dict['account_type'] == 'master' else "FALSE"

    with connection:
        db_cursor.execute("SELECT username FROM users WHERE username = %s", username)
        exists = db_cursor.fetchone()

        if exists:
            return simplejson.dumps({"success": "false", "message": "Username already exists. Please choose another."})

        else:
            update_query = "INSERT INTO users (username, password, master) VALUES ('%s', AES_ENCRYPT('%s', username), %s)" % (username, password, master)
            db_cursor.execute(update_query)
            return simplejson.dumps({"success": "true"})

def sign_in(json_data):
    # try to sign on with the given credentials
    json_dict = simplejson.loads(json_data)
    username = MySQLdb.escape_string(json_dict['username'])
    password = MySQLdb.escape_string(json_dict['password'])

    with connection:
        db_cursor.execute("SELECT username, master FROM users WHERE username = '%s' AND password = AES_ENCRYPT('%s', username)" % (username, password))
        result = db_cursor.fetchone()

        if result:
            account_type = 'master' if result['master'] else 'player'
            return simplejson.dumps({"success": "true", "account_type": account_type, "username": result['username']})

        else:
            return simplejson.dumps({"success": "false", "message": "Invalid Username or Password"})
