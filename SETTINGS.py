import peewee as pw


admins_id = [487950394]

# TOKEN = '6053260400:AAF-stwr2OZNNkAtoUtCB54hqUTBTifNRO4'
TOKEN = '5839603708:AAGAr8PgN6u8WjpbxWEC2Ni3uhngsgW8i7A'

# executable_path = '/usr/bin/chromium'
executable_path = None

set_database = {
                    "user": 'postgres',
                    "password": 'root123',
                    "host": "localhost",
                    "port": 5432,
                    }

db = pw.PostgresqlDatabase('telegram_database_insta_tt', **set_database)


# Browsers settings
TIKTOK_BROWSER_HEADLESS = False
