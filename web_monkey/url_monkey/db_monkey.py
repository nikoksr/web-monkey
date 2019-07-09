''' imports '''
import sqlite3


class DatabaseMonkey():
    '''
    A monkey thats gonna create a sqlite database based on the collected
    urls from the url-monkey.
    '''

    def __init__(self, name):
        ''' Init the db-monkey with the db-name '''

        # Database name
        self.name = name
        # Create the database
        self.create_db()
        # Attached url-monkey
        self.url_monkey = None

    def create_db(self):
        ''' Create a url-database '''

        # Connect to database and create cursor.
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()

        # Create the table 'url' if it doesn't exist.
        # id is to keep track in which order the urls were found.
        # url is simply the url that was found.
        # came_from_tree is the url under which the above mentioned url
        # was found.
        cursor.execute(
            '''create table if not exists urls (id integer primary key,
            url text, origin text)''')
        conn.commit()
        conn.close()

    def attach_to_urlmonkey(self, url_monkey=None):
        ''' Attach to a url-monkey to gain access to its url-list '''

        if url_monkey is None:
            print('You have to provide a valid url-monkey.')
            return

        self.url_monkey = url_monkey

    def parse_urllist(self):
        ''' Parse the urls from the url-monkey list into the database '''

        try:
            # Connect to database
            conn = sqlite3.connect(self.name)
            cursor = conn.cursor()

            # Read every url from the url-monkey's list and insert it
            # into the table.
            for idx, tree in enumerate(self.url_monkey.trees_and_branches):
                cursor.execute(
                    '''insert or ignore into urls(id, url, origin)
                    values (?,?,?)''', (
                        idx,
                        tree[0],
                        tree[1],
                    ))
            # Commit the changes
            conn.commit()
        finally:
            if conn is not None:
                conn.close()
