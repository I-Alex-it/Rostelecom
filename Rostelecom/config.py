
MAIN_URL = 'https://b2c.passport.rt.ru'

# Данные для авторизации
valid_phone = "+79123456789"  # Пример валидного номера
valid_mail = "valid_email@example.com"
valid_login = "valid_login123"
valid_ls = "123456789012"  # Пример валидного лицевого счета

valid_password = "ValidPass123!"
invalid_password = "invalid"
invalid_phone = 'invalid_phone'
invalid_mail = 'invalid_mail'
invalid_login = 'invalid_login'
invalid_ls = 'invalid_ls'

# Данные для регистрации
valid_first_name = "Иван"
valid_last_name = "Петров"
valid_region = "Москва г"
valid_email = "new_user@example.com"
valid_pass = "StrongPass123!"
valid_confirm_password = "StrongPass123!"

# Невалидные данные для тестов
invalid_first_name = "12345"  # Только цифры
invalid_last_name = "!@#$%"  # Только спецсимволы
invalid_region = ""  # Пустое значение
invalid_email = "invalid_email"  # Неверный формат
invalid_pass = "weak"  # Слабый пароль
invalid_confirm_password = "different"  # Несовпадающий пароль

# Граничные значения
max_length_name = "А" * 30  # Максимальная длина имени (30 символов)
min_length_name = "Ив"  # Минимальная валидная длина (2 символа)
below_min_length_name = "А"  # Ниже минимальной длины

# Данные с пробелами
name_with_spaces = "  Иван  "
email_with_spaces = " test@mail.ru "

# Данные с недопустимыми символами
name_with_special_chars = "Иван!@#"
email_with_special_chars = "test!@#$%^&*().mail.ru"

# Для теста паролей
password_no_upper = "nopass123!"  # Без заглавных
password_no_lower = "NOPASS123!"  # Без строчных
password_no_digit = "NoPassword!"  # Без цифр
password_no_special = "NoPassword123"  # Без спецсимволов