import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
<<<<<<< HEAD
from trueSolver import get_points


def solve_captcha():
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
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "iframe[id='tcaptcha_iframe_dy']")
        )
    )

    driver.switch_to.frame(iframe1)
    print("switched to the frame with captcha")

    time.sleep(3)

    background_imgage = None
    piece_image = None

    network_requests = driver.execute_script("return window.performance.getEntries()")
    for request in network_requests:
        if "cap_union_new_getcapbysig?img_index=1" in request["name"]:
            print("FOUND background")
            background_imgage = request["name"]
        elif "cap_union_new_getcapbysig?img_index=0" in request["name"]:
            print("Found piece")
            piece_image = request["name"]
            break

    distance = 0
    try:
        if background_imgage and piece_image:
            response_back = requests.get(background_imgage)
            response_piece = requests.get(piece_image)
            with open("background.png", "wb") as file:
                file.write(response_back.content)
            distance = int(get_points("background.png") / 2.6) + 5
            # Дополнительный код, использующий значение distance
        else:
            raise ValueError("Отсутствуют ссылки на изображения")
    except Exception as e:
        print("Ошибка при решении капчи:", str(e))
        print("Капча не решаема")

    print(type(distance))

    slider = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt='slider']"))
    )

    # Perform the sliding action
    actions = webdriver.ActionChains(driver)
    actions.click_and_hold(slider).perform()
    actions.move_by_offset(distance, 0).perform()
    actions.release(slider).perform()
    # Wait for verification or further actions

    time.sleep(10)

    # Close the browser
    driver.quit()
    print("Browser closed")


solve_captcha()
=======
from solver import PuzleSolver
from PIL import Image

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

time.sleep(10)
network_requests = driver.execute_script("return window.performance.getEntries()")

background_imgage = None
piece_image = None

for request in network_requests:
    if "cap_union_new_getcapbysig?img_index=1" in request["name"]:
        print("Found background")
        background_imgage = request["name"]
    elif "cap_union_new_getcapbysig?img_index=0" in request["name"]:
        print("Found piece")
        piece_image = request["name"]
        break

print("Finding distance...")
if background_imgage and piece_image:
    response_back = requests.get(background_imgage)
    response_piece = requests.get(piece_image)
    with open("background.png", "wb") as file:
        file.write(response_back.content)
    with open("piece.png", "wb") as file:
        file.write(response_piece.content)
    piece_img = Image.open("piece.png")
    piece_img_cropped = piece_img.crop((155, 504, 245, 594))
    piece_img_cropped.save("piece_cropped.png", quality=95)
    solver = PuzleSolver("background.png", "piece_cropped.png")
    distance = solver.get_position()
    print("Distance:", solver.get_position())


# Wait for the slider to load inside the second iframe
slider = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt='slider']"))
)


# Perform the sliding action
actions = webdriver.ActionChains(driver)
movable_distance = int(distance / 2.7)
actions.click_and_hold(slider).move_by_offset(movable_distance, 0).release().perform()

# Wait for verification or further actions
time.sleep(10)

# Close the browser
driver.quit()
print("Browser closed")
>>>>>>> 824bf48c18ffc234589ed90833f051c8611acb9d
