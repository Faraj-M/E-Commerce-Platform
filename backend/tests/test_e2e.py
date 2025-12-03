"""
End-to-end tests using Selenium for critical user flows.
Requires the application to be running (e.g., via Docker).

Note: These tests require Chrome/Chromium to be installed.
For CI/CD, use headless mode. For local testing, you can remove headless option.
"""
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
try:
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    ChromeDriverManager = None


@pytest.fixture(scope='module')
def driver():
    """Create and configure Chrome WebDriver for E2E tests."""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    if ChromeDriverManager:
        service = Service(ChromeDriverManager().install())
    else:
        service = Service()
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    
    yield driver
    driver.quit()


@pytest.fixture
def base_url():
    """Base URL for the application."""
    return 'http://localhost:8000'


class TestUserRegistrationAndLogin:
    """Test user registration and login flows."""
    
    def test_user_can_register_and_login(self, driver, base_url):
        """Test complete user registration and login flow."""
        driver.get(f'{base_url}/accounts/signup/')
        
        username = f'testuser_{pytest.current_time}'
        driver.find_element(By.ID, 'username').send_keys(username)
        driver.find_element(By.ID, 'email').send_keys(f'{username}@test.com')
        driver.find_element(By.ID, 'password').send_keys('testpass123')
        driver.find_element(By.ID, 'password_confirm').send_keys('testpass123')
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(driver, 10).until(
            EC.url_contains('/')
        )
        
        assert 'MarketPlace' in driver.page_source
        assert username in driver.page_source or 'Logout' in driver.page_source


class TestProductBrowsing:
    """Test product browsing and viewing."""
    
    def test_user_can_view_product_list(self, driver, base_url):
        """Test that product list page loads and displays products."""
        driver.get(f'{base_url}/')
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        
        assert 'Results' in driver.page_source or 'Products' in driver.page_source
        
        product_cards = driver.find_elements(By.CSS_SELECTOR, '.bg-slate-800.rounded-xl')
        assert len(product_cards) > 0
    
    def test_user_can_view_product_detail(self, driver, base_url):
        """Test that product detail page loads correctly."""
        driver.get(f'{base_url}/')
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="product"]'))
        )
        
        product_links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="product"]')
        if product_links:
            product_links[0].click()
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))
            )
            
            assert 'Add to Cart' in driver.page_source or 'Add' in driver.page_source


class TestShoppingCart:
    """Test shopping cart functionality."""
    
    def test_user_can_add_item_to_cart(self, driver, base_url):
        """Test adding an item to cart (requires login)."""
        driver.get(f'{base_url}/accounts/login/')
        
        driver.find_element(By.ID, 'username').send_keys('testuser')
        driver.find_element(By.ID, 'password').send_keys('testpass123')
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(driver, 10).until(
            EC.url_contains('/')
        )
        
        driver.get(f'{base_url}/')
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="product"]'))
        )
        
        product_links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="product"]')
        if product_links:
            product_links[0].click()
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'form[action*="add"]'))
            )
            
            add_to_cart_form = driver.find_element(By.CSS_SELECTOR, 'form[action*="add"]')
            add_to_cart_form.submit()
            
            WebDriverWait(driver, 10).until(
                EC.any_of(
                    EC.url_contains('cart'),
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.bg-green-500'))
                )
            )


class TestCheckoutFlow:
    """Test checkout and payment flow."""
    
    def test_user_can_access_checkout(self, driver, base_url):
        """Test that checkout page is accessible (requires items in cart)."""
        driver.get(f'{base_url}/accounts/login/')
        
        driver.find_element(By.ID, 'username').send_keys('testuser')
        driver.find_element(By.ID, 'password').send_keys('testpass123')
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(driver, 10).until(
            EC.url_contains('/')
        )
        
        driver.get(f'{base_url}/orders/checkout/')
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'form'))
        )
        
        assert 'Checkout' in driver.page_source or 'Shipping' in driver.page_source


@pytest.fixture(autouse=True)
def setup_time():
    """Setup current time for unique usernames."""
    pytest.current_time = int(time.time())

