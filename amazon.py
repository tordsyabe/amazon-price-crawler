from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import os
from dotenv import load_dotenv

load_dotenv()


def amazon_crawler(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    # os.environ.get("CHROMEDRIVER_PATH")
    webpage = ""
    pinned_price_symbol = ""
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

    split_url = url.split("/")

    search_result = 0

    if len(split_url) > 1:
        for item in split_url:

            if "www." in item:
                webpage = item

            if "B0" in item:
                asin = item
                break

    else:
        asin = split_url[0]
        webpage = "www.amazon.ae"

    print(asin)
    product_url_link = 'https://' + webpage + '/dp/' + asin.strip() + '/ref=olp_aod_redir?_encoding=UTF8&aod=1'
    driver.get(product_url_link)
    print(product_url_link)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'all-offers-display-scroller')),
        )

        driver.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight)', element)
        print("scrolled down")
        driver.execute_script('arguments[0].scrollTo(0, 0)', element)
        print("scrolled up")
    except:
        print("failed to scroll down and up")
        pass

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'aod-asin-title-text'))
        )

        product_description = element.text
    except:
        print("Failed to collect product description")
        product_description = "N/A"
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
            EC.presence_of_element_located((By.XPATH, '//a[@id="aod-pinned-offer-show-more-link"]'))
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
            "error": "Product currently has no sellers.",
            "number_of_results": 0,
            "product_url_link": product_url_link
        }

    try:

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="pinned-offer-top-id"]'))
        )

        pinned_price_symbol = element.find_element_by_xpath(
            './/div[contains(@id, "aod-price")]/span/span[2]/span[1]').text

        pinned_price_whole = element.find_element_by_xpath(
            './/div[contains(@id, "aod-price")]/span/span[2]/span[2]').text

        pinned_price_fraction = element.find_element_by_xpath(
            './/div[contains(@id, "aod-price")]/span/span[2]/span[3]').text
        pinned_delivery = element.find_element_by_xpath('.//*[@class="a-row aod-delivery-promise"]').text
        price_list.append(f"{pinned_price_whole}.{pinned_price_fraction}")
        delivery_details.append(pinned_delivery)

        if pinned_price_whole:
            search_result += 1

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
            pinned_seller_rating = element.find_element_by_xpath('.//span[@id="seller-rating-count-{iter}"]/span').text
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
                delivery = aod_offer.find_element_by_xpath('.//*[@class="a-row aod-delivery-promise"]').text

            except:
                delivery = aod_offer.find_element_by_xpath('.//div[@class="a-row aod-ship-charge"]').text
                pass

            ship_by = aod_offer.find_element_by_xpath('.//div[@id="aod-offer-shipsFrom"]/div/div/div[2]/*').text

            vendor = aod_offer.find_element_by_xpath('.//div[@id="aod-offer-soldBy"]/div/div/div[2]/*').text
            # vendor = WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.XPATH, './/div[@id="aod-offer-shipsFrom"]'))
            # )
            print("SELLER: ", vendor)

            # v = vendor.find_element_by_tag_name('a').text
            # seller_list.append(v.text)
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
            # print(rating)
            # print(price_whole + "." + price_fraction, ship_by, delivery)
            price_list.append(f"{price_whole}.{price_fraction}")
            shippers.append(ship_by)
            delivery_details.append(delivery)
            seller_ratings.append(rating)
            imports.append(seller_import)
            seller_list.append(vendor)



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
            "currency": pinned_price_symbol,
            "data": data,
            "webpage": webpage,
            "date": timestamp,
            "error": "There was a problem with the data collected",
            "number_of_results": len(aod_offers) + search_result,
            "product_url_link": product_url_link
        }

    data_list = {
        "code": asin,
        "description": product_description,
        "product_rating": product_rating,
        "currency": pinned_price_symbol,
        "data": data,
        "webpage": webpage,
        "date": timestamp,
        "error": "",
        "number_of_results": len(aod_offers) + search_result,
        "product_url_link": product_url_link

    }

    return data_list
