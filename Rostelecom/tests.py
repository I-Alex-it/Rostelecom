import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import AuthLocators, RegLocators
from config import *
import time


class TestRostelecomAuth:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        yield
        self.driver.quit()

    def perform_auth(self, auth_tab_locator, username_value, password_value, should_fail=False):
        """Общий метод для выполнения авторизации"""
        self.driver.get(MAIN_URL)

        # Выбираем таб авторизации
        self.wait.until(EC.element_to_be_clickable(auth_tab_locator)).click()

        # Вводим логин и пароль
        self.wait.until(EC.element_to_be_clickable(AuthLocators.AUTH_USERNAME)).send_keys(username_value)
        self.wait.until(EC.element_to_be_clickable(AuthLocators.AUTH_PASSWORD)).send_keys(password_value)

        # Обработка капчи (если появилась)
        try:
            captcha = self.wait.until(EC.presence_of_element_located(AuthLocators.AUTH_CAPTCHA))
            print("Пожалуйста, введите капчу вручную в течение 5 секунд")
            time.sleep(5)
        except:
            pass

        # Нажимаем кнопку входа
        self.wait.until(EC.element_to_be_clickable(AuthLocators.AUTH_BTN)).click()

        # Проверяем наличие/отсутствие сообщения об ошибке
        if should_fail:
            error_msg = self.wait.until(EC.presence_of_element_located(AuthLocators.AUTH_FORM_ERROR))
            assert error_msg.is_displayed(), "Сообщение об ошибке должно отображаться"
        else:
            with pytest.raises(Exception):
                WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(AuthLocators.AUTH_FORM_ERROR))
            assert "auth" not in self.driver.current_url.lower()

    def perform_registration(self, first_name, last_name, region, email, password, confirm_password, should_fail=False):
        """Общий метод для выполнения регистрации"""
        self.driver.get(MAIN_URL)
        self.wait.until(EC.element_to_be_clickable(AuthLocators.AUTH_REGISTER)).click()

        # Заполняем форму
        self.wait.until(EC.element_to_be_clickable(RegLocators.REG_FIRSTNAME)).send_keys(first_name)
        self.wait.until(EC.element_to_be_clickable(RegLocators.REG_LASTNAME)).send_keys(last_name)

        # Выбор региона
        region_input = self.wait.until(EC.element_to_be_clickable(RegLocators.REG_REGION))
        region_input.click()
        region_input.send_keys(region[:5])

        self.driver.execute_script(f"""
            var options = document.querySelectorAll('.rt-select__list-item');
            for (var i = 0; i < options.length; i++) {{
                if (options[i].textContent.includes('{region}')) {{
                    options[i].click();
                    break;
                }}
            }}
        """)

        # Заполняем остальные поля
        self.wait.until(EC.element_to_be_clickable(RegLocators.REG_ADDRESS)).send_keys(email)
        self.wait.until(EC.element_to_be_clickable(RegLocators.REG_PASSWORD)).send_keys(password)
        self.wait.until(EC.element_to_be_clickable(RegLocators.REG_PASS_CONFIRM)).send_keys(confirm_password)

        # Отправляем форму
        self.wait.until(EC.element_to_be_clickable(RegLocators.REG_BTN)).click()

        # Проверяем результат
        if should_fail:
            error_msg = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//span[contains(@class, 'rt-input-container__meta--error')]")))
            assert error_msg.is_displayed(), "Сообщение об ошибке должно отображаться"
        else:
            with pytest.raises(Exception):
                WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(
                    (By.XPATH, "//span[contains(@class, 'rt-input-container__meta--error')]")))

    # 1-4: Тесты авторизации с разными типами учетных данных (позитивные)
    def test_auth_with_valid_phone(self):
        self.perform_auth(AuthLocators.AUTH_PHONE, valid_phone, valid_password)

    def test_auth_with_valid_email(self):
        self.perform_auth(AuthLocators.AUTH_MAIL, valid_mail, valid_password)

    def test_auth_with_valid_login(self):
        self.perform_auth(AuthLocators.AUTH_LOGIN, valid_login, valid_password)

    def test_auth_with_valid_ls(self):
        self.perform_auth(AuthLocators.AUTH_LS, valid_ls, valid_password)

    # 5-8: Тесты авторизации с невалидными данными (негативные)
    def test_auth_with_invalid_phone(self):
        self.perform_auth(AuthLocators.AUTH_PHONE, invalid_phone, valid_password, should_fail=True)

    def test_auth_with_invalid_email(self):
        self.perform_auth(AuthLocators.AUTH_MAIL, invalid_mail, valid_password, should_fail=True)

    def test_auth_with_invalid_login(self):
        self.perform_auth(AuthLocators.AUTH_LOGIN, invalid_login, valid_password, should_fail=True)

    def test_auth_with_invalid_ls(self):
        self.perform_auth(AuthLocators.AUTH_LS, invalid_ls, valid_password, should_fail=True)

    # 9: Тест авторизации с неверным паролем
    def test_auth_with_invalid_password(self):
        self.perform_auth(AuthLocators.AUTH_PHONE, valid_phone, invalid_password, should_fail=True)

    # 10: Тест автоматического переключения табов
    def test_auto_tab_switching(self):
        self.driver.get(MAIN_URL)
        username_field = self.wait.until(EC.element_to_be_clickable(AuthLocators.AUTH_USERNAME))
        username_field.send_keys("test@example.com")
        mail_tab = self.wait.until(EC.presence_of_element_located(AuthLocators.AUTH_MAIL))
        assert "rt-tab--active" in mail_tab.get_attribute("class")

        username_field.clear()
        username_field.send_keys("79000000000")
        phone_tab = self.wait.until(EC.presence_of_element_located(AuthLocators.AUTH_PHONE))
        assert "rt-tab--active" in phone_tab.get_attribute("class")

    # 11-21: Тесты регистрации (граничные значения и классы эквивалентности)

    # 11: Регистрация с минимально допустимой длиной имени (2 символа)
    def test_reg_min_length_name(self):
        self.perform_registration(
            first_name="Ив",
            last_name="Пе",
            region="Москва г",
            email="test@example.com",
            password="ValidPass1!",
            confirm_password="ValidPass1!"
        )

    # 12: Регистрация с максимально допустимой длиной имени (30 символов)
    def test_reg_max_length_name(self):
        self.perform_registration(
            first_name=max_length_name,
            last_name=max_length_name,
            region="Москва г",
            email="test@example.com",
            password="ValidPass1!",
            confirm_password="ValidPass1!"
        )

    # 13: Регистрация с именем из цифр (недопустимый формат)
    def test_reg_name_with_digits(self):
        self.perform_registration(
            first_name=invalid_first_name,
            last_name=invalid_first_name,
            region="Москва г",
            email="test@example.com",
            password="ValidPass1!",
            confirm_password="ValidPass1!",
            should_fail=True
        )

    # 14: Регистрация с именем из спецсимволов (недопустимый формат)
    def test_reg_name_with_special_chars(self):
        self.perform_registration(
            first_name=name_with_special_chars,
            last_name=name_with_special_chars,
            region="Москва г",
            email="test@example.com",
            password="ValidPass1!",
            confirm_password="ValidPass1!",
            should_fail=True
        )

    # 15: Регистрация с пробелами в имени (должны триммиться)
    def test_reg_name_with_spaces(self):
        self.perform_registration(
            first_name=name_with_spaces,
            last_name=name_with_spaces,
            region="Москва г",
            email="test@example.com",
            password="ValidPass1!",
            confirm_password="ValidPass1!"
        )

    # 16: Регистрация с неверным форматом email
    def test_reg_invalid_email_format(self):
        self.perform_registration(
            first_name="Иван",
            last_name="Петров",
            region="Москва г",
            email=invalid_email,
            password="ValidPass1!",
            confirm_password="ValidPass1!",
            should_fail=True
        )

    # 17: Регистрация с пробелами в email (должны триммиться)
    def test_reg_email_with_spaces(self):
        self.perform_registration(
            first_name="Иван",
            last_name="Петров",
            region="Москва г",
            email=email_with_spaces,
            password="ValidPass1!",
            confirm_password="ValidPass1!"
        )

    # 18: Регистрация со слабым паролем (менее 8 символов)
    def test_reg_short_password(self):
        self.perform_registration(
            first_name="Иван",
            last_name="Петров",
            region="Москва г",
            email="test@example.com",
            password=invalid_pass,
            confirm_password=invalid_pass,
            should_fail=True
        )

    # 19: Регистрация с несовпадающими паролями
    def test_reg_password_mismatch(self):
        self.perform_registration(
            first_name="Иван",
            last_name="Петров",
            region="Москва г",
            email="test@example.com",
            password="ValidPass1!",
            confirm_password="Different1!",
            should_fail=True
        )

    # 20: Регистрация с пустым обязательным полем
    def test_reg_empty_required_field(self):
        self.perform_registration(
            first_name="",
            last_name="Петров",
            region="Москва г",
            email="test@example.com",
            password="ValidPass1!",
            confirm_password="ValidPass1!",
            should_fail=True
        )

    # 21: Регистрация с валидными данными (положительный сценарий)
    def test_reg_with_valid_data(self):
        self.perform_registration(
            first_name="Иван",
            last_name="Петров",
            region="Москва г",
            email="test@example.com",
            password="ValidPass1!",
            confirm_password="ValidPass1!"
        )