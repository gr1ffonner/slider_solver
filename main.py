from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

# Load the website
url = "https://avas.mfa.gov.cn/qzyyCoCommonController.do?yypersoninfo&status=continue&1686142874790&locale=ru_RU"
driver.get(url)
print("Website loaded successfully")

# Enter data into the form fields
fio = "John Doe"
phone = "1234567890"
email = "example@gmail.com"
number = "2023053168153296260"

fio_input = driver.find_element(By.XPATH, "//input[@id='linkname']")
phone_input = driver.find_element(By.XPATH, "//input[@id='linkphone']")
email_input = driver.find_element(By.XPATH, "//input[@id='mail']")
number_input = driver.find_element(By.XPATH, "//input[@id='applyid1']")

fio_input.send_keys(fio)
phone_input.send_keys(phone)
email_input.send_keys(email)
number_input.send_keys(number)
print("Form data entered successfully")

# Submit the form by clicking the button
submit_button = driver.find_element(
    By.XPATH, "//button[contains(text(), 'сохранить и далее')]"
)
submit_button.click()
print("Form submitted successfully")

# Wait for the first iframe to load
wait = WebDriverWait(driver, 10)
iframe1 = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[id='tcaptcha_iframe_dy']"))
)
driver.switch_to.frame(iframe1)
print("switched to the frame with captcha")


# Wait for the slider to load inside the second iframe
slider = wait.until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "div[aria-label='Проведите, чтобы собрать пазл']")
    )
)

# Calculate the distance to drag the slider
# container_width = slider.size["width"]
slider_width = slider.size["width"]
# distance = container_width - slider_width

# Perform the sliding action
actions = webdriver.ActionChains(driver)
actions.click_and_hold(slider).move_by_offset(10, 0).release().perform()


# Wait for verification or further actions
time.sleep(5)

# Close the browser
driver.quit()
print("Browser closed")



# Класс слайдера tc-fg-item tc-slider-normal

# Класс пазла(не пустого) tc-fg-item
