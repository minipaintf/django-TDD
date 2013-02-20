"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import timezone
from polls.models import Poll

class PollModelTest(TestCase):
    """
    test for polls app admin
    """
    
    def test_creating_a_new_poll_and_saving_it_to_the_database(self):
        poll = Poll()
        poll.question = "what's up?"
        poll.pub_date = timezone.now()

        # check we can save ite to the database
        poll.save()
        
        # now check we can find it in the database again
        all_polls_in_database = Poll.objects.all()
        self.assertEquals(len(all_polls_in_database), 1)
        only_poll_in_database = all_polls_in_database[0]
        self.assertEquals(only_poll_in_database, poll)
        
        # and check that it's saved its two attributes: question and
        # pub_date
        self.assertEquals(only_poll_in_database.question, "what's up?")
        self.assertEquals(only_poll_in_database.pub_date, poll.pub_date)
        
