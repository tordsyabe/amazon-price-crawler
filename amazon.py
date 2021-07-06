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
        product_rating = "N/A"
        print("Failed to collect product ratings")
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
            "product_rating": product_rating,
            "currency": "N/A",
            "data": [],
            "webpage": webpage,
            "date": timestamp,
            "error": "Product currently has no sellers."
        }

    try:

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="pinned-offer-top-id"]'))
        )

        pinned_price_whole = element.find_element_by_class_name('a-price-whole').text

        pinned_price_fraction = element.find_element_by_class_name('a-price-fraction').text
        pinned_delivery = element.find_element_by_id('ddmDeliveryMessage').text
        price_list.append(f"{pinned_price_whole}.{pinned_price_fraction}")
        delivery_details.append(pinned_delivery)

    except:
        print("pinned product price and delivery collection problem")
        pass

    try:

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "aod-pinned-offer-additional-content"))
        )

        # print("PINNED OFFER CONTENT", element)

        pinned_shipper = element.find_element_by_xpath('.//*[@id="aod-offer-shipsFrom"]/div/div/div[2]/*').text
        pinned_seller = element.find_element_by_xpath('.//div[@id="aod-offer-soldBy"]/div/div/div[2]/*').text
        try:
            pinned_seller_rating = element.find_element_by_xpath('.//div[@id="seller-rating-count-{iter}"]/span').text
        except:
            pinned_seller_rating = "N/A"
            pass
        try:
            element.find_element_by_xpath('.//*[@id="aod-import-badge"]')
            pinned_seller_import = "International Shipping"
        except:
            pinned_seller_import = "No international shipping"
            pass
        shippers.append(pinned_shipper)
        seller_list.append(pinned_seller)
        seller_ratings.append(pinned_seller_rating)
        imports.append(pinned_seller_import)

        print(f"{pinned_price_whole}.{pinned_price_fraction}", pinned_delivery, pinned_shipper)
    except:
        print("pinned shipper, seller, seller rating collection problem")
        pass

    try:

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'aod-offer-list'))
        )
        # print("AOD LIST", element)
        aod_offers = element.find_elements_by_xpath('.//*[@id="aod-offer"]')

        print(len(aod_offers))

        for aod_offer in aod_offers:
            price_whole = aod_offer.find_element_by_xpath('.//span[@class="a-price-whole"]').text
            # print("PRICE", price_whole)

            price_fraction = aod_offer.find_element_by_xpath('.//span[@class="a-price-fraction"]').text
            try:
                delivery = aod_offer.find_element_by_xpath('.//div[@id="ddmDeliveryMessage"]').text

            except:
                delivery = aod_offer.find_element_by_xpath('.//div[@class="a-row aod-ship-charge"]').text
                pass

            ship_by = aod_offer.find_element_by_xpath('.//div[@id="aod-offer-shipsFrom"]/div/div/div[2]/*').text
            vendor = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, './/div[@id="aod-offer-shipsFrom"]/div/div/div[2]/a'))
            )
            # print(vendor.find_element_by_name('a'))

            try:
                rating = aod_offer.find_element_by_xpath('.//*[@id="seller-rating-count-{iter}"]/span').text
            except:
                rating = "N/A"
                pass
            try:
                aod_offer.find_element_by_xpath('.//*[@id="aod-import-badge"]')
                seller_import = "International Shipping"
            except:
                seller_import = "No international shipping"
                pass
            print(rating)
            print(price_whole + "." + price_fraction, ship_by, delivery)
            price_list.append(f"{price_whole}.{price_fraction}")
            shippers.append(ship_by)
            delivery_details.append(delivery)
            seller_ratings.append(rating)
            imports.append(seller_import)
            seller_list.append(vendor.text)


    except:
        print("offer list details collection problem")
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
