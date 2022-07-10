import csv
import time
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By
EXE_PATH = r'C:\SmartCitySirius\chromedriver.exe'
review = {
    "name": '',
    "rating": 0,
    "text": '',
    "date": '',
    "departmentLink": ''
}
count = 0
hrefs = []
squares = []
departmentReviews = []
squaresReviews = []
kaliningradSquare = \
    'https://www.google.ru/maps/search/%D0%B3%D0%B0%D0%B7%D0%BF%D1%80%D0%BE%D0%BC%D0%B1%D0%B0%D0%BD%D0%BA/@54.8047619,20.7674278,9z'
sochiSquare = 'https://www.google.ru/maps/search/%D0%B3%D0%B0%D0%B7%D0%BF%D1%80%D0%BE%D0%BC%D0%B1%D0%B0%D0%BD%D0%BA/@43.5811411,39.962384,10.83z'
fuckingLink = 'https://www.google.ru/maps/place/%D0%93%D0%B0%D0%B7%D0%BF%D1%80%D0%BE%D0%BC%D0%B1%D0%B0%D0%BD%D0%BA/data=!4m6!3m5!1s0x40f5bfc1f77b4721:0x4df1cca2ea98d9b6!8m2!3d43.4382132!4d39.9136374!16s%2Fg%2F11mfvhl5d4?authuser=0&hl=ru&rclk=1'


def getDepartmentReviews(href):
    # переход во "Все отзывы" и скролл в самый низ
    departmentReviews = []
    driver.get(href)
    try:
        buttonFullReviews = driver.find_element(By.CLASS_NAME, 'M77dve')
        if buttonFullReviews.get_attribute("aria-label") != "Об этих данных":
            buttonFullReviews.click()
            reviewsInfo = driver.find_element(By.CLASS_NAME, 'jANrlb')
            countReviews = int(reviewsInfo.text.split(":")[1])
            time.sleep(2)

            # пролистывание до отображения всех отзывов
            for i in range(0, countReviews // 10 + 1):
                endList = driver.find_elements(By.CLASS_NAME, 'qCHGyb')
                actions = ActionChains(driver)
                scroll_origin = ScrollOrigin.from_element(endList[len(endList) - 1])
                actions.scroll_from_origin(scroll_origin, 0, 200).perform()
                time.sleep(2)
    except Exception as e:
        pass
    time.sleep(3)

    # обработка отзывов
    divsReviews = driver.find_elements(By.CLASS_NAME, 'jJc9Ad')
    if len(divsReviews) == 0:
        return 0
    for el in divsReviews:
        review = {}
        # получение имени
        divName = el.find_element(By.CLASS_NAME, 'd4r55')
        review["name"] = divName.text

        # получение рейтинга
        divRating = len(el.find_elements(By.CLASS_NAME, 'vzX5Ic'))
        review["rating"] = divRating

        # получение текста
        try:
            moreTextButton = el.find_element(By.CLASS_NAME, 'w8nwRe')
            moreTextButton.click()
        except:
            pass
        divText = el.find_element(By.CLASS_NAME, 'MyEned')
        review["text"] = divText.text

        # получение даты
        divDate = el.find_element(By.CLASS_NAME, 'DU9Pgb')
        review["date"] = divDate.text

        # получение ссылки на отделение
        review["departmentLink"] = href

        departmentReviews.append(review)
    return departmentReviews


def getListBanks(square):
    getHrefs = []
    banks = []
    driver.get(square)
    banks = driver.find_elements(By.CLASS_NAME, "hfpxzc")
    print(banks)
    for el in banks:
        getHrefs.append(el.get_attribute("href"))
    return getHrefs


def getAllSquares():
    getSquares = []
    getSquares.append(kaliningradSquare)
    getSquares.append(sochiSquare)
    for width in np.arange(81, 41, -1.5, dtype=float):
        for longitude in np.arange(27, 180, 3.3, dtype=float):
            getSquares.append(f'https://www.google.ru/maps/search/%D0%B3%D0%B0%D0%B7%D0%BF%D1%80%D0%BE%D0%BC%D0%B1%D0%B0%D0%BD%D0%BA/@{width},{longitude},8z')
    return getSquares


if __name__ == '__main__':
    start_time = time.time()
    driver = webdriver.Chrome(executable_path=EXE_PATH)

    # перебор всех квадратов
    squares = getAllSquares()
    for i in range(0, len(squares)):
        # запись в файл
        if i % 10 == 0:
            df = pd.DataFrame(squaresReviews)
            df.to_csv('googleMaps.csv', encoding="utf-8-sig")

        hrefs = getListBanks(squares[i])
        if len(hrefs) == 0:
            continue
        if (fuckingLink in hrefs) and (squares[i] != sochiSquare):
            continue
        for j in range(0, len(hrefs)):
            resultReviews = getDepartmentReviews(hrefs[j])
            if resultReviews != 0:
                count += len(resultReviews)
                for elem in resultReviews:
                    if elem in squaresReviews:
                        continue
                    squaresReviews.append(elem)

    df = pd.DataFrame(squaresReviews)
    df.to_csv('googleMaps.csv', encoding="utf-8-sig")

    driver.close()
    progTime = time.time() - start_time
    print(f'Время работы программы - {progTime} секунд или {progTime / 60} минут')
    print(f'Количество полученных отзывов - {count}')