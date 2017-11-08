import unittest
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# 1. Home Page Test Case
class HomePageTestCase(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome('./chromedriver')

    def test_home_page(self):
        browser = self.browser
        browser.get('http://127.0.0.1:8000')
        assert "Biblioteca" in browser.page_source
        assert "Current Listings" in browser.page_source

    def tearDown(self):
        self.browser.close()


# 2. Book Detail Page Test Case
class BookDetailTestCase(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome('./chromedriver')

    def test_book_detail(self):
        browser = self.browser
        browser.get('http://127.0.0.1:8000/')
        book = browser.find_element_by_tag_name("a")
        book.click()
        assert "What you were looking for could not be found, sorry!" not in browser.page_source

    def tearDown(self):
        self.browser.close()


# 3. Sign Up Page Test Case
class SignUpPageTestCase(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome('./chromedriver')

    def test_sign_up_page(self):
        browser = self.browser
        browser.get('http://127.0.0.1:8000/signup')
        assert "First Name:" in browser.page_source
        assert "Last Name:" in browser.page_source
        assert "Username:" in browser.page_source
        assert "Password:" in browser.page_source

    def tearDown(self):
        self.browser.close()


# 4. Create Account Test Case
class CreateAccountTestCase(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome('./chromedriver')

    def test_create_account(self):
        browser = self.browser
        browser.get('http://127.0.0.1:8000/signup/')
        input_fname = browser.find_element_by_name("fname")
        input_fname.send_keys("Jennifer")
        input_lname = browser.find_element_by_name("lname")
        input_lname.send_keys("Fang")
        input_username = browser.find_element_by_name("username")
        input_username.send_keys("jennifer")
        input_password = browser.find_element_by_name("password")
        input_password.send_keys("fang")
        elem = browser.find_element_by_name("signup_submit")
        elem.send_keys(Keys.RETURN)

        # Should show username already exists
        assert "username already exists" in browser.page_source

    def tearDown(self):
        self.browser.close()


# 5. Login and Create Listing Test Case
class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome('./chromedriver')

    def test_login_and_create_listing(self):
        browser = self.browser
        browser.get('http://127.0.0.1:8000/login/')
        input_username = browser.find_element_by_name("username")
        input_username.send_keys("jennifer")
        input_password = browser.find_element_by_name("password")
        input_password.send_keys("fang")

        elem = browser.find_element_by_name("login_submit")
        elem.send_keys(Keys.RETURN)

        # Should show a Log Out button
        assert "Log Out" in browser.page_source

        browser.get('http://127.0.0.1:8000/create/book/')

        input_book = browser.find_element_by_name("book")
        input_book.send_keys("1")
        input_price = browser.find_element_by_name("price")
        input_price.send_keys("10.00")
        elem = browser.find_element_by_name("listing_submit")
        elem.send_keys(Keys.RETURN)

        # Should show a success message
        assert "Listing created successfully!" in browser.page_source

    def tearDown(self):
        self.browser.close()


# 6. Search Page Test Case
class SearchPageTestCase(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome('./chromedriver')

    def test_search(self):
        browser = self.browser

        # login and create a listing first 
        LoginTestCase.test_login_and_create_listing(self)

        browser.get('http://127.0.0.1:8000/search/')
        query = browser.find_element_by_name("search_text")
        query.send_keys("Green")
        search_button = browser.find_element_by_name("search_submit")
        search_button.click()
        assert "Green Eggs and Ham" in browser.page_source

    def tearDown(self):
        self.browser.close()



if __name__ == "__main__":
    unittest.main()