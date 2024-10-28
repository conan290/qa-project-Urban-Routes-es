import data
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options




# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas."""
    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
    return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    flash_mode = (By.XPATH, "//div[@class='mode' and text()='Flash']")
    request_taxi_button = (By.CSS_SELECTOR, 'button.button.round')
    comfort_tariff = (By.XPATH, "//div[@class='tcard-icon']/img[@alt='Comfort']")
    phone_button = (By.CLASS_NAME, "np-text")
    phone_number_input = (By.ID, 'phone')
    payment_method_button = (By.XPATH, "//div[@class='pp-button filled']")
    add_card_option = (By.XPATH, "//div[text()='Agregar tarjeta']")
    card_number_field = (By.XPATH, "//input[@id='number']")
    card_code_field = (By.XPATH, "//input[@id='code' and @class='card-input']")
    link_button = (By.XPATH, "//div[@class='pp-buttons']//button[contains(text(), 'Agregar')]")
    driver_message_field = (By.ID, 'comment')
    blanket_and_tissues_checkbox = (By.XPATH, "//span[@class='slider round']")
    ice_cream_plus_button = (By.XPATH, "//div[@class='counter-plus']")
    ice_cream_value = (By.XPATH, "//div[@class='counter-value']")

    def __init__(self, driver):
        self.driver = driver

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_attribute('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_attribute('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def open_phone_number_modal(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.phone_button)
        ).click()

    def set_from(self, from_address):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.from_field))
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.to_field))
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def select_flash_mode(self):
        self.driver.find_element(*self.flash_mode).click()

    def request_taxi(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.request_taxi_button)
        ).click()

    def select_payment_method_card(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.payment_method_button)).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.add_card_option)).click()

    def select_comfort_tariff(self):
        self.driver.find_element(*self.comfort_tariff).click()

    def set_phone_number(self, phone_number):
        phone_input = self.driver.find_element(*self.phone_number_input)
        phone_input.send_keys(phone_number)
        phone_input.send_keys(Keys.TAB)

    def add_card(self, card_number, card_code):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(self.card_number_field)).send_keys(card_number)
        cvv_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(self.card_code_field))
        cvv_input.send_keys(card_code)
        cvv_input.send_keys(Keys.TAB)
        add_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.link_button)
        )
        add_button.click()

    def send_driver_message(self, message):
        message_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.driver_message_field)
        )
        message_field.send_keys(message)

    def request_blanket_and_tissues(self):
        blanket_tissues_switch = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.blanket_and_tissues_checkbox)
        )
        blanket_tissues_switch.click()

    def request_ice_cream(self, quantity):
        self.driver.execute_script("arguments[0].scrollIntoView(true);",
                                   WebDriverWait(self.driver, 20).until(
                                       EC.presence_of_element_located(self.ice_cream_plus_button)
                                   ))

        for _ in range(quantity):
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.ice_cream_plus_button)
            ).click()

        current_value = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.ice_cream_value)
        ).text
        assert current_value == str(quantity), f"Se esperaba {quantity} helados, pero el contador muestra {current_value}"


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        chrome_options = Options()
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=chrome_options)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_set_to_address(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        to_address = data.address_to
        routes_page.set_to(to_address)
        assert routes_page.get_to() == to_address

    def test_request_taxi(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.request_taxi()
        assert "Taxi solicitado" in self.driver.page_source

    def test_select_comfort_tariff(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.request_taxi()
        routes_page.select_comfort_tariff()
        assert "Comfort" in self.driver.page_source

    def test_fill_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.request_taxi()
        routes_page.select_comfort_tariff()
        routes_page.open_phone_number_modal()
        routes_page.set_phone_number(data.phone_number)
        assert data.phone_number in self.driver.page_source

    def test_add_credit_card(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.request_taxi()
        routes_page.select_comfort_tariff()
        routes_page.select_payment_method_card()
        routes_page.add_card(data.card_number, data.card_code)
        confirmation_element = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='pp-title' and text()='Tarjeta']")))
        assert confirmation_element.is_displayed()

    def test_send_driver_message(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.request_taxi()
        routes_page.select_comfort_tariff()
        routes_page.send_driver_message(data.message_for_driver)
        assert data.message_for_driver in self.driver.page_source

    def test_request_blanket_and_tissues(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.request_taxi()
        routes_page.select_comfort_tariff()
        routes_page.request_blanket_and_tissues()
        assert "Manta y pañuelos activados" in self.driver.page_source

    def test_request_ice_cream(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.request_taxi()
        routes_page.select_comfort_tariff()
        routes_page.request_ice_cream(2)
        current_value = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(routes_page.ice_cream_value)
        ).text
        assert current_value == "2", f"Se esperaba 2 helados, pero el contador muestra {current_value}"

    def test_taxi_search_modal_appears(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.select_flash_mode()
        routes_page.request_taxi()
        routes_page.select_comfort_tariff()
        routes_page.set_phone_number(data.phone_number)
        routes_page.add_card(data.card_number, data.card_code)
        routes_page.request_blanket_and_tissues()
        routes_page.request_ice_cream(2)
        taxi_modal = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'taxi-search-modal')))
        assert taxi_modal.is_displayed()


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()



