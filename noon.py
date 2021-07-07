from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import os


def noon_crawler(url):

    print("entered noon_crawler")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    # os.environ.get("CHROMEDRIVER_PATH")

    seller_list = []
    price_list = []
    rating_list = []
    start_list = []
    delivery_list = []
    fulfilled_list = []
    price_symbol = ""
    webpage = "www.noon.com"

    date_today = datetime.datetime.now()
    timestamp = date_today.strftime("%Y-%m-%d %H:%M:%S")

    split_url = url.split("/")

    if len(split_url) > 1:
        for item in split_url:

            if "N" in item:
                asin = item
                break

    else:
        asin = split_url[0]

    product_url_link = 'https://www.noon.com/uae-en/search?q=' + asin.strip()
    driver.get(product_url_link)

    print(product_url_link)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="productContainer"]'))
    )

    element.click()
    print("clicked! product container")

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f'//div[@data-qa="pdp-brand-{asin.strip()}"]'))
    )

    brand = element.text
    print("got brand")

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f'//h1[@data-qa="pdp-name-{asin.strip()}"]'))
    )

    desc = element.text
    print("got desc")

    product_description = brand + " " + desc

    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'allOffers'))
        )

        element.click()
        print("clicked allOffer")
    except:

        print("View all offer click failed")

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "priceNow"))
        )

        s_price = element.text

        print(s_price)

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "estimator_left"))
        )

        s_delivery = element.text

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "estimator_right"))
        )

        fulfill_img = element.find_element_by_css_selector('img')
        s_fulfilled_by = fulfill_img.get_attribute("alt")

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "storeLink"))
        )

        s_seller = element[1].text

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "starRating"))
        )

        s_star = element.text

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "detail_percentage"))
        )

        s_rating = element.text

        s_data = [{"seller": s_seller,
                   "price": s_price,
                   "shipped_by": s_fulfilled_by,
                   "delivery": s_delivery,
                   "star": s_star,
                   "ratings": s_rating}]

        s_data_list = {
            "code": asin,
            "description": product_description,
            "product_rating": "Product Rating",
            "currency": "AED",
            "data": s_data,
            "webpage": webpage,
            "date": timestamp,
            "error": "",
            "number_of_results": 1,
            "product_url_link": product_url_link
        }

        driver.quit()

        return s_data_list

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "y6omgk-1")]'))
    )

    for price in element:
        product_price = price.find_element_by_tag_name('strong')

        price_list.append(product_price.text)
        print(product_price.text)
        try:
            star = price.find_element_by_class_name('starValue')
            rating = price.find_element_by_class_name('normalizedNumber')
            start_list.append(star.text)
            rating_list.append(rating.text)
        except:
            start_list.append("No star")
            rating_list.append("No rating")

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@class="offerSname"]'))
    )

    for seller in element:
        seller_list.append(seller.text)
        print(seller.text)

    # element = WebDriverWait(driver, 10).until(
    #     EC.presence_of_all_elements_located((By.XPATH, '//div[@class="starValue"]'))
    # )
    #
    # for star_value in element:
    #     start_list.append(star_value.text)
    #     print(star_value.text)
    #
    # element = WebDriverWait(driver, 10).until(
    #     EC.presence_of_all_elements_located((By.XPATH, '//div[@class="normalizedNumber"]'))
    # )
    #
    # for rating in element:
    #     rating_list.append(rating.text)
    #     print(rating.text)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@type="cart"]/div'))
    )

    for delivery in element:
        delivery_list.append(delivery.text)
        print(delivery.text)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//img[@alt="fulfilment_express_v2"]'))
    )

    for express in element:
        fulfilled_list.append("Express")
        print("Express")

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//img[@alt="marketplace"]'))
    )

    for market in element:
        fulfilled_list.append("Market Place")
        print("Market")

    print(len(price_list), len(seller_list), len(rating_list), len(start_list), len(delivery_list), len(fulfilled_list))
    print(price_list, seller_list, rating_list, start_list, delivery_list, fulfilled_list)
    driver.quit()

    data = [{"seller": seller,
             "price": price,
             "shipped_by": fulfilled_by,
             "delivery": delivery,
             "star": star,
             "ratings": ratings}
            for seller, price, fulfilled_by, delivery, star, ratings in zip(seller_list,
                                                                            price_list,
                                                                            fulfilled_list,
                                                                            delivery_list,
                                                                            start_list,
                                                                            rating_list)]

    data_list = {
        "code": asin,
        "description": product_description,
        "product_rating": "Product Rating",
        "currency": "AED",
        "data": data,
        "webpage": webpage,
        "date": timestamp,
        "error": "",
        "number_of_results": len(price_list),
        "product_url_link": product_url_link

    }

    return data_list
