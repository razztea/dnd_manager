"""
This module handles any master-side functions
like saving or pulling a world.
"""
import MySQLdb
import simplejson

connection = MySQLdb.connect(user='rpg_root', passwd='rpg_root', host='localhost', db='rpg_manager')
db_cursor = connection.cursor(MySQLdb.cursors.DictCursor)

def save_world(json_data):
    # check to see if username exists
    json_dict = simplejson.loads(json_data)
    username = MySQLdb.escape_string(json_dict['username'])
    world_id = MySQLdb.escape_string(json_dict['world_id'])
    world_name = MySQLdb.escape_string(json_dict['world_name'])

    races = json_dict['Races']
    classes = json_dict['Classes']
    attributes = json_dict['Attributes']
    alignments = json_dict['Alignments']

    with connection:
        if json_dict['world_id'] == "new":
            # Insert the new world into the database and get its id
            insert_query = "INSERT INTO worlds (id, master_username, name) VALUES (UUID(), '%s', '%s')" % (username, world_name)
            db_cursor.execute(insert_query)
            db_cursor.execute("SELECT id FROM worlds WHERE master_username = '%s' AND name = '%s'" % (username, world_name))
            result = db_cursor.fetchone()
            world_id = result['id']
        else:
            # Make sure the name stays up to date
            update_query = "UPDATE worlds SET name = '%s' WHERE master_username = '%s' AND id = '%s'" % (world_name, username, world_id)
            db_cursor.execute(update_query)

        for attr in attributes:
            name = MySQLdb.escape_string(attr['name'])
            desc = MySQLdb.escape_string(attr['description'])
            delete = attr.get('_destroy', False)
            if attr['id'] and not delete:
                update_query = "UPDATE attributes SET name = '%s', description = '%s', min = %d, max = %d WHERE id = '%s'" % (name, desc, attr['min'], attr['max'], attr['id'])
                db_cursor.execute(update_query)
            elif delete:
                delete_query = "DELETE FROM attributes WHERE id = '%s'" % (attr['id'])
                db_cursor.execute(delete_query)
            else:
                insert_query = "INSERT INTO attributes (id, world_id, name, description, min, max) VALUES (UUID(), '%s', '%s', '%s', %d, %d)" % (world_id, name, desc, attr['min'], attr['max'])
                db_cursor.execute(insert_query)
                db_cursor.execute("SELECT id FROM attributes WHERE world_id = '%s' AND name = '%s'" % (world_id, name))
                result = db_cursor.fetchone()
                attr['id'] = result['id']

        for ali in alignments:
            name = MySQLdb.escape_string(ali['name'])
            desc = MySQLdb.escape_string(ali['description'])
            delete = ali.get('_destroy', False)
            if ali['id'] and not delete:
                update_query = "UPDATE alignments SET name = '%s', description = '%s' WHERE id = '%s'" % (name, desc, ali['id'])
                db_cursor.execute(update_query)
            elif delete:
                db_cursor.execute("DELETE FROM alignments WHERE id = '%s'" % (attr['id']))
            else:
                insert_query = "INSERT INTO alignments (id, world_id, name, description) VALUES (UUID(), '%s', '%s', '%s')" % (world_id, name, desc)
                db_cursor.execute(insert_query)
                db_cursor.execute("SELECT id FROM alignments WHERE world_id = '%s' AND name = '%s'" % (world_id, name))
                result = db_cursor.fetchone()
                ali['id'] = result['id']

        for cls in classes:
            name = MySQLdb.escape_string(cls['name'])
            desc = MySQLdb.escape_string(cls['description'])
            delete = cls.get('_destroy', False)
            if cls['id'] and not delete:
                update_query = "UPDATE classes SET name = '%s', description = '%s', min_hp = %d, max_hp = %d WHERE id = '%s'" % (name, desc, cls['min_hp'], cls['max_hp'], cls['id'])
                db_cursor.execute(update_query)
            elif delete:
                db_cursor.execute("DELETE FROM classes WHERE id = '%s'" % (cls['id']))
            else:
                insert_query = "INSERT INTO classes (id, world_id, name, description, min_hp, max_hp) VALUES (UUID(), '%s', '%s', '%s', %d, %d)" % (world_id, name, desc, cls['min_hp'], cls['max_hp'],)
                db_cursor.execute(insert_query)
                db_cursor.execute("SELECT id FROM classes WHERE world_id = '%s' AND name = '%s'" % (world_id, name))
                result = db_cursor.fetchone()
                cls['id'] = result['id']

            if not delete:
                for attr_req in cls['attribute_requirements']:
                    if attr_req['id']:
                        update_query = "UPDATE class_attribute_requirements SET min = %d, max = %d, WHERE id = '%s'" % (attr_req['min'], attr_req['maximum'], attr_req['id'])
                        db_cursor.execute(update_query)
                    else:
                        attribute_id = [attr['id'] for attr in attributes if attr['name'] == attr_req['attr_name']][0]
                        insert_query = "INSERT INTO class_attribute_requirements (id, class_id, attribute_id, min, max) VALUES (UUID(), '%s', '%s', %d, %d)" % (cls['id'], attribute_id, attr_req['min'], attr_req['max'])
                        db_cursor.execute(insert_query)
                        db_cursor.execute("SELECT id FROM class_attribute_requirements WHERE class_id = '%s' AND attribute_id = '%s'" % (cls['id'], attribute_id))
                        result = db_cursor.fetchone()
                        attr_req['id'] = result['id']

                for align_req in cls['alignments']:
                    allowed = "TRUE" if align_req['allowed'] else "FALSE"
                    if align_req['id']:
                        update_query = "UPDATE class_alignments SET allowed = %s WHERE id = '%s'" % (allowed, align_req['id'])
                        db_cursor.execute(update_query)
                    else:
                        alignment_id = [align['id'] for align in alignments if align['name'] == align_req['ali_name']][0]
                        insert_query = "INSERT INTO class_alignments (id, class_id, alignment_id, allowed) VALUES (UUID(), '%s', '%s', %s)" % (cls['id'], alignment_id, allowed)
                        db_cursor.execute(insert_query)
                        db_cursor.execute("SELECT id FROM class_alignments WHERE class_id = '%s' AND alignment_id = '%s'" % (cls['id'], alignment_id))
                        result = db_cursor.fetchone()
                        align_req['id'] = result['id']

        for race in races:
            name = MySQLdb.escape_string(race['name'])
            desc = MySQLdb.escape_string(race['description'])
            spec = MySQLdb.escape_string(race['special'])
            delete = race.get('_destroy', False)
            if race['id'] and not delete:
                update_query = "UPDATE races SET name = '%s', class_limit = %d, description = '%s', special = '%s' WHERE id = '%s'" % (name, race['class_limit'], desc, spec, race['id'])
                db_cursor.execute(update_query)
            elif delete:
                db_cursor.execute("DELETE FROM races WHERE id = '%s'" % (race['id']))
            else:
                insert_query = "INSERT INTO races (id, world_id, name, class_limit, description, special) VALUES (UUID(), '%s', '%s', %s, '%s', '%s')" % (world_id, name, race['class_limit'], desc, spec)
                db_cursor.execute(insert_query)
                db_cursor.execute("SELECT id FROM races WHERE world_id = '%s' AND name = '%s'" % (world_id, name))
                result = db_cursor.fetchone()
                race['id'] = result['id']

            if not delete:
                for attr_req in race['attribute_requirements']:
                    if attr_req['id']:
                        update_query = "UPDATE race_attribute_requirements SET max = %d, min = %d, modifier = %d WHERE id = '%s'" % (attr_req['max'], attr_req['min'], attr_req['modifier'], attr_req['id'])
                        db_cursor.execute(update_query)
                    else:
                        attribute_id = [attr['id'] for attr in attributes if attr['name'] == attr_req['attr_name']][0]
                        insert_query = "INSERT INTO race_attribute_requirements (id, race_id, attribute_id, min, max, modifier) VALUES (UUID(), '%s', '%s', %d, %s, %s)" % (race['id'], attribute_id, attr_req['min'], attr_req['max'], attr_req['modifier'])
                        db_cursor.execute(insert_query)
                        db_cursor.execute("SELECT id FROM race_attribute_requirements WHERE race_id = '%s' AND attribute_id = '%s'" % (race['id'], attribute_id))
                        result = db_cursor.fetchone()
                        attr_req['id'] = result['id']

                for class_req in race['class_requirements']:
                    allowed = "TRUE" if class_req['allowed'] else "FALSE"
                    max_level = class_req['max_level']
                    if class_req['id']:
                        update_query = "UPDATE race_class_requirements SET allowed = %s, max_level = %s WHERE id = '%s'" % (allowed, max_level, class_req['id'])
                        db_cursor.execute(update_query)
                    else:
                        class_id = [cls['id'] for cls in classes if cls['name'] == class_req['cls_name']][0]
                        insert_query = "INSERT INTO race_class_requirements (id, race_id, class_id, allowed, max_level) VALUES (UUID(), '%s', '%s', %s, %s)" % (race['id'], class_id, allowed, max_level)
                        db_cursor.execute(insert_query)
                        db_cursor.execute("SELECT id FROM race_class_requirements WHERE race_id = '%s' AND class_id = '%s'" % (race['id'], class_id))
                        result = db_cursor.fetchone()
                        class_req['id'] = result['id']

    return simplejson.dumps({"success": "true", "races": races, "classes": classes, "attributes": attributes, "alignments": alignments})

def retrieve_world_list(json_data):
    # try to sign on with the given credentials
    json_dict = simplejson.loads(json_data)
    username = MySQLdb.escape_string(json_dict['username'])

    with connection:
        db_cursor.execute("SELECT * FROM worlds WHERE master_username = '%s'" % (username))
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
