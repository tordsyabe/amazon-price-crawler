from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import datetime


def amazon_crawler(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-extensions')
    price_symbol = ""
    webpage = ""
    data = []

    seller_list = []
    price_list = []
    shippers = []
    imports = []
    delivery_details = []
    seller_ratings = []
    product_codes = []

    date_today = datetime.datetime.now()
    timestamp = date_today.strftime("%Y-%m-%d %H:%M:%S")

    driver = webdriver.Chrome('chromedriver')

    split_url = url.split("/")

    if len(split_url) > 1:
        for item in split_url:

            if "www." in item:
                webpage = item
            if "B0" in item:
                asin = item
                break

    else:
        asin = split_url[0]

    print(asin)

    driver.get('https://www.amazon.ae/dp/' + asin.strip() + '/ref=olp_aod_redir?_encoding=UTF8&aod=1')
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'all-offers-display-scroller')),
        )

        driver.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight)', element)
        print("scrolled down")
        driver.execute_script('arguments[0].scrollTo(0, 0)', element)
        print("scrolled up")
    except:
        print("failed")
        pass

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'aod-asin-title-text'))
        )

        product_description = element.text
    except:
        print("Failed to collect product description")
        pass

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'aod-asin-reviews-count-title'))
        )
        product_rating = element.text
    except:
        print("Failed to collect product raitings")
        pass

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="aod-pinned-offer-show-more-link"]'))
        )
        element.click()
        print("see more button clicked")
    except:
        print("see more button click failed")
        driver.quit()
        return {
            "code": asin,
            "description": product_description,
            "product_rating": "N/A",
            "currency": "N/A",
            "data": [],
            "webpage": webpage,
            "date": timestamp,
            "error": "Product currently has no sellers."
        }

    try:

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "a-price"))
        )

        for price in element:
            price_symbol = price.find_element_by_class_name("a-price-symbol").text
            price_whole = price.find_element_by_class_name("a-price-whole").text
            price_fraction = price.find_element_by_class_name("a-price-fraction").text

            if price_whole:
                price_list.append(f"{price_whole}.{price_fraction}")
                product_codes.append(asin)

        print("prices collected")
    except:
        print("prices collection problem")
        pass
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.ID, "ddmDeliveryMessage"))
        )

        for delivery_detail in element:
            details = delivery_detail.text
            if details:
                delivery_details.append(details)

        print("delivery details collected")
    except:
        print("delivery details collection failed")
        pass
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.ID, "aod-offer-shipsFrom"))
        )

        for sold_by in element:
            shipper = sold_by.find_element_by_class_name("a-color-base").text
            if shipper:
                shippers.append(shipper)
        print("shipper details collected")
    except:
        print("shipper details collection failed")
        pass
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.ID, "aod-offer-soldBy"))
        )

        for sold_by in element:
            try:
                seller = sold_by.find_element_by_class_name('a-link-normal').text
                seller_rating = sold_by.find_element_by_id("seller-rating-count-{iter}").text

                if seller:
                    seller_list.append(seller)

                if seller:
                    seller_ratings.append(seller_rating)


            except:
                print("seller or seller rating collection failed")
                seller = "Amazon.ae"
                seller_list.append(seller)
                seller_ratings.append("No ratings")
                pass

            try:
                import_badge = sold_by.find_element_by_id('aod-import-badge').text
                if seller:
                    imports.append(import_badge)
            except:
                if seller:
                    imports.append("Does not import internationally")

        print("seller collected")

    except:
        print("seller collection failed")
        pass

    driver.quit()

    print(len(seller_list), len(price_list), len(shippers), len(delivery_details), len(seller_ratings), len(imports))
    print(seller_list)
    print(price_list)
    print(shippers)
    print(delivery_details)
    print(seller_ratings)
    print(imports)

    data = [{"seller": seller,
             "price": price,
             "shipped_by": shipper,
             "delivery": delivery,
             "ratings": ratings.replace("\n", " "),
             "import": imports}
            for seller, price, shipper, delivery, ratings, imports in zip(seller_list,
                                                                          price_list,
                                                                          shippers,
                                                                          delivery_details,
                                                                          seller_ratings,
                                                                          imports)]

    it = iter([seller_list, price_list, shippers, delivery_details, seller_ratings, imports])
    the_len = len(next(it))
    if not all(len(l) == the_len for l in it):
        return {
            "code": asin,
            "description": product_description,
            "product_rating": product_rating,
            "currency": price_symbol,
            "data": data,
            "webpage": webpage,
            "date": timestamp,
            "error": "There was a problem with the data collected"
        }

    data_list = {
        "code": asin,
        "description": product_description,
        "product_rating": product_rating,
        "currency": price_symbol,
        "data": data,
        "webpage": webpage,
        "date": timestamp,
        "error": ""
    }

    return data_list
