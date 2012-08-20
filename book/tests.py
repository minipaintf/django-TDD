"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import MySQLdb

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class ConnectTest(TestCase):
    def mysqlConnect(self):
        if db = MySQLdb.connect(user='root', db='start', passwd='secret', host='localhost'):
            self.assertEqual(1 + 1, 2)
        else:
            self.assertEqual(1 + 1, 1)
        #cursor = db.cursor()
        #curser.execute('select name from books order by name')
        #names = [row[0] for row in cursor.fetchall()]
        #db.close()
        
