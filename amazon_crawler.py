from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import xlsxwriter


# from data import codes

class AmazonCrawler:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-extensions')

    _asin = ""
    _product_description = ""
    _price_symbol = ""

    _seller_list = []
    _price_list = []
    _shippers = []
    _imports = []
    _delivery_details = []
    _seller_ratings = []
    _product_codes = []

    _data = []

    def __init__(self, url):
        self.url = url
        self._data.clear()

    def price_crawler(self):

        driver = webdriver.Chrome('chromedriver')

        _split_url = self.url.split("/")

        if len(_split_url) > 1:
            self._asin = _split_url[5]
        else:
            self._asin = _split_url[0]

        print(self._asin)

        driver.get('https://www.amazon.ae/dp/' + self._asin.strip() + '/ref=olp_aod_redir?_encoding=UTF8&aod=1')

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

        self._product_description = element.text

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
                self._price_symbol = price.find_element_by_class_name("a-price-symbol").text
                price_whole = price.find_element_by_class_name("a-price-whole").text
                price_fraction = price.find_element_by_class_name("a-price-fraction").text

                if price_whole:
                    self._price_list.append(f"{price_whole}.{price_fraction}")
                    self._product_codes.append(self._asin)

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
                self._delivery_details.append(details)

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
                    self._shippers.append(shipper)
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
                        self._seller_list.append(seller)
                        self._seller_ratings.append(seller_rating)

                except:
                    self._seller_list.append("Amazon.ae")
                    self._seller_ratings.append("No ratings")
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

        print(self._seller_list)

        self._data = [{"seller": seller,
                       "price": price,
                       "shipped_by": shipper,
                       "delivery": delivery,
                       "ratings": ratings.replace("\n", " ")}
                      for seller, price, shipper, delivery, ratings in zip(self._seller_list,
                                                                           self._price_list,
                                                                           self._shippers,

                                                                           self._delivery_details,
                                                                           self._seller_ratings)]

        data = {
            "code": self._asin,
            "description": self._product_description,
            "currency": self._price_symbol,
            "data": self._data,
            # "date": datetime.datetime.now()
        }

        return data

    # def export_excel(self, *args):
    #
    #     out_workbook = xlsxwriter.Workbook("amazon-prices.xlsx")
    #     out_sheet = out_workbook.add_worksheet()
    #
    #     out_sheet.write("A1", "ASIN")
    #     out_sheet.write("B1", "Seller")
    #     out_sheet.write("C1", "Price")
    #     out_sheet.write("D1", "Shipped By")
    #     out_sheet.write("E1", "Imports")
    #     out_sheet.write("F1", "Delivery")
    #     out_sheet.write("G1", "Rating")
    #
    #     for item in range(len(*args[0])):
    #         out_sheet.write(item + 1, 0, product_codes[item])
    #         out_sheet.write(item + 1, 1, seller_list[item])
    #         out_sheet.write(item + 1, 2, price_list[item])
    #         out_sheet.write(item + 1, 3, shippers[item])
    #         out_sheet.write(item + 1, 4, imports[item])
    #         out_sheet.write(item + 1, 5, delivery_details[item])
    #         out_sheet.write(item + 1, 6, seller_ratings[item])
    #
    #     out_workbook.close()
