from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def price_crawler(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-extensions')
    price_symbol = ""

    seller_list = []
    price_list = []
    shippers = []
    imports = []
    delivery_details = []
    seller_ratings = []
    product_codes = []

    data = []

    driver = webdriver.Chrome('chromedriver')

    split_url = url.split("/")

    if len(split_url) > 1:
        asin = split_url[5]
    else:
        asin = split_url[0]

    driver.get('https://www.amazon.ae/dp/' + asin.strip() + '/ref=olp_aod_redir?_encoding=UTF8&aod=1')

    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'all-offers-display-scroller')),
    )

    driver.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight)', element)
    print("scrolled down")
    driver.execute_script('arguments[0].scrollTo(0, 0)', element)
    print("scrolled up")

    driver.implicitly_wait(5)

    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'aod-asin-title-text'))
    )

    product_description = element.text

    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'aod-pinned-offer-show-more-link'))
        )
        element.click()
        print("see more button clicked")
    except TimeoutException:
        print("see more button click failed")
        pass

    try:

        element = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@id,'aod-price-')]"))
        )

        for price in element:
            price_symbol = price.find_element_by_class_name("a-price-symbol").text
            price_whole = price.find_element_by_class_name("a-price-whole").text
            price_fraction = price.find_element_by_class_name("a-price-fraction").text

            if price_whole:
                price_list.append(f"{price_whole}.{price_fraction}")
                product_codes.append(asin)

        print("prices colledted")
    except:
        print("prices collection problem")
        pass
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.ID, "ddmDeliveryMessage"))
        )

        for delivery_detail in element:
            details = delivery_detail.text
            delivery_details.append(details)

        print("delivery details collected")
    except:
        print("delivery details collection failed")
        pass
    try:
        element = WebDriverWait(driver, 5).until(
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
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.ID, "aod-offer-soldBy"))
        )

        for sold_by in element:
            try:
                seller = sold_by.find_element_by_class_name("a-link-normal").text
                seller_rating = sold_by.find_element_by_id("aod-offer-seller-rating").text
                if seller:
                    seller_list.append(seller)
                    seller_ratings.append(seller_rating)

            except:
                seller_list.append("Amazon.ae")
                seller_ratings.append("No ratings")
                continue
        print("seller collected")

    except:
        print("seller collection failed")
        pass

    driver.quit()

    # try:
    #     element = WebDriverWait(driver, 5).until(
    #         EC.presence_of_all_elements_located((By.ID, "aod-import-badge"))
    #     )
    #     for int_ship in element:
    #         try:
    #             int_ship.find_element(By.ID, 'aod-import-badge')
    #             self._imports.append("International Shipping")
    #         except:
    #             self._imports.append("Does not import internationally")
    #             continue
    # except:
    #     pass

    data = [{"seller": seller,
             "price": price,
             "shipped_by": shipper,
             "delivery": delivery,
             "ratings": ratings.replace("\n", " ")}
            for seller, price, shipper, delivery, ratings in zip(seller_list,
                                                                 price_list,
                                                                 shippers,
                                                                 delivery_details,
                                                                 seller_ratings)]

    data_list = {
        "code": asin,
        "description": product_description,
        "currency": price_symbol,
        "data": data,
        # "date": datetime.datetime.now()
    }

    return data_list
