import cv2
import numpy as np


def get_points(background_path):
    # Загрузка изображения
    image = cv2.imread(background_path)

    # Преобразование изображения в градации серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применение фильтра Гаусса для сглаживания изображения
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Применение адаптивной пороговой обработки для выделения контура
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )

    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Фильтрация контуров по цвету и площади
    filtered_contours = []
    for i, contour in enumerate(contours):
        # Проверка иерархии контура
        if hierarchy[0][i][3] == -1:
            # Вычисление прямоугольной области, охватывающей контур
            x, y, w, h = cv2.boundingRect(contour)

            # Проверка площади и размеров
            if w * h >= 70 * 70 and w <= 100 and h <= 100:
                filtered_contours.append(contour)

    # Нахождение контура с наибольшей площадью
    largest_contour = max(filtered_contours, key=cv2.contourArea)

    # Вычисление координат и центра контура
    x, y, w, h = cv2.boundingRect(largest_contour)
    center_x = x + w // 2
    center_y = y + h // 2

    # Вывод координат центра
    print("Координаты центра пазла: ({}, {})".format(center_x, center_y))
    mask = np.zeros_like(gray)

    # Заливка контуров на маске
    cv2.drawContours(mask, filtered_contours, -1, (255), cv2.FILLED)

    # Применение маски к исходному изображению
    result = cv2.bitwise_and(image, image, mask=mask)

    # Отображение результата
    # cv2.imshow('Captcha', result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return center_x
