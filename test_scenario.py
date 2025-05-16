import pytest
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

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
# # TC02: Invalid Login (Functional, Invalid)
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
    # Wait for the notification that the product was added
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".bar-notification.success, .bar-notification")))
    driver.find_element(By.LINK_TEXT, "Shopping cart").click()
    driver.save_screenshot("screenshots/add_to_cart_screenshot.png")
    # Check for product name in cart by text, not link
    cart_content = driver.find_element(By.CSS_SELECTOR, ".order-summary-content").text.lower()
    assert "smartphone" in cart_content, f"Product was not added to cart. Cart content: {cart_content}"

# TC04: Add Product to Cart - Zero Quantity (Functional, Invalid)
def test_add_zero_quantity_to_cart(driver):
    driver.find_element(By.LINK_TEXT, "Electronics").click()
    driver.find_element(By.LINK_TEXT, "Cell phones").click()
    driver.find_element(By.LINK_TEXT, "Smartphone").click()
    quantity_box = driver.find_element(By.ID, "addtocart_43_EnteredQuantity")
    quantity_box.clear()
    quantity_box.send_keys("0")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Add to cart']"))).click()
    driver.save_screenshot("screenshots/zero_quantity_add_to_cart.png")
    # After attempting to add zero quantity, check that the cart is still empty
    driver.find_element(By.LINK_TEXT, "Shopping cart").click()
    cart_content = driver.find_element(By.CSS_SELECTOR, ".order-summary-content").text.lower()
    assert "your shopping cart is empty" in cart_content, f"Cart is not empty after adding zero quantity. Cart content: {cart_content}"

# TC05: Search for valid Product (UI, Valid)
def test_search_product(driver):
    try:
        driver.find_element(By.NAME, "q").send_keys("computer")
        driver.find_element(By.CSS_SELECTOR, "input[value='Search']").click()
        driver.save_screenshot("screenshots/search_product_screenshot.png")
        search_results = driver.find_elements(By.CSS_SELECTOR, ".product-item")
        assert len(search_results) > 0, "No products found in search results"
    except (NoSuchElementException, TimeoutException) as e:
        driver.save_screenshot("screenshots/error_search_product_screenshot.png")
        pytest.fail(f"Search test failed due to exception: {str(e)}")

# TC06: Search for Invalid/Non-existent Product (UI, Invalid)
def test_invalid_search_product(driver):
    try:
        driver.find_element(By.NAME, "q").send_keys("washing machine")
        driver.find_element(By.CSS_SELECTOR, "input[value='Search']").click()
        driver.save_screenshot("screenshots/invalid_search_product_screenshot.png")
        search_results = driver.find_elements(By.CSS_SELECTOR, ".product-item")
        assert len(search_results) == 0, "Unexpected products found in search results for invalid query"
    except (NoSuchElementException, TimeoutException) as e:
        driver.save_screenshot("screenshots/error_invalid_search_product_screenshot.png")
        pytest.fail(f"Invalid search test failed due to exception: {str(e)}")