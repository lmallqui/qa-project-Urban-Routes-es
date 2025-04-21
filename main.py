import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

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
            time.sleep(1)   #Se indica al comienzo no modificar
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    #Localizadores del formulario de ruta
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    button_round = (By.CLASS_NAME, 'button round')

    #Localizadores para seleccionar tarifa
    button_comfort = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]')

    #Localizadores para agregar numero de telefono
    button_phone_number = (By.CLASS_NAME, 'np-text')
    phone_number = (By.ID, 'phone')
    button_add_number = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[1]/form/div[2]/button')
    phone_code = (By.ID, 'code')
    button_confirm_code = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/form/div[2]/button[1]')

    #Localizadores para agregar metodo de pago
    button_payment_method = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[2]')
    button_add_card = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div[2]/div[3]')
    card_number = (By.CSS_SELECTOR, '#number')  #cambio de selector
    card_cvv = (By.XPATH, '//div[@class="card-code-input"]/input[@id="code"]')
    button_add_new_card = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')
    button_close_payment = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')

    #Localizadores para agregar mensaje para el conductor
    comment_for_the_driver = (By.CSS_SELECTOR, '#comment')  #cambio de selector

    #Localizadores de requisitos del pedido
    slide_blanket_scarves = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span')
    button_icecream_increase = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')
    icecream_count = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[2]')

    #Localizadores para solicitar orden
    button_start_order = (By.CLASS_NAME, 'smart-button')

    #Localizadores de detalles de la orden
    order_details = (By.XPATH, '//*[@id="root"]/div/div[5]/div[2]')

    def __init__(self, driver):
        self.driver = driver

    #Metodos para el formulario de ruta
    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def select_taxi(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*self.button_round).click()

    #Metodos para seleccionar tarifa
    def select_comfort_taxi(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*self.button_comfort).click()

    #Metodos para agregar numero de telefono
    def select_phone_number(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*self.button_phone_number).click()

    def input_phone_number(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*self.phone_number).send_keys(data.phone_number)

    def set_phone(self):
        self.driver.implicitly_wait(15)
        self.select_phone_number()
        self.driver.implicitly_wait(15)
        self.input_phone_number()

    def select_next_button(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*self.button_add_number).click()

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_number).get_property('value')

    def set_code(self):
        phone_code = retrieve_phone_code(driver=self.driver)
        self.driver.implicitly_wait(15)
        self.driver.find_element(*self.phone_code).send_keys(phone_code)

    def select_confirm_code(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*self.button_confirm_code).click()

    #Metodos para ingresar metodo de pago
    def select_payment_method(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*self.button_payment_method).click()

    def select_add_card(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*self.button_add_card).click()

    def add_card(self):
        self.driver.implicitly_wait(15)
        self.select_payment_method()
        self.driver.implicitly_wait(15)
        self.select_add_card()

    def input_card_number(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*self.card_number).send_keys(data.card_number)

    def get_card_number(self):
        return self.driver.find_element(*self.card_number).get_property('value')

    def input_cvv_card(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*self.card_cvv).send_keys(data.card_code)

    def get_cvv_card(self):
        return self.driver.find_element(*self.card_cvv).get_property('value')

    def select_register_card(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*self.button_add_new_card).click()

    def add_new_card(self):
        self.driver.implicitly_wait(15)
        self.input_card_number()
        self.driver.implicitly_wait(15)
        self.input_cvv_card()
        self.driver.implicitly_wait(15)
        self.select_register_card()

    def close_modal(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*self.button_close_payment).click()

    #Metodos para ingresar comentario al conductor
    def send_comment(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*self.comment_for_the_driver).send_keys(data.message_for_driver)

    def get_comment(self):
        return self.driver.find_element(*self.comment_for_the_driver).get_property('value')

    #Metodos para requisitos del pedido
    def select_blanket_scarves(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*self.slide_blanket_scarves).click()

    def get_slide(self):
        return self.driver.find_element(*self.slide_blanket_scarves).is_selected()

    def select_icecream(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*self.button_icecream_increase).click()
        self.driver.find_element(*self.button_icecream_increase).click()

    def get_icecream(self):
        return self.driver.find_element(*self.icecream_count).text

    #Metodos para solicitar orden
    def select_order(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*self.button_start_order).click()

    #Metodos para visualizar detalle de la orden
    def get_order(self):
        return self.driver.find_element(*self.order_details).text

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

    # 1. Definir rutas
    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    # 2. Seleccionar tarifa comfort
    def test_select_taxi(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.select_taxi()
        routes_page.select_comfort_taxi()
        comfort_button = self.driver.find_element(routes_page.button_comfort)
        assert 'tcard active' in comfort_button.get_attribute('class'), "No fue seleccionada la tarifa Comfort"

    # 3. Definir numero de telefono
    def test_phone_number(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_phone()
        routes_page.select_next_button()
        routes_page.set_code()
        routes_page.select_confirm_code()
        phone_number = routes_page.get_phone_number()
        assert phone_number == data.phone_number, f'Telefono ingresado es incorrecto, debe ser: "{data.phone_number}"'

    # 4. Definir metodo de pago
    def test_payment_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.add_card()
        routes_page.add_new_card()
        routes_page.close_modal()
        card_number = routes_page.get_card_number()
        assert card_number == data.card_number, f'El número de tarjeta es incorrecto, debe ser: "{data.card_number}"'
        cvv_card = routes_page.get_cvv_card()
        assert cvv_card == data.card_code, f'El cvv de la tarjeta es incorrecto, debe ser: "{data.card_code}"'

    # 5. Definir comenario para el conductor
    def test_send_comment(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.send_comment()
        comment_driver = routes_page.get_comment()
        assert comment_driver == data.message_for_driver, f'El mensaje para el conductor es incorrecto, debe ser: "{data.message_for_driver}"'

    # 6. Definir manta y pañuelo
    def test_slide_blank_scarves(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.select_blanket_scarves()
        on_slide = routes_page.get_slide()
        assert on_slide == True, f'No se encuentra activo el requisito de manta y pañuelo'

    # 7. Definir 2 helados
    def test_add_icecream(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.select_icecream()
        count_icecream = routes_page.get_icecream()
        assert count_icecream == '2', f"No ha seleccionado 2 helados"

    # 8. Solicitar orden de taxi
    def test_order_taxi(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.select_order()
        order_taxi = routes_page.get_order()
        assert 'Buscar automóvil' in order_taxi, 'No se pudo solicitar un taxi'

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
