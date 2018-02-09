"""User story
python manage.py test test_inte

https://docs.djangoproject.com/en/1.11/topics/testing/overview/#the-test-database
"""
# pylint: disable=W0611

import os
from random import choices
from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from py_webber import LoremPysum
from siteuser.models import Role
from utils import fast_multiselect

class UsageTest(LiveServerTestCase):
    """This test spawns its own server.
    No need to have local server running while
    running this test."""

    fixtures = ['fixtures/users.json', 'fixtures/roles.json', 'fixtures/profiles.json']

    # @classmethod
    # def setUpClass(cls):
    #     # os.system('cls')
    #     try:
    #         cls.browser = webdriver.Firefox()
    #     except WebDriverException:
    #         cls.browser = webdriver.Chrome()
    #     super(UsageTest, cls).setUpClass()

    # @classmethod
    # def tearDownClass(cls):
    #     cls.browser.quit()
    #     super(UsageTest, cls).tearDownClass()

    def setUp(self):
        try:
            self.browser = webdriver.Firefox()
        except WebDriverException:
            self.browser = webdriver.Chrome()

        self.address = "{}{}".format(self.live_server_url, "/chinemerem/")
        self.browser.get(self.address)

    def tearDown(self):
        self.browser.quit()

    def test_can_access_home_page(self):
        """Test Home page loads"""
        print("\ntest_can_access_home_page")
        self.assertEqual(self.browser.title, "Chinemerem » Tonic Solfa lives here")

    def test_can_register_new_profile(self):
        """Test can register new profile"""
        print("\ntest_can_register_new_profile")
        tex = LoremPysum()
        email = tex.email()
        screen_name = tex.word()
        password = tex.word() + tex.word()

        self.browser.find_element_by_link_text("Join").click()
        self.browser.find_element_by_id("id_email").send_keys(email)
        self.browser.find_element_by_id("id_screen_name").send_keys(screen_name)
        self.browser.find_element_by_id("id_password1").send_keys(password)
        self.browser.find_element_by_id("id_password2").send_keys(password)
        self.browser.find_element_by_xpath("//input[@type='submit']").click()

        WebDriverWait(self.browser, 60).until(EC.title_contains("Welcome"))
        self.assertEqual(self.browser.title, "Chinemerem » Welcome {} !!!".format(screen_name))
        print(self.browser.title)
        self.assertEqual(self.browser.find_element_by_css_selector(".section-heading").text, "Welcome {} !!!".format(screen_name))

    def test_can_create_account_and_edit_profile(self):
        """Test can register new profile, login and edit profile"""
        print("\ntest_can_create_account_and_edit_profile")
        tex = LoremPysum()
        email = tex.email()
        username = tex.word()
        password = tex.word() + tex.word()

        # create account
        self.browser.find_element_by_link_text("Join").click()
        self.browser.find_element_by_id("id_email").send_keys(email)
        self.browser.find_element_by_id("id_screen_name").send_keys(username)
        self.browser.find_element_by_id("id_password1").send_keys(password)
        self.browser.find_element_by_id("id_password2").send_keys(password)
        self.browser.find_element_by_xpath("//input[@type='submit']").click()

        self.browser.implicitly_wait(150)

        # fill out success form
        self.browser.find_element_by_id("id_first_name").send_keys(tex.word())
        self.browser.find_element_by_id("id_last_name").send_keys(tex.word())
        self.browser.find_element_by_id("id_location").send_keys(tex.word())
        fast_multiselect(self.browser, "id_roles", labels=[])
        self.browser.find_element_by_xpath("//input[@type='submit']").click()

        # WebDriverWait(self.browser, 60).until(EC.title_contains("Welcome"))
        self.assertEqual(self.browser.title, "Chinemerem » {}'s profile".format(username))

    def test_can_login_and_upload_song(self):
        print("\ntest_can_login_and_upload_song")
        """Test can login and upload song"""

        dropdown = self.browser.find_element_by_xpath("//a[@id='UploadDrawer']")
        dropdown.click()
        self.browser.implicitly_wait(150)

        newsong = dropdown.find_element_by_xpath("//div[@id='DropdownMenu']/a[@id='UploadSong']")
        newsong.click()
        self.browser.implicitly_wait(150)

        # login
        self.browser.find_element_by_id("id_username").send_keys("admin@choralcentral.com")
        self.browser.find_element_by_id("id_password").send_keys("dwarfstar")
        self.browser.find_element_by_xpath("//input[@type='submit']").click()

        self.browser.implicitly_wait(150)
        self.assertEqual(self.browser.title, "Chinemerem » Create Song")

if "__name__" == "__main__":
    pass
