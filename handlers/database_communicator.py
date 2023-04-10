import sqlite3 as sq
import uuid

class DatabaseCommunicator:
    def sql_start():
        global base, cur
        base = sq.connect("database.db")
        cur = base.cursor()
        base.execute("CREATE TABLE IF NOT EXISTS content(content_id INT PRIMARY_KEY, user_id INT, source_type TEXT, "
                     "source_link TEXT, post_link TEXT, text TEXT, datetime DATETIME)")
        base.execute("CREATE TABLE IF NOT EXISTS channels(user_id INT PRIMARY_KEY, channel_name TEXT, channel_id TEXT)")
        base.execute("CREATE TABLE IF NOT EXISTS messages(content_id INT PRIMARY_KEY, message_id INT, user_id INT)")
        base.execute("CREATE TABLE IF NOT EXISTS sources(source_id INT PRIMARY_KEY, source_link TEXT, source_type TEXT,"
                     "user_id INT)")
        base.commit()

    async def sql_add_content(post_object):
        already_in_table = cur.execute('SELECT * FROM content WHERE user_id = (?) AND post_link = (?)',
                                       [post_object[1], post_object[4]]).fetchall()
        if len(already_in_table) == 0:
            cur.execute('INSERT INTO content VALUES (?, ?, ?, ?, ?, ?, ?)', post_object)
            base.commit()

    async def sql_add_channel(user, channel_name, channel_id):
        cur.execute('INSERT INTO channels VALUES (?, ?, ?)', [user, channel_name, channel_id])
        base.commit()

    async def sql_add_message(content_id, message_id, user_id):
        cur.execute('INSERT INTO messages VALUES (?, ?, ?)', [content_id, message_id, user_id])
        base.commit()

    async def sql_add_source(user, source_link, source_type):
        source_id = str(uuid.uuid4()).replace('-', '')
        cur.execute('INSERT INTO sources VALUES (?, ?, ?, ?)', [source_id, source_link, source_type, user])
        base.commit()

    def sql_read_content(user_id):
        return cur.execute('SELECT * FROM content WHERE user_id = (?)', [user_id]).fetchall()

    def sql_read_channel(user_id):
        return cur.execute('SELECT * FROM channels WHERE user_id = (?)', [user_id]).fetchall()

    def sql_read_source(user_id):
        return cur.execute('SELECT * FROM sources WHERE user_id = (?)', [user_id]).fetchall()

    def sql_read_messages(user_id, message_id):
        return cur.execute('SELECT * FROM messages WHERE user_id = (?) AND message_id = (?)',
                           [user_id, message_id]).fetchall()

    def sql_delete_content(user_id, content_id):
        cur.execute(f'DELETE FROM content WHERE user_id = (?) AND content_id = (?)', [user_id, content_id])
        base.commit()

    def sql_delete_channel(user_id):
        cur.execute('DELETE FROM channels WHERE user_id = (?)', [user_id])
        base.commit()

    def sql_delete_message(user_id, message_id):
        content = DatabaseCommunicator.sql_read_messages(user_id, message_id)
        if len(content) > 0:
            DatabaseCommunicator.sql_delete_content(user_id, content[0][0])
            cur.execute(f'DELETE FROM messages WHERE user_id = (?) AND message_id = (?)', [user_id, message_id])
            base.commit()

    def sql_delete_source(user_id, source_link):
        cur.execute(f'DELETE FROM content WHERE user_id = (?) AND source_link = (?)', [user_id, source_link])
        cur.execute(f'DELETE FROM sources WHERE user_id = (?) AND source_link = (?)', [user_id, source_link])
        base.commit()

