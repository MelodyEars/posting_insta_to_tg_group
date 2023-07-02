
import peewee as pw

docker = False
admins_id = [487950394]

TOKEN = '5839603708:AAGAr8PgN6u8WjpbxWEC2Ni3uhngsgW8i7A'

executable_path = '/usr/bin/chromium'
# executable_path = None


if docker:
    set_database = {
                        "user": 'postgres',
                        "password": 'admin',
                        "host": "db",
                        "port": 5432,
                        }

else:
    set_database = {
                        "user": 'postgres',
                        "password": 'root123',
                        "host": "localhost",
                        "port": 5432,
                        }


db = pw.PostgresqlDatabase('admin', **set_database)


# Browsers settings
if docker:
    TIKTOK_BROWSER_HEADLESS = True
else:
    TIKTOK_BROWSER_HEADLESS = False
