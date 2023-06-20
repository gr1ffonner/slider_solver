from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()


slider = driver.find_element(
    By.CSS_SELECTOR, "div.slider-handle.min-slider-handle.round"
)


move = webdriver.ActionChains(driver)
move.click_and_hold(slider).move_by_offset(40, 0).release().perform()
