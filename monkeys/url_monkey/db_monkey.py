import sqlite3


class DatabaseMonkey:
    """
    A monkey thats gonna create a database based on the collected urls from the url-monkey
    """

    def __init__(self, name):
        """ Init the db-monkey with the db-name """

        # database name
        self.name = name
        # create the database
        self.__create_db()
        # attached url-monkey
        self.url_monkey = None

    def __create_db(self):
        """ Create a url-database """

        # connect to database
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()

        # create the table 'url' if it doesn't exist
        # id is to keep track in which order the urls were found
        # url is simply the url that was found
        # came_from_tree is the url under which the above mentioned url was found
        cursor.execute(
            'create table if not exists urls (id integer primary key, url text, came_from_tree text)'
        )
        conn.commit()
        conn.close()

    def attach_to_urlmonkey(self, url_monkey=None):
        """ Attach to a url-monkey to gain access to its url-list """

        if url_monkey is None:
            print("You have to provide a valid url-monkey.")
            return

        self.url_monkey = url_monkey

    def parse_urllist(self):
        """ Parse the urls from the url-monkey list into the database """

        conn = None

        try:
            # connect to database
            conn = sqlite3.connect(self.name)
            cursor = conn.cursor()

            # read every url from the url-monkey's list and insert it into the table
            for idx, tree in enumerate(self.url_monkey.trees_and_branches):
                cursor.execute(
                    'insert or ignore into urls(id, url, came_from_tree) values (?,?,?)',
                    (
                        idx,
                        tree[0],
                        tree[1],
                    ))
            # commit the changes
            conn.commit()
        finally:
            if conn is not None:
                conn.close()
