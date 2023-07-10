import re

# Посилання з TikTok, яке ви надали
link = "https://www.tiktok.com/@postov4/video/7246228862420520194"

# Регулярний вираз для отримання номера відео та перевірки шаблону
pattern = r"https:\/\/www\.tiktok\.com\/@.+?\/video\/(\d+)\/?$"

# Застосовуємо регулярний вираз до посилання
match = re.search(pattern, link)

if match:
    # Отримуємо номер відео
    video_number = match.group(1)
    print("Номер відео:", video_number)

    # Перевіряємо, чи співпадає номер відео зі зразком
    if video_number == "7246228862420520194":
        print("Номер відео співпадає зі зразком.")
    else:
        print("Номер відео не співпадає зі зразком.")
else:
    print("Посилання не відповідає шаблону.")
