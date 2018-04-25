# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, os

class TestSongView(unittest.TestCase):
    def setUp(self):
        try:
            self.browser = webdriver.Firefox()
        except WebDriverException:
            self.browser = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:8000/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_song_view(self):
        """Test first song on list can be viewed"""
        driver = self.driver
        driver.get(self.base_url)
        song_xpath = "/html/body/div[1]/div/div[2]/div[1]/h4/a"
        song = driver.find_element_by_xpath(song_xpath)
        song_name = song.text
        song.click()
        self.assertTrue(driver.title, "ChoralCentral | " + song_name)
    
    def test_login_and_upload_view(self):
        driver = self.driver
        driver.get(self.base_url)

        window_before = driver.window_handles[0]

        driver.find_element_by_id("djHideToolBarButton").click() # hide django debug toolbar

        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id_username").send_keys("admin@choralcentral.net")
        driver.find_element_by_id("id_password").send_keys("dwarfstar")
        driver.find_element_by_xpath("//button[@value='login']").click()

        driver.find_element_by_link_text("UPLOAD").click()
        driver.find_element_by_id("id_publish").click()
        driver.find_element_by_id("id_title").send_keys("Naranum Rie latest")
        driver.find_element_by_id("id_lyrics").send_keys("Umu Chineke, Naranum rie, nri di nso nri oma")
        driver.find_element_by_id("id_first_line").send_keys("Umu Chineke")
        driver.find_element_by_id("id_scripture_reference").send_keys("John 6")
        Select(driver.find_element_by_id("id_language")).select_by_visible_text("igbo")
        driver.find_element_by_id("id_tempo").send_keys("100")
        driver.find_element_by_id("id_bpm").send_keys("4")
        driver.find_element_by_id("id_divisions").send_keys("4")
        Select(driver.find_element_by_id("id_voicing")).select_by_visible_text("SATB")
        # Select(driver.find_element_by_id("id_authors")).select_by_visible_text("Jude Nnam")

        # create new author
        driver.find_element_by_xpath("(//img[@alt='Add'])[3]").click()
        window_after = driver.window_handles[1]

        first_name = "Some name234"
        last_name = "Some other name"
        fullname = "{} {}".format(first_name, last_name)

        driver.switch_to.window(window_after)
        driver.find_element_by_id("id_last_name").send_keys(last_name)
        driver.find_element_by_id("id_first_name").send_keys(first_name)
        driver.find_element_by_xpath("//button[@value='Save']").click()

        driver.switch_to.window(window_before)

        Select(driver.find_element_by_id("id_authors")).select_by_visible_text(fullname)

        driver.find_element_by_xpath("(//option[@value='1'])[4]").click()
        driver.find_element_by_xpath("(//option[@value='6'])[4]").click()
        driver.find_element_by_xpath("(//option[@value='6'])[5]").click()
        driver.find_element_by_xpath("//button[@value='Save']").click()

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    os.system('cls')
    unittest.main()
