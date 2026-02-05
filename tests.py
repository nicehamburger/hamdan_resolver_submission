import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()
    driver.maximize_window()

    # Navigate to the local HTML file
    file_path = "file://" + os.path.abspath("index.html")
    driver.get(file_path)

    # Set up an explicit wait for Test 5
    wait = WebDriverWait(driver, 12) 
    return driver, wait

def teardown_driver(driver):
    # Close WebDriver session and release resources
    driver.quit()

def test_1_login_form(driver):
    email_input = driver.find_element(By.ID, "inputEmail")
    password_input = driver.find_element(By.ID, "inputPassword")
    login_button = driver.find_element(By.XPATH, "//div[@id='test-1-div']//button[@type='submit']")
    
    # Verify form elements are visible
    assert email_input.is_displayed()
    assert password_input.is_displayed()
    assert login_button.is_displayed()

    # Enter test credentials and verify input is captured
    email_input.send_keys("email@test.com")
    password_input.send_keys("testpassword")
    
    # Assert values were entered correctly
    assert email_input.get_attribute("value") == "email@test.com"
    assert password_input.get_attribute("value") == "testpassword"

def test_2_list_items(driver):
    list_items = driver.find_elements(By.XPATH, "//div[@id='test-2-div']//ul[@class='list-group']/li")

    # Assert Number of List Items
    assert len(list_items) == 3

    second_item = list_items[1]

    # Extract badge element
    badge = second_item.find_element(By.TAG_NAME, "span")

    # Get list item text without badge
    item_text = second_item.text.replace(badge.text, "").strip()
    assert item_text == "List Item 2"

    # Assert badge value
    assert badge.text == "6"

def test_3_dropdown(driver):
    dropdown_button = driver.find_element(By.ID, "dropdownMenuButton")
    # Verify initial option is displayed
    assert dropdown_button.text.strip() == "Option 1"
    dropdown_button.click()
    # Locate and verify Option 3 is available in dropdown
    option_3 = driver.find_element(By.XPATH, "//div[@id='test-3-div']//a[text()='Option 3']")
    assert option_3.is_displayed()
    option_3.click()
    # Verify button text updated after selection
    assert dropdown_button.text.strip() == "Option 3"

def test_4_buttons_enabled(driver):
    # Verify button enabled/disabled states are correct
    buttons = driver.find_elements(By.XPATH, "//div[@id='test-4-div']//button")
    # Verify first button is enabled and clickable
    assert buttons[0].is_enabled()
    # Verify second button is disabled and not clickable
    assert not buttons[1].is_enabled()

def test_5_dynamic_button(driver, wait):
    # Wait for button to become visible (handles async loading)
    button = wait.until(EC.visibility_of_element_located((By.ID, "test5-button")))
    button.click()
    success_alert = driver.find_element(By.ID, "test5-alert")
    # Verify success alert appears after button click
    assert success_alert.is_displayed()
    # Verify button is disabled after use
    assert not button.is_enabled()

def get_table_cell_value(driver, table_id=None, row=0, column=0):
    # Helper method to retrieve cell value from HTML table by row and column index
    if table_id:
        table = driver.find_element(By.ID, table_id)
    else:
        table = driver.find_element(By.TAG_NAME, "table")
    # Extract all rows from table body
    rows = table.find_elements(By.XPATH, "./tbody/tr")
    target_row = rows[row]
    cells = target_row.find_elements(By.TAG_NAME, "td")
    return cells[column].text

def test_6_table_cell_lookup(driver):
    value = get_table_cell_value(driver, row=2, column=2)
    assert value == "Ventosanzap"

if __name__ == "__main__":
    driver, wait = setup_driver()
    try:
        # Execute all test cases in sequence
        test_1_login_form(driver)
        test_2_list_items(driver)
        test_3_dropdown(driver)
        test_4_buttons_enabled(driver)
        test_5_dynamic_button(driver, wait)
        test_6_table_cell_lookup(driver)
    finally:
        # Clean up and close WebDriver
        teardown_driver(driver)
