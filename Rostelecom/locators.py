from selenium.webdriver.common.by import By


class AuthLocators:
    AUTH_PHONE = (By.ID, 't-btn-tab-phone')
    AUTH_MAIL = (By.ID, 't-btn-tab-mail')
    AUTH_LOGIN = (By.ID, 't-btn-tab-login')
    AUTH_LS = (By.ID, 't-btn-tab-ls')
    AUTH_USERNAME = (By.ID, 'username')
    AUTH_PASSWORD = (By.ID, 'password')
    AUTH_BTN = (By.ID, 'kc-login')
    AUTH_CAPTCHA = (By.ID, 'captcha')
    AUTH_FORGOT_PASS = (By.ID, 'forgot_password')
    AUTH_REGISTER = (By.ID, 'kc-register')
    AUTH_FORM_ERROR = (By.ID, 'form-error-message')
    AUTH_ACTIVE_TAB = (By.CSS_SELECTOR, 'div.rt-tab.rt-tab--active')


class RegLocators:
    REG_FIRSTNAME = (By.NAME, 'firstName')
    REG_LASTNAME = (By.NAME, 'lastName')
    REG_REGION = (By.CSS_SELECTOR,
                  'input.rt-input__input.rt-select__input.rt-input__input--rounded[autocomplete="new-password"]')
    REG_ADDRESS = (By.ID, 'address')
    REG_PASSWORD = (By.ID, 'password')
    REG_PASS_CONFIRM = (By.ID, 'password-confirm')
    REG_BTN = (By.NAME, 'register')
    REG_BACK_BTN = (By.ID, 'reset-back')
    REG_ERROR_MESSAGE = (By.XPATH, "//span[contains(@class, 'rt-input-container__meta--error')]")
    REG_REGION_OPTIONS = (By.CSS_SELECTOR, '.rt-select__list-item')

    # Локаторы для проверки валидации пароля
    PASSWORD_RULE_LENGTH = (By.XPATH,
                            "//span[@class='rt-input-container__meta rt-input-container__meta--error' and contains(text(), 'Длина пароля должна быть не менее 8 символов')]")
    PASSWORD_RULE_UPPER = (By.XPATH,
                           "//span[@class='rt-input-container__meta rt-input-container__meta--error' and contains(text(), 'Пароль должен содержать хотя бы одну заглавную букву')]")
    PASSWORD_RULE_LOWER = (By.XPATH,
                           "//span[@class='rt-input-container__meta rt-input-container__meta--error' and contains(text(), 'Пароль должен содержать хотя бы одну строчную букву')]")
    PASSWORD_RULE_DIGIT = (By.XPATH,
                           "//span[@class='rt-input-container__meta rt-input-container__meta--error' and contains(text(), 'Пароль должен содержать хотя бы одну цифру')]")
    PASSWORD_RULE_SPECIAL = (By.XPATH,
                             "//span[@class='rt-input-container__meta rt-input-container__meta--error' and contains(text(), 'Пароль должен содержать хотя бы один спецсимвол')]")
    PASSWORD_MISMATCH = (By.XPATH,
                         "//span[@class='rt-input-container__meta rt-input-container__meta--error' and contains(text(), 'Пароли не совпадают')]")

    # Общий локатор для любой ошибки валидации пароля
    ANY_PASSWORD_ERROR = (By.XPATH, "//span[@class='rt-input-container__meta rt-input-container__meta--error']")