from seleniumbase import BaseCase
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os
import logging


CLIENT_NAME = "Lamdi"
ACCOUNT_NAME_TO_SEARCH = "Cash Checking"
NUMBER_TO_SEARCH = "1010000"
COLUMN_ARK_TRANSACTION_FILTER = "column-header-filter-2"
COLUMN_ATTRIBUTE_FILTER = "column-header-filter-3"
COLUMN_COLUMN_FINANCIAL_STATEMENT_FILTER = "column-header-filter-7"
COLUMN_STATUS_FILTER = "column-header-filter-9"
ARK_TRANSACTION_FILTER_VALUE = "General Expense"


class TestWebPageLogin(BaseCase):
    """
    A test case for logging into a web page and performing various actions.

    This test case inherits from the `BaseCase` class and includes methods to perform login,
    interact with elements on the page, and wait for elements to be visible.

    Attributes:
        None

    Methods:
        setUpClass: A class method that loads the environment variables.
        test_login: A method that performs the login process
    """

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        logging.basicConfig(filename="example.log", filemode="w", level=logging.DEBUG)
        logging.basicConfig(
            format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG
        )

    def test_login(self):
        # Open the web page
        logging.debug("Start Login Test")
        try:
            self.open(os.getenv("BASE_URL"))
            self.type('input[name="email"]', os.getenv("USERNAME_TEST"))
            self.type('input[name="password"]', os.getenv("PASSWORD_TEST"))
            self.click('button[type="submit"]')
            self.wait(2)
        except Exception as e:
            logging.error(f"Error on Login: {e}")
            self.fail(f"Error: {e}")

    def test_search(self):
        self.test_login()

        # Click on the "Clients" menu option
      
        autocomplete_input_xpath = "//input[@id='selector-client']"
        option_with_value_xpath = (
            f"//ul[@role='listbox']//li[contains(text(), '{CLIENT_NAME}')]"
        )
        logging.debug("Start Set Value Test on Dropdown")
        self.type(autocomplete_input_xpath, CLIENT_NAME)
        self.click(option_with_value_xpath)
        self.wait(2)
        self.click("#expand_collapse_sidebar")
        self.click("#funds_menu_option")
        self.wait(2)

        # Click on the "De Buyer" fund
        span_de_buyer = self.wait_for_element_visible("//span[text()='De Buyer']")
        span_de_buyer.click()
        self.assert_element_visible("button#general_ledger")
        button = self.find_element("button#general_ledger")
        button.click()
        self.wait_for_element_visible("ul.MuiList-root")
        self.wait(2)

        # Find the specific list item with text "Chart of Accounts (arkGL)"
        chart_of_accounts_item = self.find_element(
            'a[role="menuitem"][href="/fund-nav/chart-of-accounts/aa9c0d49-c899-4116-9729-6d03cda179df"]'
        )

        chart_of_accounts_item.click()
        self.wait(2)

        # get Input search by account name
        # self.filter_items_by_account_or_number(ACCOUNT_NAME_TO_SEARCH)

        # get Input search by number
        # self.filter_items_by_account_or_number(NUMBER_TO_SEARCH)
        # get Input search by selecting columns
        self.filter_items_by_selecting_columns(
            COLUMN_ARK_TRANSACTION_FILTER, ARK_TRANSACTION_FILTER_VALUE
        )
        self.reset_filters(COLUMN_ARK_TRANSACTION_FILTER)
       
           

    def filter_items_by_account_or_number(self, filter_value):
        """
        Filters items by account or number.

        Args:
            filter_value (str): The value to filter by.

        Returns:
            None
        """
        self.wait_for_element_visible("input#search_accounts")
        self.assert_element_visible("input#search_accounts")
        self.click("input#search_accounts")
        self.wait_for_element_clickable("input#search_accounts_popover")
        self.click("input#search_accounts_popover")
        self.wait_for_element_visible("input#search_accounts_popover")
        self.type("input#search_accounts_popover", filter_value)
        self.send_keys("input#search_accounts_popover", "\n")
        self.wait_for_element_visible("div[role='grid']")
        grid_with_value_xpath = f"//div[@role='grid']"
        grid_table = self.find_element(grid_with_value_xpath)
        self.assert_element_visible(grid_with_value_xpath)

        # Clear search items
        self.click("input#search_accounts")
        self.click("input#search_accounts_popover")
        self.wait(1)
        for i in range(len(filter_value)):
            self.send_keys("input#search_accounts_popover", Keys.BACKSPACE)
        self.wait(2)

    def filter_items_by_selecting_columns(self, column, filter_value):
        """
        Filters items by selecting columns.

        Args:
            None

        Returns:
            None
        """
        # Add your code here to filter items by selecting columns     
        self.wait_for_element_visible("div[role='grid']")
        grid_with_value_xpath = f"//div[@role='grid']"
        grid_table = self.find_element(grid_with_value_xpath)
        self.wait_for_element_visible(f"div#{column}", timeout=10)
        self.click(f"div#{column}")
        self.wait_for_element_visible("div#popover_filter_text")
        self.uncheck_if_checked("label#check_all span input")
        self.check_if_unchecked('input[name="' + filter_value + '"]')
        self.click("#btn_apply")
        
    def reset_filters(self, column):
        """
        Reset all filters.

        Args:
            None

        Returns:
            None
        """
        self.wait_for_element_visible("div[role='grid']")
        grid_with_value_xpath = f"//div[@role='grid']"
        grid_table = self.find_element(grid_with_value_xpath)
        self.wait_for_element_visible(f"div#{column}", timeout=10)
        self.click(f"div#{column}")
        self.wait_for_element_visible("div#popover_filter_text")
        self.wait_for_element_visible("button#btn_clear")
        self.click("button#btn_clear")
        self.click("#btn_apply")
        self.wait(2)
       
        


if __name__ == "__main__":
    TestWebPageLogin.main()
