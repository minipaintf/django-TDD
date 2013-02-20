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

        # TODO: use the admin site to create a Poll
        self.fail('finish this test')

        
