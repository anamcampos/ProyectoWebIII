import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin

SITE_URL = os.getenv("SITE_URL", "https://books.toscrape.com")

def create_driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    # optional user agent
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def optional_login(driver):
    """
    If LOGIN_URL and credentials provided in env, attempt login.
    For books.toscrape.com login is not necessary, but this function uses selectors from env if present.
    """
    from os import getenv
    login_url = getenv("LOGIN_URL", "")
    if not login_url:
        return
    driver.get(login_url)
    time.sleep(1)
    user_sel = getenv("LOGIN_USERNAME_SELECTOR", "")
    pass_sel = getenv("LOGIN_PASSWORD_SELECTOR", "")
    submit_sel = getenv("LOGIN_SUBMIT_SELECTOR", "")
    username = getenv("LOGIN_USERNAME", "")
    password = getenv("LOGIN_PASSWORD", "")
    try:
        if user_sel and username:
            driver.find_element(By.CSS_SELECTOR, user_sel).send_keys(username)
        if pass_sel and password:
            driver.find_element(By.CSS_SELECTOR, pass_sel).send_keys(password)
        if submit_sel:
            driver.find_element(By.CSS_SELECTOR, submit_sel).click()
        time.sleep(2)
    except Exception as e:
        print("Login attempt failed or selectors missing:", e)

def scrape_with_selenium(start_url=None, max_pages=None):
    if start_url is None:
        start_url = SITE_URL
    driver = create_driver()
    optional_login(driver)
    items = []
    url = start_url
    page = 1
    while url:
        print(f"[scraper_dynamic] opening {url}")
        driver.get(url)
        time.sleep(1.2)
        elements = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")
        for el in elements:
            try:
                a = el.find_element(By.CSS_SELECTOR, "h3 a")
                title = a.get_attribute("title").strip()
                href = a.get_attribute("href")
                price_el = el.find_element(By.CSS_SELECTOR, ".price_color")
                price = price_el.text.strip() if price_el else None
                external_id = href.split("/")[-2] if "/" in href else href
                items.append({
                    "external_id": external_id,
                    "title": title,
                    "price": price,
                    "url": href
                })
            except Exception:
                continue
        # next
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, "li.next a")
            next_href = next_btn.get_attribute("href")
            url = next_href
        except Exception:
            url = None
        page += 1
        if max_pages and page > max_pages:
            break
    driver.quit()
    return items
