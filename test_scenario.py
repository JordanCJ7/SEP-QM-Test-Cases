import pytest
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@pytest.fixture
def driver():
    service = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get("https://demowebshop.tricentis.com/")
    yield driver
    driver.quit()

# TC01: Valid Login (Functional, Valid)
def test_valid_login(driver):
    driver.find_element(By.LINK_TEXT, "Log in").click()
    driver.find_element(By.NAME, "Email").send_keys("kaviduk2002@gmail.com")
    driver.find_element(By.NAME, "Password").send_keys("BDemo@0229")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Log in']"))).click()
    driver.save_screenshot("screenshots/valid_login_screenshot.png")
    assert driver.find_element(By.LINK_TEXT, "Log out").is_displayed(), "Valid login failed"

# # TC01b: Invalid Login - Empty Credentials (Functional, Invalid)
# def test_login_empty_credentials(driver):
#             driver.find_element(By.LINK_TEXT, "Log in").click()
#             driver.find_element(By.NAME, "Email").clear()
#             driver.find_element(By.NAME, "Password").clear()
#             WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Log in']"))).click()
#             driver.save_screenshot("screenshots/empty_credentials_login_screenshot.png")
#             error_message = driver.find_element(By.CSS_SELECTOR, ".validation-summary-errors").text
#             assert "Login was unsuccessful" in error_message, "Empty credentials did not show error message"       

# TC02: Invalid Login (Functional, Invalid)
def test_invalid_login(driver):
    driver.find_element(By.LINK_TEXT, "Log in").click()
    driver.find_element(By.NAME, "Email").send_keys("kaviduk2002@gmail.com")
    driver.find_element(By.NAME, "Password").send_keys("WrongPassword")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Log in']"))).click()
    driver.save_screenshot("screenshots/invalid_login_screenshot.png")
    error_message = driver.find_element(By.CSS_SELECTOR, ".validation-summary-errors").text
    assert "Login was unsuccessful" in error_message, "Invalid login did not show error message"

# TC03: Add Product to Cart (Functional, Valid)
def test_add_to_cart(driver):
    driver.find_element(By.LINK_TEXT, "Electronics").click()
    driver.find_element(By.LINK_TEXT, "Cell phones").click()
    driver.find_element(By.LINK_TEXT, "Smartphone").click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Add to cart']"))).click()
    driver.find_element(By.LINK_TEXT, "Shopping cart").click()
    driver.save_screenshot("screenshots/add_to_cart_screenshot.png")
    # Check for product name in cart by text, not link
    product_in_cart = driver.find_element(By.XPATH, "//td[@class='product']/a[contains(text(), 'Smartphone')]").is_displayed()
    assert product_in_cart, "Product was not added to cart"

# TC04: Add Product to Cart - Invalid Product (Functional, Invalid)
def test_add_invalid_product_to_cart(driver):
        driver.find_element(By.LINK_TEXT, "Electronics").click()
        driver.find_element(By.LINK_TEXT, "Cell phones").click()
        # Try to add a product that does not exist
        product_links = driver.find_elements(By.LINK_TEXT, "NonExistentProduct")
        assert len(product_links) == 0, "Non-existent product should not be found"    

# TC05: Search for Product (UI, Valid)
def test_search_product(driver):
    driver.find_element(By.NAME, "q").send_keys("computer")
    driver.find_element(By.CSS_SELECTOR, "input[value='Search']").click()
    driver.save_screenshot("screenshots/search_product_screenshot.png")
    search_results = driver.find_elements(By.CSS_SELECTOR, ".product-item")
    assert len(search_results) > 0, "No products found in search results"