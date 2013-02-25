"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import timezone
from polls.models import Poll,Choice
from django.core.urlresolvers import reverse
from polls.forms import PollVoteForm

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

        # now create a Choice object
        choice = Choice()
        
        # link it with our Poll
        choice.poll = poll
        
        # give it some text
        choice.choice = "doin' fine..."
        
        # and let's say it's had some votes
        choice.votes = 3

        # save it
        choice.save()
        
        # try retrieving it from the database, using the poll
        # object's reverse lookup
        poll_choices = poll.choice_set.all()
        self.assertEquals(poll_choices.count(), 1)
        
        # finally, check its attributes have been saved
        choice_from_db = poll_choices[0]
        self.assertEquals(choice_from_db, choice)
        self.assertEquals(choice_from_db.choice, "doin' fine...")
        self.assertEquals(choice_from_db.votes, 3)
        
        
        # now check we can find it in the database again
        all_polls_in_database = Poll.objects.all()
        self.assertEquals(len(all_polls_in_database), 1)
        only_poll_in_database = all_polls_in_database[0]
        self.assertEquals(only_poll_in_database, poll)
        
        # and check that it's saved its two attributes: question and
        # pub_date
        self.assertEquals(only_poll_in_database.question, "what's up?")
        self.assertEquals(only_poll_in_database.pub_date, poll.pub_date)
        
    def test_verbose_name_for_pub_date(self):
        for field in Poll._meta.fields:
            if field.name == 'pub_date':
                self.assertEquals(field.verbose_name, 'Date published')

    def test_poll_objects_are_named_after_their_question(self):
        p = Poll()
        p.question = "How is babby formed?"
        self.assertEquals(unicode(p), unicode('How is babby formed?'))
    
    def test_choice_defaults(self):
        choice = Choice()
        self.assertEquals(choice.votes, 0)
        

    def test_choice_can_calculate_ite_own_percentage_of_votes(self):
        poll1 = Poll(question="who?", pub_date=timezone.now())
        poll1.save()
        choice1 = Choice(poll=poll1, choice="me", votes=2)
        choice1.save()
        choice2 = Choice(poll=poll1, choice='you', votes=1)
        choice2.save()
        
        self.assertEquals(choice1.percentage(), 100 * 2 / 3)
        self.assertEquals(choice2.percentage(), 100 * 1 / 3)
        
        # also check 0-votes case
        choice1.votes = 0
        choice1.save()
        choice2.votes = 0
        choice2.save()
        
        self.assertEquals(choice1.percentage(), 0)
        self.assertEquals(choice2.percentage(), 0)
        
    def test_poll_can_tell_you_its_total_number_of_votes(self):
        p = Poll(question='where', pub_date=timezone.now())
        p.save()
        c1 = Choice(poll=p, choice="here", votes=0)
        c1.save()
        c2 = Choice(poll=p, choice="there", votes=0)
        c2.save()
        
        self.assertEquals(p.total_votes(), 0)
        
        c1.votes = 1000
        c1.save()
        c2.votes = 22
        c2.save()
        self.assertEquals(p.total_votes(), 1022)
