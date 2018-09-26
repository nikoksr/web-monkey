""" imports """
import sqlite3


class DatabaseMonkey():
    """
    A monkey thats gonna create a database based on the collected urls from the url-monkey
    """

    def __init__(self, name):
        """ Init the db-monkey with the db-name """
        self.name = name
        self.__create_db()
        self.url_monkey = None

    def __create_db(self):
        """ Create a url-database """

        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()

        cursor.execute('create table if not exists urls (url text)')
        conn.commit()
        conn.close()

    def attach_to_urlmonkey(self, url_monkey=None):
        """ Attach to a url-monkey to gain access to its url-list """

        if (url_monkey is None):
            print("You have to provide a valid url-monkey.")
            return

        self.url_monkey = url_monkey

    def parse_urllist(self):
        """ Parse the urls from the url-monkey list into the database """

        try:
            conn = sqlite3.connect(self.name)
            cursor = conn.cursor()

            for url in self.url_monkey.trees_and_branches:
                cursor.execute('insert or ignore into urls(url) values (?)',
                               (url, ))
                conn.commit()
        finally:
            if (conn is not None):
                conn.close()
