import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from trueSolver import get_points
from selenium.common.exceptions import TimeoutException


def load_website():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    url = "https://avas.mfa.gov.cn/qzyyCoCommonController.do?yypersoninfo&status=continue&1686142874790&locale=ru_RU"
    driver.get(url)
    print("Website loaded successfully")
    return driver, url


def enter_form_data(driver):
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


def submit_form(driver):
    submit_button = driver.find_element(
        By.XPATH, "//button[contains(text(), 'сохранить и далее')]"
    )
    submit_button.click()
    print("Form submitted successfully")


def solve_captcha(driver):
    while True:
        try:
            wait = WebDriverWait(driver, 10)
            iframe1 = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "iframe[id='tcaptcha_iframe_dy']")
                )
            )
        except TimeoutException:
            print("Captcha iframe did not load within the specified timeout.")
            print("Reloading the page...")
            return False

        driver.switch_to.frame(iframe1)
        print("Switched to the frame with captcha")

        time.sleep(3)

        background_image = None
        piece_image = None

        network_requests = driver.execute_script(
            "return window.performance.getEntries()"
        )
        for request in network_requests:
            if "cap_union_new_getcapbysig?img_index=1" in request["name"]:
                print("FOUND background")
                background_image = request["name"]
            elif "cap_union_new_getcapbysig?img_index=0" in request["name"]:
                print("Found piece")
                piece_image = request["name"]
                break

        distance = 0
        try:
            if background_image and piece_image:
                response_back = requests.get(background_image)
                response_piece = requests.get(piece_image)
                with open("background.png", "wb") as file:
                    file.write(response_back.content)
                distance = int(get_points("background.png") / 2.6) + 5
                # Additional code that uses the distance value
            else:
                raise ValueError("Отсутствуют ссылки на изображения")
        except Exception as e:
            print("Ошибка при решении капчи:", str(e))
            print("Капча не решаема")
            return False

        print(type(distance))

        slider = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt='slider']"))
        )

        # Perform the sliding action
        actions = webdriver.ActionChains(driver)
        actions.click_and_hold(slider).perform()
        actions.move_by_offset(distance, 0).perform()
        actions.release(slider).perform()

        try:
            wait.until(EC.url_changes(driver.current_url))
            print("Page reloaded successfully")
            return True
        except TimeoutException:
            print("Page did not reload within the specified timeout.")
            print("Reloading the page...")

        time.sleep(3)


def main():
    # Initialize ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    # Load the website
    url = "https://avas.mfa.gov.cn/qzyyCoCommonController.do?yypersoninfo&status=continue&1686142874790&locale=ru_RU"
    driver.get(url)
    print("Website loaded successfully")

    while True:
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

        if solve_captcha(driver):
            # Captcha solved successfully, exit the loop
            break

        # Reload the page
        print("Reloading the page...")
        driver.refresh()

    # Close the browser
    driver.quit()
    print("Browser closed")


if __name__ == "__main__":
    main()
