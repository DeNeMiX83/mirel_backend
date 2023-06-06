import sys
import yadisk
from mirel.config.settings import YandexDiskSettings

setting = YandexDiskSettings()
y = yadisk.YaDisk(setting.app_id, setting.app_secret)
url = y.get_code_url()

print("Go to the following url: %s" % url)  # noqa
code = input("Enter the confirmation code: ")

try:
    response = y.get_token(code)
except yadisk.exceptions.BadRequestError:
    print("Bad code")  # noqa
    sys.exit(1)

print(response.access_token)  # noqa
