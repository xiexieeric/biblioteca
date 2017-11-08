import unittest
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)
        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source


    def tearDown(self):
        self.driver.close()


# 1. Home Page Test Case
class test_home_page(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def test_front_page(self):
        browser = self.browser
        browser.get('127.0.0.1:8001/api/v1/')
        assert "Welcome to the index page for API v1" in browser.page_source

    def tearDown(self):
        self.browser.close()


# 2. Book Detail Page Test Case

class test_book_detail(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def test_product_detail(self):
        browser = self.browser
        browser.get('http://104.236.231.206:8000/')
        self.product = browser.find_element_by_tag_name("td")
        self.product.click()
        assert "Product not found." not in browser.page_source

    def tearDown(self):
        self.browser.close()
        

# 2. Author Detail Page Test Case

class test_author_detail(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def test_product_detail(self):
        browser = self.browser
        browser.get('http://104.236.231.206:8000/')
        self.product = browser.find_element_by_tag_name("td")
        self.product.click()
        assert "Product not found." not in browser.page_source

    def tearDown(self):
        self.browser.close()

# 4. Review Detail Page Test Case

class test_review_detail(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def test_product_detail(self):
        browser = self.browser
        browser.get('http://104.236.231.206:8000/')
        self.product = browser.find_element_by_tag_name("td")
        self.product.click()
        assert "Product not found." not in browser.page_source

    def tearDown(self):
        self.browser.close()


# 5. Listing Detail Page Test Case

class test_listing_detail(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def test_product_detail(self):
        browser = self.browser
        browser.get('http://104.236.231.206:8000/')
        self.product = browser.find_element_by_tag_name("td")
        self.product.click()
        assert "Product not found." not in browser.page_source

    def tearDown(self):
        self.browser.close()



class SignUpTestCase(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def test_sign_up(self):
        browser = self.browser
        browser.get('http://104.236.231.206:8000/signup')
        assert "Sign Up" in browser.page_source

    def tearDown(self):
        self.browser.close()

# search page
class SearchPageTestCase(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def test_search(self):
        browser = self.browser
        browser.get('http://104.236.231.206:8000/search')
        q = browser.find_element_by_id("id_query")
        q.send_keys("Wool")
        search_button = browser.find_element_by_id("searchSubmit")
        search_button.click()
        assert "RF Wool Pants" in browser.page_source

    def tearDown(self):
        self.browser.close()

# test creating an account
class CreateAccountTestCase(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def test_create_account(self):
        browser = self.browser
        browser.get('http://104.236.231.206:8000/signup')
        form_elements = browser.find_elements_by_tag_name("input")
        for field in form_elements:
            if field == "Username":
                field.send_keys("max")
            if field == "Password":
                field.send_keys("nicepass")
            if field == "Fname":
                field.send_keys("Maxwell")
            if field == "Lname":
                field.send_keys("Luo")
            if field == "email":
                field.send_keys("ml3ha@virginia.edu")
            if field == "location":
                field.send_keys("Charlottesville")
        submit = browser.find_element_by_id("signupSubmit")
        submit.click()
        # should redirect to login page
        assert "Login" in browser.page_source

    def tearDown(self):
        self.browser.close()







if __name__ == "__main__":
    unittest.main()