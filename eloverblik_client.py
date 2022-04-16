from requests import get
from config_handler import load_from_config, write_to_config

class MyEnergyClient:

    def __init__(self) -> None:
        self.__refresh_token = load_from_config('RefreshToken')

    def load_access_token(self) -> str:
        return load_from_config('AccessToken')

    def fetch_new_access_token(self) -> str:
        res = get(
            url='https://api.eloverblik.dk/customerapi/api/token',
            headers={
                'Authorization': f'Bearer {self.__refresh_token}'
            }
        )

        return res.json()['result']

    def update_access_token(self) -> None:
        new_access_token = self.fetch_new_access_token()
        write_to_config('AccessToken', new_access_token)

client = MyEnergyClient()
client.update_access_token()
access_token = client.load_access_token()
print(access_token)
