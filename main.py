from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Product():
    def __init__(self):
        self._name = None
        self._old_price = None
        self._current_price = None
        self._added_info = None

    def get_name(self):
        return self._name

    def get_old_price(self):
        return self._old_price

    def get_current_price(self):
        return self._current_price

    def get_added_info(self):
        return self._added_info

    # Setter methods
    def set_name(self, name):
        self._name = name

    def set_old_price(self, old_price):
        self._old_price = old_price

    def set_current_price(self, current_price):
        self._current_price = current_price

    def set_added_info(self, percentage):
        self._added_info = percentage


class Scraper:
    def __init__(self, url: str):
        self._url = url
        self._product_list = []
        self._driver = webdriver.Chrome()
        self._wait = WebDriverWait(self._driver, 1)

    def retrieve_product_list(self) -> []:
        pass

    def show_product_list(self):
        for product in self._product_list:
            old_price_string = lambda price: "nicht vorhanden" if price is None else f"{price}€"
            added_info_string = lambda info: "nicht vorhanden" if info is None else info

            print(
                f"{product.get_name()} - Preis: {product.get_current_price()}€ - vorheriger Preis: {old_price_string(product.get_old_price())} - Zusätzliche Informationen: {added_info_string(product.get_added_info())}"
            )
            print("")

    def _get_product_elements(self) -> []:
        pass

    def _element_get_product_name(self, element) -> str:
        pass

    def _element_get_product_current_price(self, element) -> float:
        pass

    def _element_get_product_old_price(self, element) -> float | None:
        pass

    def _element_get_product_additional_info(self, element) -> str | None:
        pass

    def _load_whole_page(self, web_driver: webdriver.Chrome, web_driver_wait: WebDriverWait):
        pass

    def get_product_list(self):
        return self._product_list

    def set_product_list(self, product_list: []):
        self._product_list = product_list


class LidlScraper(Scraper):
    def __init__(self, url: str):
        super().__init__(url)

    def retrieve_product_list(self) -> []:
        self._driver.get(self._url)
        try:
            elements = self._get_product_elements()
            for element in elements:
                product = Product()
                product.set_name(self._element_get_product_name(element))
                product.set_current_price(self._element_get_product_current_price(element))
                product.set_old_price(self._element_get_product_old_price(element))
                product.set_added_info(self._element_get_product_additional_info(element))
                self._product_list.append(product)
        finally:
            self._driver.quit()
        return self._product_list

    def _get_product_elements(self) -> []:
        try:
            self._load_whole_page(self._driver, self._wait)
            elements = self._driver.find_elements(By.XPATH, "//div[@class='product-grid-box grid-box']")
            return elements
        except:
            print("no products found")


    def _load_whole_page(self, web_driver: webdriver.Chrome, web_driver_wait: WebDriverWait):
        try:
            window_height = self._driver.execute_script("return window.innerHeight;")
            while True:
                num_elements_before = len(web_driver.find_elements(By.XPATH, "//div[@class='product-grid-box grid-box']"))
                web_driver.execute_script(f"window.scrollBy(0, {window_height});")
                web_driver_wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='product-grid-box grid-box']")))
                num_elements_after = len(web_driver.find_elements(By.XPATH, "//div[@class='product-grid-box grid-box']"))
                if num_elements_after == num_elements_before:
                    break
        except:
            print("Elemente nicht gefunden")

    def _element_get_product_name(self, element) -> str:
        name_element = element.find_element(By.XPATH, ".//h2[@class='grid-box__headline grid-box__text--dense']")
        name = name_element.text.strip()
        return name

    def _element_get_product_current_price(self, element) -> float:
        current_price_element = element.find_element(By.XPATH, ".//div[@class='m-price__price m-price__price--small']")
        text = current_price_element.text
        return float(text.replace('-', '0'))

    def _element_get_product_old_price(self, element) -> float | None:
        try:
            old_price_element = element.find_element(By.XPATH, ".//span[@class='strikethrough  m-price__rrp']")
            text = old_price_element.text
            return float(text.replace('-', '0'))
        except:
            return None

    def _element_get_product_additional_info(self, element) -> str | None:
        try:
            added_info_element = element.find_element(By.XPATH, ".//div[@class='m-price__label']")
            text = added_info_element.text
            return text
        except:
            return None




url = 'https://www.lidl.de/c/billiger-montag/a10006065?channel=store&tabCode=Current_Sales_Week'
lidl_scraper = LidlScraper(url)
lidl_scraper.retrieve_product_list()
lidl_scraper.show_product_list()

