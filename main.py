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
    print("Браузер загружен")
    return driver, url


def enter_form_data(driver):
    fio = "Belkina Tatiana"
    phone = "79058323393"
    email = "miheeva-291980@mail.ru"
    number = "2023053061423288300"

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
    print("Форма отправлена")


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
            print("Фрейм с капчей не был загружен в установленное время")
            print("Перезагружаем страницу")
            return False

        driver.switch_to.frame(iframe1)
        print("Переключаемся на фрейм с капчей")

        time.sleep(3)

        background_image = None
        piece_image = None

        network_requests = driver.execute_script(
            "return window.performance.getEntries()"
        )
        for request in network_requests:
            if "cap_union_new_getcapbysig?img_index=1" in request["name"]:
                print("Скачиваем задний фон")
                background_image = request["name"]
            elif "cap_union_new_getcapbysig?img_index=0" in request["name"]:
                print("Скачиваем пазл")
                piece_image = request["name"]
                break

        distance = 0
        try:
            if background_image and piece_image:
                response_back = requests.get(background_image)
                with open("background.png", "wb") as file:
                    file.write(response_back.content)
                distance = int(get_points("background.png") / 2.6) + 5
                print(f"Нужно передвинуть на {distance} пикселей")
                # Additional code that uses the distance value
            else:
                raise ValueError("Отсутствуют ссылки на изображения")
        except Exception as e:
            print("Ошибка при решении капчи:", str(e))
            print("Капча не решаема")
            return False

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
            print("Страница успешно перезагружена")
            continue
        except TimeoutException:
            print("Фрейм с капчей не был загружен в установленное время")
            print("Перезагружаем страницу")

        # time.sleep(3)


def main():
    # # Initialize ChromeDriver
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # driver.maximize_window()
    #
    # # Load the website
    # url = "https://avas.mfa.gov.cn/qzyyCoCommonController.do?yypersoninfo&status=continue&1686142874790&locale=ru_RU"
    # driver.get(url)
    # print("Браузер загружен")

    driver, _ = load_website()

    while True:
        enter_form_data(driver)
        submit_form(driver)
        if solve_captcha(driver):
            break
        # Reload the page
        print("Перезагружаем страницу")
        driver.refresh()

    # Close the browser
    driver.quit()
    print("Закрываем браузер")


if __name__ == "__main__":
    main()
