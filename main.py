import base64
import os
import shutil
from io import BytesIO
from PIL import Image

import requests as requests
import validators
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


def prepare_filename_list(dir, count):
    filenames = []
    for i in range(count):
        filenames.append(dir + '/image_' + str(i) + '.jpeg')
    return filenames


def download_from_url(path, image):
    print(path + ' --->>> ' + image)
    response = requests.get(image)
    img = Image.open(BytesIO(response.content))
    img.convert('RGB').save(path)


def download_base64(path, image):
    print(path + ' --->>> ' + 'base64')
    if not image == None:
        image = image.replace('data:image/jpeg;base64,', '')
        image = image.replace('data:image/png;base64,', '')
        try:
            img = Image.open(BytesIO(base64.b64decode(image)))
            img.convert('RGB').save(path)
        except Exception as ex:
            print(str(ex))
    else:
        print('image is null')


def prepare_url(keywords):
    query = keywords[0]
    for key in keywords:
        if keywords[0] == key:
            continue
        query += '+' + key

    return "https://www.google.com/search?q=" + query + "&rlz=1C5CHFA_enPL1017PL1017&sxsrf=AJOqlzVzHuBM-vKGgVEGxt4RsioEAWT8HA:1674830875896&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjSpaqb_-f8AhWWHuwKHTmYB4EQ_AUoAXoECAIQAw&biw=1440&bih=681&dpr=2"


def delete_adn_create_dir(dir):
    try:
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.makedirs(dir)
    except OSError as e:
        print("error during deleting and creating dir: " + str(e))
        exit(-1)


def main2(dir, keywords, count):
    delete_adn_create_dir(dir)

    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    url = prepare_url(keywords)
    driver.get(url)

    # skip_legal_page(driver) -> if legal page is shown click skip
    try:
        legal_button = driver.find_element(By.CSS_SELECTOR,
                                           '.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.LQeN7.Nc7WLe')
        legal_button.click()
    except:
        pass

    # for till count of images is equal count
    elem = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")
    while len(elem) < count:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            load_more_button = driver.find_element(By.CLASS_NAME, "mye4qd")
            if load_more_button.is_displayed():
                load_more_button.click()
        except:
            pass

        elem = driver.find_elements(By.CLASS_NAME, "Q4LuWd")

    paths = prepare_filename_list(dir, count)

    el = iter(elem)
    for i in range(count):
        element = next(el)
        driver.execute_script("arguments[0].scrollIntoView();", element)
        # element.click()
        print('image: ' + str(i) + ' filepath: ' + paths[i])
        image = element.get_property("src")

        if validators.url(image):
            download_from_url(paths[i], image)
        else:
            download_base64(paths[i], element.screenshot_as_base64)
    print('download finished')
    driver.close()
    print('files in: ' + os.path.abspath(dir))


if __name__ == '__main__':
    keywords = [
        'ICC', 'intercity'
    ]
    count = 50
    out = './downloads'

    main2(out, keywords, count)
