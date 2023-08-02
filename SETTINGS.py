
import peewee as pw

server = True

# _________________________________________________________________________________ Telegram settings
admins_id = [487950394, 520869901]

if server:
    TOKEN = '5839603708:AAGAr8PgN6u8WjpbxWEC2Ni3uhngsgW8i7A'
else:
    TOKEN = '6053260400:AAF-stwr2OZNNkAtoUtCB54hqUTBTifNRO4'

# _________________________________________________________________________________ Database settings
if server:
    set_database = {
                        "user": 'postgres',
                        "password": 'postgres',
                        "host": "localhost",
                        "port": 5433,
                        }

else:
    set_database = {
                        "user": 'postgres',
                        "password": 'root123',
                        "host": "localhost",
                        "port": 5432,
                        }


db = pw.PostgresqlDatabase('postgres', **set_database)


# _________________________________________________________________________________ Browsers settings
if server:
    TIKTOK_BROWSER_HEADLESS = True
else:
    TIKTOK_BROWSER_HEADLESS = False


if server:
    google_version = 112
else:
    google_version = None


if server:
    executable_path = '/usr/bin/chromium-browser'
    # executable_path = None
else:
    executable_path = None


# _____________________________________________________________________________________ Proxy settings

PROXY: dict = {
    'host': 'de-1.stableproxy.com',
    'port': 11001,
    'user': 'AjYTI0_0',
    'password': 'wARRqrk6Dv5T',
    #'proxy_type': 'socks5',
}