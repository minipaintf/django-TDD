"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from collections import namedtuple
import time


PollInfo = namedtuple('PollInfo', ['question', 'choices'])
POLL1 = PollInfo(
    question = "How awesome is Test-Driven Development?",
    choices = [
        'Very awesome',
        'Quite awesome',
        'Moderately awesome',
        ],
    )
POLL2 = PollInfo(
    question = "Which workshop treat do you prefer?",
    choices = [
        'Beer',
        'Pizza',
        'The Acquisition of Knowledge',
        ],
    )


class PollsTest(LiveServerTestCase):
    """
    django admin test
    """
    # init data for admin user login
    fixtures = ['admin_user.json']
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        
    def tearDown(self):
        self.browser.quit()

    def test_can_create_new_poll_via_admin_site(self):
        # gertrude opens her web browser, and goes to the admin page
        self.browser.get(self.live_server_url + '/admin/')
        
        # She sees the familiar 'Django administration' heading
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)
        
        # she types in her username and passwords and hits return
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('daipeng')
        
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('dp123456')
        password_field.send_keys(Keys.RETURN)

        # she password are accepted , and she is taken to the Site
        # Administration Page
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)
        
        # she now see a couple of hyperlink that says "Poll"
        polls_links = self.browser.find_elements_by_link_text('Polls')
        self.assertEquals(len(polls_links), 2)

        # The second one looks more exciting, so she clicks it
        polls_links[1].click()
        # she is taken to the polls listing page, which shows she has
        # no polls yes
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('0 polls', body.text)
        
        # she sees a link to 'add' a new poll, so she clicks it
        new_poll_link = self.browser.find_elements_by_link_text('Add poll')
        new_poll_link[0].click()
        
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Question:', body.text)
        self.assertIn('Date published', body.text)
        
        # she types in an interesting question for the Poll
        question_field = self.browser.find_element_by_name('question')
        question_field.send_keys("How awsome is Test-Driven Development?")
        
        # she sets the date and time of publication - it'll be a new
        # year's poll!
        date_field = self.browser.find_element_by_name('pub_date_0')
        date_field.send_keys('01/01/12')
        time_field = self.browser.find_element_by_name('pub_date_1')
        time_field.send_keys('00:00')
        
        # She sees she can enter choices for the Poll. she adds three
        choice_1 = self.browser.find_element_by_name('choice_set-0-choice')
        choice_1.send_keys('Very awesome')
        choice_2 = self.browser.find_element_by_name('choice_set-1-choice')
        choice_2.send_keys('Quite awesome')
        choice_3 = self.browser.find_element_by_name('choice_set-2-choice')
        choice_3.send_keys('Moderately awesome')

        # Gertrude clicks the save button
        save_button = self.browser.find_element_by_css_selector("input[value='Save']")
        save_button.click()
        
        # she is returned to the "Polls" listing, where she can see
        # her new poll, listed as a clickable link
        new_poll_links = self.browser.find_elements_by_link_text("How awsome is Test-Driven Development?")
        # new_poll_links = self.browser.find_elements_by_link_text("Poll object")
        self.assertEquals(len(new_poll_links), 1)
        
        # Satisfied, she goes back to sleep
        # TODO: use the admin site to create a Poll
        # self.fail('finish this test')

    def _setup_polls_via_admin(self):
        # Gertrude logs into the admin site
        self.browser.get(self.live_server_url + '/admin/')
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('daipeng')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('dp123456')
        password_field.send_keys(Keys.RETURN)
        
        # She has a number of polls to enter. For each one, she:
        for poll_info in [POLL1, POLL2]:
            # Follows the link to the Polls app, and adds a new poll
            self.browser.find_elements_by_link_text('Polls')[1].click()
            self.browser.find_elements_by_link_text('Add poll')[0].click()
            # enters its name, and uses the today and now buttons to set
            # the publish date
            question_field = self.browser.find_element_by_name('question')
            question_field.send_keys(poll_info.question)
            self.browser.find_elements_by_link_text('Today')[0].click()
            self.browser.find_elements_by_link_text('Now')[0].click()
            
            # Sees she can enter choices for the Poll on this same page
            # so she does
            for i, choice_text in enumerate(poll_info.choices):
                choice_field = self.browser.find_element_by_name('choice_set-%d-choice' %i)
                choice_field.send_keys(choice_text)
                
            # save her new Poll
            save_button = self.browser.find_element_by_css_selector("input[value='Save']")
            save_button.click()
            
            # Is returned to the Polls listing, where she can see her
            # new poll, listed as a clickable link by its name
            new_poll_links = self.browser.find_elements_by_link_text(poll_info.question)
            self.assertEquals(len(new_poll_links), 1)
            
            # she goes back to the root of the admin site
            self.browser.get(self.live_server_url + '/admin/')
            
        # She logs out of the admin site
        self.browser.find_elements_by_link_text('Log out')[0].click()
        
        
    def test_voting_on_a_new_poll(self):
        # First, Gertrude the administrator logs into the admin site
        # and creates a couple of new Polls, and their response choices
        self._setup_polls_via_admin()
        
        # now, Herbert the regular user goes to the homepage of the site. He
        # see a list of polls.
        self.browser.get(self.live_server_url)
        heading = self.browser.find_element_by_tag_name('h1')
        self.assertEquals(heading.text, 'Polls')
        
        # He clicks on the link to the first Poll, which is called
        # 'How awesome is test-driven development?'
        first_poll_title = POLL1.question
        self.browser.find_element_by_link_text(first_poll_title).click()
        
        # He is taken to a poll 'result' page, which says
        # "no-one has voted on this poll yet"
        main_heading = self.browser.find_element_by_tag_name('h1')
        self.assertEquals(main_heading.text, 'Poll Results')
        sub_heading = self.browser.find_element_by_tag_name('h2')
        self.assertEquals(sub_heading.text, first_poll_title)
        body = self.browser.find_elements_by_tag_name('body')[0]
        self.assertIn('No-one has voted on this poll yet', body.text)
    
        # He also sees a form, which offers him several choices
        # He desided to select "very awesome"
        choice_inputs = self.browser.find_elements_by_css_selector('input[type="radio"]')
        #self.assertEquals(len(choice_inputs), 3)
        
        # the buttons have labels to explain then
        choice_labels = self.browser.find_elements_by_tag_name('label')
        choices_text = [c.text for c in choice_labels]
        self.assertEquals(choices_text, [
                'Vote:', # this label is auto-generated for the whole form
                'Very awesome',
                'Quite awesome',
                'Moderately awesome',
                ])
        # He decided to select "very awesome", which is answer #1
        chosen = self.browser.find_element_by_css_selector("input[value='1']")
        chosen.click()
        
                   
        # He clicks "submit"
        self.browser.find_element_by_css_selector('input[type="submit"]').click()
        
        # the page refreshes, and he sees that his choice
        # has updated the results. they now say
        # "100 % : very awesome"
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('100 %: Very awesome', body_text)
        
        # the page also says "1 vote"
        self.assertIn('1 vote', body_text)
        
        # but not "1 votes" -- Herbert is impressed at the attention
        # to detail
        self.assertNotIn('1 votes', body_text)
        
        # Herbert suspects that the website isn't very well
        # against people submitting multiple votes yet, so he tries
        # to do a little astrotrufing
        self.browser.find_element_by_css_selector('input[value="1"]').click()
        self.browser.find_element_by_css_selector('input[type="submit"]').click()
        
        # the page refreshes, and she sees that his choice has updated
        # the results. it still says # "100%: very awesome".
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn("2 votes", body_text)
        
        # cacking manically over his l33t haxx0ring skills, he
        # voting for a different choice
        self.browser.find_element_by_css_selector('input[value="2"]').click()
        self.browser.find_element_by_css_selector('input[type="submit"]').click()
        
        # now, the percentages update, as well as the votes
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('66 %: Very awesome', body_text)
        self.assertIn('33 %: Quite awesome', body_text)
        self.assertIn('3 votes', body_text)
                                                  
        # Satisfied, he goes back to sleep
        #self.fail('TODO')

