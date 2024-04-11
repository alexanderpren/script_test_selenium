from seleniumbase import BaseCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import logging
import datetime
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

# create log folder if not exists
log_directory = "./logs"
os.makedirs(log_directory, exist_ok=True)
log = logging.getLogger(__name__)
shell_handler = logging.StreamHandler()

log_file_path = "./logs/%s.log" % datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
file_handler = logging.FileHandler(log_file_path)

log.setLevel(logging.INFO)
shell_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)

fmt_shell = "%(message)s"
fmt_file = (
    "%(levelname)s %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
)

shell_formatter = logging.Formatter(fmt_shell)
file_formatter = logging.Formatter(fmt_file)

shell_handler.setFormatter(shell_formatter)
file_handler.setFormatter(file_formatter)

log.addHandler(shell_handler)
log.addHandler(file_handler)


class TestWebPageLogin(BaseCase):
    """
    A test case class for testing web page login functionality.

    Inherits:
        BaseCase: The base test case class.

    Methods:
        __init__: Initializes the test case.
        test_search_and_filters: Tests login, search and filters functionality.
        filter_items_by_account_or_number: Filters items by account or number.
        filter_items_by_selecting_columns: Filters items by selecting columns and passing a value.
        reset_filters: Resets the filters applied to a specific column in a grid.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Before logging setup")
        load_dotenv()

        if os.path.exists(log_file_path):
            print(f"Log file created at: {os.path.abspath(log_file_path)}")
        else:
            print("Log file was not created")


    def test_search_and_filters(self):
        # Open the web page
        print("start test_login")
        log.debug("starting test")
        try:
            log.info("Opening the web page and logging in")
            self.open(os.getenv("BASE_URL"))
            self.type('input[name="email"]', os.getenv("USERNAME_TEST"))
            self.type('input[name="password"]', os.getenv("PASSWORD_TEST"))
            self.click('button[type="submit"]')
            self.wait(2)
            log.info("Login success")
        except Exception as e:
            log.error(f"Error on Login: {e}")

        # Click on the "Clients" menu option
        self.wait_for_element_visible("input#selector-client")
        autocomplete_input_xpath = "//input[@id='selector-client']"
        option_with_value_xpath = (
            f"//ul[@role='listbox']//li[contains(text(), '{CLIENT_NAME}')]"
        )
        log.debug("Start: client Selection and sidebar option")
        try:
            self.type(autocomplete_input_xpath, CLIENT_NAME)
            self.click(option_with_value_xpath)
            self.click("#expand_collapse_sidebar")
            self.click("#funds_menu_option")
            self.wait(2)
        except Exception as e:
            log.error(f"Error selecting client and sidebar option: {e}")

        # Click on the "De Buyer" fund
        log.info("Click on 'De Buyer' fund")
        try:
            span_de_buyer = self.wait_for_element_visible("//span[text()='De Buyer']")
            span_de_buyer.click()
            self.assert_element_visible("button#general_ledger")
            button = self.find_element("button#general_ledger")
            button.click()
            self.wait_for_element_visible("ul.MuiList-root")
            log.info("Click on 'Chart of Accounts' menu option")
            # Find the specific list item with text "Chart of Accounts (arkGL)"
            self.wait(2)
            self.wait_for_element_visible(
                'a[role="menuitem"][href="/fund-nav/chart-of-accounts/aa9c0d49-c899-4116-9729-6d03cda179df"]'
            )
            chart_of_accounts_item = self.find_element(
                'a[role="menuitem"][href="/fund-nav/chart-of-accounts/aa9c0d49-c899-4116-9729-6d03cda179df"]'
            )
            chart_of_accounts_item.click()
            self.wait(2)
        except Exception as e:
            log.error(f"Error selecting on table de Buyer fund: {e}")

        # <<<<<<<<<<<<<<<search using input search and filters>>>>>>>>>>>>>>>>>>>>>>>
        log.info("Testing Search: Using input search by account name")
        self.filter_items_by_account_or_number(ACCOUNT_NAME_TO_SEARCH)

        log.info("Testing Search:  using input search by number")
        self.filter_items_by_account_or_number(NUMBER_TO_SEARCH)

        # <<<<<<<<<<<<<<<    filters using columns     >>>>>>>>>>>>>>>>>>>>>>>
        # Filter on ARK Transaction column by General Expense
        log.info("Filtering items by ARK Transaction column and General Expense value")
        self.filter_items_by_selecting_columns(
            COLUMN_ARK_TRANSACTION_FILTER, ARK_TRANSACTION_FILTER_VALUE
        )

        # reset filters

        log.info("Resetting filters")
        self.reset_filters(COLUMN_ARK_TRANSACTION_FILTER)

        # Filter on Attribute column by Gain/Loss - Income Statement
        log.info("Filtering items by Attribute Column and Gain/Loss - Income Statement")
        self.filter_items_by_selecting_columns(
            COLUMN_ATTRIBUTE_FILTER, ATTRIBUTE_FILTER_VALUE
        )
        log.info("Resetting filters")
        self.reset_filters(COLUMN_ATTRIBUTE_FILTER)

        # Filter on Financial Statement column  by Cash and  Cash Equivalents
        log.info(
            "Filtering items by Financial Statement Column and Cash and Cash Equivalents"
        )
        self.filter_items_by_selecting_columns(
            COLUMN_FINANCIAL_STATEMENT_FILTER, FINANCIAL_STATEMENT_FILTER_VALUE
        )

        self.reset_filters(COLUMN_FINANCIAL_STATEMENT_FILTER)

        # Filter on Status column by POSTED value
        log.info("Filtering items by Status Column and POSTED value")
        self.filter_items_by_selecting_columns(
            COLUMN_STATUS_FILTER, STATUS_FILTER_VALUE
        )
        self.reset_filters(COLUMN_STATUS_FILTER)

        log.info("test successfully completed")

    def filter_items_by_account_or_number(self, filter_value):
        """
        Filters items by account or number.

        Args:
            filter_value (str): The value to filter by.

        Returns:
            None
        """
        try:
            log.info(f"Starting Filtering items by account or number: {filter_value}")
            self.wait_for_element_visible("input#search_accounts")
            self.assert_element_visible("input#search_accounts")
            self.click("input#search_accounts")
            self.wait(2)
            #TODO: check this line, sometimes it fails
            # self.wait_for_element_visible("input#search_accounts_popover")
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
            log.info(f"Items filtered by account or number success: {filter_value}")
        except Exception as e:
            log.error(f"Error on filter_items_by_account_or_number: {e}")

    def filter_items_by_selecting_columns(self, column, filter_value):
        """
        Filters items by selecting columns.

        Args:
            column (str): The column identifier.
            filter_value (str): The value to filter by.

        Returns:
            None
        """
        log.info(f"Starting Filtering items by selecting columns: {column} and {filter_value}")
        self.wait_for_element_visible("div[role='grid']", timeout=10)
        grid_with_value_xpath = f"//div[@role='grid']"
        grid_table = self.find_element(grid_with_value_xpath)
        try:
            self.wait_for_element_visible(f"div#{column}", timeout=3)
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
        log.info(f"Items filtered by selecting columns success: {column}")

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
        log.info(f"Starting Resetting filters for column: {column}")
        self.wait_for_element_visible("div[role='grid']")
        grid_with_value_xpath = f"//div[@role='grid']"
        grid_table = self.find_element(grid_with_value_xpath)

        try:
            self.wait_for_element_visible(f"div#{column}", timeout=3)
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
        log.info(f"Filters reset for column success: {column}")


if __name__ == "__main__":
    main()
