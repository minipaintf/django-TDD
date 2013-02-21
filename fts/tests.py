"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class PollsTest(LiveServerTestCase):
    """
    django admin test
    """
    # init data for admin user login
    fixtures = ['admin_user.json']
    
    def setUp(self):
        self.browser = webdriver.Chrome()
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
        body = self.browser.find_elements_by_link_text('body')
        self.assertIn('o polls', body.text)
        
        # she sees a link to 'add' a new poll, so she clicks it
        new_poll_link = self.browser.find_elements_by_link_text('Add poll')
        new_poll_link.click()
        
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Question:', body.text)
        self.assertIn('Date pulished:', body.text)
        
        # she types in an interesting question for the Poll
        question_field = self.browser.find_element_by_name('question')
        question_field.send_keys("How awsome is Test-Driven Development?")
        
        # she sets the date and time of publication - it'll be a new
        # year's poll!
        date_field = self.browser.find_element_by_name('pub_date_0')
        date_field.send_keys('01/01/12')
        time_field = self.browser.find_element_by_name('pub_date_1')
        time_field.send_keys('00:00')
        
        # Gertrude clicks the save button
        save_button = self.browser.find_element_by_css_selector("input[value='Save']")
        save_button.click()
        
        # she is returned to the "Polls" listing, where she can see
        # her new poll, listed as a clickable link
        new_poll_links = self.browser.find_elements_by_link_text("How awesome is Test-Driven Development?")
        self.assertEquals(len(new_poll_links), 1)
        
        # Satisfied, she goes back to sleep
        # TODO: use the admin site to create a Poll
        # self.fail('finish this test')


                
        
