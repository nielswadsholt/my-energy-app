import configparser
from requests import get, Response

class MyEnergyClient:

    def __init__(self) -> None:
        self.__refresh_token = self.load_from_config('RefreshToken')

    def load_from_config(self, key, section='DEFAULT') -> str:
        config = configparser.ConfigParser()
        config.read('config.ini')

        return config[section][key]

    def get_access_token(self) -> Response:
        return get(
            url='https://api.eloverblik.dk/customerapi/api/token',
            headers={'Authorization': f'Bearer {self.__refresh_token}'}
        )

client = MyEnergyClient()
access_token = client.get_access_token()

print(access_token.json())