from seleniumbase import BaseCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import logging
from constants import (
    CLIENT_NAME,
    ACCOUNT_NAME_TO_SEARCH,
    NUMBER_TO_SEARCH,
    COLUMN_ARK_TRANSACTION_FILTER,
    ARK_TRANSACTION_FILTER_VALUE,
    COLUMN_ATTRIBUTE_FILTER,
    ATTRIBUTE_FILTER_VALUE,
    COLUMN_FINANCIAL_STATEMENT_FILTER,
    FINANCIAL_STATEMENT_FILTER_VALUE,
    COLUMN_STATUS_FILTER,
    STATUS_FILTER_VALUE,
)


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
        test_search_and_filters: A method that performs the search and filter process
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Before logging setup")  
        load_dotenv()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        log_file_path = os.path.join(current_dir, "py_log.log")

        try:
            logging.basicConfig(
                filename=log_file_path,
                filemode="a",  # Use "a" for append mode
                format="%(asctime)s %(levelname)s:%(message)s",
                level=logging.DEBUG
            )
        except Exception as e:
            print(f"Error setting up logging: {e}")
        else:
            print("Logging setup successful")  

     
        if os.path.exists(log_file_path):
            print(f"Log file created at: {os.path.abspath(log_file_path)}")
        else:
            print("Log file was not created")

    def test_login(self):
        # Open the web page
        print("start test_login")
        logging.debug("Start Login Test")
        logging.info("Start Login Test")
        try:
            self.open(os.getenv("BASE_URL"))
            self.type('input[name="email"]', os.getenv("USERNAME_TEST"))
            self.type('input[name="password"]', os.getenv("PASSWORD_TEST"))
            self.click('button[type="submit"]')
            self.wait(2)
        except Exception as e:
            logging.error(f"Error on Login: {e}")

    def test_search_and_filters(self):
        self.test_login()

        # Click on the "Clients" menu option

        autocomplete_input_xpath = "//input[@id='selector-client']"
        option_with_value_xpath = (
            f"//ul[@role='listbox']//li[contains(text(), '{CLIENT_NAME}')]"
        )
        logging.debug("Start Search and Filter Test")
        print("Start Search and Filter Test")
        self.type(autocomplete_input_xpath, CLIENT_NAME)
        self.click(option_with_value_xpath)
        self.wait(2)
        self.click("#expand_collapse_sidebar")
        self.click("#funds_menu_option")
        self.wait(2)

        # Click on the "De Buyer" fund
        logging.debug("Click on the 'De Buyer' fund")
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

        # <<<<<<<<<<<<<<<search using input search and filters>>>>>>>>>>>>>>>>>>>>>>>
        logging.debug("Search using input search by account name")
        self.filter_items_by_account_or_number(ACCOUNT_NAME_TO_SEARCH)
        logging.debug("Search using input search by number")
        self.filter_items_by_account_or_number(NUMBER_TO_SEARCH)
        print("End Search and Filter Test")

        # <<<<<<<<<<<<<<<    filters using columns     >>>>>>>>>>>>>>>>>>>>>>>
        # Filter on ARK Transaction column by General Expense
        # #self.filter_items_by_selecting_columns(
        #     COLUMN_ARK_TRANSACTION_FILTER, ARK_TRANSACTION_FILTER_VALUE
        # )
        self.wait(2)
        # reset filters
        # self.reset_filters(COLUMN_ARK_TRANSACTION_FILTER)

        # Filter on Attribute column by Gain/Loss - Income Statement
        # #self.filter_items_by_selecting_columns(
        #     COLUMN_ATTRIBUTE_FILTER, ATTRIBUTE_FILTER_VALUE
        # )

        # reset filters
        # self.reset_filters(COLUMN_ATTRIBUTE_FILTER)

        # Filter on Financial Statement column  by Cash and  Cash Equivalents
        # #self.filter_items_by_selecting_columns(
        #     COLUMN_FINANCIAL_STATEMENT_FILTER, FINANCIAL_STATEMENT_FILTER_VALUE
        # )

        # reset filters
        # self.reset_filters(COLUMN_FINANCIAL_STATEMENT_FILTER)

        # Filter on Status column by POSTED value
        # #self.filter_items_by_selecting_columns(
        #     COLUMN_STATUS_FILTER, STATUS_FILTER_VALUE
        # )
        # self.reset_filters(COLUMN_STATUS_FILTER)
        # reset filters

    def filter_items_by_account_or_number(self, filter_value):
        """
        Filters items by account or number.

        Args:
            filter_value (str): The value to filter by.

        Returns:
            None
        """
        try:
            logging.debug(f"Filtering items by account or number: {filter_value}")
            self.wait_for_element_visible("input#search_accounts")
            self.assert_element_visible("input#search_accounts")
            self.click("input#search_accounts")
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
        except Exception as e:
            logging.error(f"Error on filter_items_by_account_or_number: {e}")

    def filter_items_by_selecting_columns(self, column, filter_value):
        """
        Filters items by selecting columns.

        Args:
            None

        Returns:
            None
        """
        self.wait_for_element_visible("div[role='grid']")
        grid_with_value_xpath = f"//div[@role='grid']"
        grid_table = self.find_element(grid_with_value_xpath)
        try:
            self.wait_for_element_visible(f"div#{column}", timeout=10)
            self.click(f"div#{column}")
            self.wait_for_element_visible("div#popover_filter_text")
            self.uncheck_if_checked("label#check_all span input")
            self.check_if_unchecked('input[name="' + filter_value + '"]')
            self.click("#btn_apply")
        except Exception as e:
            grid = self.find_element("div[role='grid']")
            grid.click()
            cell = grid.find_element(By.XPATH, ".//div[@role='cell']")
            cell.click()
            self.driver.execute_script("arguments[0].scrollLeft += 1000;", grid)
            self.wait(10)

    def reset_filters(self, column):
        """
        Resets the filters applied to a specific column in a grid.

        Args:
            column (str): The column identifier.

        Raises:
            Exception: If an error occurs while resetting the filters.

        Returns:
            None
        """
        self.wait_for_element_visible("div[role='grid']")
        grid_with_value_xpath = f"//div[@role='grid']"
        grid_table = self.find_element(grid_with_value_xpath)

        try:
            self.wait_for_element_visible(f"div#{column}", timeout=10)
            self.click(f"div#{column}")
            self.wait_for_element_visible("div#popover_filter_text")
            self.wait_for_element_visible("button#btn_clear")
            self.click("#btn_clear")
            self.click("#btn_apply")
            self.wait(2)
        except Exception as e:
            grid = self.find_element("div[role='grid']")
            grid.click()
            cell = grid.find_element(By.XPATH, ".//div[@role='cell']")
            cell.click()
            self.driver.execute_script("arguments[0].scrollLeft += 1000;", grid)
            self.wait(10)


if __name__ == "__main__":
    main()
