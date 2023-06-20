from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://rangeslider.js.org/")
driver.maximize_window()


slider = driver.find_element(By.ID, "js-rangeslider-0")


move = webdriver.ActionChains(driver)
move.click_and_hold(slider).move_by_offset(100, 0).release().perform()

# Wait for verification or further actions
time.sleep(5)

# Close the browser
driver.quit()
print("Browser closed")
